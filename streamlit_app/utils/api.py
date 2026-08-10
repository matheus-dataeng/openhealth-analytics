import requests
import time

URL_API = "https://openhealth-analytics.onrender.com"

def _get_com_retry(endpoint, tentativas=3, espera=15):
    for i in range(tentativas):
        try:
            response = requests.get(f"{URL_API}{endpoint}", timeout=60)
            return response.json()
        except requests.exceptions.ConnectionError:
            if i < tentativas - 1:
                time.sleep(espera)
            else:
                raise

def get_casos_por_mes():
    return _get_com_retry("/casos-por-mes")

def get_casos_por_uf():
    return _get_com_retry("/casos-por-uf")

def get_classificacao_por_uf():
    return _get_com_retry("/classificacao-casos-por-uf")

def get_taxa_cura_uf():
    return _get_com_retry("/taxa-cura-por-uf")

def get_casos_regiao():
    return _get_com_retry("/casos-por-regiao")

def get_gravidade_regiao():
    return _get_com_retry("/gravidade-por-regiao")

def get_indicador_clima_uf():
    return _get_com_retry("/indicadores-clima-por-uf")