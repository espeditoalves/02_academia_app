import os
import sqlite3
from datetime import datetime

import streamlit as st

from utils.dados_treinos import *
from utils.login import *

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
        concluido,
        area_do_corpo,
        data,
    ):
        self.exercicio_id = exercicio_id
        self.treino = treino
        self.nome = nome
        self.imagem = imagem
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
        data_atual = datetime.now().strftime('%Y-%m-%d')
        if self.data == data_atual:
            return (
                'Marcado como concluído'
                if self.concluido
                else 'Marcado como não concluído'
            )
        else:
            return 'Exercício não concluído hoje'


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
    exercicios = treinos[treino]
    lista_exercicios = []
    for topico, info in exercicios.items():
        exercicio = ExercicioButton(
            exercicio_id=info['id'],
            treino=treino,
            nome=topico,
            imagem=info['imagem'],
            concluido=info['concluido'],
            area_do_corpo=info['area_do_corpo'],
            data=datetime.now().strftime(
                '%Y/%m/%d'
            ),  # Obtém a data e hora atual
        )
        lista_exercicios.append(exercicio)
    return lista_exercicios


# Página inicial
def pagina_inicio():
    global usuario_escolhido
    st.title('Treinos e Exercícios')
    # Criar um botão seletor para escolher entre "Espedito" e "Janaina"
    usuario_escolhido = st.radio(
        'Selecione o usuário:', ('Espedito', 'Janaina')
    )

    # Exibir a escolha feita
    st.write(f'Você escolheu: {usuario_escolhido}')
    col_treinos = st.selectbox('Selecione um treino:', list(treinos.keys()))

    # Adiciona um espaço em branco para melhorar a aparência
    st.write('\n')

    exercicios = carregar_exercicios(col_treinos)

    st.subheader(f'Exercícios do Treino: {col_treinos}')
    for exercicio in exercicios:
        st.write(f'## {exercicio.nome}')
        st.write(f'**Área do Corpo:** {exercicio.area_do_corpo}')

        # Verifica se a imagem existe antes de tentar exibi-la
        if os.path.exists(exercicio.imagem):
            st.image(exercicio.imagem, use_column_width=True)
        else:
            st.write('Imagem não encontrada.')

        # Verificar o status do exercício
        # status_exercicio = exercicio.verificar_status()
        # st.write(f'Status: {status_exercicio}')

        # Usar o ID do exercício como parte da chave para evitar DuplicateWidgetID
        button_concluido_key = (
            f'button_concluido_{exercicio.exercicio_id}_{exercicio.data}'
        )
        button_nao_concluido_key = (
            f'button_nao_concluido_{exercicio.exercicio_id}_{exercicio.data}'
        )

        if st.button('Concluir', key=button_concluido_key):
            exercicio.marcar_concluido()
            st.write(f'Exercício "{exercicio.nome}" marcado como concluído.')

        if st.button('Não Concluído', key=button_nao_concluido_key):
            exercicio.marcar_nao_concluido()
            st.write(
                f'Exercício "{exercicio.nome}" marcado como não concluído.'
            )

        st.write('---')  # Adicionar uma linha horizontal entre exercícios


# Executar o Streamlit app
if __name__ == '__main__':
    pagina_inicio()

# # Função para gerenciar o redirecionamento após o login
# def gerenciar_redirecionamento(login_realizado):
#        if login_realizado:
#           st.empty()
#           pagina_inicio()
#        else:
#            tela_login()

# # Variável de controle para verificar se o login foi realizado com sucesso
# login_realizado = False

# # Função para página inicial
# def tela_login():
#     criar_banco_usuarios()
#     st.title("Bem-vindo ao Sistema de Treinos e Exercícios")
#     opcao = st.radio("Escolha uma opção:", ("Cadastrar Novo Usuário", "Login"))
#     if opcao == "Cadastrar Novo Usuário":
#         cadastrar_novo_usuario()
#     elif opcao == "Login":
#         if login():
#             st.write("Login realizado com sucesso!")
#             global login_realizado
#             login_realizado = True
#             gerenciar_redirecionamento(login_realizado = login_realizado)
#         else:
#             st.warning("Você precisa fazer login para acessar o sistema.")

# # Executar o Streamlit app
# if __name__ == '__main__':
#     tela_login()  # Inicializa a tela de login
