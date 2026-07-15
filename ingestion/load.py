import pandas as pd
import logging as log
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import Engine

logger = log.getLogger(__name__)
load_dotenv()

def credentials_load() -> Engine:

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    dbname = os.getenv("POSTGRES_DB")

    if not all([user, password, host, port, dbname]):
        logger.error("Variaveis do banco não definidas no .env")
        raise ValueError("Variaveis de ambiente não encontradas")

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(url, pool_pre_ping=True)
    return engine

def load(df: pd.DataFrame, table_name: str, schema_name: str, engine: Engine) -> None:

    logger.info(f"Iniciando carga da camada raw - {schema_name}.{table_name}")
    
    try:
        
        with engine.begin() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
        
        inspector = inspect(engine)
        table_exists = inspector.has_table(table_name, schema_name) 

        if table_exists:
            
            with engine.begin() as conn:
                conn.execute(text(f"TRUNCATE TABLE {schema_name}.{table_name} CASCADE"))

        df.to_sql(name=table_name, schema=schema_name, con=engine, index=False, chunksize=1000,if_exists="append")
        logger.info(f"Camada raw carregada! {schema_name}.{table_name} / Colunas: {df.shape[1]} / Linhas: {len(df)}")

    except Exception:
        logger.exception(f"Falha ao inserir dados na tabela {schema_name}.{table_name}")
        raise