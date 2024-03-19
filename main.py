import sqlite3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage  # Importe AsyncImage para carregar imagens
from kivy.uix.scrollview import ScrollView  # Importe ScrollView para uso correto
from webbrowser import open as open_web

# Inicializando a conexão com o banco de dados SQLite
conn = sqlite3.connect('exercicios.db')
cursor = conn.cursor()

class BackButton(Button, ButtonBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Voltar'

    def on_release(self):
        app = App.get_running_app()
        app.root.current = 'inicio'

class ExercicioButton(Button):
    def __init__(self, exercicio_id, exercicio_nome, link, **kwargs):
        super().__init__(**kwargs)
        self.exercicio_id = exercicio_id
        self.exercicio_nome = exercicio_nome
        self.link = link
        self.text = exercicio_nome 
        self.bind(on_release=self.abrir_popup)

    def abrir_popup(self, *args):
        content = BoxLayout(orientation='vertical')
        
        # Carregar o vídeo ou imagem do link usando AsyncImage
        if self.link.endswith(('mp4', 'webm', 'avi')):
            # Se o link terminar com uma extensão de vídeo, carregue o vídeo
            video = AsyncImage(source=self.link, allow_stretch=True)
            content.add_widget(video)
        else:
            # Caso contrário, carregue a imagem
            image = AsyncImage(source=self.link)
            content.add_widget(image)
        
        # Botão Concluir
        concluido_button = Button(text='Concluir', size_hint_y=None, height=40)
        concluido_button.bind(on_release=self.marcar_concluido)
        content.add_widget(concluido_button)

        # Criar e exibir o Popup
        popup = Popup(title=self.exercicio_nome, content=content, size_hint=(None, None), size=(400, 400))
        popup.open()

    def marcar_concluido(self, *args):
        # Atualiza o status de conclusão do exercício no banco de dados
        cursor.execute('UPDATE exercicios SET concluido = 1 WHERE id = ?', (self.exercicio_id,))
        conn.commit()
        print(f'Exercício "{self.exercicio_id}" marcado como concluído.')

class TreinoScreen(Screen):
    def __init__(self, treino_nome, exercicios, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        for topico, link in exercicios.items():
            button = ExercicioButton(exercicio_id=topico, exercicio_nome=topico, link=link, size_hint_y=None, height=40)
            layout.add_widget(button)
        
        scrollview = ScrollView()
        scrollview.add_widget(layout)
        
        back_button = BackButton(size_hint_y=None, height=40)
        back_button.bind(on_release=self.voltar_tela)
        layout.add_widget(back_button)
        
        self.add_widget(scrollview)

    def voltar_tela(self, *args):
        self.manager.current = 'inicio'

class TreinoApp(App):
    # Definir o dicionário de treinos aqui para torná-lo global
    treinos = {
        'Treino A': {
            'Pulley Frente': 'https://www.youtube.com/watch?v=4f2A_vjEwMY',
            'Remada Articulada Pronada': 'https://www.youtube.com/watch?v=4f2A_vjEwMY',
            'Remada Cavalinho': 'https://www.youtube.com/watch?v=4f2A_vjEwMY',
            'Pull Down': 'https://www.youtube.com/watch?v=4f2A_vjEwMY',
            'Rosca Direta com Barra W': 'https://www.youtube.com/watch?v=4f2A_vjEwMY',
            'Rosca Alternada': 'https://www.youtube.com/watch?v=4f2A_vjEwMY',
            'Rosca inversa com Barra W': '',
            'Abdominal Remador': ''
        },
        'Treino B': {
            'Remada': 'https://www.youtube.com/watch?v=4f2A_vjEwMY',  # Link do vídeo
            'Exercício 4': 'https://www.youtube.com/watch?v=4f2A_vjEwMY'  # Link da imagem
        },
        'Treino C': {
            'Exercício 1': 'https://www.youtube.com/watch?v=4f2A_vjEwMY',  # Link do vídeo
            'Exercício 2': 'https://www.youtube.com/watch?v=4f2A_vjEwMY'  # Link da imagem
        },
        'Treino D': {
            'Exercício 3': 'https://www.youtube.com/watch?v=4f2A_vjEwMY',  # Link do vídeo
            'Exercício 4': 'https://www.youtube.com/watch?v=4f2A_vjEwMY'  # Link da imagem
        },
    }

    def build(self):
        # Gerenciador de tela
        sm = ScreenManager()

        # Criar tela de início com os botões para cada treino
        inicio = InicioScreen(name='inicio', treinos=TreinoApp.treinos.keys())
        sm.add_widget(inicio)

        # Criar uma tela para cada treino
        for nome, t in TreinoApp.treinos.items():
            screen = TreinoScreen(name=nome, treino_nome=nome, exercicios=t)
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
