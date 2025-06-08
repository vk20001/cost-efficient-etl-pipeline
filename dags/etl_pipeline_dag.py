from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/opt/airflow/src/etl')

from main_etl import run_etl
from validate_data import validate_data  # Import the validation function

default_args = {
    'owner': 'vaishnavi',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def run_validation():
    # Pass the filename relative to your GE datasource config
    validate_data("processed_data.csv")

with DAG(
    dag_id='cost_efficient_etl_pipeline',
    default_args=default_args,
    description='Run ETL pipeline and validate with Great Expectations',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['ETL'],
) as dag:

    run_etl_task = PythonOperator(
        task_id='run_etl_script',
        python_callable=run_etl,
    )
    
    ge_validation_task = PythonOperator(
        task_id='run_ge_validation',
        python_callable=run_validation,
    )

    run_etl_task >> ge_validation_task
