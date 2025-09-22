from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
from mathematical_validation import validate_ai_math # Import your validation function

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 3, 
    'retry_delay': timedelta(minutes=15),
    'email_on_failure': True
}

def run_validation():
    ai_claim = {
        'quarter': '2024Q3',
        'metric': 'revenue',
        'growth_pct': 15.0
    }
    result = validate_ai_math("sales-data.csv", ai_claim)
    if result != "All checks passed":
        raise ValueError(f"Validation failed: {result}")

with DAG(
    'ai_validation_pipeline',
    default_args=default_args, 
    schedule_interval='@daily',
    start_Date=datetime(2024, 1, 1),
    catchup=False   # Prevents backfilling
) as dag:
    
    validate_task = PythonOperator(
        task_id='run_validation',
        python_callable=run_validation
    )

    alert_task = EmailOperator(
        task_id='send_alert',
        to='your-email@example.com',
        subject='AI Validation Alert',
        html_content='Validation checks failed - please investigate'
    )

    validate_task >> alert_task