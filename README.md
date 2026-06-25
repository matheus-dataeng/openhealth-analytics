# 🦟 OpenHealth Analytics

Plataforma de dados em saúde pública, construída como uma trilha prática de Engenharia de Dados moderna — não apenas um pipeline de dengue, mas uma arquitetura pensada para crescer com múltiplas fontes de dados em saúde.

> **Status atual:** v1.0 — pipeline completo de ponta a ponta sobre dados de dengue (SINAN/DataSUS), do dado bruto ao dashboard.

---

## 🎯 Sobre o projeto

O **OpenHealth Analytics** nasceu com um objetivo claro: aprender Engenharia de Dados na prática, simulando as decisões e os trade-offs que aparecem em ambientes reais de mercado, modelagem de dados, arquitetura Medallion, transformação com dbt e, futuramente, processamento distribuído com Spark.

A v1 usa um dataset público de **dengue no Brasil**, 1º semestre de 2026 como primeira fonte de dados. A visão de longo prazo é expandir para múltiplas fontes (dados populacionais do IBGE, clima, indicadores socioeconômicos), o que vai justificar tecnicamente a adoção de Apache Spark conforme o volume e a complexidade dos joins crescerem.

---

## 🏗️ Arquitetura

```
SINAN/DataSUS (CSV)
        ↓
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
| 🥉 **Bronze** | `view` | Ingestão crua, sem tratamento. Preserva o dado original. |
| 🥈 **Silver** | `view` | Padronização: tradução de códigos, tipagem, regras de negócio (`CASE WHEN`). |
| 🥇 **Gold** | `table` | Camada analítica, pronta para consumo via API. Materializada para performance de leitura. |

> **Por que Bronze/Silver são views e Gold é table?** Bronze e Silver alimentam a Gold e não são consumidas diretamente — mantê-las como `view` garante que qualquer mudança na fonte se propaga automaticamente, sem reprocessamento manual. A Gold é a camada de consumo (API/dashboard), onde performance de leitura importa mais do que atualização em tempo real — por isso é materializada como tabela.

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

| Modelo | Descrição |
|---|---|
| `casos_por_mes` | Total de casos de dengue agregados por mês |
| `casos_por_uf` | Total de casos por Unidade Federativa |
| `classificacao_por_uf` | Distribuição percentual da classificação final dos casos (dengue, dengue grave, descartado...) por UF |
| `taxa_cura_por_uf` | Percentual de cura por UF |

---

## 🔌 API — Endpoints

A API expõe a camada Gold via FastAPI, com documentação automática (Swagger) em `/docs`.

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/casos-por-mes` | Casos de dengue agregados por mês |
| `GET` | `/casos-por-uf` | Casos de dengue agregados por UF |
| `GET` | `/classificacao-casos-por-uf` | Classificação final dos casos, em percentual, por UF |
| `GET` | `/taxa-cura-por-uf` | Taxa de cura por UF |

### Rodando a API localmente

```bash
uvicorn app.main:app --reload
```

A API fica disponível em `http://localhost:8000`, com a documentação interativa em `http://localhost:8000/docs`.

---

## 📈 Dashboard

O dashboard é construído em Streamlit, com estrutura **multi-page**: uma página dedicada para cada indicador da camada Gold, consumindo os dados diretamente da API.

```
streamlit_app/
├── Home.py
├── pages/
│   ├── 1_📅_Casos_por_Mes.py
│   ├── 2_📍_Casos_por_UF.py
│   ├── 3_🩺_Classificacao_por_UF.py
│   └── 4_💊_Taxa_de_Cura_por_UF.py
└── utils/
    └── api.py
```

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

### 5. Executar o pipeline de ingestão

```bash
python ingestion/main.py
```

### 6. Executar as transformações dbt

```bash
cd openhealth_dbt
dbt run
```

### 7. Subir a API

```bash
uvicorn app.main:app --reload
```

### 8. Subir o dashboard

```bash
streamlit run streamlit_app/Home.py
```

---

## 🗺️ Roadmap

A v1 cobre o ciclo completo com uma única fonte de dados (dengue). Os próximos passos planejados:

- [ ] **Segunda fonte de dados**: integração com dados populacionais do IBGE, criando uma dimensão geográfica (`dim_municipio`) compartilhada entre fontes.
- [ ] **Avaliação de Spark**: medir se Pandas ainda é suficiente após a segunda fonte, ou se os joins entre fontes de granularidades diferentes justificam a migração.
- [ ] **Terceira fonte**: dados climáticos (INMET/CPTEC), para investigar a relação entre clima e incidência de dengue.
- [ ] **Quarta fonte**: indicadores socioeconômicos (IBGE/Atlas Brasil).
- [ ] **Deploy**: publicação da API e do dashboard em ambiente cloud (AWS EC2).

---

## 📌 Fonte dos Dados

Dados públicos do **SINAN (Sistema de Informação de Agravos de Notificação)**, disponibilizados pelo **DataSUS** — Ministério da Saúde do Brasil.

