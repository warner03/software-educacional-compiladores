/* Interface do Visualizador Educacional de Compiladores (Mini-C) - Etapa 2.
 * Envia o código ao backend por POST /api/analisar (o nginx repassa ao FastAPI).
 * As análises léxica, sintática e semântica serão feitas nas próximas etapas. */
(function (global) {
  "use strict";

  var URL_API = "/api/analisar";

  var MSG = {
    vazio: "Informe um código-fonte antes de solicitar a análise.",
    espacos: "O código informado contém apenas espaços em branco. Digite um programa para analisar.",
    comunicacao: "Não foi possível comunicar com o servidor. Verifique a conexão e tente novamente.",
    inesperado: "Ocorreu um erro inesperado. Tente novamente.",
    sucesso: "Código recebido com sucesso."
  };

  /** Validação rápida no navegador (o backend valida de novo). Retorna mensagem ou null. */
  function validarLocalmente(codigo) {
    if (typeof codigo !== "string" || codigo === "") return MSG.vazio;
    if (codigo.trim() === "") return MSG.espacos;
    return null;
  }

  /** Envia o código ao backend. Retorna {tipo, mensagem, dados}.
   *  tipo: 'sucesso' | 'entrada' | 'comunicacao' | 'servidor' */
  async function enviarCodigo(codigo, fetchFn, url) {
    var resp;
    var controlador = typeof AbortController !== "undefined" ? new AbortController() : null;
    var temporizador = controlador ? setTimeout(function () { controlador.abort(); }, 8000) : null;
    try {
      resp = await fetchFn(url || URL_API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ codigo: codigo }),
        signal: controlador ? controlador.signal : undefined
      });
    } catch (e) {
      return { tipo: "comunicacao", mensagem: MSG.comunicacao, dados: null };
    } finally {
      if (temporizador) clearTimeout(temporizador);
    }

    if (resp.status === 502 || resp.status === 503 || resp.status === 504) {
      return { tipo: "comunicacao", mensagem: MSG.comunicacao, dados: null };
    }

    var dados;
    try {
      dados = await resp.json();
    } catch (e) {
      return { tipo: "servidor", mensagem: MSG.inesperado, dados: null };
    }

    if (resp.status === 200 && dados && dados.recebido === true) {
      return { tipo: "sucesso", mensagem: dados.mensagem || MSG.sucesso, dados: dados };
    }
    if (resp.status >= 400 && resp.status < 500 && dados && typeof dados.mensagem === "string") {
      return { tipo: "entrada", mensagem: dados.mensagem, dados: dados };
    }
    return { tipo: "servidor", mensagem: MSG.inesperado, dados: null };
  }

  /** Liga os elementos da página aos comportamentos. */
  function iniciar(doc, win) {
    var campo = doc.getElementById("codigo");
    var seletor = doc.getElementById("exemplos");
    var botao = doc.getElementById("btn-analisar");
    var saida = doc.getElementById("resultado");

    function mostrar(tipo, texto, dados) {
      saida.textContent = "";
      var caixa = doc.createElement("div");
      caixa.className = "msg " + tipo;
      caixa.textContent = texto;
      saida.appendChild(caixa);
      if (tipo === "sucesso" && dados) {
        var detalhes = doc.createElement("p");
        detalhes.className = "detalhes";
        detalhes.textContent = "Caracteres: " + dados.total_caracteres + " · Linhas: " + dados.total_linhas;
        var nota = doc.createElement("p");
        nota.className = "nota";
        nota.textContent = "As análises léxica, sintática e semântica serão implementadas nas próximas etapas.";
        saida.appendChild(detalhes);
        saida.appendChild(nota);
      }
    }

    function limpar() {
      saida.textContent = "";
      var p = doc.createElement("p");
      p.className = "dica";
      p.textContent = "Os resultados da análise aparecerão aqui.";
      saida.appendChild(p);
    }

    seletor.addEventListener("change", function () {
      var opcao = seletor.options[seletor.selectedIndex];
      if (seletor.value && opcao && opcao.dataset.codigo !== undefined) {
        campo.value = opcao.dataset.codigo;
        limpar();
      }
    });

    botao.addEventListener("click", async function () {
      var codigo = campo.value;
      var erroLocal = validarLocalmente(codigo);
      if (erroLocal) {
        mostrar("entrada", erroLocal, null);
        return;
      }
      botao.disabled = true;
      try {
        var r = await enviarCodigo(codigo, win.fetch.bind(win));
        mostrar(r.tipo, r.mensagem, r.dados);
      } catch (e) {
        mostrar("servidor", MSG.inesperado, null);
      } finally {
        botao.disabled = false;
      }
    });
  }

  var api = { MSG: MSG, URL_API: URL_API, validarLocalmente: validarLocalmente, enviarCodigo: enviarCodigo, iniciar: iniciar };
  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  } else {
    global.CompiladorApp = api;
    document.addEventListener("DOMContentLoaded", function () { iniciar(document, window); });
  }
})(typeof window !== "undefined" ? window : globalThis);
