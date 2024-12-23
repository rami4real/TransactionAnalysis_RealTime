import logging
import os
import shutil
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from confluent_kafka import Consumer, KafkaError, Producer
from hdfs import InsecureClient

# Kafka and HDFS Configurations
KAFKA_BROKERS = 'master:9092,slave1:9092,slave2:9092'
KAFKA_TOPIC = 'csv-topic'
HDFS_URL = 'http://master:50070'
HDFS_BASE_PATH = '/kafka_ingestion/csv_files'

# Use a directory in the user's home folder
MONITORED_FOLDER = os.path.join(os.path.expanduser('~'), 'kafka_ingestion')
PROCESSED_FOLDER = os.path.join(MONITORED_FOLDER, 'processed')

CURRENT_USER = os.environ.get('USER', 'master')

# Airflow Default Arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Initialize Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure monitored and processed folders exist
os.makedirs(MONITORED_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# HDFS Client
hdfs_client = InsecureClient(HDFS_URL, user=CURRENT_USER)

def scan_csv_files(**kwargs):
    """
    Scan the monitored folder for new CSV files.
    """
    csv_files = [f for f in os.listdir(MONITORED_FOLDER) 
                 if f.lower().endswith('.csv') and os.path.isfile(os.path.join(MONITORED_FOLDER, f))]
    kwargs['ti'].xcom_push(key='csv_files', value=csv_files)
    logger.info(f"Found CSV files: {csv_files}")

def produce_to_kafka(**kwargs):
    """
    Produce file paths of CSV files to Kafka.
    """
    csv_files = kwargs['ti'].xcom_pull(key='csv_files', task_ids='scan_csv_files')
    producer_conf = {'bootstrap.servers': KAFKA_BROKERS, 'client.id': 'airflow_producer'}
    producer = Producer(producer_conf)

    for csv_file in csv_files:
        full_path = os.path.join(MONITORED_FOLDER, csv_file)
        try:
            producer.produce(KAFKA_TOPIC, full_path.encode('utf-8'))
            producer.flush()
            logger.info(f"Produced file path to Kafka: {full_path}")
        except Exception as e:
            logger.error(f"Error producing file to Kafka: {e}")

def consume_and_ingest_to_hdfs(**kwargs):
    """
    Consume file paths from Kafka and ingest CSV files to HDFS.
    """
    consumer_conf = {
        'bootstrap.servers': KAFKA_BROKERS,
        'group.id': 'csv-hdfs-ingestion-airflow',
        'auto.offset.reset': 'earliest',
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe([KAFKA_TOPIC])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                break

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info("End of Kafka partition")
                else:
                    logger.error(f"Kafka error: {msg.error()}")
                continue

            csv_path = msg.value().decode('utf-8').strip()
            logger.info(f"Processing CSV path: {csv_path}")

            try:
                filename = os.path.basename(csv_path)
                hdfs_destination = os.path.join(HDFS_BASE_PATH, filename)

                hdfs_client.makedirs(os.path.dirname(hdfs_destination))
                with open(csv_path, 'rb') as local_file:
                    with hdfs_client.write(hdfs_destination, overwrite=True) as hdfs_file:
                        shutil.copyfileobj(local_file, hdfs_file)

                processed_file = os.path.join(PROCESSED_FOLDER, filename)
                shutil.move(csv_path, processed_file)

                logger.info(f"CSV file '{csv_path}' ingested to HDFS at '{hdfs_destination}'")

            except Exception as e:
                logger.error(f"Failed to ingest '{csv_path}' to HDFS: {e}")

    finally:
        consumer.close()

# Define Airflow DAG
with DAG(
    'kafka_hdfs_ingestion_pipeline',
    default_args=default_args,
    description='Pipeline to monitor folder, send to Kafka, and ingest to HDFS',
    schedule_interval='*/1 * * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    scan_task = PythonOperator(
        task_id='scan_csv_files',
        python_callable=scan_csv_files,
        provide_context=True,
    )

    produce_task = PythonOperator(
        task_id='produce_to_kafka',
        python_callable=produce_to_kafka,
        provide_context=True,
    )

    ingest_task = PythonOperator(
        task_id='consume_and_ingest_to_hdfs',
        python_callable=consume_and_ingest_to_hdfs,
        provide_context=True,
    )

    # Define task dependencies
    scan_task >> produce_task >> ingest_task
