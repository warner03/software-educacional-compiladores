"""Scanner manual de Mini-C: sem parser e sem dependências externas.

Posições são baseadas em 1 e contam caracteres Unicode (tab conta uma coluna).
CRLF e CR são normalizados para LF antes da leitura.
"""
import re

RESERVADAS = frozenset({"int", "float", "if", "else"})
OPERADORES = frozenset({"+", "-", "*", "/", "=", "==", "!=", "<", ">", "<=", ">="})
DELIMITADORES = frozenset("(){};,")
NAO_SUPORTADOS = frozenset({
    "++", "--", "+=", "-=", "*=", "/=", "%=", "&&", "||", "<<", ">>",
    "->", "&=", "|=", "^=",
})
NUMERO = re.compile(r"[0-9]+(?:\.[0-9]+)?\Z")


def _inicio_identificador(c):
    return "a" <= c <= "z" or "A" <= c <= "Z" or c == "_"


def _parte_identificador(c):
    return _inicio_identificador(c) or "0" <= c <= "9"


def analisar_lexico(codigo: str) -> dict:
    """Retorna tokens e erros, recuperando a leitura após trechos inválidos."""
    fonte = codigo.replace("\r\n", "\n").replace("\r", "\n")
    tokens, erros = [], []
    i, linha, coluna = 0, 1, 1

    def avancar(fim):
        nonlocal i, linha, coluna
        while i < fim:
            if fonte[i] == "\n":
                linha, coluna = linha + 1, 1
            else:
                coluna += 1
            i += 1

    def registrar(fim, tipo, mensagem=None):
        item = {"tipo": tipo, "lexema": fonte[i:fim], "linha": linha, "coluna": coluna}
        if mensagem is None:
            tokens.append(item)
        else:
            item["mensagem"] = mensagem
            erros.append(item)
        avancar(fim)

    while i < len(fonte):
        c = fonte[i]
        par = fonte[i:i + 2]
        if c in " \t\n\v\f":
            avancar(i + 1)
        elif par == "//":
            fim = fonte.find("\n", i + 2)
            avancar(len(fonte) if fim == -1 else fim)
        elif par == "/*":
            fim = fonte.find("*/", i + 2)
            if fim == -1:
                registrar(len(fonte), "ERRO_LEXICO", "Comentário de bloco não fechado. Acrescente */ para encerrá-lo.")
            else:
                avancar(fim + 2)
        elif _inicio_identificador(c):
            fim = i + 1
            while fim < len(fonte) and _parte_identificador(fonte[fim]):
                fim += 1
            tipo = "PALAVRA_RESERVADA" if fonte[i:fim] in RESERVADAS else "IDENTIFICADOR"
            registrar(fim, tipo)
        elif "0" <= c <= "9" or (c == "." and i + 1 < len(fonte) and "0" <= fonte[i + 1] <= "9"):
            fim = i + 1
            while fim < len(fonte):
                atual = fonte[fim]
                if _parte_identificador(atual) or atual == ".":
                    fim += 1
                elif atual in "+-" and fonte[fim - 1] in "eE":
                    fim += 1
                else:
                    break
            lexema = fonte[i:fim]
            if NUMERO.fullmatch(lexema):
                registrar(fim, "LITERAL_REAL" if "." in lexema else "LITERAL_INTEIRO")
            else:
                registrar(fim, "ERRO_LEXICO", "Sequência numérica inválida. Use dígitos (10) ou decimal com dígitos dos dois lados do ponto (7.5); nomes não podem começar com dígito.")
        elif c in "\"'":
            # Literais fora do subconjunto: agrupar evita um erro por letra.
            fim = i + 1
            while fim < len(fonte) and fonte[fim] != "\n":
                if fonte[fim] == c:
                    fim += 1
                    break
                if fonte[fim] == "\\" and fim + 1 < len(fonte) and fonte[fim + 1] != "\n":
                    fim += 2
                else:
                    fim += 1
            registrar(fim, "ERRO_LEXICO", "Literais entre aspas (strings e caracteres) não fazem parte desta Mini-C. Use números ou identificadores.")
        elif par in NAO_SUPORTADOS:
            registrar(i + 2, "ERRO_LEXICO", f"Operador {par!r} fora do subconjunto suportado. Consulte o guia de Mini-C.")
        elif len(par) == 2 and par in OPERADORES:
            registrar(i + 2, "OPERADOR")
        elif c in OPERADORES:
            registrar(i + 1, "OPERADOR")
        elif c in DELIMITADORES:
            registrar(i + 1, "DELIMITADOR")
        else:
            registrar(i + 1, "ERRO_LEXICO", f"Caractere não reconhecido: {c!r}. Verifique o subconjunto Mini-C suportado.")

    return {"sucesso": not erros, "tokens": tokens, "erros": erros}
