import streamlit as st
import requests

st.set_page_config(page_title="Visualizador de Compiladores", layout="centered")

st.title("⚙️ Visualizador Educacional de Compiladores")
st.write("Bem-vindo à interface do analisador léxico e sintático.")
st.markdown("---")
st.subheader("Teste de Comunicação (Frontend -> Backend)")

try:
    response = requests.get("http://backend:8000/api/hello")
    if response.status_code == 200:
        data = response.json()
        st.success(f"**Mensagem recebida:** {data['message']}")
    else:
        st.warning("O backend respondeu, mas com erro.")
except Exception as e:
    st.error(f"Erro ao conectar com o backend: {e}")
