from fastapi import FastAPI
from ingestion.utils.logger_config import log_config
from app.routers.casos_por_mes import router as casos_por_mes
from app.routers.casos_por_uf import router as casos_por_uf
from app.routers.classificacao_por_uf import router as classificacao_por_uf
from app.routers.taxa_cura_por_uf import router as taxa_cura_por_uf
from app.routers.casos_por_municipio import router as casos_por_municipio
from app.routers.casos_por_regiao import router as casos_por_regiao
from app.routers.gravidade_por_regiao import router as gravidade_por_regiao
from app.routers.taxa_cura_por_municipio import router as taxa_cura_por_municipio
from app.routers.indicadores_clima_uf import router as indicadores_clima_uf

log_config()

app = FastAPI(
    title="🦟 OpenHealth Analytics API",
    description=(
        "API de dados analíticos sobre dengue no Brasil, construída sobre uma "
        "arquitetura Medallion (Bronze/Silver/Gold) com PostgreSQL e dbt. "
        "Parte do projeto OpenHealth Analytics, uma plataforma de dados voltada "
        "à área da saúde."
    ),
    version="3.0.0",
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
        {
            "name": "Dengue + IBGE",
            "description": "Indicadores que cruzam casos de dengue com a "
                           "dimensão geográfica do IBGE (município, UF, região).",
        },
        {
            "name": "Dengue + Clima",
            "description": "Indicadores que cruzam casos de dengue com dados "
                           "climáticos do INMET (temperatura, precipitação, umidade).",
        },
    ],
)


app.include_router(casos_por_mes, tags=["Casos por Mês 📅"])
app.include_router(casos_por_uf, tags=["Casos por UF 📍"])
app.include_router(classificacao_por_uf, tags=["Classificação 🩺"])
app.include_router(taxa_cura_por_uf, tags=["Taxa de Cura UF 💊"])
app.include_router(casos_por_municipio, tags=["Casos por Município 🏘️"])
app.include_router(casos_por_regiao, tags=["Casos por Região 🗺️"])
app.include_router(gravidade_por_regiao, tags=["Gravidade por Região ⚠️"])
app.include_router(taxa_cura_por_municipio, tags=["Taxa de Cura por Município 💉"])
app.include_router(indicadores_clima_uf, tags=["Indicadores Clima por UF 🌡️"])