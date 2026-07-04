import pandas as pd
import streamlit as st
import plotly.express as px
from utils.api import get_gravidade_regiao

st.title("Gravidade por Região")

dados = get_gravidade_regiao()

df = pd.DataFrame(dados)

with st.expander("Visualizar dados"):
    st.dataframe(df, use_container_width=True)

df = df.sort_values("percentual_dengue_grave", ascending=True)

graph_gravidade_regiao = px.bar(
    df,
    x="percentual_dengue_grave",
    y="regiao",
    orientation="h",
    text="casos_dengue_grave",
    hover_data=["total_casos"],
    title="Percentual de casos de dengue grave por região",
)

st.plotly_chart(graph_gravidade_regiao, use_container_width=True)