import streamlit as st
import pandas as pd
import plotly.express as px

from utils.api import get_classificacao_por_uf

st.title("Classificação de Casos por UF")

dados = get_classificacao_por_uf()

df = pd.DataFrame(dados)

with st.expander("Visualizar dados"):
    st.dataframe(df, use_container_width=True)

st.subheader("Análise por Estado")

uf = st.selectbox(
    "Selecione uma UF",
    sorted(df["uf"].unique())
)

df_uf = df[df["uf"] == uf]


graph_classificacao_uf = px.pie(
    df_uf,
    names="classificacao_final",
    values="porcentagem",
    title=f"Distribuição das Classificações - {uf}"
)

st.plotly_chart(graph_classificacao_uf,use_container_width=True)

