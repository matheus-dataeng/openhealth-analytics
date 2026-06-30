import requests 
import pandas as pd 
import logging as log 
from pathlib import Path

logger = log.getLogger(__name__)

def extract_ibge() -> pd.DataFrame:
    
    logger.info("Iniciando extração dos dados do ibge")

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
        
        df_ibge = df[colunas_selecionadas]
        logger.info(f"Dados extraidos! / Colunas:{df_ibge.shape[1]} / Linhas: {len(df_ibge)}")
        return df_ibge 
    
    except Exception:
        logger.exception(f"Erro ao extrair dados")
        raise 

def load_bronze_datalake_ibge(df_ibge: pd.DataFrame) -> None:
    
    logger.info("Iniciando carga do datalake bronze ibge")
    
    try:
        bronze_ibge = Path("data_lake/bronze/bronze_ibge/bronze_ibge.parquet")
        bronze_ibge.parent.mkdir(parents=True, exist_ok=True)
        df_ibge.to_parquet(bronze_ibge, index=False)        
        logger.info(f"Arquivo salvo: {bronze_ibge}")
    
    except Exception:
        logger.exception("Erro ao carregar arquivo")        
        raise 