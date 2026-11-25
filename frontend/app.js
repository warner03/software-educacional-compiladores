/* Mini-C — Etapa 4: tokens, diagnósticos e AST navegável. Sem dependências. */
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

  function filhosAST(no) {
    if (no.tipo === "Programa" || no.tipo === "Bloco") {
      return no.comandos.map(function (n, i) { return ["Comando " + (i + 1), n]; });
    }
    var campos = {
      Declaracao: [["Inicializador", "inicializador"]],
      Atribuicao: [["Alvo", "alvo"], ["Valor", "valor"]],
      Se: [["Condição", "condicao"], ["Então", "entao"], ["Senão", "senao"]],
      Binario: [["Esquerda", "esquerda"], ["Direita", "direita"]],
      Unario: [["Operando", "operando"]]
    };
    return (campos[no.tipo] || []).filter(function (c) { return no[c[1]] !== null; })
      .map(function (c) { return [c[0], no[c[1]]]; });
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
      if (resp.status === 200 && respostaLexicaValida(dados) && sintaticaValida(dados, codigo)) {
        var tipo = dados.sucesso ? "sucesso" : "lexico";
        var mensagem = dados.mensagem || (dados.sucesso ? MSG.sucesso : "Análise léxica concluída com erros.");
        if (dados.sintatica && dados.sintatica.estado === "erro") {
          tipo = "sintatico";
          mensagem = "Análise léxica concluída sem erros. A análise sintática encontrou erros.";
        } else if (dados.sintatica && dados.sintatica.estado === "sucesso") {
          mensagem = "Análises léxica e sintática concluídas sem erros.";
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
      function desenhar(no, relacao, nivel) {
        var detalhe = el("details", undefined, "ast-no ast-" + no.tipo.toLowerCase());
        detalhe.dataset.tipo = no.tipo; detalhe.open = nivel < 2;
        var nome = rotulo(no);
        detalhe.appendChild(el("summary", (relacao ? relacao + ": " : "") + nome));
        var informacoes = el("div", undefined, "ast-informacoes");
        var intervalo = "linha " + no.inicio.linha + ", coluna " + no.inicio.coluna + " até linha " + no.fim.linha + ", coluna " + no.fim.coluna + " (fim exclusivo)";
        informacoes.appendChild(el("p", intervalo, "nota"));
        informacoes.appendChild(el("p", "Regra / leitura: " + REGRAS[no.tipo], "nota"));
        var localizar = el("button", "Localizar " + nome, "ast-localizar");
        localizar.type = "button"; localizar.setAttribute("aria-pressed", "false");
        localizar.addEventListener("click", function () {
          selecionar(no, localizar);
          posicao.textContent = nome + " selecionado: " + intervalo + ". Use Destacar token atual para voltar aos tokens.";
        });
        informacoes.appendChild(localizar); detalhe.appendChild(informacoes);
        var filhos = filhosAST(no);
        if (filhos.length) {
          var lista = el("ul", undefined, "ast-filhos");
          filhos.forEach(function (f) { var item = el("li"); item.appendChild(desenhar(f[1], f[0], nivel + 1)); lista.appendChild(item); });
          detalhe.appendChild(lista);
        }
        return detalhe;
      }
      arvore.appendChild(desenhar(s.ast, "", 0)); painel.appendChild(arvore);
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
    function mostrar(tipo, texto, dados, codigo) {
      saida.textContent = "";
      var aviso = el("p", texto, "msg " + tipo);
      aviso.setAttribute("role", "status");
      saida.appendChild(aviso);
      if (!dados) return;
      saida.appendChild(el("p", "Caracteres: " + dados.total_caracteres + " · Linhas: " + dados.total_linhas +
        " · Tokens: " + dados.tokens.length + " · Erros léxicos: " + dados.erros.length, "detalhes"));
      var estadoLexico = el("p", "Léxica: " + (dados.sucesso ? "sem erros." : "com erros."), "estado-analise");
      estadoLexico.id = "estado-lexico"; saida.appendChild(estadoLexico);
      saida.appendChild(el("p", "Reconhecer tokens não comprova que o programa esteja correto. O parser verifica a organização gramatical; a análise semântica (declarações e tipos) ficará para a Etapa 5.", "nota"));
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
          posicao.textContent = "Destaque da AST ativo. Use Destacar token atual ou navegue para voltar à sequência de tokens.";
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
      }
      anterior.addEventListener("click", function () { if (passo > 0) { voltarAosTokens(); passo--; atualizarPasso(); } });
      proximo.addEventListener("click", function () { if (passo + 1 < dados.tokens.length) { voltarAosTokens(); passo++; atualizarPasso(); } });
      voltarToken.addEventListener("click", function () { voltarAosTokens(); atualizarPasso(); });

      mostrarSintatica(dados.sintatica, function (no, botaoNo) {
        if (botaoSelecionado) botaoSelecionado.setAttribute("aria-pressed", "false");
        botaoSelecionado = botaoNo; botaoNo.setAttribute("aria-pressed", "true");
        selecaoAST = no; atualizarPasso();
      });

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
