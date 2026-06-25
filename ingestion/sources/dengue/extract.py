import pandas as pd 
import logging as log 
import os 
from dotenv import load_dotenv
from pathlib import Path

logger = log.getLogger(__name__)
load_dotenv()

def extract_csv() -> pd.DataFrame:
    
    logger.info("Extraindo dados...")
    
    try:
        csv_path = os.getenv("DENGUE_CSV")
        
        if not csv_path:
            logger.error("Variável de ambiente não encontrado")
            raise ValueError("Variável de ambiente não foi definida.")

        df = pd.read_csv(filepath_or_buffer= csv_path, encoding= "utf-8", low_memory= False, sep= ",")
        logger.info(f"Arquivo extraido! / Colunas: {df.shape[1]} / Linhas: {len(df)}")
    
    except Exception:
        logger.exception("Erro ao extrair arquivo")
        raise 
    
    return df 
    
def load_bronze_datalake(df: pd.DataFrame) -> None: 
        
    logger.info("Iniciando carga no data lake bronze")
    
    try:    
        
        bronze_path = Path("data_lake/bronze/DENGBR26.parquet")
        bronze_path.parent.mkdir(parents= True, exist_ok= True)
        df.to_parquet(bronze_path, index= False)
        
        logger.info(f"Arquivo salvo: {bronze_path}")
    
    except Exception:
        logger.exception(f"Erro ao carregar arquivo no datalake bronze")
        raise 