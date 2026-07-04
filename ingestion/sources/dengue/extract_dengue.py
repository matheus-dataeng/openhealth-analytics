import pandas as pd 
import logging as log 
import os 
from dotenv import load_dotenv
from pathlib import Path

logger = log.getLogger(__name__)
load_dotenv()

def extract_dengue() -> pd.DataFrame:
    
    logger.info("Iniciando extração dos dados de casos de dengue")
    
    try:
        csv_dengue = os.getenv("DENGUE_CSV")
        
        if not csv_dengue:
            logger.error("Variável de ambiente não encontrado")
            raise ValueError("Variável de ambiente não foi definida")

        df_dengue = pd.read_csv(filepath_or_buffer= csv_dengue, encoding= "utf-8", low_memory= False, sep= ",")
        logger.info(f"Arquivo extraido! / Colunas: {df_dengue.shape[1]} / Linhas: {len(df_dengue)}")
    
    except Exception:
        logger.exception("Erro ao extrair arquivo")
        raise 
    
    return df_dengue 
    
def load_bronze_datalake_dengue(df_dengue: pd.DataFrame) -> None: 
        
    logger.info("Iniciando carga no data lake bronze dengue")
    
    try:    
        
        bronze_dengue = Path("data_lake/bronze/bronze_dengue/bronze_dengue.parquet")
        bronze_dengue.parent.mkdir(parents= True, exist_ok= True)
        df_dengue.to_parquet(bronze_dengue, index= False)        
        logger.info(f"Arquivo salvo: {bronze_dengue}")
    
    except Exception:
        logger.exception(f"Erro ao carregar arquivo")
        raise 