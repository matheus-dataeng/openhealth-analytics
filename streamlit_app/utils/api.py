import requests

URL_API = "http://localhost:8000"

def get_casos_por_mes():
    
    response = requests.get(f"{URL_API}/casos-por-mes")
    return response.json()

def get_casos_por_uf():
    
    response = requests.get(f"{URL_API}/casos-por-uf")
    return response.json()

def get_classificacao_por_uf():
    
     response = requests.get(f"{URL_API}/classificacao-casos-por-uf")
     return response.json()

def get_taxa_cura_uf():
    
    response = requests.get(f"{URL_API}/taxa-cura-por-uf")
    return response.json()

def get_casos_regiao():
    
    response = requests.get(f"{URL_API}/casos-por-regiao")
    return response.json()

def get_gravidade_regiao():
    
    response = requests.get(f"{URL_API}/gravidade-por-regiao")
    return response.json()