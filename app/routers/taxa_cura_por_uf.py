import logging as log 
from app.dependencies import get_db
from sqlalchemy.exc import SQLAlchemyError 
from sqlalchemy import text 
from fastapi import APIRouter, Depends, HTTPException

logger = log.getLogger(__name__)
router = APIRouter()

@router.get("/taxa-cura-por-uf")

def taxa_cura_uf(db = Depends(get_db)) -> list[dict]:
    
    try:
        
        result = db.execute(text("SELECT * FROM gold.taxa_cura_por_uf ORDER BY percentual_cura DESC"))
        logger.info("taxa de cura por UF")
        return result.mappings().all()
    
    except SQLAlchemyError as e:
        logger.error(f"Falha ao consultar taxa de cura por UF:{e} ❌")
        raise HTTPException(status_code= 500, detail="Erro ao consultar taxa de cura por UF ❌")
        