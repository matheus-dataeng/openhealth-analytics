import logging as log 
from app.dependencies import get_db
from sqlalchemy.exc import SQLAlchemyError 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text 

logger = log.getLogger(__name__)
router = APIRouter() 

@router.get("/casos-por-uf")

def casos_por_uf(db = Depends(get_db)) -> list[dict]:
    
    try:
        
        result = db.execute(text("SELECT * FROM gold.casos_por_uf"))
        logger.info("Casos por UF")
        return result.mappings().all()
    
    except SQLAlchemyError as e:
        logger.error(f"Falha ao consultar casos por UF: {e} ❌") 
        raise HTTPException(status_code= 500, detail= "Erro ao consultar casos por UF ❌")
    