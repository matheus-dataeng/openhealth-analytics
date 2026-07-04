import logging as log 
from app.dependencies import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text 
from sqlalchemy.exc import SQLAlchemyError

logger = log.getLogger(__name__)
router = APIRouter()

@router.get("/gravidade-por-regiao")

def gravidade_regiao(db = Depends(get_db)) -> list[dict]:
    
    try:
             
        result = db.execute(text("SELECT * FROM gold.gravidade_por_regiao"))
        logger.info("Gravidade por Região")
        return result.mappings().all()
    
    except SQLAlchemyError as e:
        logger.error(f"Falha ao consultar gravidade por região: {e}")
        raise HTTPException(status_code= 500, detail= "Erro ao consultar gravidade por região ❌")
        