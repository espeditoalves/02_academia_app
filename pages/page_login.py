from appWeb import *

# Inicializa o session_state
class SessionState:
    def __init__(self):
        self.login_realizado = False

# Função para gerenciar o redirecionamento após o login
def gerenciar_redirecionamento(session_state):
    if session_state.login_realizado:
        if session_state.mostrar_pagina_inicio:
            # st.page_link("pages/teste.py", label="Home", icon="🏠")
            pagina_inicio()

# Função para página inicial
def tela_login(session_state):
    st.title("Bem-vindo ao Sistema de Treinos e Exercícios")
    opcao = st.radio("Escolha uma opção:", ("Cadastrar Novo Usuário", "Login"))

    if opcao == "Cadastrar Novo Usuário":
        cadastrar_novo_usuario()
    elif opcao == "Login":
        if login():
            st.write("Login realizado com sucesso!")
            session_state.login_realizado = True
            session_state.mostrar_pagina_inicio = True
            gerenciar_redirecionamento(session_state)
        else:
            st.warning("Você precisa fazer login para acessar o sistema.")

# Inicializa o session_state
class SessionState:
    def __init__(self):
        self.login_realizado = False
        self.mostrar_pagina_inicio = False

# Executa o Streamlit app
if __name__ == '__main__':
    session_state = SessionState()
    tela_login(session_state)  # Inicializa a tela de login