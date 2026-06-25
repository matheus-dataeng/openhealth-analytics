import logging as log 
from extract_csv import extract_csv, load_bronze_datalake
from load import load 
from utils.logger_config import log_config

logger = log.getLogger(__name__)
log_config()

def main(): 
    
    try: 
        logger.info("Iniciando Pipeline")
        
        extract = extract_csv()
        load_bronze_datalake(extract)
        
        load_dw = load(extract)
        
        logger.info("Pipeline finalizado")
        
    except Exception:
        logger.exception("Pipeline falhou")
        raise
if __name__ == "__main__":
    main() 