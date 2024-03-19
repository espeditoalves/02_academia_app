import os
import sqlite3
import streamlit as st

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
            'area_do_corpo': 'Costas'
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
        }
    }
}

# Verificar se o banco de dados existe, caso contrário, criar
if not os.path.exists('exercicios_stre.db'):
    conn = sqlite3.connect('exercicios_stre.db')
    cursor = conn.cursor()

    # Criar a tabela de exercícios se ainda não existir
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS exercicios_stre
           (id INTEGER PRIMARY KEY,
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
    def __init__(self, exercicio_id, treino, nome, imagem, concluido, area_do_corpo, data):
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

def salvar_atualizar_exercicio(exercicio):
    cursor.execute("SELECT * FROM exercicios_stre WHERE id=? AND data=?", (exercicio.exercicio_id, exercicio.data))
    exercicio_db = cursor.fetchone()
    if exercicio_db:
        # Atualizar o exercício existente
        cursor.execute("UPDATE exercicios_stre SET treino=?, nome=?, imagem=?, concluido=?, area_do_corpo=? WHERE id=? AND data=?", (exercicio.treino, exercicio.nome, exercicio.imagem, int(exercicio.concluido), exercicio.area_do_corpo, exercicio.exercicio_id, exercicio.data))
    else:
        # Inserir um novo exercício
        cursor.execute("INSERT INTO exercicios_stre (id, treino, nome, imagem, concluido, area_do_corpo, data) VALUES (?, ?, ?, ?, ?, ?, ?)", (exercicio.exercicio_id, exercicio.treino, exercicio.nome, exercicio.imagem, int(exercicio.concluido), exercicio.area_do_corpo, exercicio.data))
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
            data='2024-03-21'  # Adicione a data atual ou uma data relevante
        )
        lista_exercicios.append(exercicio)
    return lista_exercicios

# Página inicial
def pagina_inicio():
    st.title('Treinos e Exercícios')
    col_treinos = st.sidebar.selectbox('Selecione um treino:', list(treinos.keys()))
    exercicios = carregar_exercicios(col_treinos)

    st.sidebar.title('Treinos')
    for treino in treinos.keys():
        st.sidebar.write(f'- {treino}')

    st.subheader(f'Exercícios do Treino: {col_treinos}')
    for exercicio in exercicios:
        st.write(f'## {exercicio.nome}')
        st.write(f'**Área do Corpo:** {exercicio.area_do_corpo}')
        
        # Verifica se a imagem existe antes de tentar exibi-la
        if os.path.exists(exercicio.imagem):
            st.image(exercicio.imagem, use_column_width=True)
        else:
            st.write("Imagem não encontrada.")
        
        # Usar o ID do exercício como parte da chave para evitar DuplicateWidgetID
        button_concluido_key = f'button_concluido_{exercicio.exercicio_id}_{exercicio.data}'
        button_nao_concluido_key = f'button_nao_concluido_{exercicio.exercicio_id}_{exercicio.data}'
        
        if st.button('Concluir', key=button_concluido_key):
            exercicio.marcar_concluido()
            st.write(f'Exercício "{exercicio.nome}" marcado como concluído.')
        if st.button('Não Concluído', key=button_nao_concluido_key):
            exercicio.marcar_nao_concluido()
            st.write(f'Exercício "{exercicio.nome}" marcado como não concluído.')
        
        st.write('---')  # Adicionar uma linha horizontal entre exercícios

# Executar o Streamlit app
if __name__ == '__main__':
    pagina_inicio()

# Fechar a conexão com o banco de dados ao final do programa
conn.close()

