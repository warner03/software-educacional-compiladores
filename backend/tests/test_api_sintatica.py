import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.scanner import analisar_lexico
from test_parser import CASOS

client = TestClient(app, raise_server_exceptions=False)

# Expectativas fixadas pelo protocolo, não inferidas da resposta do parser.
HTTP_400 = {"B01", "B02", "B05"}
NAO_EXECUTADA = {"L01", "L02", "L03", "B08"}
ERRO = {f"S{i:02}" for i in range(1, 11)} | {"B03", "B07"}
ETAPA4 = [id for id in CASOS if not id.startswith("M")]


@pytest.mark.parametrize("id", ETAPA4)
def test_33_casos_planejados_na_api(id):
    codigo = CASOS[id]["codigo"]
    resposta = client.post("/analisar", json={"codigo": codigo})
    if id in HTTP_400:
        assert resposta.status_code == 400 and resposta.json()["recebido"] is False
        return
    assert resposta.status_code == 200
    dados = resposta.json()
    # Scanner original é chamado independentemente como oráculo de regressão.
    lexico = analisar_lexico(codigo)
    assert {k: dados[k] for k in ("sucesso", "tokens", "erros")} == lexico
    assert "EOF" not in [t["tipo"] for t in dados["tokens"]]
    sintatica = dados["sintatica"]
    if id in NAO_EXECUTADA:
        assert sintatica == {"estado": "nao_executada", "sucesso": None, "motivo": "erros_lexicos", "ast": None, "erros": []}
    elif id in ERRO:
        assert sintatica["estado"] == "erro" and sintatica["sucesso"] is False
        assert sintatica["ast"] is None and sintatica["erros"]
    else:
        assert sintatica["estado"] == "sucesso" and sintatica["sucesso"] is True
        assert sintatica["ast"]["tipo"] == "Programa" and sintatica["erros"] == []


def test_parser_nao_e_chamado_com_erros_lexicos(monkeypatch):
    def nao_deve_ser_chamado(*_):
        raise AssertionError("parser recebeu sequência léxica inválida")
    monkeypatch.setattr("app.main.analisar_sintatico", nao_deve_ser_chamado)
    r = client.post("/analisar", json={"codigo": "@ int x;"})
    assert r.status_code == 200 and r.json()["sintatica"]["estado"] == "nao_executada"


@pytest.mark.parametrize("codigo", ["", "  ", "x" * 10001])
def test_validacao_ocorre_antes_de_scanner_e_parser(codigo, monkeypatch):
    def proibido(*_):
        raise AssertionError("analisador chamado antes da validação")
    monkeypatch.setattr("app.main.analisar_lexico", proibido)
    monkeypatch.setattr("app.main.analisar_sintatico", proibido)
    assert client.post("/analisar", json={"codigo": codigo}).status_code == 400


@pytest.mark.parametrize("codigo,codigo_erro", [
    ("int x=" + "+".join(["1"] * 2500) + ";", "limite_altura"),
    ("{}" * 2000, "limite_nos"),
    ("int x=" + "(" * 1000 + "1" + ")" * 1000 + ";", "limite_profundidade"),
])
def test_entradas_grandes_nunca_retornam_500(codigo, codigo_erro):
    r = client.post("/analisar", json={"codigo": codigo})
    assert r.status_code == 200
    dados = r.json()
    assert dados["sucesso"] is True
    assert dados["sintatica"]["ast"] is None
    assert dados["sintatica"]["erros"][0]["codigo"] == codigo_erro
    assert "Traceback" not in r.text


def test_comentarios_unicode_e_linhas_crlf_preservam_contrato_e_posicoes():
    r = client.post("/analisar", json={"codigo": "/* 😀 */\r\n\tint x = 10;"}).json()
    assert r["total_linhas"] == 2
    assert r["tokens"][0] == {"tipo": "PALAVRA_RESERVADA", "lexema": "int", "linha": 2, "coluna": 2}
    assert r["sintatica"]["ast"]["comandos"][0]["inicio"] == {"linha": 2, "coluna": 2}


def test_sintaxe_invalida_nao_muda_significado_de_sucesso_lexico():
    r = client.post("/analisar", json={"codigo": "int = ;"}).json()
    assert r["recebido"] is True and r["sucesso"] is True
    assert r["mensagem"] == "Análise léxica concluída sem erros."
    assert r["erros"] == [] and r["sintatica"]["sucesso"] is False


def test_api_serializa_ast_no_limite_de_altura_128():
    codigo = "int x=" + "+".join(["1"] * 126) + ";"
    r = client.post("/analisar", json={"codigo": codigo})
    assert r.status_code == 200
    assert r.json()["sintatica"]["sucesso"] is True
