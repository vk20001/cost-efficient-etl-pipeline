from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
import os

# Adjust this path if different
LOG_FILE = "/opt/airflow/logs/etl.log"

default_args = {
    'owner': 'vaishnavi',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def scan_log_file():
    if not os.path.exists(LOG_FILE):
        raise ValueError("ETL log file not found.")

    with open(LOG_FILE, 'r') as f:
        logs = f.readlines()[-50:]  # last N lines (recent run)

    has_error = any("ERROR" in line or "❌" in line for line in logs)
    no_rows_loaded = any("rows: 0" in line.lower() for line in logs)

    if has_error or no_rows_loaded:
        raise ValueError("ETL error or no rows loaded detected!")

with DAG(
    dag_id='etl_monitoring_alert',
    default_args=default_args,
    start_date=datetime(2025, 6, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=["monitoring"]
) as dag:

    check_logs = PythonOperator(
        task_id='check_etl_health',
        python_callable=scan_log_file,
    )

    send_email = EmailOperator(
        task_id='send_alert_email',
        to='vaishnavikanchan19@gmail.com',  # TODO: Replace with your actual email
        subject='🚨 ETL Alert: Something Went Wrong!',
        html_content="""
        <h3>ETL Alert!</h3>
        <p>Either the ETL failed or no rows were loaded.</p>
        <p>Check logs at: /opt/airflow/logs/etl.log</p>
        """
    )

    check_logs >> send_email
