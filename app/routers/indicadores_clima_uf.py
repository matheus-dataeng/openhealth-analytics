import logging as log 
from sqlalchemy import text 
from sqlalchemy.exc import SQLAlchemyError
from app.dependencies import get_db
from fastapi import APIRouter, HTTPException, Depends

logger = log.getLogger(__name__)
router = APIRouter()

@router.get("/indicadores-clima-por-uf")

def indicadores_clima_uf(db = Depends(get_db)):
    
    try:
        
        result = db.execute(text('SELECT * FROM gold.indicadores_clima_uf'))
        logger.info("Indicadores de clima por UF")
        return result.mappings().all()
    
    except SQLAlchemyError as e:
        logger.error(f"Falha ao consultar indicadores de clima por UF: {e}")
        raise HTTPException(status_code=500, detail="Erro ao consultar indicadores de clima por UF ❌")