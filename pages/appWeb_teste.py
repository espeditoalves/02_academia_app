import os
import sqlite3
from datetime import datetime

import streamlit as st

from utils.dados_treinos import *
from utils.login import *

# Obtém a data e hora atual
data_atual = datetime.now().strftime('%Y/%m/%d')
usuario_escolhido = None
treinos = transformar_excel_em_dicionario()
# Verificar se o banco de dados existe, caso contrário, criar
if not os.path.exists('exercicios_stre.db'):
    conn = sqlite3.connect('exercicios_stre.db')
    cursor = conn.cursor()

    # Criar a tabela de exercícios se ainda não existir
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS exercicios_stre
           (id INTEGER,
           usuario TEXT,
           treino TEXT,
           nome TEXT,
           imagem TEXT,
           concluido INTEGER,
           area_do_corpo TEXT,
           data TEXT)"""
    )
    conn.commit()
    conn.close()

# Conectar-se ao banco de dados SQLite
conn = sqlite3.connect('exercicios_stre.db')
cursor = conn.cursor()


class ExercicioButton:
    def __init__(
        self,
        exercicio_id,
        treino,
        nome,
        imagem,
        gif,
        concluido,
        area_do_corpo,
        data,
    ):
        self.exercicio_id = exercicio_id
        self.treino = treino
        self.nome = nome
        self.imagem = imagem
        self.gif = gif
        self.concluido = concluido
        self.area_do_corpo = area_do_corpo
        self.data = data

    def marcar_concluido(self):
        self.concluido = True
        salvar_atualizar_exercicio(self)

    def marcar_nao_concluido(self):
        self.concluido = False
        salvar_atualizar_exercicio(self)

    def verificar_status(self):
        global conn, cursor, usuario_escolhido  # Adicionar variáveis globais
        cursor.execute(
            'SELECT concluido FROM exercicios_stre WHERE id=? AND data=? AND usuario=?',
            (self.exercicio_id, self.data, usuario_escolhido),
        )
        resultado = cursor.fetchone()
        if resultado:
            if resultado[0] == 1:  # Se concluido for 1, significa que está pago
                return f'Exercício "{self.nome}" Pago.'
            else:
                return f'Exercício "{self.nome}" Não Pago.'
        else:
            return f'Exercício "{self.nome}" Não Foi Iniciado.'


def salvar_atualizar_exercicio(exercicio):
    global usuario_escolhido
    cursor.execute(
        'SELECT * FROM exercicios_stre WHERE id=? AND data=? AND usuario=?',
        (exercicio.exercicio_id, exercicio.data, usuario_escolhido),
    )
    exercicio_db = cursor.fetchone()
    if exercicio_db:
        # Registro já existe para o usuário usuario_escolhido, então atualize-o
        cursor.execute(
            'UPDATE exercicios_stre SET treino=?, nome=?, imagem=?, concluido=?, area_do_corpo=? WHERE id=? AND data=? AND usuario=?',
            (
                exercicio.treino,
                exercicio.nome,
                exercicio.imagem,
                int(exercicio.concluido),
                exercicio.area_do_corpo,
                exercicio.exercicio_id,
                exercicio.data,
                usuario_escolhido,
            ),
        )
        st.warning(
            f'Exercício "{exercicio.nome}" atualizado para o usuário "{usuario_escolhido}".'
        )
    else:
        # Nenhum registro para o usuário Espedito, então insira um novo
        cursor.execute(
            'INSERT INTO exercicios_stre (id, usuario, treino, nome, imagem, concluido, area_do_corpo, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (
                exercicio.exercicio_id,
                usuario_escolhido,
                exercicio.treino,
                exercicio.nome,
                exercicio.imagem,
                int(exercicio.concluido),
                exercicio.area_do_corpo,
                exercicio.data,
            ),
        )
        st.success(
            f'Exercício "{exercicio.nome}" salvo para o usuário "{usuario_escolhido}".'
        )
    conn.commit()


# Função para carregar os exercícios
def carregar_exercicios(treino):
    global data_atual
    exercicios = treinos[treino]
    lista_exercicios = []
    for topico, info in exercicios.items():
        exercicio = ExercicioButton(
            exercicio_id=info['id'],
            treino=treino,
            nome=topico,
            imagem=info['imagem'],
            gif=info['gif'],
            concluido=info['concluido'],
            area_do_corpo=info['area_do_corpo'],
            data=data_atual,  # Obtém a data e hora atual
        )
        lista_exercicios.append(exercicio)
    return lista_exercicios


# Página inicial
def pagina_inicio():
    global usuario_escolhido
    st.title('Treinos e Exercícios')
    with st.container(border = True):
        # Criar um botão seletor 
        usuario_escolhido = st.radio(
            'Selecione o usuário:', ('Espedito', 'Janaina')
        )
        st.markdown(f"Data: **{datetime.now().strftime('%d/%m/%Y')}**")
        col_treinos = st.selectbox('Selecione um treino:', list(treinos.keys()))

    exercicios = carregar_exercicios(col_treinos)
    st.write(f'Usuário Selecionado: {usuario_escolhido}')
    st.subheader(f'{col_treinos}')
    
    for exercicio in exercicios:
        st.write('\n')
        # Criar um container para cada exercício
        with st.container(border=True):
            st.write(f'## {exercicio.nome}')
            st.write(f'**Área do Corpo:** {exercicio.area_do_corpo}')
            st.write(f'**Status:** {exercicio.verificar_status()}')

            # Insert a multi-element container that can be expanded/collapsed.
            with st.expander("Veja como deve ser executado"):
                # Insert containers separated into tabs.
                tab1, tab2 = st.tabs(["Imagem", "Gif"])
                with tab1:
                    if os.path.exists(exercicio.imagem):
                        st.image(exercicio.imagem, use_column_width=True)
                    else:
                        st.write('Imagem não encontrada.')
                with tab2:
                    if  os.path.exists(exercicio.gif):
                        # st.video(exercicio_gif)
                        # st.markdown(exercicio_gif)
                        # st.markdown(f"![GIF]({exercicio.gif})")
                        # st.image(exercicio_gif, format='gif')
                        # st.markdown(f'<img src="data:image/gif;base64,{converter_gif_base64(exercicio_gif)}">')
                        gif_bytes = open(exercicio.gif, "rb").read()
                        st.image(gif_bytes, use_column_width=True, )
                    else:
                        st.write('GIF não encontrado.')

            # Criar as duas colunas para os botões
            button_1, button_2 = st.columns(2)
            with button_1:
                button_concluido_key = st.button(f'Concluir: {exercicio.nome}')
                if button_concluido_key:
                    exercicio.marcar_concluido()
                    # st.write(f'Exercício "{exercicio.nome}" marcado como concluído.')

            with button_2:
                button_nao_concluido_key = st.button(f'Não Concluir: {exercicio.nome}')
                if button_nao_concluido_key:
                    exercicio.marcar_nao_concluido()
                    # st.write(f'Exercício "{exercicio.nome}" marcado como não concluído.')

# Função para converter o GIF para base64
def converter_gif_base64(file_path):
    import base64
    with open(file_path, "rb") as gif_file:
        return base64.b64encode(gif_file.read()).decode()

# Executar o Streamlit app
if __name__ == '__main__':
    pagina_inicio()


