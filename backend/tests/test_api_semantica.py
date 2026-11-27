import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.parser import analisar_sintatico
from app.scanner import analisar_lexico
from test_semantica import CASOS

client = TestClient(app, raise_server_exceptions=False)


@pytest.mark.parametrize("caso", CASOS, ids=lambda c: c["id"])
def test_casos_semanticos_na_api_preservam_contratos_anteriores(caso):
    resposta = client.post("/analisar", json={"codigo": caso["codigo"]})
    assert resposta.status_code == 200
    dados = resposta.json()
    lexico = analisar_lexico(caso["codigo"])
    sintatica = analisar_sintatico(lexico["tokens"], caso["codigo"])
    assert dados["sucesso"] is True
    assert {k: dados[k] for k in ("sucesso", "tokens", "erros")} == lexico
    assert dados["sintatica"] == sintatica
    assert dados["semantica"]["sucesso"] is caso["sucesso_esperado"]
    assert [e["regra"] for e in dados["semantica"]["erros"]] == caso["regras_esperadas"]
    assert dados["semantica"]["escopos"][0]["id"] == "E0"


@pytest.mark.parametrize("codigo,motivo", [("@ int x;", "erros_lexicos"), ("int x = ;", "erros_sintaticos"), ("/* comentário */", "erros_sintaticos")])
def test_semantica_nao_e_chamada_apos_erros_anteriores(codigo, motivo, monkeypatch):
    def proibido(*_):
        raise AssertionError("Semântica não deve receber árvore inválida")
    monkeypatch.setattr("app.main.analisar_semantico", proibido)
    resposta = client.post("/analisar", json={"codigo": codigo})
    assert resposta.status_code == 200
    assert resposta.json()["semantica"] == {"estado": "nao_executada", "sucesso": None, "motivo": motivo, "tabelaSimbolos": [], "escopos": [], "erros": []}


def test_validacao_de_entrada_ocorre_antes_da_semantica(monkeypatch):
    def proibido(*_):
        raise AssertionError("Semântica executada para entrada inválida")
    monkeypatch.setattr("app.main.analisar_semantico", proibido)
    for corpo in [{"codigo": ""}, {"codigo": "x" * 10001}, {"codigo": 1}, {}]:
        r = client.post("/analisar", json=corpo)
        assert r.status_code == 400 and "semantica" not in r.json()


def test_erro_semantico_preserva_ast_e_tabela_de_declaracoes():
    r = client.post("/analisar", json={"codigo": "int x=1; total=x+5;"}).json()
    assert r["sucesso"] is True and r["sintatica"]["sucesso"] is True
    assert r["semantica"]["sucesso"] is False and r["sintatica"]["ast"] is not None
    assert [s["nome"] for s in r["semantica"]["tabelaSimbolos"]] == ["x"]
    assert r["semantica"]["erros"][0]["noAst"] == "/comandos/1/alvo"
