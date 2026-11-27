/* Mini-C — Etapa 5: tokens, AST, semântica e modos visuais. Sem dependências. */
(function (global) {
  "use strict";
  var URL_API = "/api/analisar";
  var CATEGORIAS = {
    PALAVRA_RESERVADA: "Palavra reservada", IDENTIFICADOR: "Identificador",
    LITERAL_INTEIRO: "Literal inteiro", LITERAL_REAL: "Literal real",
    OPERADOR: "Operador", DELIMITADOR: "Delimitador"
  };
  var MSG = {
    vazio: "Informe um código-fonte antes de solicitar a análise.",
    espacos: "O código informado contém apenas espaços em branco. Digite um programa para analisar.",
    comunicacao: "Não foi possível comunicar com o servidor. Verifique a conexão e tente novamente.",
    inesperado: "Ocorreu um erro inesperado. Tente novamente.",
    sucesso: "Análise léxica concluída sem erros."
  };
  var REGRAS = {
    Programa: "programa = item, { item }, EOF",
    Declaracao: "declaracao = tipo, IDENTIFICADOR, [ '=', expressao ], ';'",
    Atribuicao: "atribuicao = IDENTIFICADOR, '=', expressao, ';'",
    Bloco: "bloco = '{', { item }, '}'",
    Se: "condicional = 'if', '(', expressao, ')', bloco, [ 'else', bloco ]",
    Binario: "Expressão binária: dois operandos, com precedência e associação à esquerda.",
    Unario: "unaria = ( '+' | '-' ), unaria | primaria",
    Identificador: "primaria = IDENTIFICADOR (ou alvo de atribuição)",
    Literal: "primaria = LITERAL_INTEIRO | LITERAL_REAL"
  };
  var REGRAS_SEMANTICAS = {
    IDENTIFICADOR_NAO_DECLARADO: "Declaração antes do uso",
    REDECLARACAO_NO_ESCOPO: "Uma declaração por nome no mesmo escopo",
    TIPOS_INCOMPATIVEIS: "Compatibilidade de tipos na atribuição",
    OPERANDOS_NAO_NUMERICOS: "Operandos aritméticos numéricos",
    TIPOS_NAO_COMPARAVEIS: "Tipos comparáveis",
    CONDICAO_NAO_BOOLEANA: "Condição booleana no if",
    VARIAVEL_NAO_INICIALIZADA: "Inicialização antes da leitura"
  };

  function resolverNo(ast, caminho) {
    if (typeof caminho !== "string" || (caminho !== "" && !caminho.startsWith("/"))) return null;
    var partes = caminho === "" ? [] : caminho.slice(1).split("/");
    var no = ast;
    for (var i = 0; i < partes.length; i++) {
      if (!no || !Object.hasOwn(no, partes[i]) || ["__proto__", "constructor", "prototype"].includes(partes[i])) return null;
      no = no[partes[i]];
    }
    return no && Object.hasOwn(REGRAS, no.tipo) ? no : null;
  }

  function semanticaValida(dados, codigo) {
    if (!Object.hasOwn(dados, "semantica")) return true; // respostas antigas continuam legíveis
    var s = dados.semantica, sintatica = dados.sintatica;
    if (!s || !sintatica || !Array.isArray(s.tabelaSimbolos) || !Array.isArray(s.escopos) || !Array.isArray(s.erros)) return false;
    if (sintatica.sucesso !== true) return s.estado === "nao_executada" && s.sucesso === null &&
      s.motivo === (dados.sucesso ? "erros_sintaticos" : "erros_lexicos") &&
      s.tabelaSimbolos.length === 0 && s.escopos.length === 0 && s.erros.length === 0;
    if (!["sucesso", "erro"].includes(s.estado) || s.sucesso !== (s.estado === "sucesso") || s.sucesso !== (s.erros.length === 0) ||
      s.tabelaSimbolos.length > 2000 || !s.escopos.length || s.escopos.length > 2000 || s.erros.length > 2000) return false;
    var linhas = codigo.replace(/\r\n?/g, "\n").split("\n").map(function (l) { return Array.from(l).length; });
    function pos(p) {
      return p && Number.isInteger(p.linha) && p.linha > 0 && p.linha <= linhas.length &&
        Number.isInteger(p.coluna) && p.coluna > 0 && p.coluna <= linhas[p.linha - 1] + 1;
    }
    function ordem(a, b) { return a.linha < b.linha || (a.linha === b.linha && a.coluna <= b.coluna); }
    function intervalo(inicio, fim, no) {
      return no && pos(inicio) && pos(fim) && ordem(inicio, fim) &&
        !(inicio.linha === fim.linha && inicio.coluna === fim.coluna) && ordem(no.inicio, inicio) && ordem(fim, no.fim);
    }
    var escopos = new Set(), ids = new Set(), ast = sintatica.ast;
    for (var e of s.escopos) {
      if (!e || typeof e.id !== "string" || escopos.has(e.id) || typeof e.nome !== "string") return false;
      var noEscopo = resolverNo(ast, e.noAst);
      if (!noEscopo || !intervalo(e.inicio, e.fim, noEscopo)) return false;
      if (escopos.size === 0 ? e.pai !== null || e.id !== "E0" || e.noAst !== "" : !escopos.has(e.pai) || noEscopo.tipo !== "Bloco") return false;
      escopos.add(e.id);
    }
    var totalReferencias = 0;
    for (var simbolo of s.tabelaSimbolos) {
      if (!simbolo || typeof simbolo.id !== "string" || ids.has(simbolo.id) || !escopos.has(simbolo.escopo) ||
        typeof simbolo.nome !== "string" || !["int", "float"].includes(simbolo.tipo) || typeof simbolo.inicializado !== "boolean" ||
        (simbolo.sombreia !== null && !ids.has(simbolo.sombreia)) || !Array.isArray(simbolo.referencias)) return false;
      var decl = resolverNo(ast, simbolo.noAst);
      if (!decl || decl.tipo !== "Declaracao" || decl.nome !== simbolo.nome || decl.tipoDado !== simbolo.tipo || !intervalo(simbolo, simbolo.fim, decl)) return false;
      ids.add(simbolo.id);
      for (var ref of simbolo.referencias) {
        var noRef = ref && resolverNo(ast, ref.noAst);
        if (++totalReferencias > 2000 || !noRef || noRef.tipo !== "Identificador" || noRef.nome !== simbolo.nome ||
          !["leitura", "atribuicao"].includes(ref.contexto) || !intervalo(ref, ref.fim, noRef)) return false;
      }
    }
    return s.erros.every(function (erro) {
      var no = erro && resolverNo(ast, erro.noAst);
      return erro && erro.tipo === "ERRO_SEMANTICO" && Object.hasOwn(REGRAS_SEMANTICAS, erro.regra) &&
        typeof erro.lexema === "string" && typeof erro.mensagem === "string" && typeof erro.sugestao === "string" &&
        (erro.simboloId === null || ids.has(erro.simboloId)) && intervalo(erro, erro.fim, no);
    });
  }

  function filhosAST(no) {
    if (no.tipo === "Programa" || no.tipo === "Bloco") {
      return no.comandos.map(function (n, i) { return ["Comando " + (i + 1), n, "comandos/" + i]; });
    }
    var campos = {
      Declaracao: [["Inicializador", "inicializador"]],
      Atribuicao: [["Alvo", "alvo"], ["Valor", "valor"]],
      Se: [["Condição", "condicao"], ["Então", "entao"], ["Senão", "senao"]],
      Binario: [["Esquerda", "esquerda"], ["Direita", "direita"]],
      Unario: [["Operando", "operando"]]
    };
    return (campos[no.tipo] || []).filter(function (c) { return no[c[1]] !== null; })
      .map(function (c) { return [c[0], no[c[1]], c[1]]; });
  }

  function astValida(ast, codigo) {
    var linhas = codigo.replace(/\r\n?/g, "\n").split("\n").map(function (l) { return Array.from(l).length; });
    function pos(p) {
      return p && Number.isInteger(p.linha) && p.linha > 0 && p.linha <= linhas.length &&
        Number.isInteger(p.coluna) && p.coluna > 0 && p.coluna <= linhas[p.linha - 1] + 1;
    }
    if (!ast || ast.tipo !== "Programa") return false;
    var pendentes = [[ast, 1]], total = 0;
    while (pendentes.length) {
      var entrada = pendentes.pop(), n = entrada[0], altura = entrada[1];
      if (++total > 2000 || altura > 128 || !n || !Object.hasOwn(REGRAS, n.tipo) || !pos(n.inicio) || !pos(n.fim) ||
        n.fim.linha < n.inicio.linha || (n.fim.linha === n.inicio.linha && n.fim.coluna <= n.inicio.coluna)) return false;
      if ((n.tipo === "Programa" || n.tipo === "Bloco") && (!Array.isArray(n.comandos) || (n.tipo === "Programa" && !n.comandos.length))) return false;
      if (n.tipo === "Declaracao" && (!["int", "float"].includes(n.tipoDado) || typeof n.nome !== "string" || n.inicializador === undefined)) return false;
      if (n.tipo === "Identificador" && typeof n.nome !== "string") return false;
      if (n.tipo === "Literal" && (typeof n.lexema !== "string" || !["inteiro", "real"].includes(n.categoria))) return false;
      if (n.tipo === "Binario" && !["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="].includes(n.operador)) return false;
      if (n.tipo === "Unario" && !["+", "-"].includes(n.operador)) return false;
      if (n.tipo === "Se" && (!n.entao || n.entao.tipo !== "Bloco" || (n.senao !== null && (!n.senao || n.senao.tipo !== "Bloco")))) return false;
      if (n.tipo === "Atribuicao" && (!n.alvo || n.alvo.tipo !== "Identificador")) return false;
      // Filhos obrigatórios não podem desaparecer como null.
      var obrigatorios = { Atribuicao: ["alvo", "valor"], Se: ["condicao", "entao"], Binario: ["esquerda", "direita"], Unario: ["operando"] };
      if ((obrigatorios[n.tipo] || []).some(function (c) { return !n[c]; })) return false;
      var filhos = filhosAST(n);
      for (var i = 0; i < filhos.length; i++) pendentes.push([filhos[i][1], altura + 1]);
    }
    return true;
  }

  function sintaticaValida(dados, codigo) {
    if (!Object.hasOwn(dados, "sintatica")) return true; // compatibilidade com servidor da Etapa 3
    var s = dados.sintatica;
    if (!s || !Array.isArray(s.erros)) return false;
    if (!dados.sucesso) return s.estado === "nao_executada" && s.sucesso === null && s.motivo === "erros_lexicos" && s.ast === null && !s.erros.length;
    if (s.estado === "sucesso") return s.sucesso === true && !s.erros.length && astValida(s.ast, codigo);
    return s.estado === "erro" && s.sucesso === false && s.ast === null && s.erros.length > 0 && s.erros.every(function (e) {
      return e && e.tipo === "ERRO_SINTATICO" && Number.isInteger(e.linha) && e.linha > 0 &&
        Number.isInteger(e.coluna) && e.coluna > 0 && typeof e.lexema === "string" && typeof e.mensagem === "string" &&
        typeof e.encontrado === "string" && Array.isArray(e.esperado) && e.esperado.length && e.esperado.every(function (x) { return typeof x === "string"; });
    });
  }

  function validarLocalmente(codigo) {
    if (typeof codigo !== "string" || codigo === "") return MSG.vazio;
    if (codigo.trim() === "") return MSG.espacos;
    return null;
  }

  function respostaLexicaValida(dados) {
    function posicao(item) {
      return item && typeof item.lexema === "string" && item.lexema.length > 0 &&
        Number.isInteger(item.linha) && item.linha > 0 && Number.isInteger(item.coluna) && item.coluna > 0;
    }
    return dados && dados.recebido === true && typeof dados.sucesso === "boolean" &&
      Array.isArray(dados.tokens) && Array.isArray(dados.erros) &&
      dados.sucesso === (dados.erros.length === 0) &&
      dados.tokens.every(function (t) { return posicao(t) && Object.hasOwn(CATEGORIAS, t.tipo); }) &&
      dados.erros.every(function (e) { return posicao(e) && e.tipo === "ERRO_LEXICO" && typeof e.mensagem === "string"; });
  }

  async function enviarCodigo(codigo, fetchFn, url) {
    var resp;
    var controlador = typeof AbortController !== "undefined" ? new AbortController() : null;
    var temporizador = controlador ? setTimeout(function () { controlador.abort(); }, 8000) : null;
    try {
      resp = await fetchFn(url || URL_API, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ codigo: codigo }), signal: controlador ? controlador.signal : undefined
      });
      if (resp.status === 502 || resp.status === 503 || resp.status === 504) {
        return { tipo: "comunicacao", mensagem: MSG.comunicacao, dados: null };
      }
      var dados;
      try { dados = await resp.json(); }
      catch (e) { return { tipo: "servidor", mensagem: MSG.inesperado, dados: null }; }
      if (resp.status === 200 && respostaLexicaValida(dados) && sintaticaValida(dados, codigo) && semanticaValida(dados, codigo)) {
        var tipo = dados.sucesso ? "sucesso" : "lexico";
        var mensagem = dados.mensagem || (dados.sucesso ? MSG.sucesso : "Análise léxica concluída com erros.");
        if (dados.sintatica && dados.sintatica.estado === "erro") {
          tipo = "sintatico";
          mensagem = "Análise léxica concluída sem erros. A análise sintática encontrou erros.";
        } else if (dados.sintatica && dados.sintatica.estado === "sucesso") {
          mensagem = "Análises léxica e sintática concluídas sem erros.";
        }
        if (dados.semantica && dados.semantica.estado === "erro") {
          tipo = "semantico";
          mensagem = "Análises léxica e sintática sem erros. A análise semântica encontrou regras violadas.";
        } else if (dados.semantica && dados.semantica.estado === "sucesso") {
          mensagem = "Análises léxica, sintática e semântica concluídas sem erros.";
        }
        return { tipo: tipo, mensagem: mensagem, dados: dados };
      }
      if (resp.status >= 400 && resp.status < 500 && dados && typeof dados.mensagem === "string") {
        return { tipo: "entrada", mensagem: dados.mensagem, dados: null };
      }
      return { tipo: "servidor", mensagem: MSG.inesperado, dados: null };
    } catch (e) {
      return { tipo: "comunicacao", mensagem: MSG.comunicacao, dados: null };
    } finally {
      if (temporizador) clearTimeout(temporizador);
    }
  }

  function iniciar(doc, win) {
    var campo = doc.getElementById("codigo"), seletor = doc.getElementById("exemplos");
    var botao = doc.getElementById("btn-analisar"), saida = doc.getElementById("resultado");
    var revisao = 0;
    var visual = doc.getElementById("modo-visual");
    var modos = { padrao: "Padrão", "sem-cores": "Sem cores: padrões e rótulos ativos", contraste: "Alto contraste ativo" };
    function aplicarVisual(modo, salvar) {
      if (!Object.hasOwn(modos, modo)) modo = "padrao";
      doc.documentElement.dataset.visual = modo;
      if (visual) visual.value = modo;
      var avisoVisual = doc.getElementById("estado-visual");
      if (avisoVisual) avisoVisual.textContent = modos[modo] + ". Estados e categorias também são identificados por texto.";
      if (salvar) { try { win.localStorage.setItem("mini-c.visual", modo); } catch (e) { /* modo continua funcional sem persistência */ } }
    }
    var salvo = "padrao";
    try { salvo = win.localStorage.getItem("mini-c.visual") || "padrao"; } catch (e) { /* armazenamento indisponível */ }
    aplicarVisual(salvo, false);
    if (visual) visual.addEventListener("change", function () { aplicarVisual(visual.value, true); });
    function el(tag, texto, classe) {
      var n = doc.createElement(tag);
      if (texto !== undefined) n.textContent = texto;
      if (classe) n.className = classe;
      return n;
    }
    function limpar(mensagem) {
      saida.textContent = "";
      saida.appendChild(el("p", mensagem || "Os resultados da análise aparecerão aqui.", "dica"));
    }
    function mostrarSintatica(s, selecionar) {
      var painel = el("section", undefined, "painel-sintatica");
      painel.setAttribute("aria-labelledby", "titulo-sintatica");
      var titulo = el("h3", "Análise sintática e AST"); titulo.id = "titulo-sintatica";
      painel.appendChild(titulo);
      var estado = el("p", undefined, "estado-analise"); estado.id = "estado-sintatica";
      painel.appendChild(estado); saida.appendChild(painel);
      if (!s) { estado.textContent = "Sintática: indisponível nesta resposta. Atualize o servidor para a Etapa 4."; return; }
      if (s.estado === "nao_executada") {
        estado.textContent = "Sintática: não executada, pois existem erros léxicos. Corrija-os e analise novamente.";
        return;
      }
      if (s.estado === "erro") {
        estado.textContent = "Sintática: com erros. A AST não é apresentada enquanto houver erros.";
        var erros = el("ul", undefined, "erros-sintaticos"); erros.id = "erros-sintaticos";
        s.erros.forEach(function (e) {
          var item = el("li");
          item.append(el("strong", "Linha " + e.linha + ", coluna " + e.coluna + ": "), el("span", e.mensagem),
            el("p", "Esperado: " + e.esperado.join(", ") + ". Encontrado: " + (e.lexema ? "“" + e.lexema + "” (" + e.encontrado + ")" : "fim do código (EOF)") + ".", "nota"));
          erros.appendChild(item);
        });
        painel.appendChild(erros); return;
      }
      estado.textContent = "Sintática: sem erros. A AST representa a estrutura reconhecida.";
      painel.appendChild(el("p", "Tokens formam uma sequência. A árvore sintática abstrata (AST) organiza as construções e omite pontuação e regras intermediárias. A árvore de derivação mostraria essas regras; ela não é exibida aqui. A navegação abaixo explora a AST pronta.", "nota"));
      var controles = el("div", undefined, "controles-ast");
      var expandir = el("button", "Expandir tudo"), recolher = el("button", "Recolher tudo"), exportar = el("button", "Baixar AST em JSON");
      expandir.id = "ast-expandir"; recolher.id = "ast-recolher"; exportar.id = "ast-exportar";
      [expandir, recolher, exportar].forEach(function (b) { b.type = "button"; controles.appendChild(b); });
      painel.appendChild(controles);
      var posicao = el("p", "Abra um nó e use Localizar para destacar seu trecho no código acima. Fim é exclusivo: a posição seguinte ao último caractere.", "nota");
      posicao.id = "posicao-ast"; posicao.setAttribute("aria-live", "polite"); painel.appendChild(posicao);
      var verFonte = el("a", "Ver trecho destacado no código"); verFonte.href = "#codigo-analisado"; painel.appendChild(verFonte);
      var arvore = el("div", undefined, "arvore-ast"); arvore.id = "arvore-ast";
      arvore.tabIndex = 0; arvore.setAttribute("role", "region"); arvore.setAttribute("aria-label", "AST navegável; abra nós com Enter ou Espaço e role dentro da árvore");
      function rotulo(no) {
        var nomes = { Declaracao: "Declaração", Atribuicao: "Atribuição", Se: "Condicional if", Binario: "Operação binária", Unario: "Operação unária" };
        var texto = nomes[no.tipo] || no.tipo;
        if (no.tipo === "Declaracao") texto += " · " + no.tipoDado + " " + no.nome;
        if (no.tipo === "Identificador") texto += " · " + no.nome;
        if (no.tipo === "Literal") texto += " " + no.categoria + " · " + no.lexema;
        if (no.operador) texto += " · " + no.operador;
        return texto;
      }
      function desenhar(no, relacao, nivel, caminho) {
        var detalhe = el("details", undefined, "ast-no ast-" + no.tipo.toLowerCase());
        detalhe.dataset.tipo = no.tipo; detalhe.dataset.noAst = caminho; detalhe.open = nivel < 2;
        var nome = rotulo(no);
        detalhe.appendChild(el("summary", (relacao ? relacao + ": " : "") + nome));
        var informacoes = el("div", undefined, "ast-informacoes");
        var intervalo = "linha " + no.inicio.linha + ", coluna " + no.inicio.coluna + " até linha " + no.fim.linha + ", coluna " + no.fim.coluna + " (fim exclusivo)";
        informacoes.appendChild(el("p", intervalo, "nota"));
        informacoes.appendChild(el("p", "Regra / leitura: " + REGRAS[no.tipo], "nota"));
        var localizar = el("button", "Localizar " + nome, "ast-localizar");
        localizar.type = "button"; localizar.setAttribute("aria-pressed", "false");
        localizar.addEventListener("click", function () {
          selecionar(no, localizar, "AST", caminho);
          posicao.textContent = nome + " selecionado: " + intervalo + ". Use Destacar token atual para voltar aos tokens.";
        });
        informacoes.appendChild(localizar); detalhe.appendChild(informacoes);
        var filhos = filhosAST(no);
        if (filhos.length) {
          var lista = el("ul", undefined, "ast-filhos");
          filhos.forEach(function (f) { var item = el("li"); item.appendChild(desenhar(f[1], f[0], nivel + 1, caminho + "/" + f[2])); lista.appendChild(item); });
          detalhe.appendChild(lista);
        }
        return detalhe;
      }
      arvore.appendChild(desenhar(s.ast, "", 0, "")); painel.appendChild(arvore);
      expandir.addEventListener("click", function () { arvore.querySelectorAll("details").forEach(function (n) { n.open = true; }); });
      recolher.addEventListener("click", function () { arvore.querySelectorAll("details").forEach(function (n) { n.open = false; }); });
      exportar.addEventListener("click", function () {
        var url;
        try {
          url = win.URL.createObjectURL(new win.Blob([JSON.stringify(s.ast, null, 2)], { type: "application/json;charset=utf-8" }));
          var link = el("a"); link.href = url; link.download = "mini-c-ast.json";
          doc.body.appendChild(link); link.click(); link.remove();
          win.setTimeout(function () { win.URL.revokeObjectURL(url); }, 1000);
        } catch (e) {
          if (url) win.URL.revokeObjectURL(url);
          posicao.textContent = "Não foi possível baixar a AST neste navegador. Tente novamente em um navegador atualizado.";
        }
      });
    }
    function mostrarSemantica(s, selecionar) {
      var painel = el("section", undefined, "painel-semantica");
      painel.setAttribute("aria-labelledby", "titulo-semantica");
      var titulo = el("h3", "Análise semântica e tabela de símbolos"); titulo.id = "titulo-semantica";
      var estado = el("p", undefined, "estado-analise"); estado.id = "estado-semantica";
      painel.append(titulo, estado); saida.appendChild(painel);
      if (!s) { estado.textContent = "[—] Semântica: indisponível nesta resposta. Atualize o servidor para a Etapa 5."; return; }
      if (s.estado === "nao_executada") {
        estado.textContent = "[—] Semântica: não executada. Corrija os erros " + (s.motivo === "erros_lexicos" ? "léxicos" : "sintáticos") + " para analisar as regras semânticas.";
        return;
      }
      estado.textContent = s.sucesso ? "[OK] Semântica: sem erros nas regras do subconjunto." : "[!] Semântica: com erros. A AST reconhecida continua disponível.";
      var posicao = el("p", "Selecione um símbolo, referência ou erro para destacar seu trecho no código e a construção na AST.", "nota");
      posicao.id = "selecao-semantica"; posicao.setAttribute("aria-live", "polite"); painel.appendChild(posicao);
      var verFonte = el("a", "Ver trecho destacado no código"); verFonte.href = "#codigo-analisado"; painel.appendChild(verFonte);
      function localizar(item, botaoNo, rotulo) {
        selecionar({ inicio: { linha: item.linha, coluna: item.coluna }, fim: item.fim }, botaoNo, rotulo, item.noAst);
        posicao.textContent = rotulo + ": linha " + item.linha + ", coluna " + item.coluna + " até linha " + item.fim.linha + ", coluna " + item.fim.coluna + " (fim exclusivo). O nó relacionado está marcado na AST.";
      }
      if (s.erros.length) {
        var erros = el("ul", undefined, "erros-semanticos"); erros.id = "erros-semanticos";
        s.erros.forEach(function (erro) {
          var item = el("li"); item.dataset.regra = erro.regra;
          item.append(el("strong", "Erro semântico — linha " + erro.linha + ", coluna " + erro.coluna + ": "),
            el("span", erro.mensagem), el("p", "Regra: " + REGRAS_SEMANTICAS[erro.regra] + " (" + erro.regra + ").", "regra-semantica"),
            el("p", "Sugestão: " + erro.sugestao));
          var botaoErro = el("button", "Localizar erro na linha " + erro.linha + ", coluna " + erro.coluna, "localizar-semantica");
          botaoErro.type = "button"; botaoErro.setAttribute("aria-pressed", "false");
          botaoErro.addEventListener("click", function () { localizar(erro, botaoErro, "Erro semântico"); });
          item.appendChild(botaoErro); erros.appendChild(item);
        });
        painel.appendChild(erros);
        painel.appendChild(el("p", "A tabela mostra as declarações reconhecidas durante uma análise com erros. Corrija os diagnósticos antes de considerar o programa semanticamente válido.", "nota"));
      }
      painel.appendChild(el("p", "Inicialização garantida indica o estado ao final do escopo que declarou a variável. Uma declaração sem leitura pode ser válida mesmo sem inicialização; após if/else, a garantia exige os dois caminhos. A tabela representa a análise estática, sem calcular valores.", "nota"));
      var label = el("label", "Filtrar tabela por escopo"); label.htmlFor = "filtro-escopo";
      var filtro = el("select"); filtro.id = "filtro-escopo";
      var todos = el("option", "Todos os escopos"); todos.value = ""; filtro.appendChild(todos);
      var nomesEscopos = new Map();
      s.escopos.forEach(function (e) {
        var nome = e.id + " — " + e.nome + (e.pai ? " (externo: " + e.pai + ")" : "");
        nomesEscopos.set(e.id, nome);
        var opcao = el("option", nome); opcao.value = e.id; filtro.appendChild(opcao);
      });
      painel.append(label, filtro);
      var contagem = el("p", undefined, "nota"); contagem.id = "contagem-simbolos";
      contagem.setAttribute("aria-live", "polite"); painel.appendChild(contagem);
      var regiao = el("div", undefined, "tabela-responsiva"); regiao.tabIndex = 0; regiao.setAttribute("role", "region");
      regiao.setAttribute("aria-label", "Tabela de símbolos; role horizontalmente em telas pequenas");
      var tabela = el("table"); tabela.id = "tabela-simbolos";
      tabela.appendChild(el("caption", "Variáveis declaradas, escopos e referências"));
      var cabecalho = el("thead"), linha = el("tr");
      ["Nome", "Tipo", "Escopo", "Declaração", "Inicialização garantida", "Sombreia", "Localizar"].forEach(function (texto) {
        var th = el("th", texto); th.scope = "col"; linha.appendChild(th);
      });
      cabecalho.appendChild(linha); tabela.appendChild(cabecalho);
      var corpo = el("tbody"); tabela.appendChild(corpo); regiao.appendChild(tabela); painel.appendChild(regiao);
      function desenharTabela() {
        corpo.textContent = "";
        var simbolos = s.tabelaSimbolos.filter(function (item) { return !filtro.value || item.escopo === filtro.value; });
        contagem.textContent = simbolos.length + " de " + s.tabelaSimbolos.length + " declarações exibidas. " + (!s.tabelaSimbolos.length ? "Nenhuma variável declarada neste programa." : "Nomes iguais podem pertencer a escopos diferentes.");
        simbolos.forEach(function (simbolo) {
          var tr = el("tr"); tr.dataset.simboloId = simbolo.id;
          tr.append(el("td", simbolo.nome), el("td", simbolo.tipo), el("td", nomesEscopos.get(simbolo.escopo)),
            el("td", "Linha " + simbolo.linha + ", coluna " + simbolo.coluna),
            el("td", simbolo.inicializado ? "Sim — garantida" : "Não garantida"), el("td", simbolo.sombreia || "Nenhum"));
          var acoes = el("td");
          var declaracao = el("button", "Localizar declaração de " + simbolo.nome + " (" + simbolo.escopo + ")", "localizar-simbolo");
          declaracao.type = "button"; declaracao.setAttribute("aria-pressed", "false");
          declaracao.addEventListener("click", function () { localizar(simbolo, declaracao, "Símbolo " + simbolo.nome + " em " + simbolo.escopo); });
          acoes.appendChild(declaracao);
          if (simbolo.referencias.length) {
            var detalhes = el("details", undefined, "referencias-simbolo");
            detalhes.appendChild(el("summary", "Referências (" + simbolo.referencias.length + ")"));
            simbolo.referencias.forEach(function (ref) {
              var texto = (ref.contexto === "leitura" ? "Leitura" : "Atribuição") + " de " + simbolo.nome + " — linha " + ref.linha + ", coluna " + ref.coluna;
              var b = el("button", texto, "localizar-referencia"); b.type = "button"; b.setAttribute("aria-pressed", "false");
              b.addEventListener("click", function () { localizar(ref, b, texto); });
              detalhes.appendChild(b);
            });
            acoes.appendChild(detalhes);
          }
          tr.appendChild(acoes); corpo.appendChild(tr);
        });
      }
      filtro.addEventListener("change", desenharTabela); desenharTabela();
    }

    function mostrar(tipo, texto, dados, codigo) {
      saida.textContent = "";
      var aviso = el("p", texto, "msg " + tipo);
      aviso.setAttribute("role", "status");
      saida.appendChild(aviso);
      if (!dados) return;
      saida.appendChild(el("p", "Caracteres: " + dados.total_caracteres + " · Linhas: " + dados.total_linhas +
        " · Tokens: " + dados.tokens.length + " · Erros léxicos: " + dados.erros.length, "detalhes"));
      var estadoLexico = el("p", (dados.sucesso ? "[OK] " : "[!] ") + "Léxica: " + (dados.sucesso ? "sem erros." : "com erros."), "estado-analise");
      estadoLexico.id = "estado-lexico"; saida.appendChild(estadoLexico);
      saida.appendChild(el("p", "Reconhecer tokens não comprova que o programa esteja correto. O parser verifica a organização gramatical; a semântica da Etapa 5 verifica declarações, tipos e inicialização. A execução do programa e a representação semântica ampliada ficam para etapas seguintes.", "nota"));
      if (dados.erros.length) {
        saida.appendChild(el("h3", "Erros léxicos"));
        var lista = el("ul", undefined, "erros-lexicos");
        lista.id = "erros-lexicos";
        dados.erros.forEach(function (erro) {
          var item = el("li");
          item.appendChild(el("strong", "Linha " + erro.linha + ", coluna " + erro.coluna + ": "));
          item.appendChild(el("span", erro.mensagem));
          item.appendChild(el("code", erro.lexema, "trecho-erro"));
          lista.appendChild(item);
        });
        saida.appendChild(lista);
      }
      var contagem = el("ul", undefined, "contagem");
      contagem.id = "contagem-tokens";
      Object.keys(CATEGORIAS).forEach(function (tipoToken) {
        var n = dados.tokens.filter(function (t) { return t.tipo === tipoToken; }).length;
        if (n) contagem.appendChild(el("li", CATEGORIAS[tipoToken] + ": " + n));
      });
      if (dados.tokens.length) {
        saida.appendChild(el("h3", "Contagem por categoria"));
        saida.appendChild(contagem);
      }

      saida.appendChild(el("h3", "Código analisado e sequência de tokens"));
      saida.appendChild(el("p", "As cores indicam categorias; a tabela também informa cada tipo por escrito. Navegue pelos tokens para localizar seus lexemas no código. Espaços e comentários são ignorados pelo scanner.", "nota"));
      var fonte = codigo.replace(/\r\n?/g, "\n");
      var caracteres = Array.from(fonte), inicios = [0];
      caracteres.forEach(function (c, i) { if (c === "\n") inicios.push(i + 1); });
      var pre = el("pre", undefined, "codigo-analisado");
      pre.id = "codigo-analisado";
      pre.tabIndex = 0;
      pre.setAttribute("aria-label", "Código enviado para esta análise");
      saida.appendChild(pre);
      var passo = 0;
      var controles = el("div", undefined, "controles-passo");
      var anterior = el("button", "Token anterior"), proximo = el("button", "Próximo token"), voltarToken = el("button", "Destacar token atual");
      anterior.id = "token-anterior"; proximo.id = "token-proximo";
      voltarToken.id = "token-destacar";
      anterior.type = proximo.type = voltarToken.type = "button";
      var posicao = el("p"); posicao.id = "passo-token";
      posicao.setAttribute("aria-live", "polite");
      controles.append(anterior, proximo, voltarToken, posicao);
      if (dados.tokens.length) saida.appendChild(controles);
      else saida.appendChild(el("p", "Nenhum token reconhecido. Comentários não formam comandos: sozinhos, não compõem um programa sintaticamente válido."));
      var linhas = [];
      var selecaoAST = null, botaoSelecionado = null;
      function atualizarPasso() {
        pre.textContent = "";
        if (selecaoAST) {
          var inicioNo = inicios[selecaoAST.inicio.linha - 1] + selecaoAST.inicio.coluna - 1;
          var fimNo = inicios[selecaoAST.fim.linha - 1] + selecaoAST.fim.coluna - 1;
          pre.append(doc.createTextNode(caracteres.slice(0, inicioNo).join("")),
            el("mark", caracteres.slice(inicioNo, fimNo).join(""), "trecho-ast"),
            doc.createTextNode(caracteres.slice(fimNo).join("")));
          posicao.textContent = "Destaque de " + (selecaoAST.origem || "AST") + " ativo. Use Destacar token atual ou navegue para voltar à sequência de tokens.";
          linhas.forEach(function (l) { l.classList.remove("token-atual"); });
          return;
        }
        var cursor = 0;
        dados.tokens.forEach(function (t, i) {
          var inicio = inicios[t.linha - 1] + t.coluna - 1;
          pre.appendChild(doc.createTextNode(caracteres.slice(cursor, inicio).join("")));
          var n = el(i === passo ? "mark" : "span", t.lexema, "token token-" + t.tipo.toLowerCase());
          n.title = CATEGORIAS[t.tipo] + " — linha " + t.linha + ", coluna " + t.coluna;
          pre.appendChild(n);
          cursor = inicio + Array.from(t.lexema).length;
          if (linhas[i]) linhas[i].classList.toggle("token-atual", i === passo);
        });
        pre.appendChild(doc.createTextNode(caracteres.slice(cursor).join("")));
        anterior.disabled = passo === 0;
        proximo.disabled = passo >= dados.tokens.length - 1;
        if (dados.tokens.length) {
          var t = dados.tokens[passo];
          posicao.textContent = "Token " + (passo + 1) + " de " + dados.tokens.length + ": " +
            CATEGORIAS[t.tipo] + " “" + t.lexema + "” — linha " + t.linha + ", coluna " + t.coluna + ".";
        }
      }
      function voltarAosTokens() {
        selecaoAST = null;
        if (botaoSelecionado) { botaoSelecionado.setAttribute("aria-pressed", "false"); botaoSelecionado = null; }
        var status = doc.getElementById("posicao-ast");
        if (status) status.textContent = "Destaque por token ativo. Selecione Localizar em um nó para destacar sua construção.";
        saida.querySelectorAll(".ast-relacionado").forEach(function (n) { n.classList.remove("ast-relacionado"); });
      }
      anterior.addEventListener("click", function () { if (passo > 0) { voltarAosTokens(); passo--; atualizarPasso(); } });
      proximo.addEventListener("click", function () { if (passo + 1 < dados.tokens.length) { voltarAosTokens(); passo++; atualizarPasso(); } });
      voltarToken.addEventListener("click", function () { voltarAosTokens(); atualizarPasso(); });

      function selecionarFonte(no, botaoNo, origem, caminho) {
        if (botaoSelecionado) botaoSelecionado.setAttribute("aria-pressed", "false");
        botaoSelecionado = botaoNo; botaoNo.setAttribute("aria-pressed", "true");
        selecaoAST = { inicio: no.inicio, fim: no.fim, origem: origem }; atualizarPasso();
        saida.querySelectorAll(".ast-relacionado").forEach(function (n) { n.classList.remove("ast-relacionado"); });
        var relacionado = Array.from(saida.querySelectorAll(".ast-no")).find(function (n) { return n.dataset.noAst === caminho; });
        if (relacionado) {
          relacionado.classList.add("ast-relacionado");
          for (var pai = relacionado; pai && pai.id !== "arvore-ast"; pai = pai.parentElement) {
            if (pai.tagName === "DETAILS") pai.open = true;
          }
        }
      }
      mostrarSintatica(dados.sintatica, selecionarFonte);
      mostrarSemantica(dados.semantica, selecionarFonte);

      var regiao = el("div", undefined, "tabela-responsiva");
      regiao.tabIndex = 0; regiao.setAttribute("role", "region");
      regiao.setAttribute("aria-label", "Tabela de tokens; role horizontalmente em telas pequenas");
      var tabela = el("table"); tabela.id = "tabela-tokens";
      tabela.appendChild(el("caption", "Tokens reconhecidos, na ordem de leitura"));
      var cabecalho = el("thead"), tr = el("tr");
      ["Tipo", "Lexema", "Linha", "Coluna"].forEach(function (s) {
        var th = el("th", s); th.scope = "col"; tr.appendChild(th);
      });
      cabecalho.appendChild(tr); tabela.appendChild(cabecalho);
      var corpo = el("tbody");
      dados.tokens.forEach(function (t) {
        var linha = el("tr");
        var tipoCelula = el("td", CATEGORIAS[t.tipo]); tipoCelula.title = t.tipo;
        linha.appendChild(tipoCelula);
        var lexema = el("td"); lexema.appendChild(el("code", t.lexema)); linha.appendChild(lexema);
        linha.append(el("td", t.linha), el("td", t.coluna));
        linhas.push(linha); corpo.appendChild(linha);
      });
      tabela.appendChild(corpo); regiao.appendChild(tabela); saida.appendChild(regiao);
      atualizarPasso();
    }
    campo.addEventListener("input", function () {
      revisao++; seletor.value = "";
      limpar("Código alterado. Analise novamente para atualizar os resultados.");
    });
    seletor.addEventListener("change", function () {
      var opcao = seletor.options[seletor.selectedIndex];
      if (seletor.value && opcao && opcao.dataset.codigo !== undefined) {
        revisao++; campo.value = opcao.dataset.codigo; limpar();
      }
    });
    botao.addEventListener("click", async function () {
      var codigo = campo.value, versao = revisao;
      var erroLocal = validarLocalmente(codigo);
      if (erroLocal) { mostrar("entrada", erroLocal, null); return; }
      botao.disabled = true;
      limpar("Analisando o código…");
      try {
        var r = await enviarCodigo(codigo, win.fetch.bind(win));
        if (versao === revisao) mostrar(r.tipo, r.mensagem, r.dados, codigo);
      } catch (e) {
        if (versao === revisao) mostrar("servidor", MSG.inesperado, null);
      } finally { botao.disabled = false; }
    });
  }
  var api = { MSG: MSG, URL_API: URL_API, validarLocalmente: validarLocalmente, enviarCodigo: enviarCodigo, iniciar: iniciar };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else {
    global.CompiladorApp = api;
    document.addEventListener("DOMContentLoaded", function () { iniciar(document, window); });
  }
})(typeof window !== "undefined" ? window : globalThis);
