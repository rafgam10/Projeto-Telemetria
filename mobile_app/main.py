from kivymd.app import MDApp
from kaki.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
import os

class LoginScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class LoginApp(MDApp, App):
    def build(self):
        Builder.load_file(os.path.join("mobile_app", "screens", "login.kv"))
        Builder.load_file(os.path.join("mobile_app", "screens", "home.kv"))

        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(HomeScreen(name="home"))

        return self.sm

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

LoginApp().run()
