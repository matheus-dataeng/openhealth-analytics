import logging as log 
from utils.logger_config import log_config
from sources.dengue.extract_dengue import extract_dengue, load_bronze_datalake_dengue
from sources.regiao.extract_regiao import extract_regiao, load_bronze_datalake_regiao
from sources.clima.extract_clima import extract_clima, load_bronze_datalake_clima
from sources.populacao.extract_populacao import extract_populacao, load_bronze_datalake_populacao
from export.export_datalake import credentials_datalake, silver_datalake, gold_datalake
from load import credentials_load, load

logger = log.getLogger(__name__)
log_config()

def main() -> None:
    
    logger.info("Iniciando Pipeline")
    
    try: 
        
        engine_load = credentials_load()
        
        dados_dengue = extract_dengue()
        load_bronze_datalake_dengue(dados_dengue)
        load(dados_dengue, table_name="raw_dengue", schema_name="bronze", engine=engine_load)
        
        dados_regiao = extract_regiao()
        load_bronze_datalake_regiao(dados_regiao)
        load(dados_regiao, table_name="raw_regiao", schema_name="bronze", engine=engine_load)
        
        dados_clima = extract_clima()
        load_bronze_datalake_clima(dados_clima)
        load(dados_clima, table_name="raw_clima", schema_name="bronze", engine=engine_load)
        
        dados_populacao = extract_populacao()
        load_bronze_datalake_populacao(dados_populacao)
        load(dados_populacao, table_name="raw_populacao", schema_name="bronze", engine=engine_load)
    
        logger.info("Pipeline Finalizado")
        
    except Exception as e:
        logger.error(f"Falha no Pipeline: {e}")
        raise
    
    try: 
        
        logger.info("Iniciando carga nos datalakes silver e gold")
        
        engine_datalake = credentials_datalake()
        
        silver_datalake(engine=engine_datalake)
        gold_datalake(engine=engine_datalake)
        
        logger.info("Arquivos carregados")
    
    except Exception:
        logger.exception("Falha ao carregar arquivos")
        raise
            
if __name__ == "__main__":
    main()