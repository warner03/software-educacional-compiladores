"""Esperados definidos pela política Mini-C, não pelo analisador em teste."""
import copy
import json
from pathlib import Path

import pytest

from app.scanner import analisar_lexico
from app.parser import analisar_sintatico
from app.semantica import analisar_semantico

CASOS = json.loads((Path(__file__).parent / "fixtures/etapa5-semantica.json").read_text())["casos"]


def analisar(codigo):
    lexico = analisar_lexico(codigo)
    assert lexico["sucesso"], lexico["erros"]
    sintatica = analisar_sintatico(lexico["tokens"], codigo)
    assert sintatica["sucesso"], sintatica["erros"]
    antes = copy.deepcopy((sintatica["ast"], lexico["tokens"]))
    resultado = analisar_semantico(sintatica["ast"], lexico["tokens"])
    assert antes == (sintatica["ast"], lexico["tokens"])
    return resultado


def resolver(ast, caminho):
    for parte in caminho.split("/")[1:] if caminho else []:
        ast = ast[int(parte)] if isinstance(ast, list) else ast[parte]
    return ast


@pytest.mark.parametrize("caso", CASOS, ids=lambda c: c["id"])
def test_30_casos_fixados_antes_da_implementacao(caso):
    r = analisar(caso["codigo"])
    assert r["sucesso"] is caso["sucesso_esperado"]
    assert r["estado"] == ("sucesso" if caso["sucesso_esperado"] else "erro")
    assert [e["regra"] for e in r["erros"]] == caso["regras_esperadas"]


def test_tabela_posicoes_unicode_crlf_e_ligacoes_para_ast():
    codigo = "// 😀\r\n\tfloat media = 1;\r\n{\r\n\tint x;\r\n\tx = media;\r\n}"
    r = analisar(codigo)
    media, x = r["tabelaSimbolos"]
    assert (media["id"], media["nome"], media["tipo"], media["escopo"], media["linha"], media["coluna"], media["inicializado"]) == ("S1", "media", "float", "E0", 2, 8, True)
    assert media["fim"] == {"linha": 2, "coluna": 13}
    assert (x["id"], x["escopo"], x["linha"], x["coluna"], x["inicializado"]) == ("S2", "E1", 4, 6, False)
    erro = r["erros"][0]
    assert (erro["linha"], erro["coluna"], erro["regra"], erro["simboloId"]) == (5, 2, "TIPOS_INCOMPATIVEIS", "S2")
    assert erro["fim"] == {"linha": 5, "coluna": 3}
    assert erro["noAst"] == "/comandos/1/comandos/1"
    assert r["escopos"][0]["pai"] is None
    assert r["escopos"][1]["pai"] == "E0"
    ast = analisar_sintatico(analisar_lexico(codigo)["tokens"], codigo)["ast"]
    for s in r["tabelaSimbolos"]:
        assert resolver(ast, s["noAst"])["tipo"] == "Declaracao"
        for ref in s["referencias"]:
            assert resolver(ast, ref["noAst"])["tipo"] == "Identificador"
    assert resolver(ast, erro["noAst"])["tipo"] == "Atribuicao"


def test_sombreamento_liga_referencias_ao_simbolo_visivel():
    codigo = "int x=1; {float x=2.0; x=x+1.0;} x=x+1;"
    r = analisar(codigo)
    global_, local = r["tabelaSimbolos"]
    assert r["sucesso"]
    assert global_["sombreia"] is None and local["sombreia"] == global_["id"]
    assert [ref["contexto"] for ref in global_["referencias"]] == ["atribuicao", "leitura"]
    assert [ref["contexto"] for ref in local["referencias"]] == ["atribuicao", "leitura"]
    assert global_["referencias"][0]["noAst"] == "/comandos/2/alvo"
    assert local["referencias"][0]["noAst"] == "/comandos/1/comandos/1/alvo"
    assert all(s["inicializado"] for s in r["tabelaSimbolos"])


def test_blocos_irmaos_nao_compartilham_declaracoes():
    r = analisar("{int x=1;} {float x=2.0; int y=1;}")
    assert r["sucesso"]
    assert [(s["nome"], s["escopo"], s["sombreia"]) for s in r["tabelaSimbolos"]] == [("x", "E1", None), ("x", "E2", None), ("y", "E2", None)]
    assert [e["pai"] for e in r["escopos"]] == [None, "E0", "E0"]


def test_redeclaracao_nao_sobrescreve_tipo_ou_inicializacao_anterior():
    r = analisar("int x=1; float x=2.0; int y=x;")
    assert [e["regra"] for e in r["erros"]] == ["REDECLARACAO_NO_ESCOPO"]
    assert [(s["nome"], s["tipo"], s["inicializado"]) for s in r["tabelaSimbolos"]] == [("x", "int", True), ("y", "int", True)]
    assert (r["erros"][0]["linha"], r["erros"][0]["coluna"]) == (1, 16)


@pytest.mark.parametrize("codigo,inicializado", [
    ("int x; if(1<2){x=1;}else{x=2;}", True),
    ("int x; if(1<2){x=1;}", False),
    ("int x=1; if(1<2){x=2;}", True),
    ("int x; if(1<2){int x=1;}else{x=2;}", False),
    ("int x; {x=1;}", True),
    ("int x; if(1<2){x=1;} x=2;", True),
    ("int x; if(1<2){x=1;}else{if(2<3){x=2;}}", False),
])
def test_intersecao_dos_caminhos_e_estado_final_do_escopo(codigo, inicializado):
    r = analisar(codigo)
    assert r["sucesso"]
    assert r["tabelaSimbolos"][0]["inicializado"] is inicializado


@pytest.mark.parametrize("codigo", [
    "int x=1.0;", "int x; x=1.0;", "int x=1.0/2;", "int x=1<2;",
])
def test_atribuicoes_sem_conversao_estreitadora_ou_bool_numerico(codigo):
    r = analisar(codigo)
    assert [e["regra"] for e in r["erros"]] == ["TIPOS_INCOMPATIVEIS"]
    assert r["tabelaSimbolos"][0]["inicializado"] is False


@pytest.mark.parametrize("codigo", [
    "float x=1;", "float x=1+2.0;", "int x=5/2;", "float x=5/2;", "float x=- +1.5;",
])
def test_promocao_e_tipos_numericos_sem_executar_expressoes(codigo):
    assert analisar(codigo)["sucesso"]


@pytest.mark.parametrize("codigo,regra", [
    ("if(1<2<3){}", "TIPOS_NAO_COMPARAVEIS"),
    ("if((1<2)<(3<4)){}", "TIPOS_NAO_COMPARAVEIS"),
    ("if((1<2)+1){}", "OPERANDOS_NAO_NUMERICOS"),
    ("if(1){}", "CONDICAO_NAO_BOOLEANA"),
])
def test_comparacoes_e_condicoes_conforme_politica(codigo, regra):
    assert [e["regra"] for e in analisar(codigo)["erros"]] == [regra]


def test_erros_independentes_e_sem_cascata_por_tipo_desconhecido():
    r = analisar("int a=u+1;\nint b=v*2;\nif(z){}")
    assert [e["regra"] for e in r["erros"]] == ["IDENTIFICADOR_NAO_DECLARADO"] * 3
    assert [(e["linha"], e["coluna"]) for e in r["erros"]] == [(1, 7), (2, 7), (3, 4)]
    assert len(r["tabelaSimbolos"]) == 2
    assert all(not s["inicializado"] for s in r["tabelaSimbolos"])
    assert all(e["sugestao"] and e["mensagem"] for e in r["erros"])


def test_uso_antes_de_declaracao_e_posicao_do_erro():
    r = analisar("x=1; int x=2;")
    assert [e["regra"] for e in r["erros"]] == ["IDENTIFICADOR_NAO_DECLARADO"]
    assert r["erros"][0]["coluna"] == 1
    assert len(r["tabelaSimbolos"]) == 1
    assert r["tabelaSimbolos"][0]["inicializado"]


def test_leitura_no_proprio_inicializador_sombreia_variavel_externa():
    r = analisar("int x=1; {int x=x;}")
    assert r["erros"][0]["regra"] == "VARIAVEL_NAO_INICIALIZADA"
    assert r["erros"][0]["simboloId"] == "S2"
    assert [s["inicializado"] for s in r["tabelaSimbolos"]] == [True, False]


def test_limites_anteriores_continuam_serializaveis():
    for codigo in ["{}" * 1999, "{" * 64 + "int x=1;" + "}" * 64, "int x=" + "+".join(["1"] * 126) + ";"]:
        r = analisar(codigo)
        assert r["sucesso"]
        json.dumps(r)
