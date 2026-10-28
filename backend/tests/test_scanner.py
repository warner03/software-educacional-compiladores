import pytest

from app.scanner import analisar_lexico


@pytest.mark.parametrize("palavra", ["int", "float", "if", "else"])
def test_reservadas(palavra):
    assert analisar_lexico(palavra) == {
        "sucesso": True,
        "tokens": [{"tipo": "PALAVRA_RESERVADA", "lexema": palavra, "linha": 1, "coluna": 1}],
        "erros": [],
    }


@pytest.mark.parametrize("nome", ["x", "numero", "_x1", "A12_b", "ifelse", "INT", "while"])
def test_identificadores_e_limite_de_palavra(nome):
    r = analisar_lexico(nome)
    assert r["sucesso"]
    assert [(t["tipo"], t["lexema"]) for t in r["tokens"]] == [("IDENTIFICADOR", nome)]


@pytest.mark.parametrize("lexema,tipo", [
    ("0", "LITERAL_INTEIRO"), ("42", "LITERAL_INTEIRO"), ("001", "LITERAL_INTEIRO"),
    ("7.5", "LITERAL_REAL"), ("0.0", "LITERAL_REAL"), ("12.003", "LITERAL_REAL"),
])
def test_literais(lexema, tipo):
    r = analisar_lexico(lexema)
    assert r["sucesso"]
    assert r["tokens"][0] == {"tipo": tipo, "lexema": lexema, "linha": 1, "coluna": 1}


@pytest.mark.parametrize("operador", ["+", "-", "*", "/", "=", "==", "!=", "<", ">", "<=", ">="])
def test_operadores(operador):
    r = analisar_lexico(operador)
    assert r["sucesso"]
    assert [(t["tipo"], t["lexema"]) for t in r["tokens"]] == [("OPERADOR", operador)]


@pytest.mark.parametrize("delimitador", list("(){};,"))
def test_delimitadores(delimitador):
    r = analisar_lexico(delimitador)
    assert r["sucesso"]
    assert r["tokens"][0]["tipo"] == "DELIMITADOR"
    assert r["tokens"][0]["lexema"] == delimitador


def test_prioridade_de_operadores_e_sinal_separado():
    r = analisar_lexico("a>=-1; b!=2; c==3; d<=4;")
    assert r["sucesso"]
    assert [t["lexema"] for t in r["tokens"]] == [
        "a", ">=", "-", "1", ";", "b", "!=", "2", ";", "c", "==", "3", ";", "d", "<=", "4", ";",
    ]


@pytest.mark.parametrize("codigo", ["", " \t\n\r\v\f", "// comentário 😀", "/* bloco\ncom @#$ */"])
def test_vazio_espacos_e_apenas_comentarios(codigo):
    assert analisar_lexico(codigo) == {"sucesso": True, "tokens": [], "erros": []}


def test_comentarios_nao_confundem_divisao_e_posicoes():
    r = analisar_lexico("int/* @ */x; // ignora\n\tfloat y=10/2;")
    assert r["sucesso"]
    assert [(t["lexema"], t["linha"], t["coluna"]) for t in r["tokens"]] == [
        ("int", 1, 1), ("x", 1, 11), (";", 1, 12), ("float", 2, 2),
        ("y", 2, 8), ("=", 2, 9), ("10", 2, 10), ("/", 2, 12), ("2", 2, 13), (";", 2, 14),
    ]


@pytest.mark.parametrize("quebra", ["\n", "\r\n", "\r"])
def test_linha_e_coluna_com_diferentes_quebras(quebra):
    r = analisar_lexico("int a;" + quebra + "  float b")
    assert r["tokens"][-2] == {"tipo": "PALAVRA_RESERVADA", "lexema": "float", "linha": 2, "coluna": 3}
    assert r["tokens"][-1]["coluna"] == 9


@pytest.mark.parametrize("invalido", ["12abc", "1.", ".5", "1.2.3", "1e3", "1e-3", "0x10", "3_foo"])
def test_numero_malformado_agrupado_e_recuperacao(invalido):
    r = analisar_lexico(invalido + "; int x;")
    assert not r["sucesso"]
    assert len(r["erros"]) == 1
    assert r["erros"][0]["lexema"] == invalido
    assert r["erros"][0]["linha"] == r["erros"][0]["coluna"] == 1
    assert [t["lexema"] for t in r["tokens"]] == [";", "int", "x", ";"]


@pytest.mark.parametrize("invalido", ["@", "#", "$", "%", "!", "&", "|", "[", "]", "é", "😀"])
def test_caracteres_invalidos_com_localizacao(invalido):
    r = analisar_lexico("int x;\n  " + invalido + " y;")
    assert not r["sucesso"]
    assert r["erros"][0] == {
        "tipo": "ERRO_LEXICO", "lexema": invalido, "linha": 2, "coluna": 3,
        "mensagem": f"Caractere não reconhecido: {invalido!r}. Verifique o subconjunto Mini-C suportado.",
    }
    assert r["tokens"][-2]["lexema"] == "y"
    assert r["tokens"][-2]["coluna"] == 5


@pytest.mark.parametrize("invalido", ["++", "--", "+=", "-=", "*=", "/=", "%=", "&&", "||", "<<", ">>", "->", "&=", "|=", "^="])
def test_operadores_fora_do_recorte(invalido):
    r = analisar_lexico("x " + invalido + " 1;")
    assert not r["sucesso"]
    assert len(r["erros"]) == 1
    assert r["erros"][0]["lexema"] == invalido
    assert [t["lexema"] for t in r["tokens"]] == ["x", "1", ";"]


@pytest.mark.parametrize("literal", ['"texto @"', "'a'", '"aspas \\" dentro"', '"não fechado'])
def test_literais_fora_do_escopo_nao_geram_cascata(literal):
    r = analisar_lexico(literal + "\nint x;")
    assert not r["sucesso"]
    assert len(r["erros"]) == 1
    assert r["erros"][0]["lexema"] == literal
    assert r["tokens"][0]["lexema"] == "int"
    assert r["tokens"][0]["linha"] == 2


def test_comentario_nao_fechado_preserva_tokens_anteriores():
    r = analisar_lexico("int x;\n/* falta fechar\nfloat y;")
    assert [t["lexema"] for t in r["tokens"]] == ["int", "x", ";"]
    assert r["erros"][0]["lexema"] == "/* falta fechar\nfloat y;"
    assert (r["erros"][0]["linha"], r["erros"][0]["coluna"]) == (2, 1)
    assert "não fechado" in r["erros"][0]["mensagem"]


def test_acumula_erros_e_continua_ate_o_fim():
    r = analisar_lexico("@ int x=12abc;\n$ float y=2.5;")
    assert [e["lexema"] for e in r["erros"]] == ["@", "12abc", "$"]
    assert r["tokens"][-2]["lexema"] == "2.5"
    assert r["tokens"][-1]["lexema"] == ";"


def test_erros_sintaticos_nao_sao_erros_lexicos():
    r = analisar_lexico("int = ; } if ( )")
    assert r["sucesso"]
    assert len(r["tokens"]) == 7


def test_codigo_longo_no_limite_nao_perde_token_final():
    r = analisar_lexico(" " * 9999 + "x")
    assert r["tokens"] == [{"tipo": "IDENTIFICADOR", "lexema": "x", "linha": 1, "coluna": 10000}]
