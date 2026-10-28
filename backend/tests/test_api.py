from fastapi.testclient import TestClient

from app.main import app
from app.validation import MSG_AUSENTE, MSG_SO_ESPACOS, MSG_VAZIO

client = TestClient(app, raise_server_exceptions=False)


def test_saude():
    r = client.get("/saude")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_requisicao_valida():
    r = client.post("/analisar", json={"codigo": "int numero = 10;"})
    assert r.status_code == 200
    dados = r.json()
    assert dados["recebido"] is True
    assert dados["mensagem"] == "Análise léxica concluída sem erros."
    assert dados["total_caracteres"] == len("int numero = 10;")
    assert dados["total_linhas"] == 1
    assert dados["sucesso"] is True
    assert dados["erros"] == []
    assert dados["tokens"] == [
        {"tipo": "PALAVRA_RESERVADA", "lexema": "int", "linha": 1, "coluna": 1},
        {"tipo": "IDENTIFICADOR", "lexema": "numero", "linha": 1, "coluna": 5},
        {"tipo": "OPERADOR", "lexema": "=", "linha": 1, "coluna": 12},
        {"tipo": "LITERAL_INTEIRO", "lexema": "10", "linha": 1, "coluna": 14},
        {"tipo": "DELIMITADOR", "lexema": ";", "linha": 1, "coluna": 16},
    ]


def test_contagem_de_linhas():
    r = client.post("/analisar", json={"codigo": "int a;\nint b;\nint c;"})
    assert r.json()["total_linhas"] == 3


def test_codigo_com_caracteres_especiais():
    r = client.post("/analisar", json={"codigo": 'printf("olá, %d\\n", x); // 😀'})
    assert r.status_code == 200
    assert r.json()["sucesso"] is False  # aspas não fazem parte da Mini-C


def test_erro_lexico_retorna_tokens_validos_e_mantem_http_200():
    r = client.post("/analisar", json={"codigo": "@ int x; $"})
    assert r.status_code == 200
    dados = r.json()
    assert dados["recebido"] is True
    assert dados["sucesso"] is False
    assert [e["lexema"] for e in dados["erros"]] == ["@", "$"]
    assert [t["lexema"] for t in dados["tokens"]] == ["int", "x", ";"]


def test_apenas_comentarios_retorna_sucesso_sem_tokens():
    dados = client.post("/analisar", json={"codigo": "/* comentário */"}).json()
    assert dados["sucesso"] is True
    assert dados["tokens"] == dados["erros"] == []


def test_estrutura_invalida_ainda_e_tokenizada():
    dados = client.post("/analisar", json={"codigo": "int = ;"}).json()
    assert dados["sucesso"] is True


def test_codigo_vazio():
    r = client.post("/analisar", json={"codigo": ""})
    assert r.status_code == 400
    assert r.json() == {"recebido": False, "erro": "entrada_invalida", "mensagem": MSG_VAZIO}


def test_codigo_somente_espacos():
    r = client.post("/analisar", json={"codigo": "   \n\t "})
    assert r.status_code == 400
    assert r.json()["mensagem"] == MSG_SO_ESPACOS


def test_campo_ausente():
    r = client.post("/analisar", json={"outro": "x"})
    assert r.status_code == 400
    assert r.json()["erro"] == "requisicao_invalida"
    assert r.json()["mensagem"] == MSG_AUSENTE


def test_tipo_errado():
    r = client.post("/analisar", json={"codigo": 42})
    assert r.status_code == 400
    assert r.json()["erro"] == "entrada_invalida"


def test_json_malformado():
    r = client.post("/analisar", content="{nao e json", headers={"Content-Type": "application/json"})
    assert r.status_code == 400
    assert r.json()["erro"] == "requisicao_invalida"


def test_corpo_nao_objeto():
    r = client.post("/analisar", json=["int x;"])
    assert r.status_code == 400


def test_metodo_nao_permitido():
    assert client.get("/analisar").status_code == 405


def test_erro_inesperado_nao_vaza_detalhes(monkeypatch):
    import app.main as main

    def quebra(_):
        raise RuntimeError("segredo interno /etc/caminho")

    monkeypatch.setattr(main, "validar_codigo", quebra)
    r = client.post("/analisar", json={"codigo": "int x;"})
    assert r.status_code == 500
    corpo = r.text
    assert "segredo" not in corpo and "/etc" not in corpo and "Traceback" not in corpo
    assert r.json()["erro"] == "erro_interno"
