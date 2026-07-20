import pandas as pd 
import logging as log
import os 
from dotenv import load_dotenv 
from pathlib import Path
from ingestion.export.s3_export import bucket_s3

logger = log.getLogger(__name__)
load_dotenv()

def extract_populacao() -> pd.DataFrame:
    
    logger.info("Iniciando extração dos dados populacionais")
    
    try:
            csv_populacao = os.getenv("POPULACAO_XSL")
            
            if not csv_populacao:
                logger.error("Variavel não definida no .env")
                raise ValueError("Variável de ambiente não foi definida")
            
            df_populacao = pd.read_excel(
                csv_populacao, 
                sheet_name="MUNICÍPIOS", 
                skiprows=1, 
                usecols=["UF", "COD. UF", "COD. MUNIC", "NOME DO MUNICÍPIO", "POPULAÇÃO ESTIMADA"]
            )
            
            logger.info(f"Arquivo extraido / Colunas: {df_populacao.shape[1]} / Linhas: {len(df_populacao)}")

            return df_populacao
        
    except Exception:
        logger.exception("Erro ao extrair dados de populacionais")
        raise

def load_bronze_datalake_populacao(df_populacao: pd.DataFrame) -> None:
    
    logger.info("Inciando carga no datalake bronze populacional")
    
    try:
        bronze_populacao = Path("data_lake/bronze/bronze_populacao.parquet")
        bronze_populacao.parent.mkdir(parents=True, exist_ok=True)
        df_populacao.to_parquet(bronze_populacao, index=False)
        bucket_s3(bronze_populacao, "bronze/bronze_populacao.parquet")
        logger.info(f"Arquivo salvo em {bronze_populacao}")
    
    except Exception:
        logger.exception("Falha ao carregar arquivo")
        raise 