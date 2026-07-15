import pandas as pd
import streamlit as st
import plotly.express as px
from utils.api import get_indicador_clima_uf

st.title("Indicadores de Clima por UF")

dados = get_indicador_clima_uf()

df = pd.DataFrame(dados)

colunas_numericas = [
    "temperatura_media_c",
    "temperatura_max_c", 
    "temperatura_min_c",
    "precipitacao_total_mm",
    "umidade_media_pct"
]

df[colunas_numericas] = df[colunas_numericas].apply(pd.to_numeric, errors="coerce")

df = df.dropna(subset=colunas_numericas)

with st.expander("Visualizar dados"):
    st.dataframe(df)

graph_indicador_clima = px.scatter(
    df,
    x="temperatura_media_c",
    y="total_casos",
    size="precipitacao_total_mm",
    color="umidade_media_pct",
    hover_name="uf",
    hover_data={
        "temperatura_media_c": ":.1f",
        "temperatura_max_c": ":.1f",
        "temperatura_min_c": ":.1f",
        "precipitacao_total_mm": ":,.0f",
        "umidade_media_pct": ":.1f",
        "total_casos": ":,"
    },
    color_continuous_scale="Turbo",
    title="Temperatura Média x Casos de Dengue"
)

graph_indicador_clima.update_traces(marker=dict(opacity=0.75, line=dict(width=0.5, color="white")))

graph_indicador_clima.update_layout(
    template="plotly_dark",
    height=650,
    xaxis_title="Temperatura Média (°C)",
    yaxis_title="Total de Casos",
    title_x=0.5
)

st.plotly_chart(graph_indicador_clima, use_container_width=True)