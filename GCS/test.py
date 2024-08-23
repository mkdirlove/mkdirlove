#!/usr/bin/env python

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
                "--ssl-ca={}".format(os.path.join(SSL_PATH, server, "server-ca.pem")),
                "--ssl-cert={}".format(os.path.join(SSL_PATH, server, "client-cert.pem")),
                "--ssl-key={}".format(os.path.join(SSL_PATH, server, "client-key.pem")),
                "--ssl-mode=VERIFY_CA"
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

def start_dump_process(dump_command):
    """Start the mysqldump process."""
    try:
        logging.info("Starting dump process: {}".format(" ".join(dump_command)))
        return subprocess.Popen(dump_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    except Exception as e:
        logging.error("Failed to start dump process: {}".format(e))
        raise

def compress_data(dump_proc):
    """Compress data from the dump process into a gzip-compressed buffer."""
    buffer = io.BytesIO()
    try:
        with gzip.GzipFile(fileobj=buffer, mode='wb') as gz_out:
            while True:
                chunk = dump_proc.stdout.read(1024)
                if not chunk:
                    break
                gz_out.write(chunk)
        buffer.seek(0)  # Rewind buffer to the start
        return buffer
    except Exception as e:
        logging.error("Failed to compress data: {}".format(e))
        raise

def upload_to_gcs(buffer, gcs_path):
    """Upload the gzip-compressed buffer to Google Cloud Storage."""
    if not isinstance(buffer, io.BytesIO):
        logging.error("Invalid file object: {}".format(type(buffer)))
        raise TypeError("Expected an io.BytesIO object.")

    try:
        client = storage.Client.from_service_account_json(KEY_FILE)
        bucket = client.bucket(BUCKET)
        blob = bucket.blob(gcs_path)
        buffer.seek(0)  # Rewind buffer to the start
        blob.upload_from_file(buffer, content_type='application/gzip')
        logging.info("Uploaded to GCS: {}".format(gcs_path))
    except Exception as e:
        logging.error("Failed to upload to GCS: {}".format(e))
        raise

def handle_dump_process(dump_command, gcs_path, db):
    """Handle the entire process of dumping, compressing, and uploading."""
    start_time = time.time()
    dump_proc = None
    buffer = None

    try:
        dump_proc = start_dump_process(dump_command)
        buffer = compress_data(dump_proc)
        
        # Ensure dump process is completed and check for errors
        dump_proc.stdout.close()
        dump_output, dump_err = dump_proc.communicate()

        if dump_proc.returncode != 0:
            logging.error("mysqldump failed: {}".format(dump_err.decode() if dump_err else 'No error message'))
            return
        
        upload_to_gcs(buffer, gcs_path)

        elapsed_time = time.time() - start_time
        logging.info("Dumped and streamed database {} to GCS successfully in {:.2f} seconds.".format(db, elapsed_time))

    except Exception as e:
        logging.error("Unexpected error processing database {}: {}".format(db, e))
    
    finally:
        if buffer:
            buffer.close()

def stream_database_to_gcs(dump_command, gcs_path, db):
    """Stream the database dump to GCS."""
    handle_dump_process(dump_command, gcs_path, db)

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
