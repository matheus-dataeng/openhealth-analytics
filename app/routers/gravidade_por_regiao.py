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
        query = text(
            '''
            SELECT
                ibge.regiao,
                COUNT(*) AS total_casos,
                SUM(CASE WHEN den.classificacao_final = 'dengue grave' THEN 1 ELSE 0 END) AS casos_dengue_grave,
                ROUND(100.0 * SUM(CASE WHEN den.classificacao_final = 'dengue grave' THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentual_dengue_grave
            FROM silver.silver_dengue AS den
            LEFT JOIN silver.silver_ibge AS ibge
                ON CAST(den.cod_municipio_residencia AS BIGINT)::text = LEFT(ibge.cod_municipio::text, 6)
            GROUP BY ibge.regiao
            ORDER BY percentual_dengue_grave DESC
        
            '''      
        )
        
        result = db.execute(query)
        logger.info("Gravidade por Região")
        return result.mappings().all()
    
    except SQLAlchemyError as e:
        logger.error(f"Falha ao consultar gravidade por região: {e}")
        raise HTTPException(status_code= 500, detail= "Erro ao consultar gravidade por região ❌")
        