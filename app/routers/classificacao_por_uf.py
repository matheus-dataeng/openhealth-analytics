import logging as log 
from app.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text 
from sqlalchemy.exc import SQLAlchemyError

logger = log.getLogger(__name__)
router = APIRouter()

@router.get("/classificacao-casos-por-uf")

def classificacao_por_uf(db = Depends(get_db)) :
    
    try:
        
        result = db.execute(text("SELECT * FROM gold.classificacao_por_uf"))
        logger.info("classificação por UF")
        return result.mappings().all()
    
    except SQLAlchemyError as e:
        logger.error(f"Falha ao consultar classificação por UF: {e}")
        raise HTTPException(status_code= 500, detail="Erro ao consultar classificação por UF ❌")