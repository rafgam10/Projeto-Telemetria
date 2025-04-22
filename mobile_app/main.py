from kivymd.app import MDApp
from kivy.core.window import Window
from kaki.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDIconButton, MDRectangleFlatIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.toolbar import MDTopAppBar  # tudo junto: MDToolbar
import os


#Tamanho da Janela:
Window.size = (400, 640)  # largura x altura em pixels

class LoginScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class SuporteScreen(Screen):
    pass

class PerfilScreen(Screen):
    pass

class HistoryScreen(Screen):
    pass
    

class LoginApp(MDApp, App):

    def build(self):
        Builder.load_file(os.path.join("mobile_app", "screens", "login.kv"))
        Builder.load_file(os.path.join("mobile_app", "screens", "home.kv"))
        Builder.load_file(os.path.join("mobile_app", "screens", "perfil.kv"))

        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(SuporteScreen(name="suporte"))
        self.sm.add_widget(PerfilScreen(name="perfil"))
        self.sm.add_widget(HistoryScreen(name="historico"))

        # return self.sm
        # return Builder.load_file(os.path.join("mobile_app", "screens", "home.kv"))
        return Builder.load_file(os.path.join("mobile_app", "screens", "suporte.kv"))

    def pegar_placa(self):
        placa = self.sm.get_screen("login").ids.placa_input.text
        print(f"Placa digitada: {placa}")
        self.sm.get_screen("login").ids.placa_input.text = ""

        if placa == "123":
            self.sm.current = "home"

    def ir_para_login(self):
        self.sm = ScreenManager()
        Builder.load_file(os.path.join("screens", "login.kv"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.current = "login"
        return self.sm

    def mudar_tela(self, nome_tela):
        self.app.current = nome_tela

LoginApp().run()
