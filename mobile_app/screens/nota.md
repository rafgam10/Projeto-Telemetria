# Icon Button
`kv`

    MDIconButton:
                icon: "home-variant-outline"
                style: "standard"
                theme_text_color: "Custom"
                text_color: (0.66, 0.73, 0.27, 1)  # cor #A8BA44
                on_release: #Função de suporte

            MDIconButton:
                icon: "account"
                style: "standard"
                theme_text_color: "Custom"
                text_color: (0.66, 0.73, 0.27, 1)  # cor #A8BA44
                on_release: #Função de suporte

            MDIconButton:
                icon: "history"
                style: "standard"
                theme_text_color: "Custom"
                text_color: (0.66, 0.73, 0.27, 1)  # cor #A8BA44
                on_release: #Função de suporte

            MDIconButton:
                icon: "cog-outline"
                style: "standard"
                theme_text_color: "Custom"
                text_color: (0.66, 0.73, 0.27, 1)  # cor #A8BA44
                on_release: #Função de suporte

            MDIconButton:
                icon: "help-circle-outline"
                style: "standard"
                theme_text_color: "Custom"
                text_color: (0.66, 0.73, 0.27, 1)  # cor #A8BA44
                on_release: #Função de suporte
```

# Button Sair:

``` kv
MDRaisedButton:
            text: "SAIR"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 1, 0.3, 0.3, 1
            on_release:
                app.sm.current = "login"
``

# MDTopAppBar versão 1 em uma array:
```kv
MDBoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(10)
        md_bg_color: 0.05, 0.07, 0.12, 1  # Fundo principal escuro (quase preto)

        MDTopAppBar:
            title: "[color=FFFFFF]Motorista[/color][color=A8BA44]Legal[/color]"
            icon: "steering"
            font_size: "12sp"
            elevation: 4.5
            padding: "3sp"
            spacing: "2sp"
            # icon_size: "10sp"
            # mode: "end"
            # type: "bottom"
            markup: True
            # left_action_items: [["menu", lambda x: app.abrir_menu()]]
            right_action_items:[["home", lambda x: app.ir_para_home()], ["account-outline", lambda x: app.ir_perfil()], ["history", lambda x: app.abrir_historico()], ["cog", lambda x: app.abrir_config()]]
            use_overflow: True
            md_bg_color: 0.05, 0.07, 0.12, 1
            icon_color: 0.66, 0.73, 0.27, 1
            title_color: 1, 1, 1, 1

```