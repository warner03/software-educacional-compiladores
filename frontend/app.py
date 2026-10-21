"""Interface web - Visualizador Educacional de Compiladores (Mini-C) - Etapa 2."""
import streamlit as st

import api_client
from examples import CODIGO_INICIAL, EXEMPLO_NENHUM, EXEMPLOS

LINGUAGEM = "Mini-C (subconjunto da linguagem C)"

st.set_page_config(page_title="Visualizador Educacional de Compiladores", page_icon="🛠️", layout="wide")

if "codigo" not in st.session_state:
    st.session_state["codigo"] = CODIGO_INICIAL
if "resultado" not in st.session_state:
    st.session_state["resultado"] = None


def carregar_exemplo():
    nome = st.session_state.get("exemplo_sel")
    if nome in EXEMPLOS:
        st.session_state["codigo"] = EXEMPLOS[nome]
        st.session_state["resultado"] = None


def analisar():
    codigo = st.session_state.get("codigo", "")
    erro_local = api_client.validar_localmente(codigo)
    if erro_local:
        st.session_state["resultado"] = {"tipo": "entrada", "mensagem": erro_local, "dados": None}
        return
    st.session_state["resultado"] = api_client.enviar_codigo(codigo)


st.title("🛠️ Visualizador Educacional de Compiladores")
st.caption(f"Linguagem analisada: **{LINGUAGEM}**")

col_entrada, col_resultado = st.columns(2)

with col_entrada:
    st.subheader("Código-fonte")
    st.selectbox("Exemplos de programas", [EXEMPLO_NENHUM, *EXEMPLOS.keys()], key="exemplo_sel")
    st.button("Carregar exemplo", key="btn_carregar", on_click=carregar_exemplo)
    st.text_area(
        "Escreva, cole ou edite o programa Mini-C:",
        key="codigo",
        height=320,
        help="O código pode conter erros intencionais; eles serão tratados nas próximas etapas.",
    )
    st.button("Analisar código", key="btn_analisar", type="primary", on_click=analisar)

with col_resultado:
    st.subheader("Resultados")
    resultado = st.session_state["resultado"]
    if resultado is None:
        st.info("Os resultados da análise aparecerão aqui.")
    elif resultado["tipo"] == "sucesso":
        st.success(resultado["mensagem"])
        dados = resultado["dados"] or {}
        st.write(f"Caracteres: **{dados.get('total_caracteres')}** · Linhas: **{dados.get('total_linhas')}**")
        st.caption("As análises léxica, sintática e semântica serão implementadas nas próximas etapas.")
    elif resultado["tipo"] == "entrada":
        st.warning(resultado["mensagem"])
    else:
        st.error(resultado["mensagem"])
