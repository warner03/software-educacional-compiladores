"""Esperados derivados da gramática e de oráculos definidos antes do parser."""
import json
from pathlib import Path

import pytest

from app.parser import analisar_sintatico
from app.scanner import analisar_lexico

FIXTURES = Path(__file__).parent / "fixtures"
CASOS = {c["id"]: c for c in json.loads((FIXTURES / "etapa4-casos.json").read_text())["casos"]}
REFERENCIAS = json.loads((FIXTURES / "etapa4-ast-referencias.json").read_text())["referencias"]


def analisar(codigo):
    lexico = analisar_lexico(codigo)
    assert lexico["sucesso"], lexico["erros"]
    antes = json.dumps(lexico["tokens"], sort_keys=True)
    resultado = analisar_sintatico(lexico["tokens"], codigo)
    assert json.dumps(lexico["tokens"], sort_keys=True) == antes
    return resultado


def sem_posicoes(valor):
    if isinstance(valor, dict):
        return {k: sem_posicoes(v) for k, v in valor.items() if k not in ("inicio", "fim")}
    if isinstance(valor, list):
        return [sem_posicoes(v) for v in valor]
    return valor


def literal(lexema):
    return {"tipo": "Literal", "categoria": "inteiro", "lexema": lexema}


def binario(op, esquerda, direita):
    return {"tipo": "Binario", "operador": op, "esquerda": esquerda, "direita": direita}


@pytest.mark.parametrize("caso", [f"V{i:02}" for i in range(1, 13)])
def test_programas_validos_do_plano(caso):
    r = analisar(CASOS[caso]["codigo"])
    assert r["estado"] == "sucesso" and r["sucesso"] is True
    assert r["erros"] == [] and r["ast"]["tipo"] == "Programa"


@pytest.mark.parametrize("referencia", REFERENCIAS, ids=lambda r: r["caso"])
def test_oraculos_independentes_fixados_na_tarefa4(referencia):
    ast = analisar(CASOS[referencia["caso"]]["codigo"])["ast"]
    assert sem_posicoes(ast["comandos"][0]["inicializador"]) == referencia["subarvore_esperada"]


@pytest.mark.parametrize("expressao,esperado", [
    ("2 + 3 * 4", binario("+", literal("2"), binario("*", literal("3"), literal("4")))),
    ("10 - 3 - 2", binario("-", binario("-", literal("10"), literal("3")), literal("2"))),
    ("(10 + 5) * 2", binario("*", binario("+", literal("10"), literal("5")), literal("2"))),
    ("24 / 3 / 2", binario("/", binario("/", literal("24"), literal("3")), literal("2"))),
    ("1 < 2 == 3 >= 4", binario("==", binario("<", literal("1"), literal("2")), binario(">=", literal("3"), literal("4")))),
    ("1 == 2 != 3", binario("!=", binario("==", literal("1"), literal("2")), literal("3"))),
    ("1 < 2 < 3", binario("<", binario("<", literal("1"), literal("2")), literal("3"))),
])
def test_precedencia_e_associatividade(expressao, esperado):
    r = analisar(f"int x = {expressao};")
    assert r["sucesso"]
    assert sem_posicoes(r["ast"]["comandos"][0]["inicializador"]) == esperado


def test_unarios_associam_a_direita_sem_avaliar_valores():
    r = analisar("float x = - + -7.50 * 2;")
    expr = sem_posicoes(r["ast"]["comandos"][0]["inicializador"])
    assert expr == binario("*", {
        "tipo": "Unario", "operador": "-", "operando": {
            "tipo": "Unario", "operador": "+", "operando": {
                "tipo": "Unario", "operador": "-", "operando": {
                    "tipo": "Literal", "categoria": "real", "lexema": "7.50"}}}}, literal("2"))


def test_formato_de_declaracao_atribuicao_blocos_e_condicionais():
    ast = sem_posicoes(analisar("int x; if (x) { x = 1; if (x) {} else {} } else { float y; }")["ast"])
    declaracao, condicional = ast["comandos"]
    assert declaracao == {"tipo": "Declaracao", "tipoDado": "int", "nome": "x", "inicializador": None}
    assert condicional["tipo"] == "Se"
    assert condicional["condicao"] == {"tipo": "Identificador", "nome": "x"}
    atribuicao, interno = condicional["entao"]["comandos"]
    assert atribuicao == {"tipo": "Atribuicao", "alvo": {"tipo": "Identificador", "nome": "x"}, "valor": literal("1")}
    assert interno["entao"] == interno["senao"] == {"tipo": "Bloco", "comandos": []}
    assert condicional["senao"]["comandos"][0]["nome"] == "y"
    assert analisar("if (1) {}")["ast"]["comandos"][0]["senao"] is None


@pytest.mark.parametrize("caso,lexema,esperado", [
    ("S01", "", ";"), ("S02", "{", ")"), ("S03", "", "}"),
    ("S04", ";", "LITERAL_INTEIRO"), ("S05", "else", "if"),
    ("S06", "*", "LITERAL_INTEIRO"), ("S07", "if", "IDENTIFICADOR"),
    ("S08", "", "LITERAL_INTEIRO"), ("S09", ",", ";"), ("S10", "(", "="),
])
def test_erros_do_plano_com_esperado_e_encontrado(caso, lexema, esperado):
    codigo = CASOS[caso]["codigo"]
    r = analisar(codigo)
    assert r["estado"] == "erro" and r["sucesso"] is False and r["ast"] is None
    erro = r["erros"][0]
    assert erro["tipo"] == "ERRO_SINTATICO"
    assert erro["lexema"] == lexema and esperado in erro["esperado"]
    assert erro["linha"] == 1
    assert erro["coluna"] == (codigo.index(lexema) + 1 if lexema else len(codigo) + 1)
    assert erro["encontrado"] == ("EOF" if not lexema else analisar_lexico(lexema)["tokens"][0]["tipo"])
    assert "Encontrado:" in erro["mensagem"]
    assert "Traceback" not in erro["mensagem"]


@pytest.mark.parametrize("codigo,esperado", [
    ("if x {}", "("), ("if (1) int x;", "{"), ("if (1) {} else if (1) {}", "{"),
    ("int x = (1 + 2;", ")"), ("x 1;", "="), (";", "int"),
    ("int x = if;", "LITERAL_INTEIRO"), ("int x = 1 = 2;", ";"),
    ("int f() {}", ";"), ("return 1;", "="), ("}", "int"),
])
def test_construcoes_fora_da_gramatica_nao_sao_aceitas(codigo, esperado):
    r = analisar(codigo)
    assert not r["sucesso"] and r["ast"] is None
    assert esperado in r["erros"][0]["esperado"]


@pytest.mark.parametrize("codigo", ["", " ", "// só comentário", "/* apenas comentário */"])
def test_programa_vazio_para_parser_direto(codigo):
    r = analisar(codigo)
    assert not r["sucesso"] and r["ast"] is None
    assert r["erros"][0]["encontrado"] == "EOF"
    assert "Programa vazio" in r["erros"][0]["mensagem"]


def test_recuperacao_em_ponto_e_virgula_acumula_erros_independentes():
    r = analisar("int a = ;\nint b;\nb = ;\nint c = 3;")
    assert r["ast"] is None and not r["sucesso"]
    assert [(e["linha"], e["coluna"], e["lexema"]) for e in r["erros"]] == [(1, 9, ";"), (3, 5, ";")]


def test_recuperacao_em_chave_nao_consumida_pelo_item_do_bloco():
    r = analisar("{ int a = }\nint b = ;\nint c;")
    assert [(e["linha"], e["coluna"], e["lexema"]) for e in r["erros"]] == [(1, 11, "}"), (2, 9, ";")]
    assert r["ast"] is None


def test_chaves_avulsas_e_else_nao_causam_loop():
    r = analisar("} } else {} int x;")
    assert r["ast"] is None
    assert [e["lexema"] for e in r["erros"]] == ["}", "}", "else"]


def test_posicoes_unicode_crlf_cr_tab_e_fim_exclusivo():
    codigo = "// 😀\r\n\tint x = (10 + 2) * 3;\r x = -x; // fim"
    r = analisar(codigo)
    assert r["sucesso"]
    ast = r["ast"]
    assert ast["inicio"] == {"linha": 2, "coluna": 2}
    assert ast["fim"] == {"linha": 3, "coluna": 9}
    decl, atr = ast["comandos"]
    assert decl["fim"] == {"linha": 2, "coluna": 23}
    expr = decl["inicializador"]
    assert expr["inicio"] == {"linha": 2, "coluna": 10}  # inclui '(' do operando
    assert expr["fim"] == {"linha": 2, "coluna": 22}
    dez = expr["esquerda"]["esquerda"]
    assert dez["inicio"] == {"linha": 2, "coluna": 11}
    assert dez["fim"] == {"linha": 2, "coluna": 13}
    assert atr["alvo"]["inicio"] == {"linha": 3, "coluna": 2}
    assert atr["valor"]["inicio"] == {"linha": 3, "coluna": 6}


def test_folhas_agrupadas_apontam_para_tokens_e_parenteses_nao_viram_nos():
    ast = analisar("int x = ((123));")["ast"]
    valor = ast["comandos"][0]["inicializador"]
    assert valor == {"tipo": "Literal", "inicio": {"linha": 1, "coluna": 11},
                     "fim": {"linha": 1, "coluna": 14}, "categoria": "inteiro", "lexema": "123"}


def test_eof_conta_comentarios_e_quebras_apos_ultimo_token():
    r = analisar("int x // 😀\r\n\t/* fim */")
    erro = r["erros"][0]
    assert (erro["linha"], erro["coluna"], erro["encontrado"]) == (2, 11, "EOF")
    r = analisar("{\n int x;")
    assert "bloco aberto na linha 1, coluna 1" in r["erros"][0]["mensagem"]


@pytest.mark.parametrize("forma", ["bloco", "parenteses", "unarios", "misto"])
@pytest.mark.parametrize("niveis,aceita", [(64, True), (65, False)])
def test_limite_aninhamento_definido_antes_dos_testes(forma, niveis, aceita):
    if forma == "bloco":
        codigo = "{" * niveis + "int x;" + "}" * niveis
    elif forma == "parenteses":
        codigo = "int x = " + "(" * niveis + "1" + ")" * niveis + ";"
    elif forma == "unarios":
        codigo = "int x = " + "- " * niveis + "1;"
    else:
        codigo = "{" * 32 + "int x = " + "(" * (niveis - 32) + "1" + ")" * (niveis - 32) + ";" + "}" * 32
    r = analisar(codigo)
    assert r["sucesso"] is aceita
    if not aceita:
        assert r["ast"] is None and r["erros"][0]["codigo"] == "limite_profundidade"


@pytest.mark.parametrize("literais,aceita", [(126, True), (127, False), (2500, False)])
def test_altura_limita_cadeias_associativas_sem_erro_de_serializacao(literais, aceita):
    r = analisar("int x = " + "+".join(["1"] * literais) + ";")
    assert r["sucesso"] is aceita
    json.dumps(r)
    if not aceita:
        assert r["erros"][0]["codigo"] == "limite_altura"


@pytest.mark.parametrize("blocos,aceita", [(1999, True), (2000, False)])
def test_quantidade_de_nos_inclui_raiz_e_nao_confunde_com_profundidade(blocos, aceita):
    r = analisar("{}" * blocos)
    assert r["sucesso"] is aceita
    if aceita:
        assert len(r["ast"]["comandos"]) == 1999
    else:
        assert r["ast"] is None and r["erros"][0]["codigo"] == "limite_nos"


@pytest.mark.parametrize("caso", ["M01", "M02", "M03"])
def test_futuras_questoes_semanticas_sao_sintaticamente_validas(caso):
    assert analisar(CASOS[caso]["codigo"])["sucesso"] is True


def test_posicoes_de_todas_as_folhas_correspondem_aos_tokens_consumidos():
    codigo = "/* 😀 */ int x = (10 + 2) * -3;\nif (x >= 0) { x = x / 2; } else {}"
    tokens = analisar_lexico(codigo)["tokens"]
    folhas = {(t["lexema"], t["linha"], t["coluna"]) for t in tokens}
    pendentes = [analisar(codigo)["ast"]]
    while pendentes:
        no = pendentes.pop()
        if isinstance(no, dict):
            if no.get("tipo") in ("Identificador", "Literal"):
                lexema = no.get("nome", no.get("lexema"))
                assert (lexema, no["inicio"]["linha"], no["inicio"]["coluna"]) in folhas
                assert no["fim"]["coluna"] - no["inicio"]["coluna"] == len(lexema)
            pendentes.extend(no.values())
        elif isinstance(no, list):
            pendentes.extend(no)
