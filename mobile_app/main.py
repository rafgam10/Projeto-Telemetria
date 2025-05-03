from kivymd.app import MDApp
from kivy.core.window import Window
from kaki.app import App
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton, MDRectangleFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.toolbar import MDTopAppBar  # tudo junto: MDToolbar
#import matplotlib.pyplot as plt # Lib do Gráfico
import os
from services.func import *


# from kivy.config import Config
# Config.set('kivy', 'keyboard_mode', 'dock')


#Tamanho da Janela:
Window.size = (400, 640)  # largura x altura em pixels

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

class MainApp(MDApp, App):

    def build(self, **kwargs):
        Builder.load_file(os.path.join("mobile_app", "screens", "login.kv"))
        Builder.load_file(os.path.join("mobile_app", "screens", "home.kv"))
        Builder.load_file(os.path.join("mobile_app", "screens", "perfil.kv"))
        Builder.load_file(os.path.join('mobile_app', 'screens', 'historico.kv'))
        Builder.load_file(os.path.join('mobile_app', 'screens', 'config.kv'))
        Builder.load_file(os.path.join('mobile_app', 'screens', 'suporte.kv'))

        self.sm = MDScreenManager()
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(SuporteScreen(name="suporte"))
        self.sm.add_widget(PerfilScreen(name="perfil"))
        self.sm.add_widget(HistoryScreen(name="historico"))
        self.sm.add_widget(ConfigScreen(name="config"))

        #return self.sm
        return Builder.load_file(os.path.join("mobile_app", "screens", "login.kv"))
        #return Builder.load_file(os.path.join("mobile_app", "screens", "historico.kv"))

    def pegar_placa(self):
        placaInput = self.sm.get_screen("login").ids.placa_input.text
        print(f"Placa digitada: {placaInput}")
        self.sm.get_screen("login").ids.placa_input.text = ""

        if verificar_placa_no_servidor(placaInput):
        # if placa == "123":
            self.sm.current = "home"

    def ir_para_login(self):
        self.sm = MDScreenManager()
        Builder.load_file(os.path.join("screens", "login.kv"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.current = "login"
        return self.sm

    def mudar_tela(self, nome_tela):
        self.app.current = nome_tela

    def salvar_config(self):
        pass

if __name__ == "__main__":
    MainApp().run()
