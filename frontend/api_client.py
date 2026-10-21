"""Cliente HTTP do frontend para o backend FastAPI."""
import os

import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

MSG_VAZIO = "Informe um código-fonte antes de solicitar a análise."
MSG_SO_ESPACOS = "O código informado contém apenas espaços em branco. Digite um programa para analisar."
MSG_COMUNICACAO = "Não foi possível comunicar com o servidor. Verifique a conexão e tente novamente."
MSG_INESPERADO = "Ocorreu um erro inesperado. Tente novamente."


def validar_localmente(codigo):
    """Validação rápida no frontend (o backend valida de novo). Retorna mensagem ou None."""
    if not codigo:
        return MSG_VAZIO
    if not codigo.strip():
        return MSG_SO_ESPACOS
    return None


def enviar_codigo(codigo, url=None, timeout=5):
    """Envia o código ao backend. Retorna dict: {tipo, mensagem, dados}.

    tipo: 'sucesso' | 'entrada' | 'comunicacao' | 'servidor'
    """
    base = (url or BACKEND_URL).rstrip("/")
    try:
        resp = requests.post(f"{base}/analisar", json={"codigo": codigo}, timeout=timeout)
    except requests.RequestException:
        return {"tipo": "comunicacao", "mensagem": MSG_COMUNICACAO, "dados": None}

    try:
        dados = resp.json()
    except ValueError:
        return {"tipo": "servidor", "mensagem": MSG_INESPERADO, "dados": None}

    if resp.status_code == 200 and isinstance(dados, dict) and dados.get("recebido") is True:
        return {"tipo": "sucesso", "mensagem": dados.get("mensagem", ""), "dados": dados}
    if 400 <= resp.status_code < 500 and isinstance(dados, dict):
        return {"tipo": "entrada", "mensagem": dados.get("mensagem", MSG_INESPERADO), "dados": dados}
    return {"tipo": "servidor", "mensagem": MSG_INESPERADO, "dados": None}
