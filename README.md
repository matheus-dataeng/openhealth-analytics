# 🦟 OpenHealth Analytics

Plataforma de dados em saúde pública, construída como uma trilha prática de Engenharia de Dados moderna — não apenas um pipeline de dengue, mas uma arquitetura pensada para crescer com múltiplas fontes de dados em saúde.

> **Status atual:** v2.0 — pipeline multi-fonte (SINAN/DataSUS + IBGE), com cruzamento geográfico entre dengue e localidades, do dado bruto ao dashboard.

---

## 🎯 Sobre o projeto

O **OpenHealth Analytics** nasceu com um objetivo claro: aprender Engenharia de Dados na prática, simulando as decisões e os trade-offs que aparecem em ambientes reais de mercado, modelagem de dados, arquitetura Medallion, transformação com dbt e, futuramente, processamento distribuído com Spark.

A v1 usou um dataset público de **dengue no Brasil** (SINAN/DataSUS, 1º semestre de 2026) como primeira fonte de dados. A v2 introduziu a **API de Localidades do IBGE** como segunda fonte, trazendo a dimensão geográfica (município, UF, região) que permite enriquecer e cruzar os casos de dengue por localidade — o primeiro passo real rumo à plataforma multi-fonte que o projeto sempre teve como visão.

---

## 🏗️ Arquitetura

```
SINAN/DataSUS (CSV)        IBGE (API)
        ↓                       ↓
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
| 🥈 **Silver** | `view` | Padronização: tradução de códigos, tipagem, regras de negócio (`CASE WHEN`). Cada fonte permanece isolada. |
| 🥇 **Gold** | `table` | Camada analítica, pronta para consumo via API. É aqui que as fontes se cruzam. |

> **Por que Bronze/Silver são views e Gold é table?** Bronze e Silver alimentam a Gold e não são consumidas diretamente — mantê-las como `view` garante que qualquer mudança na fonte se propaga automaticamente, sem reprocessamento manual. A Gold é a camada de consumo (API/dashboard), onde performance de leitura importa mais do que atualização em tempo real — por isso é materializada como tabela.

> **Por que Bronze e Silver não se misturam entre fontes?** Cada fonte (dengue, IBGE) tem sua própria Bronze e Silver, isoladas. O cruzamento entre dengue e IBGE só acontece na camada Gold, via `JOIN` — preservando a granularidade de cada fonte intacta até o momento certo de combiná-las.

### Organização de pastas (dbt)

As pastas de modelos são organizadas por fonte dentro de cada camada, como organização visual — todas seguem o mesmo schema único por camada no banco (`bronze`, `silver`, `gold`), sem subdivisão de schema por fonte.

```
models/
├── staging/
│   ├── staging_dengue/
│   └── staging_ibge/
├── silver/
│   ├── silver_dengue/
│   └── silver_ibge/
└── gold/
     # métricas só de dengue
     # métricas cruzando dengue + IBGE
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
| Versionamento | Git / GitHub |

---

## 📊 Camada Gold — Indicadores Disponíveis

### Dengue

| Modelo | Descrição |
|---|---|
| `casos_por_mes` | Total de casos de dengue agregados por mês |
| `casos_por_uf` | Total de casos por Unidade Federativa |
| `classificacao_por_uf` | Distribuição percentual da classificação final dos casos (dengue, dengue grave, descartado...) por UF |
| `taxa_cura_por_uf` | Percentual de cura por UF |

### Dengue + IBGE

| Modelo | Descrição |
|---|---|
| `casos_por_municipio` | Total de casos por município, com nome, UF, estado e região |
| `casos_por_regiao` | Total de casos agregados por região do Brasil |
| `gravidade_por_regiao` | Percentual de casos de dengue grave por região |
| `taxa_cura_por_municipio` | Percentual de cura por município |

> O cruzamento entre dengue e IBGE é feito pelo código de município, com truncamento do código IBGE (7 dígitos) para o padrão de 6 dígitos usado pelo SINAN (`ID_MN_RESI`).

---

## 🔌 API — Endpoints

A API expõe a camada Gold via FastAPI, com documentação automática (Swagger) em `/docs`, organizada em duas categorias: **Dengue** e **Dengue + IBGE**.

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/casos-por-mes` | Casos de dengue agregados por mês |
| `GET` | `/casos-por-uf` | Casos de dengue agregados por UF |
| `GET` | `/classificacao-casos-por-uf` | Classificação final dos casos, em percentual, por UF |
| `GET` | `/taxa-cura-por-uf` | Taxa de cura por UF |
| `GET` | `/casos-por-municipio` | Casos de dengue por município, UF, estado e região |
| `GET` | `/casos-por-regiao` | Casos de dengue agregados por região |
| `GET` | `/gravidade-por-regiao` | Percentual de dengue grave por região |
| `GET` | `/taxa-cura-por-municipio` | Taxa de cura por município |

### Rodando a API localmente

```bash
uvicorn app.main:app --reload
```

A API fica disponível em `http://localhost:8000`, com a documentação interativa em `http://localhost:8000/docs`.

---

## 📈 Dashboard

O dashboard é construído em Streamlit, com estrutura **multi-page**: uma página dedicada para cada indicador, consumindo os dados diretamente da API.

```
streamlit_app/
├── Home.py
├── pages/
│   ├── 1_📅_Casos_por_Mes.py
│   ├── 2_📍_Casos_por_UF.py
│   ├── 3_🩺_Classificacao_por_UF.py
│   ├── 4_💊_Taxa_de_Cura_por_UF.py
│   ├── 5_🗺️_Casos_por_Regiao.py
│   └── 6_⚠️_Gravidade_por_Regiao.py
└── utils/
    └── api.py
```

> Os endpoints de `casos-por-municipio` e `taxa-cura-por-municipio` estão disponíveis na API, mas não possuem página própria no dashboard nesta versão.

### Rodando o dashboard localmente

```bash
streamlit run streamlit_app/Home.py
```

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- dbt

### 2. Clonar o repositório

```bash
git clone https://github.com/<seu-usuario>/OpenHealth-Analytics.git
cd OpenHealth-Analytics
```

### 3. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as credenciais do banco de dados (veja `.env.example`, se disponível).

### 4. Subir o banco de dados

```bash
docker-compose up -d
```

### 5. Executar o pipeline de ingestão (dengue + IBGE)

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
- [x] **v2 — Segunda fonte (IBGE)**: integração com a API de Localidades do IBGE, criando a dimensão geográfica (`silver_ibge`) e cruzando com dengue na camada Gold.
- [ ] **Avaliação de Spark**: medir se Pandas ainda é suficiente conforme novas fontes entram, ou se os joins entre fontes de granularidades diferentes justificam a migração.
- [ ] **Terceira fonte**: dados climáticos (INMET/CPTEC), para investigar a relação entre clima e incidência de dengue.
- [ ] **Quarta fonte**: indicadores socioeconômicos (IBGE/Atlas Brasil).
- [ ] **Deploy**: publicação da API e do dashboard em ambiente cloud (AWS EC2).
- [ ] **Orquestração com Airflow**: introduzida ao final do projeto, quando a arquitetura multi-fonte estiver madura e estável.

---

## 📌 Fonte dos Dados

- **Dengue**: Sistema de Informação de Agravos de Notificação (**SINAN**), disponibilizado pelo **DataSUS** — Ministério da Saúde do Brasil.
- **Localidades**: API de Localidades do **IBGE** (Instituto Brasileiro de Geografia e Estatística).