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
        
        query = text(
            '''
            SELECT
                ibge.nome_municipio,
                ibge.uf,
                COUNT(*) AS total_casos,
                ROUND(100.0 * SUM(CASE WHEN den.evolucao = 'cura' THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentual_cura
            FROM silver.silver_dengue AS den
            LEFT JOIN silver.silver_ibge AS ibge
                ON CAST(den.cod_municipio_residencia AS BIGINT)::text = LEFT(ibge.cod_municipio::text, 6)
            GROUP BY ibge.nome_municipio, ibge.uf
            ORDER BY percentual_cura DESC
            
            '''
            
        )
        
        result = db.execute(query)
        logger.info("Taxa de Cura por Municipio")
        return result.mappings().all()
    
    except SQLAlchemyError as e:
        logger.error(f"Falha ao consultar taxa de cura por municipio: {e}")
        raise HTTPException(status_code= 500, detail="Erro ao consultar taxa de cura por municipio ❌")