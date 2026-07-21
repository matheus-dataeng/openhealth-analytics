import pandas as pd 
import logging as log 
import os 
from dotenv import load_dotenv
from pathlib import Path
from ingestion.export.s3_export import bucket_s3

logger = log.getLogger(__name__)
load_dotenv()

def extract_clima() -> pd.DataFrame:
    
    logger.info("Iniciando extração de dados climaticos")
    
    try:
        
        csv_clima = os.getenv("CLIMA_CSV")
        
        if not csv_clima:
            logger.error("Variavel não definida no .env")
            raise ValueError("Variável de ambiente não foi definida")
        
        df_clima = pd.read_csv(filepath_or_buffer= csv_clima, encoding="latin1", sep=",", low_memory=False)
        logger.info(f"Arquivo extraido! / Colunas: {df_clima.shape[1]} / Linhas: {len(df_clima)}")
    
    except Exception:
        logger.exception("Erro ao extrair arquivo")
        raise 
    
    return df_clima

def load_bronze_datalake_clima(df_clima: pd.DataFrame) -> None:
    
    logger.info("Iniciando carga no datalake bronze clima")
    
    try:
        
        bronze_clima = Path("data_lake/bronze/bronze_clima.parquet")
        bronze_clima.parent.mkdir(parents=True, exist_ok=True)
        df_clima.to_parquet(bronze_clima, index= False)
        bucket_s3(bronze_clima, "bronze/bronze_clima.parquet")
        logger.info(f"Arquivo salvo: {bronze_clima}")
    
    except Exception:
        logger.error("Falha ao carregar arquivo")
        raise 
        