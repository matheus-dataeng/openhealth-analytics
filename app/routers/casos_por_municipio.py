import logging as log 
from app.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text 
from sqlalchemy.exc import SQLAlchemyError

logger = log.getLogger(__name__)
router = APIRouter()

@router.get("/casos-por-municipio")

def casos_municipio(db = Depends(get_db)) -> list[dict]:
    
    try:
        result = db.execute(text("SELECT * FROM gold.casos_por_municipio"))
        logger.info("Casos por municipio")
        return result.mappings().all()

    except SQLAlchemyError as e:
        logger.error(f"Falha ao consultar casos por municipio: {e}")
        raise HTTPException(status_code= 500, detail= "Erro ao consultar casos por municipio ❌")

