from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

from datetime import datetime, timedelta
from dotenv import load_dotenv

import pandas as pd
import logging

load_dotenv()


def extract_the_data(source: str, output: str) -> None:
    df = pd.read_csv(source)
    df_score = df[(df["score"] >= 7) & (df["popularity"] < 100)]
    df_score.to_csv(output, index=False)
    logging.info("Finish to transform the csv")


dag = DAG(
    dag_id="transform_csv",
    start_date=(datetime.now() - timedelta(days=1)),
    catchup=False,
    tags=["airflow_template", "demo"],
)

start = EmptyOperator(task_id="start", dag=dag)

transform = PythonOperator(
    task_id="transform",
    python_callable=extract_the_data,
    op_kwargs={
        "source": "data/src/animes.csv",
        "output": "data/out/transform_animes.csv",
    },
    dag=dag,
)

end = EmptyOperator(task_id="end", dag=dag)

start >> transform >> end
