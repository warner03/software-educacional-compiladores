"""Validações de entrada do backend (independentes do FastAPI, fáceis de testar)."""

TAMANHO_MAXIMO = 10_000  # caracteres

MSG_VAZIO = "Informe um código-fonte antes de solicitar a análise."
MSG_SO_ESPACOS = (
    "O código informado contém apenas espaços em branco. "
    "Digite um programa para analisar."
)
MSG_TIPO = "O campo 'codigo' deve ser um texto."
MSG_AUSENTE = "O campo obrigatório 'codigo' não foi enviado."
MSG_GRANDE = f"O código excede o limite de {TAMANHO_MAXIMO} caracteres."


def validar_codigo(codigo):
    """Retorna (ok, mensagem). Não presume que o código seja válido em Mini-C."""
    if not isinstance(codigo, str):
        return False, MSG_TIPO
    if codigo == "":
        return False, MSG_VAZIO
    if codigo.strip() == "":
        return False, MSG_SO_ESPACOS
    if len(codigo) > TAMANHO_MAXIMO:
        return False, MSG_GRANDE
    return True, ""
