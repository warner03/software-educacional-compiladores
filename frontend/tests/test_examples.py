from examples import CODIGO_INICIAL, EXEMPLOS


def test_ha_ao_menos_tres_exemplos():
    assert len(EXEMPLOS) >= 3


def test_exemplos_nao_vazios_e_distintos():
    codigos = list(EXEMPLOS.values())
    assert all(c.strip() for c in codigos)
    assert len(set(codigos)) == len(codigos)


def test_codigo_inicial_e_um_exemplo():
    assert CODIGO_INICIAL in EXEMPLOS.values()
