from kivymd.app import MDApp
from kivy.core.window import Window
from kaki.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton, MDRectangleFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.toolbar import MDTopAppBar  # tudo junto: MDToolbar
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget

import os

from services.func import *
import requests, json




#Tamanho da Janela:
Window.size = (390, 640)  # largura x altura em pixels

class LoginScreen(MDScreen):
    pass

class HomeScreen(MDScreen):
    pass

class SuporteScreen(MDScreen):
    pass

class PerfilScreen(MDScreen):
    pass

class HistoryScreen(MDScreen):
    pass
    
class ConfigScreen(MDScreen):
    pass

class ErroScreen(MDScreen):
    pass


class MainApp(MDApp, App):

    def build(self, **kwargs):
        Builder.load_file(os.path.join("mobile_app", "screens", "login.kv"))
        Builder.load_file(os.path.join("mobile_app", "screens", "home.kv"))
        Builder.load_file(os.path.join("mobile_app", "screens", "perfil.kv"))
        Builder.load_file(os.path.join('mobile_app', 'screens', 'historico.kv'))
        Builder.load_file(os.path.join('mobile_app', 'screens', 'config.kv'))
        Builder.load_file(os.path.join('mobile_app', 'screens', 'suporte.kv'))
        Builder.load_file(os.path.join("mobile_app", "screens", "404.kv"))

        self.sm = MDScreenManager()
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(SuporteScreen(name="suporte"))
        self.sm.add_widget(PerfilScreen(name="perfil"))
        self.sm.add_widget(HistoryScreen(name="historico"))
        self.sm.add_widget(ConfigScreen(name="config"))
        self.sm.add_widget(ErroScreen(name="erro"))


        self.dados_motorista = {}  # Armazena os dados do motorista

        try:
            requests.get("https://www.google.com", timeout=3)
        except requests.ConnectionError:
            self.sm.current = "erro"

        return self.sm
        #return Builder.load_file(os.path.join("mobile_app", "screens", "home.kv"))
        #return Builder.load_file(os.path.join("mobile_app", "screens", "suporte.kv"))
    
    def verificar_conexao(self):
        try:
            requests.get("https://www.google.com", timeout=3)
            self.sm.current = "login"
        except requests.ConnectionError:
            self.sm.current = "erro"    

    
    def pegar_placa(self):
        placaInput = self.sm.get_screen("login").ids.placa_input.text
        print(f"Placa digitada: {placaInput}")
        self.sm.get_screen("login").ids.placa_input.text = ""

        if verificar_placa_no_servidor(placaInput):
            
            data = pegar_dado(placaId=placaInput)
            
            if data:
                self.lista_historico = data
                self.dados_motorista = data[-1]
                self.atualizar_dados_app()
                self.sm.current = "home"
            else:
                print("Nenhum dado encontrado.")
                self.mostrar_snackbar_erro()
        else:
            self.mostrar_snackbar_erro()

    def atualizar_dados_app(self):
        
        #Páginas para atualizar com dados:
        perfil_screen = self.sm.get_screen("perfil")
        home_screen = self.sm.get_screen('home')
        
        listaNOMEeID = self.dados_motorista.get("motorista", "Desconhecido").split(' - ')
        
        #Atulizar os dados do Historico.kv
        self.add_obj_historico()
        
        # Variaveis do Perfil.kv
        labelId = f"[b]{listaNOMEeID[0]}[/b]"
        labelNome = f"[b]{listaNOMEeID[1]}[/b]"
        labelPlaca = f"[b]{self.dados_motorista.get("placa")}[/b]"
        labelCaminhao = f"[b]{self.dados_motorista.get("marca")}[/b]"
        labelFrota = f"[b]{self.dados_motorista.get("frota")}[/b]"
        labelqtdDias = f"[b]{self.dados_motorista.get("qtdDias")}[/b]"
        labeltotalHrs = f"[b]{self.dados_motorista.get("totalHrs")}[/b]"
        
        # Variaveis do Home.kv
        labelKmRodado = f"[b]{self.dados_motorista.get('KmRodado')}[/b]"
        labelKmChegado = f"[b]{self.dados_motorista.get('KmChegada')}[/b]"
        labelKmSaida = f"[b]{self.dados_motorista.get('KmSaida')}[/b]"
        labelLtDiesel = f"[b]{float(self.dados_motorista.get('LtDiesel')):.2f}[/b]"
        labelLtArla = f"[b]{float(self.dados_motorista.get('LtArla')):.2f}[/b]"
        labelLtPorDia = f"[b]{float(self.dados_motorista.get('LtPorDia')):.2f}[/b]"
        labelData = f"[b]{self.dados_motorista.get('data')}[/b]"
        labelDataChegada = f"[b]{self.dados_motorista.get('dataChegada')}[/b]"
        labelDataSaida = f"[b]{self.dados_motorista.get('datasSaida')}[/b]"
                
        #Colocar no Ids Screen Perfil.kv:
        perfil_screen.ids.Label_ideficador.text = labelId
        perfil_screen.ids.Label_nome.text = labelNome
        perfil_screen.ids.Label_placa.text = labelPlaca
        perfil_screen.ids.Label_caminhao.text = labelCaminhao
        perfil_screen.ids.Label_frota.text = labelFrota
        perfil_screen.ids.Label_qtdDias.text = labelqtdDias
        perfil_screen.ids.Label_totalHrs.text = labeltotalHrs

        #Colocar no Ids Screen Home.kv:
        home_screen.ids.Label_KmRodado.text = labelKmRodado
        home_screen.ids.Label_KmChegada.text = labelKmChegado
        home_screen.ids.Label_KmSaida.text = labelKmSaida
        home_screen.ids.Label_LtPorDia.text = labelLtPorDia
        home_screen.ids.Label_LtDiesel.text = labelLtDiesel
        home_screen.ids.Label_LtArla.text = labelLtArla
        home_screen.ids.Label_Data.text = labelData
        home_screen.ids.Label_DataChegada.text = labelDataChegada
        home_screen.ids.Label_DataSaida.text = labelDataSaida

    def mostrar_snackbar_erro(self, *args):
        Snackbar(
            text="[b][color=#FFFFFF]Placa Não Encontrada![/color][/b]",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            snackbar_y="20dp",
            bg_color=(0.66, 0.73, 0.27, 1),
            duration=3,
            radius=[15, 15, 15, 15]
        ).open()

    def ir_para_login(self):
        self.sm = MDScreenManager()
        Builder.load_file(os.path.join("screens", "login.kv"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.current = "login"
        return self.sm

    def add_obj_historico(self):
        container = self.root.get_screen("historico").ids.lista_de_historico
        container.clear_widgets()
        
        if not self.lista_historico:
            return
        
        for item in reversed(self.lista_historico):
            if not isinstance(item, dict):
                print(f"Dado inválido em lista_historico: {item}")
                continue

            data = item.get("data", "Sem data")
            km = item.get("KmRodado", "Sem KM")
            icone = IconLeftWidget(icon="truck-check-outline",
                                   theme_text_color="Custom",
                                   text_color=(0.66, 0.73, 0.27, 1))

            lista_item = TwoLineIconListItem(
                theme_text_color="Custom",
                secondary_theme_text_color="Custom",
                text=f"{data}",
                text_color=(0.66, 0.73, 0.27, 1),
                secondary_text=f"{km} Km Rodado",
                secondary_text_color=(0.18, 0.54, 0.47, 1),
                
            )
            lista_item.add_widget(icone)
            container.add_widget(lista_item)
        
    
    def mudar_tela(self, nome_tela):
        self.app.current = nome_tela

    def salvar_config(self):
        pass


if __name__ == "__main__":
    MainApp().run()
