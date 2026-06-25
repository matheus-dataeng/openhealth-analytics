import pandas as pd 
import logging as log 
import os 
from dotenv import load_dotenv 
from sqlalchemy import create_engine, text

logger = log.getLogger(__name__)
load_dotenv()

def load(df: pd.DataFrame) -> None: 
    
    logger.info("Iniciando carga da camada bronze")
    
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port =  os.getenv("POSTGRES_PORT")
    dbname =  os.getenv("POSTGRES_DB")
    table_name = os.getenv("TABLE_NAME_BRONZE")
    schema_name = os.getenv("SCHEMA")   
    
    if not all ([user, host, password, port, dbname, table_name, schema_name]):
        logger.error("Variaveis do banco não definidas no .env")
        raise ValueError("Variaveis de ambiente não encontradas")   
    
    try:
       
        url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}" 
        engine = create_engine(url, pool_pre_ping=True)
        
        with engine.begin() as conn:
            
            conn.execute(text(f"TRUNCATE TABLE {schema_name}.{table_name} CASCADE"))
            
            df.to_sql(name= table_name, schema= schema_name, con = conn, index= False, chunksize= 1000, if_exists= "append")
            logger.info(f"Camada raw carregada! / Colunas: {df.shape[1]} / Linhas: {len(df)}")
    
    except Exception:
        logger.exception("Falha ao inserir dados no banco")
        raise 