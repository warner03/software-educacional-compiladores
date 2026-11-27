"""API Mini-C — Etapa 5: scanner, parser e semântica com resultados separados."""
import json
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.validation import MSG_AUSENTE, validar_codigo
from app.scanner import analisar_lexico
from app.parser import analisar_sintatico
from app.semantica import analisar_semantico

logger = logging.getLogger("uvicorn.error.compilador")
app = FastAPI(title="Visualizador Educacional de Compiladores", version="0.5.0")

MSG_INTERNO = "Ocorreu um erro inesperado no servidor. Tente novamente."


def _erro(status, codigo_erro, mensagem):
    return JSONResponse(
        status_code=status,
        content={"recebido": False, "erro": codigo_erro, "mensagem": mensagem},
    )


@app.get("/saude")
def saude():
    return {"status": "ok"}


@app.post("/analisar")
async def analisar(request: Request):
    try:
        corpo = json.loads(await request.body())
    except (ValueError, UnicodeDecodeError):
        return _erro(400, "requisicao_invalida", "O corpo da requisição não é um JSON válido.")

    if not isinstance(corpo, dict):
        return _erro(400, "requisicao_invalida", "O corpo da requisição deve ser um objeto JSON.")
    if "codigo" not in corpo:
        return _erro(400, "requisicao_invalida", MSG_AUSENTE)

    ok, mensagem = validar_codigo(corpo["codigo"])
    if not ok:
        return _erro(400, "entrada_invalida", mensagem)

    codigo = corpo["codigo"]
    resultado = analisar_lexico(codigo)
    sintatica = analisar_sintatico(resultado["tokens"], codigo) if resultado["sucesso"] else {
        "estado": "nao_executada", "sucesso": None, "motivo": "erros_lexicos", "ast": None, "erros": [],
    }
    semantica = analisar_semantico(sintatica["ast"], resultado["tokens"]) if sintatica["sucesso"] is True else {
        "estado": "nao_executada", "sucesso": None,
        "motivo": "erros_lexicos" if not resultado["sucesso"] else "erros_sintaticos",
        "tabelaSimbolos": [], "escopos": [], "erros": [],
    }
    logger.info("Análise: lexico=%s sintatica=%s semantica=%s tokens=%d simbolos=%d erros_semanticos=%d",
                resultado["sucesso"], sintatica["estado"], semantica["estado"], len(resultado["tokens"]),
                len(semantica["tabelaSimbolos"]), len(semantica["erros"]))
    return {
        "recebido": True,
        "mensagem": "Análise léxica concluída sem erros." if resultado["sucesso"] else "Análise léxica concluída com erros. Revise os trechos indicados.",
        "total_caracteres": len(codigo),
        "total_linhas": len(codigo.splitlines()),
        **resultado,
        "sintatica": sintatica,
        "semantica": semantica,
    }


@app.exception_handler(Exception)
async def erro_inesperado(request: Request, exc: Exception):
    logger.exception("Erro inesperado")  # detalhes só no log, nunca na resposta
    return _erro(500, "erro_interno", MSG_INTERNO)
