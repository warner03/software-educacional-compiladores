"""Testes de interface com o framework de testes do Streamlit (AppTest)."""
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

import api_client
from examples import CODIGO_INICIAL, EXEMPLOS

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def novo_app():
    return AppTest.from_file(APP, default_timeout=15).run()


def textos(at):
    return " ".join(e.value for e in [*at.success, *at.warning, *at.error, *at.info])


def test_tela_principal_tem_elementos_obrigatorios():
    at = novo_app()
    assert not at.exception
    assert "Visualizador Educacional de Compiladores" in at.title[0].value
    assert "Mini-C" in at.caption[0].value
    assert at.text_area(key="codigo").value == CODIGO_INICIAL
    assert at.button(key="btn_analisar") is not None
    assert at.selectbox(key="exemplo_sel") is not None


def test_edicao_do_codigo_e_preservada():
    at = novo_app()
    at.text_area(key="codigo").set_value("int a = 1;").run()
    assert at.text_area(key="codigo").value == "int a = 1;"
    at.button(key="btn_analisar").click().run()  # interação não apaga o texto
    assert at.text_area(key="codigo").value == "int a = 1;"


def test_cada_exemplo_e_carregado():
    for nome, codigo in EXEMPLOS.items():
        at = novo_app()
        at.selectbox(key="exemplo_sel").select(nome).run()
        at.button(key="btn_carregar").click().run()
        assert at.text_area(key="codigo").value == codigo


def test_novo_exemplo_substitui_o_anterior_e_permite_edicao():
    nomes = list(EXEMPLOS)
    at = novo_app()
    at.selectbox(key="exemplo_sel").select(nomes[0]).run()
    at.button(key="btn_carregar").click().run()
    at.selectbox(key="exemplo_sel").select(nomes[1]).run()
    at.button(key="btn_carregar").click().run()
    assert at.text_area(key="codigo").value == EXEMPLOS[nomes[1]]
    at.text_area(key="codigo").set_value(EXEMPLOS[nomes[1]] + "\nint z;").run()
    assert at.text_area(key="codigo").value.endswith("int z;")


def test_entrada_vazia_mostra_mensagem_sem_chamar_backend():
    with patch.object(api_client, "enviar_codigo") as env:
        at = novo_app()
        at.text_area(key="codigo").set_value("").run()
        at.button(key="btn_analisar").click().run()
        assert api_client.MSG_VAZIO in textos(at)
        env.assert_not_called()


def test_somente_espacos_mostra_mensagem():
    with patch.object(api_client, "enviar_codigo") as env:
        at = novo_app()
        at.text_area(key="codigo").set_value("   \n  ").run()
        at.button(key="btn_analisar").click().run()
        assert api_client.MSG_SO_ESPACOS in textos(at)
        env.assert_not_called()


def test_envio_com_sucesso_exibe_resposta():
    resp = {"tipo": "sucesso", "mensagem": "Código recebido com sucesso.",
            "dados": {"recebido": True, "total_caracteres": 16, "total_linhas": 1}}
    with patch.object(api_client, "enviar_codigo", return_value=resp) as env:
        at = novo_app()
        at.button(key="btn_analisar").click().run()
        env.assert_called_once_with(CODIGO_INICIAL)
        assert "Código recebido com sucesso." in textos(at)


def test_falha_de_comunicacao_mostra_erro_e_mantem_interface_consistente():
    resp = {"tipo": "comunicacao", "mensagem": api_client.MSG_COMUNICACAO, "dados": None}
    with patch.object(api_client, "enviar_codigo", return_value=resp):
        at = novo_app()
        at.button(key="btn_analisar").click().run()
        assert not at.exception
        assert api_client.MSG_COMUNICACAO in [e.value for e in at.error]
        assert at.text_area(key="codigo").value == CODIGO_INICIAL
