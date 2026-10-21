import requests

import api_client
from api_client import MSG_COMUNICACAO, MSG_INESPERADO, MSG_SO_ESPACOS, MSG_VAZIO


class FakeResp:
    def __init__(self, status, dados=None, json_invalido=False):
        self.status_code, self._d, self._inv = status, dados, json_invalido

    def json(self):
        if self._inv:
            raise ValueError("json inválido")
        return self._d


def test_validacao_local():
    assert api_client.validar_localmente("") == MSG_VAZIO
    assert api_client.validar_localmente("  \n\t") == MSG_SO_ESPACOS
    assert api_client.validar_localmente("int x;") is None


def test_envio_com_sucesso(monkeypatch):
    chamado = {}

    def fake_post(url, json, timeout):
        chamado.update(url=url, json=json)
        return FakeResp(200, {"recebido": True, "mensagem": "Código recebido com sucesso."})

    monkeypatch.setattr(requests, "post", fake_post)
    r = api_client.enviar_codigo("int x;", url="http://backend:8000/")
    assert r["tipo"] == "sucesso"
    assert chamado["url"] == "http://backend:8000/analisar"
    assert chamado["json"] == {"codigo": "int x;"}


def test_erro_de_entrada_400(monkeypatch):
    monkeypatch.setattr(requests, "post", lambda *a, **k: FakeResp(400, {"recebido": False, "mensagem": "msg x"}))
    r = api_client.enviar_codigo("x")
    assert r["tipo"] == "entrada" and r["mensagem"] == "msg x"


def test_falha_de_comunicacao(monkeypatch):
    def falha(*a, **k):
        raise requests.ConnectionError("recusada")

    monkeypatch.setattr(requests, "post", falha)
    r = api_client.enviar_codigo("int x;")
    assert r["tipo"] == "comunicacao" and r["mensagem"] == MSG_COMUNICACAO


def test_timeout(monkeypatch):
    def falha(*a, **k):
        raise requests.Timeout()

    monkeypatch.setattr(requests, "post", falha)
    assert api_client.enviar_codigo("int x;")["tipo"] == "comunicacao"


def test_erro_500_nao_expoe_detalhes(monkeypatch):
    monkeypatch.setattr(requests, "post", lambda *a, **k: FakeResp(500, {"mensagem": "Traceback..."}))
    r = api_client.enviar_codigo("int x;")
    assert r["tipo"] == "servidor" and r["mensagem"] == MSG_INESPERADO


def test_resposta_nao_json(monkeypatch):
    monkeypatch.setattr(requests, "post", lambda *a, **k: FakeResp(200, json_invalido=True))
    assert api_client.enviar_codigo("int x;")["tipo"] == "servidor"
