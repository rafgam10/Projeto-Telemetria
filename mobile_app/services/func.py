import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import os
import requests, json

# Objeto do Historico:
class ObjHistorico:
    
    def __init__(self, *args, **kwargs):
         super(CLASS_NAME, self).__init__(*args, **kwargs)
    
    


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


#Gráficos:
def atualizar_swiper_com_graficos(self):
    home_screen = self.sm.get_screen("home")
    swiper = home_screen.ids.meu_swiper  # << Certifique-se que o ID no .kv está correto

    swiper.clear_widgets()  # Limpa os swiper items anteriores

    lista_de_dados = [self.dados_motorista]  # Pode ser múltiplos conjuntos futuramente

    for i, dados in enumerate(lista_de_dados):
        caminho_grafico = gerar_grafico_dados_motorista([dados], salvar_em=f"grafico{i}.png")
        caminho_grafico = os.path.join("mobile_app", "static", f"grafico{i}.png")

        swiper_item = MDSwiperItem()
        imagem = FitImage(
            source=caminho_grafico,
            radius=[20],
            size_hint=(None, None),
            size=(250, 350),
            pos_hint={"center_x": 0.5, "center_y": 0.53},
        )
        swiper_item.add_widget(imagem)
        swiper.add_widget(swiper_item)