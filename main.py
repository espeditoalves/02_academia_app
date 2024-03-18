from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout  # Importe o GridLayout aqui
from kivy.uix.screenmanager import ScreenManager, Screen
from webbrowser import open as open_web

# Lista de treinos e seus tópicos com links
treinos = {
    'Treino A': {
        'Tópico 1': 'https://www.exemplo.com/treino_a/topico1',
        'Tópico 2': 'https://www.exemplo.com/treino_a/topico2'
    },
    'Treino B': {
        'Tópico 1': 'https://www.exemplo.com/treino_b/topico1',
        'Tópico 2': 'https://www.exemplo.com/treino_b/topico2'
    },
    'Treino C': {
        'Tópico 1': 'https://www.exemplo.com/treino_c/topico1',
        'Tópico 2': 'https://www.exemplo.com/treino_c/topico2'
    },
    'Treino D': {
        'Tópico 1': 'https://www.exemplo.com/treino_d/topico1',
        'Tópico 2': 'https://www.exemplo.com/treino_d/topico2'
    }
}

class TreinoScreen(Screen):
    def __init__(self, treino, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        for topico, link in treino.items():
            button = Button(text=topico, size_hint_y=None, height=40)
            button.bind(on_release=self.abrir_link(link))
            layout.add_widget(button)
        
        scrollview = ScrollView()
        scrollview.add_widget(layout)
        self.add_widget(scrollview)
    
    def abrir_link(self, link):
        def callback(instance):
            open_web(link)
        return callback

class TreinoApp(App):
    def build(self):
        # Gerenciador de tela
        sm = ScreenManager()

        # Criar tela de início com os botões para cada treino
        inicio = InicioScreen(name='inicio', treinos=treinos.keys())
        sm.add_widget(inicio)

        # Criar uma tela para cada treino
        for nome, t in treinos.items():
            screen = TreinoScreen(name=nome, treino=t)
            sm.add_widget(screen)

        return sm

class InicioScreen(Screen):
    def __init__(self, treinos, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for treino in treinos:
            button = Button(text=treino, size_hint_y=None, height=40)
            button.bind(on_release=self.mudar_tela(treino))
            layout.add_widget(button)

        scrollview = ScrollView()
        scrollview.add_widget(layout)
        self.add_widget(scrollview)

    def mudar_tela(self, treino):
        def callback(instance):
            self.manager.current = treino
        return callback

if __name__ == '__main__':
    TreinoApp().run()

