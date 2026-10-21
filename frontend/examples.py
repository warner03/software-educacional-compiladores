"""Exemplos de programas Mini-C disponíveis na interface."""

EXEMPLOS = {
    "1 - Declaração e inicialização de variável": "int numero = 10;",
    "2 - Operação aritmética": "int resultado = 10 + 5;",
    "3 - Estrutura condicional (if)": "int numero = 10;\nif (numero > 0) {\n    numero = numero + 1;\n}",
    "4 - Condicional com else e float": (
        "float media = 7.5;\nif (media >= 6.0) {\n    media = media + 1.0;\n} else {\n    media = media - 1.0;\n}"
    ),
}

EXEMPLO_NENHUM = "— Selecione um exemplo —"
CODIGO_INICIAL = EXEMPLOS["1 - Declaração e inicialização de variável"]
