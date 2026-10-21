import pytest
from app.validation import (MSG_GRANDE, MSG_SO_ESPACOS, MSG_TIPO, MSG_VAZIO,
                            TAMANHO_MAXIMO, validar_codigo)


def test_codigo_valido():
    assert validar_codigo("int numero = 10;") == (True, "")


def test_codigo_com_erro_intencional_e_aceito():
    # O backend não faz análise sintática nesta etapa
    assert validar_codigo("int = = 10 ;;; }{")[0] is True


def test_texto_vazio():
    assert validar_codigo("") == (False, MSG_VAZIO)


@pytest.mark.parametrize("entrada", [" ", "   ", "\n", "\t\n  \r\n"])
def test_apenas_espacos(entrada):
    assert validar_codigo(entrada) == (False, MSG_SO_ESPACOS)


@pytest.mark.parametrize("entrada", [None, 123, ["int x;"], {"a": 1}, True])
def test_tipo_invalido(entrada):
    assert validar_codigo(entrada) == (False, MSG_TIPO)


def test_caracteres_especiais():
    assert validar_codigo('printf("ação: %d\\n", x); // çãé 😀 @#$')[0] is True


def test_limite_de_tamanho():
    assert validar_codigo("a" * TAMANHO_MAXIMO)[0] is True
    assert validar_codigo("a" * (TAMANHO_MAXIMO + 1)) == (False, MSG_GRANDE)
