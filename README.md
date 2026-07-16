# 🦟 OpenHealth Analytics

> Plataforma de dados em saúde pública (dengue), construída como uma trilha prática de Engenharia de Dados moderna, do dado bruto ao dashboard, com múltiplas fontes integradas e arquitetura Medallion.

---

## 🎯 Sobre o projeto

O **OpenHealth Analytics** simula o trabalho de um Engenheiro de Dados em ambiente real: decisões de arquitetura, múltiplas fontes de dados heterogêneas, camadas de transformação, APIs e dashboards analíticos, tudo aplicado ao domínio de saúde pública.

O projeto foi construído de forma incremental, com cada versão introduzindo uma nova fonte de dados e expandindo a capacidade analítica da plataforma:

| Versão | Fonte | O que foi introduzido |
|---|---|---|
| **v1** | SINAN/DataSUS (CSV) | Pipeline completo: extração, dbt, API, dashboard |
| **v2** | IBGE — Localidades (API) | Dimensão geográfica, primeiro cruzamento entre fontes na Gold |
| **v3** | INMET/BDMEP (CSV) | Dados climáticos, cruzamento clima × dengue por UF e mês |
| **v4** | IBGE — População (XLS) | Taxa de incidência por 100k habitantes, métrica epidemiológica real |

---

## 🏗️ Arquitetura

```
SINAN/DataSUS     IBGE Localidades     INMET/BDMEP     IBGE População
    (CSV)              (API)               (CSV)            (XLS)
      ↓                  ↓                   ↓                ↓
                  Extração (Python / Pandas)
                              ↓
              Data Lake (Parquet) + PostgreSQL (RDS)
                              ↓
                 dbt — Medallion Architecture
                   Bronze → Silver → Gold
                              ↓
                          FastAPI
                              ↓
                          Streamlit
                              ↓
                        Usuário Final
```

### Medallion Architecture

| Camada | Materialização | Responsabilidade |
|---|---|---|
| 🥉 **Bronze** | `view` | Dado bruto, preservado fielmente da fonte. Sem regras de negócio. |
| 🥈 **Silver** | `view` | Padronização: tipos, tradução de códigos. Cada fonte isolada. |
| 🥇 **Gold** | `table` | Camada analítica. Fontes se cruzam. Pronta pra consumo. |

> **Bronze e Silver como views**: qualquer mudança na fonte se propaga automaticamente, sem reprocessamento manual.

> **Gold como table**: performance de leitura importa para a API e o dashboard — por isso é materializada.

> **JOINs só na Gold**: cada fonte permanece isolada até o momento certo de ser combinada, preservando rastreabilidade e granularidade.

### Estrutura de modelos dbt

```
models/
├── staging/
│   ├── staging_dengue/       ← stg_raw_dengue.sql
│   ├── staging_regiao/       ← stg_raw_regiao.sql
│   ├── staging_clima/        ← stg_raw_clima.sql
│   └── staging_populacao/    ← stg_raw_populacao.sql
├── silver/
│   ├── silver_dengue/        ← tradução de códigos SINAN
│   ├── silver_regiao/        ← renomeação de colunas IBGE
│   ├── silver_clima/         ← filtros de sanidade (temperatura, umidade)
│   └── silver_populacao/     ← construção do cod_municipio (7 dígitos)
└── gold/
    ├── casos_por_mes.sql
    ├── casos_por_uf.sql
    ├── classificacao_por_uf.sql
    ├── taxa_cura_por_uf.sql
    ├── casos_por_municipio.sql        
    ├── casos_por_regiao.sql
    ├── gravidade_por_regiao.sql
    ├── taxa_cura_por_municipio.sql
    └── indicadores_clima_uf.sql       
```

---

## 🛠️ Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| Processamento | Pandas |
| Banco de Dados | PostgreSQL 17 (AWS RDS) |
| ORM / Conexão | SQLAlchemy + psycopg2 |
| Transformação | dbt-postgres |
| Orquestração | Apache Airflow |
| API | FastAPI + Uvicorn |
| Dashboard | Streamlit + Plotly |
| Infraestrutura | Docker / Docker Compose |
| Cloud | AWS EC2 + AWS RDS |
| Versionamento | Git / GitHub |

---

## 📊 Camada Gold — Indicadores

### Dengue

| Modelo | Descrição |
|---|---|
| `casos_por_mes` | Total de casos agregados por mês |
| `casos_por_uf` | Total de casos por UF |
| `classificacao_por_uf` | Distribuição percentual da classificação final por UF |
| `taxa_cura_por_uf` | Percentual de cura por UF |

### Dengue + IBGE

| Modelo | Descrição |
|---|---|
| `casos_por_municipio` | Casos por município, com população e taxa de incidência por 100k hab. |
| `casos_por_regiao` | Casos agregados por região do Brasil |
| `gravidade_por_regiao` | Percentual de dengue grave por região |
| `taxa_cura_por_municipio` | Percentual de cura por município |

### Dengue + Clima

| Modelo | Descrição |
|---|---|
| `indicadores_clima_uf` | Casos de dengue × temperatura, precipitação e umidade por UF e mês |

> ⚠️ **Limitação**: 8 capitais (CE, PB, PE, PI, RO, RR, SC, SE) apresentam dados climáticos ausentes por indisponibilidade dos sensores INMET no período analisado (jan–jun/2026).

---

## 🔌 API

Documentação interativa disponível em `/docs` (Swagger UI), organizada em três grupos.

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/casos-por-mes` | Casos de dengue por mês |
| `GET` | `/casos-por-uf` | Casos de dengue por UF |
| `GET` | `/classificacao-casos-por-uf` | Classificação final por UF |
| `GET` | `/taxa-cura-por-uf` | Taxa de cura por UF |
| `GET` | `/casos-por-municipio` | Casos por município com população e incidência |
| `GET` | `/casos-por-regiao` | Casos por região |
| `GET` | `/gravidade-por-regiao` | Percentual de dengue grave por região |
| `GET` | `/taxa-cura-por-municipio` | Taxa de cura por município |
| `GET` | `/indicadores-clima-por-uf` | Casos + variáveis climáticas por UF e mês |

---

## 📈 Dashboard

Dashboard multi-page em Streamlit, com uma página por indicador, consumindo os dados diretamente da API.

```
streamlit_app/
├── Home.py
├── pages/
│   ├── 1_📅_Casos_por_Mes.py
│   ├── 2_📍_Casos_por_UF.py
│   ├── 3_🩺_Classificacao_por_UF.py
│   ├── 4_💊_Taxa_de_Cura_por_UF.py
│   ├── 5_🗺️_Casos_por_Regiao.py
│   ├── 6_⚠️_Gravidade_por_Regiao.py
│   └── 7_🌡️_Indicadores_Clima_por_UF.py
└── utils/
    └── api.py
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- dbt-postgres
- Conta AWS (pra RDS) ou PostgreSQL local

### 1. Clonar o repositório

```bash
git clone https://github.com/matheus-dataeng/OpenHealth-Analytics.git
cd OpenHealth-Analytics
```

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env.docker` na raiz com base no exemplo:

```env
POSTGRES_HOST=<endpoint-do-rds-ou-localhost>
POSTGRES_PORT=5432
POSTGRES_DB=openhealth
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<sua-senha>

DENGUE_CSV_2026=data/DENGBR26.csv
CLIMA_CSV=data/clima_capitais_2026.csv
POPULACAO_CSV=data/POP2024_20241230.xls
```

### 3. Subir os serviços (API + Streamlit)

```bash
docker compose up -d --build
```

### 4. Executar o pipeline de ingestão

```bash
python ingestion/main.py
```

### 5. Executar as transformações dbt

```bash
cd openhealth_dbt
dbt run
```

### 6. Exportar o Data Lake

```bash
python ingestion/export/export_datalake.py
```

### 7. Acessar

| Serviço | URL |
|---|---|
| Dashboard | `http://localhost:8501` |
| API (Swagger) | `http://localhost:8000/docs` |

---

## 🗺️ Roadmap

- [x] **v1** — Pipeline completo: dengue (SINAN/DataSUS), dbt, FastAPI, Streamlit
- [x] **v2** — IBGE Localidades: dimensão geográfica, cruzamento por município/UF/região
- [x] **v3** — INMET/BDMEP: dados climáticos das 27 capitais, cruzamento clima × dengue
- [x] **v4** — IBGE População: taxa de incidência por 100k habitantes por município
- [x] **Deploy** — AWS EC2 (FastAPI + Streamlit) + AWS RDS (PostgreSQL)
- [x] **Orquestração** — Apache Airflow (on-premise) orquestrando o pipeline completo
- [ ] **Landing page** — Frontend estático apresentando o projeto com links pro dashboard e API

---

## 📌 Fontes dos Dados

| Fonte | Descrição |
|---|---|
| **SINAN/DataSUS** | Casos de dengue notificados no Brasil — Ministério da Saúde |
| **IBGE — Localidades** | Municípios, UFs e regiões do Brasil |
| **INMET/BDMEP** | Dados climáticos históricos das estações automáticas das 27 capitais |
| **IBGE — Estimativas Populacionais** | População estimada por município, referência julho/2024 |
