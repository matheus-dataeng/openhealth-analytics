import streamlit as st 
import pandas as pd 
import plotly.express as px
from utils.api import get_taxa_cura_uf

st.title("Taxa de cura por UF")

dados = get_taxa_cura_uf()

df = pd.DataFrame(dados)

with st.expander("Visualizar dados"):
    st.dataframe(df, use_container_width=True)

graph_taxa_cura = px.bar(
    df,
    x="uf",
    y="percentual_cura",
    title="Porcentagem de cura por UF"
)

st.plotly_chart(graph_taxa_cura, use_container_width=True)