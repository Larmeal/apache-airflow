from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

import pandas as pd
import logging


def transform_csv(source: str, output: str) -> None:
    df = pd.read_csv(source)
    df_score = df[(df["score"] >= 7) & (df["popularity"] < 100)]
    df_score.to_csv(output, index=False)
    logging.info("Finish to transform the csv")


default_args = {
    "owner": "airflow",
    "start_date": "2024-09-01",
    "retries": 1,
    "retry_delay_sec": 30,
}

dag = DAG(
    dag_id="transform_csv",
    description="this is an example dag",
    default_args=default_args,
    schedule=None,
    catchup=False,
    dagrun_timeout=300,
    tags=["airflow_template", "demo"],
)

start = EmptyOperator(task_id="start", dag=dag)

transform = PythonOperator(
    task_id="transform",
    python_callable=transform_csv,
    op_kwargs={
        "source": "data/src/animes.csv",
        "output": "data/out/transform_animes.csv",
    },
    dag=dag,
)

end = EmptyOperator(task_id="end", dag=dag)

t1 = EmptyOperator(task_id="transform_a", dag=dag)

t2 = EmptyOperator(task_id="transform_b", dag=dag)

t3 = EmptyOperator(task_id="transform_c", dag=dag)

t4 = EmptyOperator(task_id="transform_d", dag=dag)


start >> [transform, t1, t2, t3, t4] >> end
