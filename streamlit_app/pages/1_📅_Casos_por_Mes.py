import streamlit as st 
import pandas as pd 
import plotly.express as px 
from utils.api import get_casos_por_mes

st.title("Casos por Mês")

dados = get_casos_por_mes()

df = pd.DataFrame(dados)

with st.expander("Visualizar dados"):
    st.dataframe(df, use_container_width=True)

graph_casos_mes = px.line(
    df,
    x="mes",
    y="total_casos",
    markers=True,
    title= "Evolução de casos de dengue por mês"
)

st.plotly_chart(graph_casos_mes, use_container_width=True)