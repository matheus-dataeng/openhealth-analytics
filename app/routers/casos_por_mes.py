import logging as log 
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError 
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db

logger = log.getLogger(__name__)
router = APIRouter()

@router.get("/casos-por-mes")

def casos_por_mes(db = Depends(get_db)) -> list[dict]:
    
    try:
           
        result = db.execute(text("SELECT * FROM gold.casos_por_mes ORDER BY mes"))
        logger.info("Casos por mês")
        return result.mappings().all()
    
    except SQLAlchemyError as e:
        logger.error(f"Falha ao consultar casos por mês: {e}")
        raise HTTPException(status_code= 500, detail="Erro ao consultar casos por mês ❌")
    
    
        