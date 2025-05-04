import requests, json
import matplotlib.pyplot as plt


# Função para verificar a placa para acesso de login:
def verificar_placa_no_servidor(placa):
    response = requests.get(f"http://127.0.0.1:5000/api/placas")
    if response.status_code == 200:
        placas = response.json()["placas"]
        return placa.upper() in placas
    return False

# Função Todos os Dados da API:
def Dados_API():
    response = requests.get(f"http://127.0.0.1:5000/api/dados")
    #Código para retorna o dict dos dados gerais.


# Função para pegar Dados da placa:
def pegar_dado(placaId):
        url = f'http://127.0.0.1:5000/api/dados/{placaId}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()


