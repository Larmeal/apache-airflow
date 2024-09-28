from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
from google.cloud import storage, bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv
from io import BytesIO

import pandas as pd
import os

load_dotenv()

# SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT")
# BUCKET_NAME = os.getenv("BUCKET_NAME")
# PROJECT_ID = os.getenv("PROJECT_ID")
# DATASET_ID = os.getenv("DATASET_ID")
# TABLE_ID = os.getenv("TABLE_ID")
# LOCATION = os.getenv("LOCATION")

SERVICE_ACCOUNT = Variable.get("SERVICE_ACCOUNT")
BUCKET_NAME = Variable.get("BUCKET_NAME")
PROJECT_ID = Variable.get("PROJECT_ID")
DATASET_ID = Variable.get("DATASET_ID")
TABLE_ID = Variable.get("TABLE_ID")
LOCATION = Variable.get("LOCATION")

CREDENTIALS = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT)


def extract_the_data() -> None:
    global CREDENTIALS
    df = pd.read_csv("data/src/animes.csv")
    df_score = df[(df["score"] >= 7) & (df["popularity"] < 100)]

    client = storage.Client(credentials=CREDENTIALS)
    bucket = client.get_bucket(BUCKET_NAME)
    bucket.blob("resource/animes.csv").upload_from_string(
        df_score.to_csv(index=False), "text/csv"
    )


def load_data_to_bigquery() -> None:
    # Construct a BigQuery client object.
    global CREDENTIALS
    client = bigquery.Client(credentials=CREDENTIALS)
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    schema = [
        bigquery.SchemaField("uid", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("title", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("synopsis", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("genre", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("aired", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("episodes", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("members", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("popularity", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("ranked", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("score", "FLOAT", mode="REQUIRED"),
        bigquery.SchemaField("img_url", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("link", "STRING", mode="REQUIRED"),
    ]

    try:
        table = client.get_table(table_id)
    except Exception as e:
        table = bigquery.Table(table_id, schema=schema)
        job = client.create_table(table)
    finally:
        storage_client = storage.Client(credentials=CREDENTIALS)
        bucket = storage_client.get_bucket(BUCKET_NAME)
        blob = bucket.get_blob("resource/animes.csv")
        data = blob.download_as_bytes()
        df = pd.read_csv(BytesIO(data))
        df.to_gbq(
            destination_table=f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}",
            if_exists="replace",
            credentials=CREDENTIALS,
        )


dag = DAG(
    dag_id="LOCAL_TO_BIGQUERY",
    start_date=(datetime.now() - timedelta(days=1)),
    catchup=False,
)

t1 = PythonOperator(task_id="transform_data", python_callable=extract_the_data, dag=dag)

t2 = PythonOperator(task_id="load_data", python_callable=load_data_to_bigquery, dag=dag)

t1 >> t2
