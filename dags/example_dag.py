"""
Example DAG — provided for reference only.

This minimal DAG shows the local Airflow environment is working. Candidates
should NOT modify this file. It demonstrates basic task structure and how
to use the mock Databricks operator.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


def _hello():
    print("Airflow is running. Environment is set up correctly.")


with DAG(
    dag_id="example_hello_world",
    default_args=default_args,
    description="Smoke test — confirms the local environment works",
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:
    hello_task = PythonOperator(
        task_id="say_hello",
        python_callable=_hello,
    )
