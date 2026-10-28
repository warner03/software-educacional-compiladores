/* Mini-C — Etapa 3: envio, apresentação de tokens e navegação educacional. */
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
      if (resp.status === 200 && respostaLexicaValida(dados)) {
        return { tipo: dados.sucesso ? "sucesso" : "lexico", mensagem: dados.mensagem || (dados.sucesso ? MSG.sucesso : "Análise léxica concluída com erros."), dados: dados };
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
    function mostrar(tipo, texto, dados, codigo) {
      saida.textContent = "";
      var aviso = el("p", texto, "msg " + tipo);
      aviso.setAttribute("role", "status");
      saida.appendChild(aviso);
      if (!dados) return;
      saida.appendChild(el("p", "Caracteres: " + dados.total_caracteres + " · Linhas: " + dados.total_linhas +
        " · Tokens: " + dados.tokens.length + " · Erros léxicos: " + dados.erros.length, "detalhes"));
      saida.appendChild(el("p", "Reconhecer tokens não comprova que o programa esteja correto. A análise sintática será desenvolvida na Etapa 4; a semântica, posteriormente.", "nota"));
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
      var anterior = el("button", "Token anterior"), proximo = el("button", "Próximo token");
      anterior.id = "token-anterior"; proximo.id = "token-proximo";
      anterior.type = proximo.type = "button";
      var posicao = el("p"); posicao.id = "passo-token";
      posicao.setAttribute("aria-live", "polite");
      controles.append(anterior, proximo, posicao);
      if (dados.tokens.length) saida.appendChild(controles);
      else saida.appendChild(el("p", "Nenhum token reconhecido. Entradas apenas com comentários são aceitas; consulte também os erros, se houver."));
      var linhas = [];
      function atualizarPasso() {
        pre.textContent = "";
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
      anterior.addEventListener("click", function () { if (passo > 0) { passo--; atualizarPasso(); } });
      proximo.addEventListener("click", function () { if (passo + 1 < dados.tokens.length) { passo++; atualizarPasso(); } });

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
