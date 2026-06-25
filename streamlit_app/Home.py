import streamlit as st

st.set_page_config(
    page_title="OpenHealth Analytics",
    page_icon="🦟",
    layout="wide"
)

st.markdown("""
# 🦟 OpenHealth Analytics
### Plataforma de Dados em Saúde Pública • Dengue • SINAN/DataSUS 2026

Este dashboard apresenta análises sobre os casos de dengue notificados no Brasil,
utilizando dados públicos do Sistema de Informação de Agravos de Notificação (SINAN/DataSUS).

Os dados são processados por um pipeline de engenharia de dados com arquitetura medallion
(Bronze → Silver → Gold), transformados com dbt, salvos em um Data Warehouse PostgreSQL
e disponibilizados através de uma API FastAPI.

---
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Abrangência",
        value="Brasil"
    )

with col2:
    st.metric(
        label="Período de Referência",
        value="1º Semestre 2026"
    )

with col3:
    st.metric(
        label="Fonte dos Dados",
        value="SINAN/DataSUS"
    )

st.markdown("## 📊 Análises Disponíveis")

st.markdown("""
- Evolução dos casos por mês
- Ranking de casos por UF
- Classificação final dos casos por UF
- Taxa de cura por UF
""")

st.info(
    "Utilize o menu lateral para navegar entre as análises disponíveis."
)