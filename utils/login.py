import os
import sqlite3
from datetime import datetime

import streamlit as st


# Função para criar o banco de dados de usuários
def criar_banco_usuarios():
    if not os.path.exists('usuarios.db'):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS usuarios
               (id INTEGER PRIMARY KEY,
               username TEXT UNIQUE,
               password TEXT)"""
        )
        conn.commit()
        conn.close()


# Função para verificar se o usuário existe
def verificar_usuario(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM usuarios WHERE username=? AND password=?',
        (username, password),
    )
    user = cursor.fetchone()

    conn.close()
    return user


# Função para cadastrar um novo usuário
def cadastrar_usuario(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            'INSERT INTO usuarios (username, password) VALUES (?, ?)',
            (username, password),
        )
        conn.commit()
        st.success('Usuário cadastrado com sucesso!')
    except sqlite3.IntegrityError:
        st.error('Erro: Usuário já existe.')

    conn.close()


# Função para login
def login():
    st.title('Login')
    username = st.text_input('Usuário')
    password = st.text_input('Senha', type='password')
    if st.button('Login'):
        user = verificar_usuario(username, password)
        if user:
            st.success('Login bem-sucedido!')
            return True
        else:
            st.error('Usuário ou senha incorretos.')
    return False


# Função para cadastrar novo usuário
def cadastrar_novo_usuario():
    st.title('Cadastro de Novo Usuário')
    username = st.text_input('Novo Usuário')
    password = st.text_input('Nova Senha', type='password')
    if st.button('Cadastrar'):
        cadastrar_usuario(username, password)
