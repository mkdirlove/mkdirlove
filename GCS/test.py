#!/usr/bin/python3.5

import os
import time
import subprocess
import datetime
import logging
import configparser
from google.cloud import storage
import io
import gzip

# Backup and log path
BUCKET = "ti-sql-02"
GCS_PATH = "Backups/Current/MYSQL"
SSL_PATH = "/ssl-certs/"
SERVERS_LIST = "/backup/configs/MYSQL_servers_list.conf"
KEY_FILE = "/root/jsonfiles/ti-ca-infrastructure-d1696a20da16.json"
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
        command = [
            "mysql", "-u{}".format(DB_USR), "-p{}".format(DB_PWD), "-h", host,
            "--default-auth=mysql_native_password",
            "-B", "--silent", "-e", "SHOW DATABASES"

        ]

        if use_ssl:
            command += [
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

def stream_database_to_gcs(dump_command, gcs_path, db):
  start_time = time.time()

  try:
    logging.info("Starting dump process: {}".format(" ".join(dump_command)))

    # Start the dump process
    dump_proc = subprocess.Popen(dump_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    logging.info("Starting GCS upload process")
    client = storage.Client.from_service_account_json(KEY_FILE)
    bucket = client.bucket(BUCKET)
    blob = bucket.blob(gcs_path)

    buffer = io.BytesIO()

    # Increase chunk size here (e.g., 65536 bytes or 64 KB)
    chunk = dump_proc.stdout.read(65536)  # Adjust chunk size as needed

    with gzip.GzipFile(fileobj=buffer, mode='wb') as gz_out:
      while chunk:
        gz_out.write(chunk)
        chunk = dump_proc.stdout.read(65536)

    # Ensure the buffer is closed before uploading
    buffer.seek(0)

    logging.info("Uploading to GCS...")
    blob.upload_from_file(buffer)

    elapsed_time = time.time() - start_time
    logging.info("Dumped and streamed database {} to GCS successfully in {:.2f} seconds.".format(db, elapsed_time))

  except Exception as e:
    logging.error("Unexpected error streaming database {} to GCS: {}".format(db, e))

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
