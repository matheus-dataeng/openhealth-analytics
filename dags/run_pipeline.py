import pendulum 
import subprocess
from airflow import DAG
from airflow.operators.python import PythonOperator
from ingestion.sources.extract_dengue import extract_dengue, load_bronze_datalake_dengue
from ingestion.sources.extract_regiao import extract_regiao, load_bronze_datalake_regiao
from ingestion.sources.extract_clima import extract_clima, load_bronze_datalake_clima
from ingestion.sources.extract_populacao import extract_populacao, load_bronze_datalake_populacao
from ingestion.export.export_datalake import credentials_datalake, silver_datalake, gold_datalake
from ingestion.load import credentials_load, load as load_dw

def task_extract_load_bronze():
    
    engine_load = credentials_load()
    
    df_dengue = extract_dengue()
    load_bronze_datalake_dengue(df_dengue) 
    load_dw(df_dengue, table_name="raw_dengue", schema_name="bronze", engine=engine_load)
    
    df_regiao = extract_regiao()
    load_bronze_datalake_regiao(df_regiao)
    load_dw(df_regiao, table_name="raw_regiao", schema_name="bronze", engine=engine_load)
    
    df_clima = extract_clima()
    load_bronze_datalake_clima(df_clima)
    load_dw(df_clima, table_name="raw_clima", schema_name="bronze", engine=engine_load)
    
    df_populacao = extract_populacao()
    load_bronze_datalake_populacao(df_populacao)
    load_dw(df_populacao, table_name="raw_populacao", schema_name="bronze", engine=engine_load)

def task_run_dbt():
    
    result = subprocess.run(
    [
        "dbt", "run",
        "--project-dir", "/opt/airflow/project/openhealth_dbt",
        "--profiles-dir", "/opt/airflow/project/openhealth_dbt",
    ],
    capture_output=True,
    text=True,
)

    if result.returncode != 0:
        raise Exception(f"dbt run falhou: {result.stderr}")
    
def task_datalake_silver_gold():
    
    engine_datalake = credentials_datalake()
    
    silver_datalake(engine=engine_datalake)
    gold_datalake(engine=engine_datalake)

with DAG (
    dag_id = "OpenHealth_Analytics",
    start_date = pendulum.datetime(2026, 1, 1, tz="America/Sao_Paulo"),
    catchup = False,
    schedule = None 
) as dag: 
    
    extract_task = PythonOperator(
        task_id = "extract_load_bronze",
        python_callable = task_extract_load_bronze
    )
    
    dbt_run_task = PythonOperator (
        task_id = "dbt_run",
        python_callable = task_run_dbt
    )
    
    task_load_datalake_silver_gold = PythonOperator(
        task_id = "load_datalake_silver_gold",
        python_callable = task_datalake_silver_gold
    )
    
    extract_task >> dbt_run_task >> task_load_datalake_silver_gold