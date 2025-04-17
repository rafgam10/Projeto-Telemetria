from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import os


class LoginScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class LoginApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        Builder.load_file(os.path.join("screens", "login.kv"))
        Builder.load_file(os.path.join("screens", "home.kv"))

        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(HomeScreen(name="home"))

        return self.sm

    def pegar_placa(self):
        placa = self.sm.get_screen("login").ids.placa_input.text
        print(f"Placa digitada: {placa}")
        self.sm.get_screen("login").ids.placa_input.text = ""

        if placa == "123":
            self.sm.current = "home"

LoginApp().run()
