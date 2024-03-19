import os
import sqlite3
import pandas as pd
from datetime import datetime

from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
# from dados_treinos import treinos  # Importar dados fictícios de treinos
treinos = {
    'Treino A': {
        'Pulley Frente': {
            'id': 1, 
            'imagem': 'local/Pulley_Frente.png', 
            'concluido': False, 
            'area_do_corpo': 'Costas'
            }, 
        'Remada Articulada Pronada': {
            'id': 2, 
            'imagem': 'local/Remada_Articulada_Pronada.png', 
            'concluido': False, 
            'area_do_corpo': 'Costas'
            }, 
        'Remada Cavalinho': {
            'id': 3, 
            'imagem': 'local/Remada_Cavalinho.png', 
            'concluido': False, 
            'area_do_corpo': 'Costas'
            }, 
        'Pull Down': {
            'id': 4, 
            'imagem': 'local/Pull_Down.png', 
            'concluido': False, 
            'area_do_corpo': 
            'Costas'
            }, 
        'Rosca Direta com Barra W': {
            'id': 5, 
            'imagem': 'local/Rosca_Direta_Bar_W.png', 
            'concluido': False, 
            'area_do_corpo': 'Bíceps'
            }, 
        'Rosca Alternada': {
            'id': 6, 
            'imagem': 'local/Rosca_Alternada.png', 
            'concluido': False, 
            'area_do_corpo': 'Bíceps'
            }, 
        'Rosca Inversa com Barra W': {
            'id': 7, 
            'imagem': 'local/Rosca_Inversa_Bar_W.png', 
            'concluido': False, 
            'area_do_corpo': 'Antebraço'
            }, 
        'Abdominal Remador': {
            'id': 8, 
            'imagem': 'local/Abdominal_Remador.png', 
            'concluido': False, 
            'area_do_corpo': 'Abdominais'
            }
        },
    'Treino B': {
        'Pulley Frente': {
            'id': 1, 
            'imagem': 'local/Pulley_Frente.png', 
            'concluido': False, 
            'area_do_corpo': 'Costas'
            },}
}

# Inicializar a conexão com o banco de dados SQLite
conn = sqlite3.connect('exercicios.db')
cursor = conn.cursor()

# Criar a tabela de exercícios se ainda não existir
cursor.execute(
    """CREATE TABLE IF NOT EXISTS exercicios
                  (id INTEGER PRIMARY KEY,
                  treino TEXT,
                  nome TEXT,
                  imagem TEXT,
                  concluido INTEGER,
                  area_do_corpo TEXT,
                  data TEXT)"""
)
conn.commit()


class BackButton(Button, ButtonBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Voltar'

    def on_release(self):
        app = App.get_running_app()
        app.root.current = 'inicio'


class ExercicioButton(Button):
    def __init__(
        self, exercicio_id, exercicio_nome, imagem_path, concluido, area_do_corpo, **kwargs
    ):
        super().__init__(**kwargs)
        self.exercicio_id = exercicio_id
        self.exercicio_nome = exercicio_nome
        self.imagem_path = imagem_path
        self.concluido = concluido
        self.area_do_corpo = area_do_corpo
        self.update_button_text()  # Atualiza o texto do botão de acordo com o status
        self.bind(on_release=self.abrir_popup)
        self.treino = None
        self.data = None

    def set_info(self, treino, data_atual=True):
        self.treino = treino
        if data_atual:
            hoje = datetime.now()
            self.data = hoje.strftime('%Y/%m/%d')



    def update_button_text(self):
        # Define o texto do botão com base no status de conclusão
        if self.concluido:
            self.text = f'{self.exercicio_nome} (Concluído)'
        else:
            self.text = f'{self.exercicio_nome} (Não Concluído)'

    def abrir_popup(self, *args):
        content = BoxLayout(orientation='vertical')

        # Verifica se a imagem existe no diretório local
        if os.path.isfile(self.imagem_path):
            # Carrega a imagem a partir do diretório local
            image = Image(source=self.imagem_path)
            content.add_widget(image)
        else:
            content.add_widget(Label(text='Imagem não encontrada.'))

        # Botão Concluir
        concluido_button = Button(text='Concluir', size_hint_y=None, height=40)
        concluido_button.bind(on_release=self.toggle_conclusao)
        content.add_widget(concluido_button)

        # Criar e exibir o Popup
        popup = Popup(
            title=self.exercicio_nome,
            content=content,
            size_hint=(None, None),
            size=(400, 400),
        )
        popup.open()

    def toggle_conclusao(self, *args):
        # Alterna entre concluído e não concluído
        self.concluido = not self.concluido
        self.update_button_text()  # Atualiza o texto do botão
        self.update_database()  # Atualiza o banco de dados
        print(
            f'Exercício "{self.exercicio_id}" marcado como {"concluído" if self.concluido else "não concluído"}.'
        )

    # def update_database(self):
    #     # Atualiza o registro no banco de dados
    #     cursor.execute(
    #         'UPDATE exercicios SET concluido = ?, area_do_corpo = ? WHERE id = ?',
    #         (int(self.concluido), self.area_do_corpo, self.exercicio_id),
    #     )
    #     conn.commit()
    def update_database(self):
        # Verificar se o exercício já existe na tabela
        cursor.execute('SELECT id FROM exercicios WHERE id = ?', (self.exercicio_id,))
        exercicio_existente = cursor.fetchone()

        if exercicio_existente:
            # Exercício já existe, então vamos atualizá-lo
            cursor.execute(
                'UPDATE exercicios SET treino = ?, nome = ?, imagem = ?, concluido = ?, area_do_corpo = ?, data = ? WHERE id = ?',
                (self.treino, self.exercicio_nome, self.imagem_path, int(self.concluido), self.area_do_corpo, self.data, self.exercicio_id),
            )
        else:
            # Exercício não existe, então vamos inseri-lo
            cursor.execute(
                'INSERT INTO exercicios (id, treino, nome, imagem, concluido, area_do_corpo, data) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (self.exercicio_id, self.treino, self.exercicio_nome, self.imagem_path, int(self.concluido), self.area_do_corpo, self.data),
            )

        # Commit das alterações no banco de dados
        conn.commit()


class TreinoScreen(Screen):
    def __init__(self, treino_nome, exercicios, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for topico, info in exercicios.items():
            button = ExercicioButton(
                exercicio_id=info['id'],
                exercicio_nome=topico,
                imagem_path=info['imagem'],
                concluido=info['concluido'],
                area_do_corpo=info['area_do_corpo'],
                # treino=treino_nome,  # Passa o nome do treino para o botão
                # data='2024/03/21',  # Exemplo de data (você pode usar a data atual aqui)
                size_hint_y=None,
                height=40,
            )
            button.set_info(treino=treino_nome)
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
    def build(self):
        # Gerenciador de tela
        sm = ScreenManager()

        # Criar tela de início com os botões para cada treino
        inicio = InicioScreen(name='inicio', treinos=treinos.keys())
        sm.add_widget(inicio)

        # Criar uma tela para cada treino
        for nome, exercicios in treinos.items():
            screen = TreinoScreen(
                name=nome, treino_nome=nome, exercicios=exercicios
            )
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
