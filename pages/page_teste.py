import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Título da página
st.title('Exemplo de Gráfico no Streamlit')

# Gerar dados fictícios
labels = ['A', 'B', 'C', 'D', 'E']
values = np.random.randint(1, 10, size=len(labels))

# Criar o gráfico de barras
fig, ax = plt.subplots()
ax.bar(labels, values)

# Adicionar título e rótulos aos eixos
plt.title('Gráfico de Barras Simples')
plt.xlabel('Categorias')
plt.ylabel('Valores')

# Exibir o gráfico no Streamlit
st.pyplot(fig)
