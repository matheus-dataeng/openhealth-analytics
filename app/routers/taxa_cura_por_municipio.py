import logging as log 
from app.dependencies import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text 
from sqlalchemy.exc import SQLAlchemyError

logger = log.getLogger(__name__)
router = APIRouter()

@router.get("/taxa-cura-por-municipio")

def taxa_cura_municipio(db = Depends(get_db)):
    
    try:

        result = db.execute(text("SELECT * FROM gold.taxa_cura_por_municipio"))
        logger.info("Taxa de Cura por Municipio")
        return result.mappings().all()
    
    except SQLAlchemyError as e:
        logger.error(f"Falha ao consultar taxa de cura por municipio: {e}")
        raise HTTPException(status_code= 500, detail="Erro ao consultar taxa de cura por municipio ❌")