"""Descida recursiva Mini-C sobre os tokens da Etapa 3, sem refazer o scanner.

AST, gramática, limites e recuperação estão documentados em docs/gramatica.md.
Nenhuma expressão é executada e nenhuma verificação semântica é realizada.
"""
from dataclasses import dataclass

MAX_ANINHAMENTO = 64
MAX_NOS = 2000
MAX_ALTURA_AST = 128
INICIOS_ITEM = ["int", "float", "IDENTIFICADOR", "if", "{"]
OPERANDOS = ["IDENTIFICADOR", "LITERAL_INTEIRO", "LITERAL_REAL", "(", "+", "-"]


def _pos(token):
    return {"linha": token["linha"], "coluna": token["coluna"]}


def _fim(token):
    return {"linha": token["linha"], "coluna": token["coluna"] + len(token["lexema"])}


@dataclass
class _No:
    dados: dict
    inicio: dict
    fim: dict
    altura: int


class _ErroSintatico(Exception):
    def __init__(self, diagnostico):
        self.diagnostico = diagnostico


class _Limite(_ErroSintatico):
    """Interrompe toda a análise; recuperar não reduz o custo já atingido."""


class _Parser:
    def __init__(self, tokens, codigo):
        fonte = codigo.replace("\r\n", "\n").replace("\r", "\n")
        linhas = fonte.split("\n")
        eof = {"tipo": "EOF", "lexema": "", "linha": len(linhas), "coluna": len(linhas[-1]) + 1}
        self.tokens = [*tokens, eof]  # não modifica a sequência pública do scanner
        self.indice = 0
        self.profundidade = 0
        self.nos = 0
        self.erros = []

    @property
    def atual(self):
        return self.tokens[self.indice]

    def _avancar(self):
        token = self.atual
        if token["tipo"] != "EOF":
            self.indice += 1
        return token

    def _diagnostico(self, esperado, explicacao, token=None, codigo="gramatica"):
        token = token if token is not None else self.atual
        encontrado = "o fim do código" if token["tipo"] == "EOF" else repr(token["lexema"])
        return {
            "tipo": "ERRO_SINTATICO", "codigo": codigo,
            "lexema": token["lexema"], **_pos(token),
            "esperado": esperado, "encontrado": token["tipo"],
            "mensagem": f"{explicacao} Encontrado: {encontrado}.",
        }

    def _esperar(self, lexema, explicacao):
        if self.atual["lexema"] != lexema:
            raise _ErroSintatico(self._diagnostico([lexema], explicacao))
        return self._avancar()

    def _identificador(self, explicacao):
        if self.atual["tipo"] != "IDENTIFICADOR":
            raise _ErroSintatico(self._diagnostico(["IDENTIFICADOR"], explicacao))
        return self._avancar()

    def _entrar(self, token):
        if self.profundidade >= MAX_ANINHAMENTO:
            raise _Limite(self._diagnostico(
                ["menos aninhamento"],
                f"Limite de {MAX_ANINHAMENTO} níveis de blocos, parênteses e sinais unários. Simplifique o trecho.",
                token, "limite_profundidade"))
        self.profundidade += 1

    def _no(self, tipo, inicio, fim, filhos=(), **atributos):
        altura = 1 + max((f.altura for f in filhos if f is not None), default=0)
        self.nos += 1
        if self.nos > MAX_NOS:
            raise _Limite(self._diagnostico(
                ["programa menor"], f"Limite de {MAX_NOS} nós da AST. Divida o programa em exemplos menores.",
                codigo="limite_nos"))
        if altura > MAX_ALTURA_AST:
            raise _Limite(self._diagnostico(
                ["expressão ou estrutura menor"],
                f"Limite de altura {MAX_ALTURA_AST} da AST. Reduza a sequência de operações ou o aninhamento.",
                codigo="limite_altura"))
        return _No({"tipo": tipo, "inicio": inicio, "fim": fim, **atributos}, inicio, fim, altura)

    def _sincronizar(self, dentro_bloco):
        # ';' encerra a instrução defeituosa; '}' pertence ao chamador do bloco.
        # No nível superior, uma chave avulsa também deve ser consumida.
        while self.atual["tipo"] != "EOF":
            if self.atual["lexema"] == ";":
                self._avancar()
                return
            if self.atual["lexema"] == "}":
                if not dentro_bloco:
                    self._avancar()
                return
            self._avancar()

    def _itens(self, dentro_bloco=False):
        itens = []
        while self.atual["tipo"] != "EOF" and not (dentro_bloco and self.atual["lexema"] == "}"):
            try:
                itens.append(self._item())
            except _Limite:
                raise
            except _ErroSintatico as erro:
                self.erros.append(erro.diagnostico)
                self._sincronizar(dentro_bloco)
        return itens

    def programa(self):
        if self.atual["tipo"] == "EOF":
            raise _ErroSintatico(self._diagnostico(
                INICIOS_ITEM, "Programa vazio: escreva ao menos uma declaração, atribuição, condicional ou bloco. Comentários não formam comandos."))
        itens = self._itens()
        if self.erros:
            return None
        return self._no("Programa", itens[0].inicio, itens[-1].fim, itens,
                        comandos=[n.dados for n in itens]).dados

    def _item(self):
        token = self.atual
        if token["lexema"] in ("int", "float"):
            return self._declaracao()
        if token["tipo"] == "IDENTIFICADOR":
            return self._atribuicao()
        if token["lexema"] == "if":
            return self._condicional()
        if token["lexema"] == "{":
            return self._bloco()
        explicacao = "Era esperado o início de uma declaração, atribuição, if ou bloco."
        if token["lexema"] == "else":
            explicacao = "Um else precisa acompanhar um if e vir logo após o bloco desse if."
        raise _ErroSintatico(self._diagnostico(INICIOS_ITEM, explicacao))

    def _declaracao(self):
        tipo = self._avancar()
        nome = self._identificador("Após int ou float, era esperado um identificador de variável; palavras reservadas não podem ser nomes.")
        inicializador = None
        if self.atual["lexema"] == "=":
            self._avancar()
            inicializador = self._expressao()
        fim = self._esperar(";", "Era esperado ';' ao final da declaração. Declare uma variável por instrução.")
        return self._no("Declaracao", _pos(tipo), _fim(fim), [inicializador],
                        tipoDado=tipo["lexema"], nome=nome["lexema"],
                        inicializador=inicializador.dados if inicializador else None)

    def _atribuicao(self):
        nome = self._avancar()
        alvo = self._no("Identificador", _pos(nome), _fim(nome), nome=nome["lexema"])
        self._esperar("=", "Era esperado '=' após o nome para formar uma atribuição. Chamadas e laços não pertencem a este subconjunto.")
        valor = self._expressao()
        fim = self._esperar(";", "Era esperado ';' ao final da atribuição.")
        return self._no("Atribuicao", _pos(nome), _fim(fim), [alvo, valor], alvo=alvo.dados, valor=valor.dados)

    def _bloco(self):
        abertura = self._esperar("{", "Era esperado um bloco iniciado por '{'. Chaves são obrigatórias em if e else.")
        self._entrar(abertura)
        try:
            itens = self._itens(dentro_bloco=True)
            fim = self._esperar("}", f"Era esperado '}}' para fechar o bloco aberto na linha {abertura['linha']}, coluna {abertura['coluna']}.")
            return self._no("Bloco", _pos(abertura), _fim(fim), itens, comandos=[n.dados for n in itens])
        finally:
            self.profundidade -= 1

    def _condicional(self):
        inicio = self._avancar()
        abertura = self._esperar("(", "Era esperado '(' para iniciar a condição do if.")
        self._entrar(abertura)
        try:
            condicao = self._expressao()
            self._esperar(")", "Era esperado ')' para fechar a condição do if.")
        finally:
            self.profundidade -= 1
        entao = self._bloco()
        senao = None
        if self.atual["lexema"] == "else":
            self._avancar()
            senao = self._bloco()
        return self._no("Se", _pos(inicio), (senao or entao).fim, [condicao, entao, senao],
                        condicao=condicao.dados, entao=entao.dados, senao=senao.dados if senao else None)

    def _expressao(self):
        return self._binaria(self._relacional, ("==", "!="))

    def _relacional(self):
        return self._binaria(self._aditiva, ("<", ">", "<=", ">="))

    def _aditiva(self):
        return self._binaria(self._multiplicativa, ("+", "-"))

    def _multiplicativa(self):
        return self._binaria(self._unaria, ("*", "/"))

    def _binaria(self, proximo_nivel, operadores):
        esquerda = proximo_nivel()
        while self.atual["lexema"] in operadores:
            operador = self._avancar()
            direita = proximo_nivel()
            esquerda = self._no("Binario", esquerda.inicio, direita.fim, [esquerda, direita],
                                operador=operador["lexema"], esquerda=esquerda.dados, direita=direita.dados)
        return esquerda

    def _unaria(self):
        sinais = []
        try:
            while self.atual["lexema"] in ("+", "-"):
                token = self.atual
                self._entrar(token)
                sinais.append(self._avancar())
            operando = self._primaria()
            for sinal in reversed(sinais):
                operando = self._no("Unario", _pos(sinal), operando.fim, [operando],
                                    operador=sinal["lexema"], operando=operando.dados)
            return operando
        finally:
            self.profundidade -= len(sinais)

    def _primaria(self):
        token = self.atual
        if token["tipo"] == "IDENTIFICADOR":
            self._avancar()
            return self._no("Identificador", _pos(token), _fim(token), nome=token["lexema"])
        if token["tipo"] in ("LITERAL_INTEIRO", "LITERAL_REAL"):
            self._avancar()
            return self._no("Literal", _pos(token), _fim(token),
                            categoria="inteiro" if token["tipo"] == "LITERAL_INTEIRO" else "real", lexema=token["lexema"])
        if token["lexema"] == "(":
            self._avancar()
            self._entrar(token)
            try:
                expressao = self._expressao()
                fim = self._esperar(")", "Era esperado ')' para fechar a expressão entre parênteses.")
                # Intervalo interno de agrupamento: preserva posições das folhas,
                # mas permite ao pai abranger os parênteses sem criar nó concreto.
                return _No(expressao.dados, _pos(token), _fim(fim), expressao.altura)
            finally:
                self.profundidade -= 1
        raise _ErroSintatico(self._diagnostico(
            OPERANDOS, "Era esperado um operando: identificador, número ou expressão entre parênteses, com sinal opcional."))


def analisar_sintatico(tokens, codigo):
    """Recebe somente tokens válidos do scanner; retorna AST completa ou erros."""
    parser = _Parser(tokens, codigo)
    ast = None
    try:
        ast = parser.programa()
    except _ErroSintatico as erro:
        parser.erros.append(erro.diagnostico)
    sucesso = not parser.erros
    return {"estado": "sucesso" if sucesso else "erro", "sucesso": sucesso,
            "ast": ast if sucesso else None, "erros": parser.erros}
