import streamlit as st 
import pandas as pd 
import plotly.express as px 
from utils.api import get_casos_por_uf

st.title("Casos por UF")

dados = get_casos_por_uf()

df = pd.DataFrame(dados)

with st.expander("Visualizar dados"):
    st.dataframe(df, use_container_width=True)

df = df.sort_values(
    "total_casos",
    ascending=False
)

graph_casos_uf = px.bar(
    df,
    x="uf",
    y="total_casos",
    text_auto=True,
    title="Quantidade de Casos por UF"
)

st.plotly_chart(graph_casos_uf,use_container_width=True)