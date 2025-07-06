from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append('/opt/airflow/src')
from validation.gx_runner import run_all_checkpoints


DBT_BIN = "/home/airflow/.local/bin/dbt"   # ← the dbt executable path

default_args = {
    "owner": "vaishnavi",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="etl_brazil_pipeline",
    default_args=default_args,
    description="ETL → GE → dbt pipeline (company-style)",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["etl", "brazil"],
) as dag:

    # 1️⃣ ETL: read CSVs, clean, load Postgres
    run_etl_script = BashOperator(
        task_id="run_etl_script",
        bash_command="python3 /opt/airflow/src/etl/brazil_etl.py",
    )

    # 2️⃣ Great Expectations validation for all checkpoints
    run_gx_validations = PythonOperator(
        task_id="run_gx_validations",
        python_callable=run_all_checkpoints,
    )

    # 3️⃣ dbt run: build staging models
    dbt_run = BashOperator(
        task_id="run_dbt_models",
        bash_command=f"cd /opt/airflow/dbt_project && {DBT_BIN} run",
    )

    # 4️⃣ dbt test: run model tests
    dbt_test = BashOperator(
        task_id="run_dbt_tests",
        bash_command=f"cd /opt/airflow/dbt_project && {DBT_BIN} test",
    )

    run_etl_script >> run_gx_validations >> dbt_run >> dbt_test
