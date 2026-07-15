import pandas as pd
import logging as log 
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine import Engine
from pathlib import Path
import os
from ingestion.export.s3_export import bucket_s3

logger = log.getLogger(__name__)
load_dotenv()

def credentials_datalake() -> Engine:

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port =  os.getenv("POSTGRES_PORT")
    dbname =  os.getenv("POSTGRES_DB") 

    if not all([user, password, host, port, dbname]):
        logger.error("Variáveis de ambiente do banco não definidas")
        raise ValueError("Variáveis de ambiente não encontradas")
    
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}" 
    engine = create_engine(url, pool_pre_ping=True)
    return engine 
    
def silver_datalake(engine: Engine) -> None:
    
    logger.info("Iniciando carga da camada silver")
    
    modelos_silver = ["silver_clima", "silver_dengue", "silver_regiao", "silver_populacao"]
    
    silver_path = Path(f"data_lake/silver")
    silver_path.mkdir(parents=True, exist_ok=True)
    
    try:
        for tabela in modelos_silver:
            arquivos_silver = silver_path / f"{tabela}.parquet"
        
            df_silver = pd.read_sql(f"SELECT * FROM silver.{tabela}", engine)
            df_silver.to_parquet(arquivos_silver, index=False)
            bucket_s3(arquivos_silver, f"silver/{tabela}.parquet")
            logger.info(f"Camada silver exportada:{tabela} {len(df_silver)} linhas")
    
    except SQLAlchemyError as e:
        logger.error(f"Erro ao exportar camada silver: {e}")
        raise

def gold_datalake(engine: Engine) -> None:
    
    logger.info("Iniciando carga da camada gold")
    
    gold_path = Path(f"data_lake/gold")
    gold_path.mkdir(parents=True, exist_ok=True)
        
    try:
        tabelas = [
            "casos_por_uf",
            "casos_por_mes",
            "classificacao_por_uf",
            "taxa_cura_por_uf",
            "casos_por_municipio",
            "casos_por_regiao",
            "gravidade_por_regiao",
            "taxa_cura_por_municipio",
            "indicadores_clima_uf"
        ]
         
        for tabela in tabelas:
            arquivos_gold = gold_path / f"{tabela}.parquet"
            df_gold = pd.read_sql(f"SELECT * FROM gold.{tabela}", engine)
            df_gold.to_parquet(arquivos_gold, index= False)
            bucket_s3(arquivos_gold, f"gold/{tabela}.parquet")
            logger.info(f"Camada gold exportada: {tabela} / {len(df_gold)} linhas")
    
    except SQLAlchemyError as e:
        logger.error(f"Erro ao exportar camada gold: {e}")
        raise