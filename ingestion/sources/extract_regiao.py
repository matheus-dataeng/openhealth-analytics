import requests 
import pandas as pd 
import logging as log 
from pathlib import Path
from ingestion.export.s3_export import bucket_s3

logger = log.getLogger(__name__)

def extract_regiao() -> pd.DataFrame:
    
    logger.info("Iniciando extração dos dados regionais")

    try:
        url_api = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        response = requests.get(url_api, timeout=10)
        dados = response.json()

        df = pd.json_normalize(dados)

        colunas_selecionadas = [
            "id",
            "nome",
            "microrregiao.mesorregiao.UF.sigla",
            "microrregiao.mesorregiao.UF.nome",
            "microrregiao.mesorregiao.UF.regiao.nome"
        ]
        
        df_regiao = df[colunas_selecionadas]
        logger.info(f"Dados extraidos! / Colunas:{df_regiao.shape[1]} / Linhas: {len(df_regiao)}")
        return df_regiao 
    
    except Exception:
        logger.exception(f"Erro ao extrair dados")
        raise 

def load_bronze_datalake_regiao(df_regiao: pd.DataFrame) -> None:
    
    logger.info("Iniciando carga do datalake bronze regiao")
    
    try:
        bronze_regiao = Path("data_lake/bronze/bronze_regiao.parquet")
        bronze_regiao.parent.mkdir(parents=True, exist_ok=True)
        df_regiao.to_parquet(bronze_regiao, index=False)
        bucket_s3(bronze_regiao, "bronze/bronze_regiao.parquet")        
        logger.info(f"Arquivo salvo: {bronze_regiao}")
    
    except Exception:
        logger.exception("Erro ao carregar arquivo")        
        raise 