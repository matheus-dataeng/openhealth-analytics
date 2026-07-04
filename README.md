# 🦟 OpenHealth Analytics

Plataforma de dados em saúde pública, construída como uma trilha prática de Engenharia de Dados moderna — não apenas um pipeline de dengue, mas uma arquitetura pensada para crescer com múltiplas fontes de dados em saúde.

> **Status atual:** v3.0 — pipeline multi-fonte (SINAN/DataSUS + IBGE + INMET), com cruzamento geográfico e climático sobre casos de dengue, do dado bruto ao dashboard.

---

## 🎯 Sobre o projeto

O **OpenHealth Analytics** nasceu com um objetivo claro: aprender Engenharia de Dados na prática, simulando as decisões e os trade-offs que aparecem em ambientes reais de mercado — modelagem de dados, arquitetura Medallion, transformação com dbt e, futuramente, processamento distribuído com Spark.

- **v1**: pipeline completo sobre dados de dengue (SINAN/DataSUS, 1º semestre de 2026).
- **v2**: segunda fonte integrada — API de Localidades do IBGE, introduzindo a dimensão geográfica (município, UF, região) e o primeiro cruzamento entre fontes na camada Gold.
- **v3**: terceira fonte integrada — dados climáticos históricos do INMET (BDMEP), cobrindo 27 estações das capitais brasileiras, com cruzamento de temperatura, precipitação e umidade por UF e mês.

---

## 🏗️ Arquitetura

```
SINAN/DataSUS (CSV)    IBGE (API)    INMET/BDMEP (CSV)
        ↓                  ↓                ↓
             Extração (Python/Pandas)
                        ↓
        Data Lake (Parquet) + PostgreSQL
                        ↓
           dbt (Bronze → Silver → Gold)
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
| 🥉 **Bronze** | `view` | Ingestão crua, sem tratamento. Preserva o dado original de cada fonte. |
| 🥈 **Silver** | `view` | Padronização: tradução de códigos, tipagem, regras de negócio. Cada fonte permanece isolada. |
| 🥇 **Gold** | `table` | Camada analítica, pronta para consumo via API. É aqui que as fontes se cruzam. |

> **Por que Bronze/Silver são views e Gold é table?** Bronze e Silver alimentam a Gold e não são consumidas diretamente — mantê-las como `view` garante que qualquer mudança na fonte se propaga automaticamente, sem reprocessamento manual. A Gold é a camada de consumo (API/dashboard), onde performance de leitura importa mais — por isso é materializada como tabela.

> **Por que Bronze e Silver não se misturam entre fontes?** Cada fonte tem sua própria Bronze e Silver, isoladas. O cruzamento entre fontes só acontece na camada Gold, via `JOIN` — preservando a granularidade de cada fonte intacta até o momento certo de combiná-las.

### Organização de pastas (dbt)

```
models/
├── staging/
│   ├── staging_dengue/
│   ├── staging_ibge/
│   └── staging_clima/
├── silver/
│   ├── silver_dengue/
│   ├── silver_ibge/
│   └── silver_clima/
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

## 🛠️ Stack Atual

| Camada | Tecnologia |
|---|---|
| Linguagem | Python |
| Processamento | Pandas |
| Banco de Dados | PostgreSQL |
| ORM / Conexão | SQLAlchemy |
| Transformação | dbt |
| API | FastAPI |
| Dashboard | Streamlit |
| Visualização | Plotly |
| Containerização | Docker / Docker Compose |
| Versionamento | Git / GitHub |

---

## 📊 Camada Gold — Indicadores Disponíveis

### Dengue

| Modelo | Descrição |
|---|---|
| `casos_por_mes` | Total de casos de dengue agregados por mês |
| `casos_por_uf` | Total de casos por Unidade Federativa |
| `classificacao_por_uf` | Distribuição percentual da classificação final por UF |
| `taxa_cura_por_uf` | Percentual de cura por UF |

### Dengue + IBGE

| Modelo | Descrição |
|---|---|
| `casos_por_municipio` | Total de casos por município, com nome, UF, estado e região |
| `casos_por_regiao` | Total de casos agregados por região do Brasil |
| `gravidade_por_regiao` | Percentual de casos de dengue grave por região |
| `taxa_cura_por_municipio` | Percentual de cura por município |

### Dengue + Clima

| Modelo | Descrição |
|---|---|
| `indicadores_clima_uf` | Casos de dengue cruzados com temperatura, precipitação e umidade por UF e mês |

> **Limitação conhecida**: 8 capitais (CE, PB, PE, PI, RO, RR, SC, SE) apresentam dados climáticos ausentes no modelo `indicadores_clima_uf` por indisponibilidade dos sensores das respectivas estações INMET no período analisado (jan–mai/2026).

---

## 🔌 API — Endpoints

A API expõe a camada Gold via FastAPI, com documentação automática (Swagger) em `/docs`, organizada em três grupos.

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/casos-por-mes` | Casos de dengue por mês |
| `GET` | `/casos-por-uf` | Casos de dengue por UF |
| `GET` | `/classificacao-casos-por-uf` | Classificação final dos casos por UF |
| `GET` | `/taxa-cura-por-uf` | Taxa de cura por UF |
| `GET` | `/casos-por-municipio` | Casos por município, UF, estado e região |
| `GET` | `/casos-por-regiao` | Casos por região do Brasil |
| `GET` | `/gravidade-por-regiao` | Percentual de dengue grave por região |
| `GET` | `/taxa-cura-por-municipio` | Taxa de cura por município |
| `GET` | `/indicadores-clima-por-uf` | Casos + clima (temperatura, precipitação, umidade) por UF e mês |

### Rodando a API localmente

```bash
uvicorn app.main:app --reload
```

Disponível em `http://localhost:8000` — documentação interativa em `http://localhost:8000/docs`.

---

## 📈 Dashboard

Dashboard construído em Streamlit com estrutura **multi-page**, consumindo os dados diretamente da API.

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

### Rodando o dashboard localmente

```bash
streamlit run streamlit_app/Home.py
```

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- dbt

### 1. Clonar o repositório

```bash
git clone https://github.com/matheus-dataeng/OpenHealth-Analytics.git
cd OpenHealth-Analytics
```

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz com as credenciais do banco (veja `.env.example` se disponível).

### 3. Subir o banco de dados

```bash
docker-compose up -d
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Executar o pipeline de ingestão

```bash
python ingestion/main.py
```

### 6. Executar as transformações dbt

```bash
cd openhealth_dbt
dbt run
```

### 7. Exportar o Data Lake (Silver e Gold em Parquet)

```bash
python ingestion/export/export_datalake.py
```

### 8. Subir a API

```bash
uvicorn app.main:app --reload
```

### 9. Subir o dashboard

```bash
streamlit run streamlit_app/Home.py
```

---

## 🗺️ Roadmap

- [x] **v1 — Dengue isolada**: pipeline completo (extração, dbt, API, dashboard) com uma única fonte.
- [x] **v2 — IBGE**: dimensão geográfica (município, UF, região), primeiro cruzamento entre fontes na Gold.
- [x] **v3 — Clima (INMET)**: dados climáticos históricos das 27 capitais, cruzados com casos de dengue por UF e mês.
- [ ] **v4 — Indicadores socioeconômicos**: integração com dados do Censo IBGE 2022, cruzando dengue com IDH, renda e densidade populacional.
- [ ] **Avaliação de Spark**: conforme o volume e a complexidade dos joins crescem com novas fontes, avaliar migração de Pandas para Apache Spark.
- [ ] **Deploy**: publicação da API e do dashboard em ambiente cloud (AWS EC2).
- [ ] **Orquestração com Airflow**: introduzida ao final do projeto, quando a arquitetura multi-fonte estiver madura e estável.

---

## 📌 Fonte dos Dados

- **Dengue**: SINAN (Sistema de Informação de Agravos de Notificação) — DataSUS/Ministério da Saúde.
- **Localidades**: API de Localidades do IBGE.
- **Clima**: BDMEP (Banco de Dados Meteorológicos) — INMET, estações automáticas das 27 capitais, jan–mai/2026.

---

[LinkedIn](https://linkedin.com/in/matheus-men) 
