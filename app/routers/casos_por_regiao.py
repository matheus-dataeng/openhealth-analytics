import logging as log 
from app.dependencies import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

logger = log.getLogger(__name__)
router = APIRouter()

@router.get("/casos-por-regiao")

def casos_regiao(db = Depends(get_db)) -> list[dict]: 
    
    try:
        
        query = text(
            '''
            SELECT
                ibge.regiao,
                COUNT(*) AS total_casos
            FROM silver.silver_dengue AS den
            LEFT JOIN silver.silver_ibge AS ibge
                ON CAST(den.cod_municipio_residencia AS BIGINT)::text = LEFT(ibge.cod_municipio::text, 6)
            GROUP BY ibge.regiao
            ORDER BY total_casos DESC
            
            '''
            
        )
        
        result = db.execute(query)
        logger.info("Casos por Região")
        return result.mappings().all()
    
    except SQLAlchemyError as e:
        logger.error(f"Falha ao consultar casos por mes: {e}")
        raise HTTPException(status_code= 500, detail= "Erro ao consultar casos por mes ❌")