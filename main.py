import sqlite3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage  # Importe AsyncImage para carregar imagens
from kivy.utils import platform
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from webbrowser import open as open_web

# Inicializando a conexão com o banco de dados SQLite
conn = sqlite3.connect('exercicios.db')
cursor = conn.cursor()

class BackButton(ButtonBehavior, Label):
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
        self.text = 'Concluir'
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
            'Exercício 1': 'https://www.youtube.com/watch?v=4f2A_vjEwMY',  # Link do vídeo
            'Exercício 2': 'https://www.youtube.com/watch?v=4f2A_vjEwMY'   # Link da imagem
        },
        'Treino B': {
            'Exercício 3': 'https://www.bing.com/images/search?view=detailV2&ccid=Lfs4MvD%2f&id=048A35A8562964AC26E10B48900DD84E22E396EF&thid=OIP.Lfs4MvD_GgZVqZy4OUK9AAHaEn&mediaurl=https%3a%2f%2f2.bp.blogspot.com%2f-IqOjhqPsb0w%2fVUuEDUY6rJI%2fAAAAAAACHHw%2fG_NzBFk7oDI%2fs1600%2fVW-Gol-2016%252B(2).jpg&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.2dfb3832f0ff1a0655a99cb83942bd00%3frik%3d75bjIk7YDZBICw%26pid%3dImgRaw%26r%3d0&exph=997&expw=1600&q=gol&simid=608012703736816243&FORM=IRPRST&ck=568519A7096DEE38C2364E1CBD0BE567&selectedIndex=0&itb=0',  # Link do vídeo
            'Exercício 4': 'https://www.bing.com/images/search?view=detailV2&ccid=Lfs4MvD%2f&id=048A35A8562964AC26E10B48900DD84E22E396EF&thid=OIP.Lfs4MvD_GgZVqZy4OUK9AAHaEn&mediaurl=https%3a%2f%2f2.bp.blogspot.com%2f-IqOjhqPsb0w%2fVUuEDUY6rJI%2fAAAAAAACHHw%2fG_NzBFk7oDI%2fs1600%2fVW-Gol-2016%252B(2).jpg&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.2dfb3832f0ff1a0655a99cb83942bd00%3frik%3d75bjIk7YDZBICw%26pid%3dImgRaw%26r%3d0&exph=997&expw=1600&q=gol&simid=608012703736816243&FORM=IRPRST&ck=568519A7096DEE38C2364E1CBD0BE567&selectedIndex=0&itb=0'    # Link da imagem
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
