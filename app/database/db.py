import logging as log 
import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = log.getLogger(__name__)
load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

if not all([user, password, host, port, dbname]):
    logger.error("Variaveis não definidas no arquivo .env")
    raise ValueError("Variaveis não definidas")

try:
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}?sslmode=require&channel_binding=require"
    engine = create_engine(url, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)
    logger.info("✅")

except Exception as e:
    logger.exception(f"Falha na conexão com banco de dados:{e} ❌")
    raise  