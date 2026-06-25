from fastapi import FastAPI
from ingestion.utils.logger_config import log_config
from app.routers.casos_por_mes import router as casos_por_mes
from app.routers.casos_por_uf import router as casos_por_uf
from app.routers.classificacao_por_uf import router as classificacao_por_uf
from app.routers.taxa_cura_por_uf import router as taxa_cura_por_uf

log_config()

app = FastAPI(
    title="OpenHealth Analytics API",
    description=(
        "API de dados analíticos sobre dengue no Brasil, construída sobre uma "
        "arquitetura Medallion (Bronze/Silver/Gold) com PostgreSQL e dbt. "
        "Parte do projeto OpenHealth Analytics, uma plataforma de dados voltada "
        "à área da saúde."
    ),
    version="1.0.0",
    contact={
        "name": "Matheus",
        "url": "https://github.com/matheus-dataeng",
    },
    openapi_tags=[
        {
            "name": "Dengue",
            "description": "Indicadores analíticos sobre casos de dengue, "
                            "agregados a partir da camada Gold.",
        },
    ],
)

app.include_router(
    casos_por_mes,
    tags=["Casos por Mês 📅"]
)
app.include_router(
    casos_por_uf,
    tags=["Casos por UF 📍"]
)
app.include_router(
    classificacao_por_uf,
    tags=["Classificação 🩺"]
)
app.include_router(
    taxa_cura_por_uf,
    tags=["Taxa de Cura 💊"]
)