"""Semântica Mini-C: escopos, tipos e inicialização definida sobre AST válida.

Não altera a AST/tokens nem executa expressões. Regras: docs/semantica.md.
"""

NUMERICOS = {"int", "float"}


def _compativel(destino, origem):
    return destino == origem or (destino == "float" and origem == "int")


class _Analise:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indices = {(t["linha"], t["coluna"]): i for i, t in enumerate(tokens)}
        self.pilha = []
        self.escopos = []
        self.simbolos = []
        self.erros = []

    def _abrir(self, no, caminho, nome=None):
        escopo = {
            "id": f"E{len(self.escopos)}", "nome": nome or f"Bloco {len(self.escopos)}",
            "pai": self.pilha[-1]["escopo"]["id"] if self.pilha else None,
            "inicio": dict(no["inicio"]), "fim": dict(no["fim"]), "noAst": caminho,
        }
        self.escopos.append(escopo)
        self.pilha.append({"escopo": escopo, "nomes": {}})

    def _fechar(self, inicializados):
        quadro = self.pilha.pop()
        for simbolo in quadro["nomes"].values():
            simbolo["inicializado"] = simbolo["id"] in inicializados
            inicializados.discard(simbolo["id"])

    def _buscar(self, nome):
        for quadro in reversed(self.pilha):
            if nome in quadro["nomes"]:
                return quadro["nomes"][nome]
        return None

    def _erro(self, regra, no, caminho, mensagem, sugestao, lexema, simbolo=None, inicio=None, fim=None):
        pos = inicio or no["inicio"]
        self.erros.append({
            "tipo": "ERRO_SEMANTICO", "regra": regra, "lexema": lexema,
            "linha": pos["linha"], "coluna": pos["coluna"],
            "fim": dict(fim or no["fim"]), "noAst": caminho,
            "simboloId": simbolo["id"] if simbolo else None,
            "mensagem": mensagem, "sugestao": sugestao,
        })

    def _referencia(self, simbolo, no, caminho, contexto):
        simbolo["referencias"].append({
            "linha": no["inicio"]["linha"], "coluna": no["inicio"]["coluna"],
            "fim": dict(no["fim"]), "noAst": caminho, "contexto": contexto,
        })

    def _declaracao(self, no, caminho, inicializados):
        # O parser guarda nome como atributo. A posição vem do token original
        # imediatamente posterior ao token int/float, sem refazer o scanner.
        indice = self.indices[(no["inicio"]["linha"], no["inicio"]["coluna"])]
        token = self.tokens[indice + 1]
        inicio = {"linha": token["linha"], "coluna": token["coluna"]}
        fim = {"linha": token["linha"], "coluna": token["coluna"] + len(token["lexema"])}
        nomes = self.pilha[-1]["nomes"]
        if no["nome"] in nomes:
            anterior = nomes[no["nome"]]
            self._erro("REDECLARACAO_NO_ESCOPO", no, caminho,
                       f"A variável '{no['nome']}' já foi declarada neste escopo na linha {anterior['linha']}, coluna {anterior['coluna']}.",
                       "Use outro nome ou aproveite a variável já declarada. Um bloco interno pode declarar um nome que sombreia o externo.",
                       no["nome"], anterior, inicio, fim)
            if no["inicializador"] is not None:
                self._expressao(no["inicializador"], caminho + "/inicializador", inicializados)
            return
        externo = self._buscar(no["nome"])
        simbolo = {
            "id": f"S{len(self.simbolos) + 1}", "nome": no["nome"], "tipo": no["tipoDado"],
            "escopo": self.pilha[-1]["escopo"]["id"], **inicio, "fim": fim, "noAst": caminho,
            "inicializado": False, "sombreia": externo["id"] if externo else None, "referencias": [],
        }
        nomes[no["nome"]] = simbolo
        self.simbolos.append(simbolo)
        if no["inicializador"] is not None:
            tipo = self._expressao(no["inicializador"], caminho + "/inicializador", inicializados)
            if tipo is not None:
                if _compativel(simbolo["tipo"], tipo):
                    inicializados.add(simbolo["id"])
                else:
                    self._incompativel(no, caminho, simbolo, tipo, inicio, fim)

    def _incompativel(self, no, caminho, simbolo, tipo, inicio, fim):
        self._erro("TIPOS_INCOMPATIVEIS", no, caminho,
                   f"A variável '{simbolo['nome']}' tem tipo '{simbolo['tipo']}', mas recebeu uma expressão do tipo '{tipo}'. O Mini-C permite promoção de int para float, sem conversão inversa nem conversão de bool para número.",
                   "Ajuste o tipo da declaração ou a expressão para produzir um tipo compatível. Conversões explícitas não fazem parte deste recorte.",
                   simbolo["nome"], simbolo, inicio, fim)

    def _atribuicao(self, no, caminho, inicializados):
        alvo = no["alvo"]
        simbolo = self._buscar(alvo["nome"])
        if simbolo is None:
            self._erro("IDENTIFICADOR_NAO_DECLARADO", alvo, caminho + "/alvo",
                       f"O identificador '{alvo['nome']}' não foi declarado antes deste uso no escopo atual nem nos escopos externos.",
                       "Declare a variável antes de usá-la e confira se ela está visível neste bloco.", alvo["nome"])
        else:
            self._referencia(simbolo, alvo, caminho + "/alvo", "atribuicao")
        tipo = self._expressao(no["valor"], caminho + "/valor", inicializados)
        if simbolo is not None and tipo is not None:
            if _compativel(simbolo["tipo"], tipo):
                inicializados.add(simbolo["id"])
            else:
                self._incompativel(no, caminho, simbolo, tipo, alvo["inicio"], alvo["fim"])

    def _bloco(self, no, caminho, inicializados):
        self._abrir(no, caminho)
        self._comandos(no["comandos"], caminho, inicializados)
        self._fechar(inicializados)

    def _comandos(self, comandos, caminho, inicializados):
        for i, no in enumerate(comandos):
            pos = f"{caminho}/comandos/{i}"
            if no["tipo"] == "Declaracao":
                self._declaracao(no, pos, inicializados)
            elif no["tipo"] == "Atribuicao":
                self._atribuicao(no, pos, inicializados)
            elif no["tipo"] == "Bloco":
                self._bloco(no, pos, inicializados)
            elif no["tipo"] == "Se":
                tipo = self._expressao(no["condicao"], pos + "/condicao", inicializados)
                if tipo is not None and tipo != "bool":
                    self._erro("CONDICAO_NAO_BOOLEANA", no["condicao"], pos + "/condicao",
                               f"A condição do if tem tipo '{tipo}', mas este Mini-C exige uma comparação de resultado bool.",
                               "Use uma comparação, por exemplo x != 0, para expressar a condição.",
                               no["condicao"].get("nome", no["condicao"].get("lexema", no["condicao"].get("operador", "if"))))
                entao = set(inicializados)
                senao = set(inicializados)
                self._bloco(no["entao"], pos + "/entao", entao)
                if no["senao"] is not None:
                    self._bloco(no["senao"], pos + "/senao", senao)
                inicializados.clear()
                inicializados.update(entao & senao)

    def _expressao(self, no, caminho, inicializados):
        tipo_no = no["tipo"]
        if tipo_no == "Literal":
            return "int" if no["categoria"] == "inteiro" else "float"
        if tipo_no == "Identificador":
            simbolo = self._buscar(no["nome"])
            if simbolo is None:
                self._erro("IDENTIFICADOR_NAO_DECLARADO", no, caminho,
                           f"O identificador '{no['nome']}' não foi declarado antes deste uso no escopo atual nem nos escopos externos.",
                           "Declare a variável antes de usá-la e confira os limites de seu bloco.", no["nome"])
                return None
            self._referencia(simbolo, no, caminho, "leitura")
            if simbolo["id"] not in inicializados:
                self._erro("VARIAVEL_NAO_INICIALIZADA", no, caminho,
                           f"A leitura de '{no['nome']}' ocorre sem uma inicialização garantida neste ponto. A declaração, sozinha, não fornece um valor.",
                           "Inicialize a variável antes da leitura. Se a atribuição estiver em um if, garanta-a nos dois caminhos.", no["nome"], simbolo)
                return None
            return simbolo["tipo"]
        if tipo_no == "Unario":
            tipo = self._expressao(no["operando"], caminho + "/operando", inicializados)
            if tipo is None:
                return None
            if tipo not in NUMERICOS:
                self._erro("OPERANDOS_NAO_NUMERICOS", no, caminho,
                           f"O sinal unário '{no['operador']}' exige um número int ou float, mas recebeu '{tipo}'.",
                           "Aplique o sinal a uma expressão numérica, sem usar uma comparação como número.", no["operador"])
                return None
            return tipo
        esquerda = self._expressao(no["esquerda"], caminho + "/esquerda", inicializados)
        direita = self._expressao(no["direita"], caminho + "/direita", inicializados)
        if esquerda is None or direita is None:
            return None
        operador = no["operador"]
        if operador in ("+", "-", "*", "/"):
            if esquerda not in NUMERICOS or direita not in NUMERICOS:
                self._erro("OPERANDOS_NAO_NUMERICOS", no, caminho,
                           f"A operação '{operador}' exige dois números, mas recebeu '{esquerda}' e '{direita}'.",
                           "Use operandos int ou float; resultados de comparações têm tipo bool.", operador)
                return None
            return "float" if "float" in (esquerda, direita) else "int"
        numericos = esquerda in NUMERICOS and direita in NUMERICOS
        booleanos = operador in ("==", "!=") and esquerda == direita == "bool"
        if not (numericos or booleanos):
            self._erro("TIPOS_NAO_COMPARAVEIS", no, caminho,
                       f"A comparação '{operador}' não aceita os tipos '{esquerda}' e '{direita}' juntos. Relações ordenadas exigem números; igualdade também aceita dois bool.",
                       "Compare dois valores numéricos ou, na igualdade, dois resultados booleanos.", operador)
            return None
        return "bool"


def analisar_semantico(ast, tokens):
    """Recebe AST válida e tokens originais. Posições e ligações são preservadas."""
    analise = _Analise(tokens)
    inicializados = set()
    analise._abrir(ast, "", "Global")
    analise._comandos(ast["comandos"], "", inicializados)
    analise._fechar(inicializados)
    sucesso = not analise.erros
    return {"estado": "sucesso" if sucesso else "erro", "sucesso": sucesso,
            "tabelaSimbolos": analise.simbolos, "escopos": analise.escopos, "erros": analise.erros}
