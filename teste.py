import streamlit as st
import numpy as np

with st.container():
   st.write("This is inside the container")

   # You can call any Streamlit command, including custom components:
   st.bar_chart(np.random.randn(50, 3))

st.write("This is outside the container")


import streamlit as st
import time

with st.empty():
    for seconds in range(5):
        st.write(f"⏳ {seconds} seconds have passed")
        time.sleep(1)
    st.write("✔️ 1 minute over!")

# Substitui o gráfico pelo texto final
st.empty()
st.write("DEU certo")