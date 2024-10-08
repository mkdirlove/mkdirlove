import os
import time
import subprocess
import datetime
import logging
import configparser
import io
from google.cloud import storage

# Backup and log path
BUCKET = "ti-sql-02"
GCS_PATH = "Backups/Current/MYSQL"
SSL_PATH = "/ssl-certs/"
SERVERS_LIST = "/backup/configs/MYSQL_servers_list.conf"
KEY_FILE = "/root/jsonfiles/ti-ca-infrastructure-d1696a20da16.json"

# Define the path for the database credentials
CREDENTIALS_PATH = "/backup/configs/db_credentials.conf"

# Logging Configuration
log_path = "/backup/logs/"
os.makedirs(log_path, exist_ok=True)
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
log_filename = os.path.join(log_path, "MYSQL_backup_activity_{}.log".format(current_date))
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Load Database credentials
config = configparser.ConfigParser()
config.read(CREDENTIALS_PATH)
DB_USR = config['credentials']['DB_USR']
DB_PWD = config['credentials']['DB_PWD']

def load_server_list(file_path):
    """Load the server list from a given file."""
    config = configparser.ConfigParser()
    try:
        config.read(file_path)
        return config.sections(), config
    except Exception as e:
        logging.error("Failed to load server list: {}".format(e))
        return [], None

def get_database_list(host, use_ssl, server):
    """Retrieve the list of databases from the MySQL server."""
    try:
        if not use_ssl:
            command = [
                "mysql", "-u{}".format(DB_USR), "-p{}".format(DB_PWD), "-h", host,
                "--default-auth=mysql_native_password",
                "-B", "--silent", "-e", "SHOW DATABASES"
            ]
        else:
            command = [
                "mysql", "-u{}".format(DB_USR), "-p{}".format(DB_PWD), "-h", host,
                "--ssl-ca=" + os.path.join(SSL_PATH, server, "server-ca.pem"),
                "--ssl-cert=" + os.path.join(SSL_PATH, server, "client-cert.pem"),
                "--ssl-key=" + os.path.join(SSL_PATH, server, "client-key.pem"),
                "--ssl-mode=VERIFY_CA", "--default-auth=mysql_native_password",
                "-B", "--silent", "-e", "SHOW DATABASES"
            ]

        result = subprocess.check_output(command, stderr=subprocess.STDOUT)
        db_list = result.decode("utf-8").strip().split('\n')
        valid_db_list = [
            db for db in db_list if db.isidentifier() and db not in (
                "information_schema", "performance_schema", "sys", "mysql"
            )
        ]

        return valid_db_list
    except subprocess.CalledProcessError as e:
        logging.error("Failed to get database list from {}: {} - Output: {}".format(
            host, e, e.output.decode()
        ))
        return []

def execute_subprocess(command):
    """Execute a subprocess command and return the process."""
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def upload_stream_to_gcs(stream, bucket_name, gcs_path):
    """Upload a stream to Google Cloud Storage using a BytesIO buffer."""
    client = storage.Client.from_service_account_json(KEY_FILE)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)

    logging.info("Starting GCS upload process")
    with io.BytesIO() as buffer:
        # Read from stream and write to buffer
        while True:
            chunk = stream.read(4096)
            if not chunk:
                break
            buffer.write(chunk)
        
        # Ensure the buffer is at the beginning before uploading
        buffer.seek(0)
        
        # Upload the buffer to GCS
        blob.upload_from_file(buffer, content_type='application/gzip')

def handle_errors(dump_proc, gzip_proc):
    """Handle errors from subprocesses."""
    dump_output, dump_err = dump_proc.communicate()
    gzip_output, gzip_err = gzip_proc.communicate()

    if dump_proc.returncode != 0:
        logging.error("mysqldump failed: %s", dump_err.decode() if dump_err else 'No error message')
        return False
    if gzip_proc.returncode != 0:
        logging.error("gzip failed: %s", gzip_err.decode() if gzip_err else 'No error message')
        return False
    return True

def stream_database_to_gcs(dump_command, gcs_path, db):
    start_time = time.time()

    try:
        logging.info("Starting dump process: %s", " ".join(dump_command))

        # Start the dump and gzip processes
        dump_proc = execute_subprocess(dump_command)
        logging.info("Starting gzip process")
        gzip_proc = execute_subprocess(["gzip"])
        dump_proc.stdout.close()  # Allow dump_proc to receive a SIGPIPE if gzip_proc exits

        # Upload the stream to GCS
        logging.info("Uploading to GCS")
        upload_stream_to_gcs(gzip_proc.stdout, BUCKET, gcs_path)

        # Handle errors from subprocesses
        if not handle_errors(dump_proc, gzip_proc):
            return

        elapsed_time = time.time() - start_time
        logging.info("Dumped and streamed database %s to GCS successfully in %.2f seconds.", db, elapsed_time)

    except Exception as e:
        logging.error("Unexpected error streaming database %s to GCS: %s", db, e)
        
def main():
    """Main function to execute the backup process."""
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    sections, config = load_server_list(SERVERS_LIST)
    if not sections:
        logging.error("No servers to process. Exiting.")
        return

    logging.info("================================== {} =============================================".format(current_date))
    logging.info("==== Backup Process Started ====")
    servers = []
    for section in sections:
        try:
            host = config[section]['host']
            ssl = config[section].get('ssl', 'n')  # Provide default value 'n' if 'ssl' key is missing
            servers.append((section, host, ssl))
        except KeyError as e:
            logging.error("Missing configuration for server '{}': {}".format(section, e))

    for server in servers:
        SERVER, HOST, SSL = server
        use_ssl = SSL.lower() == "y"
        logging.info("DUMPING SERVER: {}".format(SERVER))

        try:
            db_list = get_database_list(HOST, use_ssl, SERVER)
            if not db_list:
                logging.warning("No databases found for server: {}".format(SERVER))
                continue

            for db in db_list:
                logging.info("Backing up database: {}".format(db))
                gcs_path = os.path.join(GCS_PATH, SERVER, "{}_{}.sql.gz".format(current_date, db))
                dump_command = [
                    "mysqldump", "-u{}".format(DB_USR), "-p{}".format(DB_PWD), "-h", HOST, db,
                    "--set-gtid-purged=OFF", "--single-transaction", "--quick",
                    "--triggers", "--events", "--routines"
                ]
                if use_ssl:
                    dump_command += [
                        "--ssl-ca={}".format(os.path.join(SSL_PATH, SERVER, "server-ca.pem")),
                        "--ssl-cert={}".format(os.path.join(SSL_PATH, SERVER, "client-cert.pem")),
                        "--ssl-key={}".format(os.path.join(SSL_PATH, SERVER, "client-key.pem")),
                        "--ssl-mode=VERIFY_CA"
                    ]

                logging.info("Dump command: {}".format(" ".join(dump_command)))
                stream_database_to_gcs(dump_command, gcs_path, db)

        except Exception as e:
            logging.error("Error processing server {}: {}".format(SERVER, e))

    logging.info("==== Backup Process Completed ====")

if __name__ == "__main__":
    main()
