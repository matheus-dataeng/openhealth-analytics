import pandas as pd
import streamlit as st
import plotly.express as px
from utils.api import get_casos_regiao

st.title("Casos por Região")

dados = get_casos_regiao()

df = pd.DataFrame(dados)

with st.expander("Visualizar dados"):
    st.dataframe(df, use_container_width=True)

graph_casos_regiao = px.bar(
    df,
    x="total_casos",
    y="regiao",
    orientation="h",
    text_auto=True,
    title="Casos por Região"
)

st.plotly_chart(graph_casos_regiao, use_container_width=True)