const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { JSDOM } = require("jsdom");
const { iniciar, enviarCodigo, MSG } = require("../app.js");

const html = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf8");
// Entradas de contrato obtidas do backend; esperados da UI escritos de forma
// independente abaixo. A semântica tem seus próprios oráculos de política.
const fixture = nome => JSON.parse(fs.readFileSync(path.join(__dirname, "fixtures", nome + ".json"), "utf8"));
const esperar = () => new Promise(resolve => setTimeout(resolve, 10));
const resposta = dados => ({ status: 200, json: async () => dados });

async function montar(nome = "valido", preparar, dadosAlternativos) {
  const f = fixture(nome), dom = new JSDOM(html, { url: "http://localhost/" }), win = dom.window;
  if (preparar) preparar(win);
  let chamadas = 0;
  win.fetch = async () => { chamadas++; return resposta(dadosAlternativos || f.dados); };
  iniciar(win.document, win);
  const $ = id => win.document.getElementById(id);
  $("codigo").value = f.codigo; $("btn-analisar").click();
  await esperar();
  return { win, $, fonte: f.codigo, dados: f.dados, saida: $("resultado"), chamadas: () => chamadas };
}

test("três fases são identificadas por texto e símbolos são exibidos com atributos", async () => {
  const ui = await montar();
  assert.match(ui.$("estado-lexico").textContent, /sem erros/);
  assert.match(ui.$("estado-sintatica").textContent, /sem erros/);
  assert.match(ui.$("estado-semantica").textContent, /\[OK\].*sem erros/);
  const linha = ui.$("tabela-simbolos").querySelector("tbody tr");
  assert.deepEqual([...linha.cells].slice(0, 6).map(c => c.textContent), ["x", "int", "E0 — Global", "Linha 1, coluna 5", "Sim — garantida", "Nenhum"]);
  assert.ok(ui.$("tabela-tokens")); assert.ok(ui.$("arvore-ast"));
});

test("selecionar declaração destaca o nome e marca o nó da AST", async () => {
  const ui = await montar();
  const b = ui.$("tabela-simbolos").querySelector(".localizar-simbolo"); b.click();
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "x");
  assert.equal(ui.$("codigo-analisado").textContent, ui.fonte);
  assert.equal(b.getAttribute("aria-pressed"), "true");
  const relacionado = ui.$("arvore-ast").querySelector(".ast-relacionado");
  assert.equal(relacionado.dataset.noAst, "/comandos/0");
  assert.equal(relacionado.dataset.tipo, "Declaracao");
  assert.match(ui.$("selecao-semantica").textContent, /coluna 5.*coluna 6/);
  ui.$("token-destacar").click();
  assert.equal(b.getAttribute("aria-pressed"), "false");
  assert.equal(ui.$("arvore-ast").querySelector(".ast-relacionado"), null);
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "int");
});

test("referências de leitura e atribuição apontam para os identificadores corretos", async () => {
  const ui = await montar();
  const referencias = ui.$("tabela-simbolos").querySelectorAll(".localizar-referencia");
  assert.equal(referencias.length, 2);
  referencias[1].click();
  assert.match(ui.$("selecao-semantica").textContent, /Leitura de x.*coluna 16/);
  assert.equal(ui.$("arvore-ast").querySelector(".ast-relacionado").dataset.noAst, "/comandos/1/valor/esquerda");
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "x");
});

test("filtro de escopos distingue o símbolo interno que sombreia o global", async () => {
  const ui = await montar("escopos");
  assert.equal(ui.$("tabela-simbolos").querySelectorAll("tbody tr").length, 2);
  ui.$("filtro-escopo").value = "E1";
  ui.$("filtro-escopo").dispatchEvent(new ui.win.Event("change"));
  const linhas = ui.$("tabela-simbolos").querySelectorAll("tbody tr");
  assert.equal(linhas.length, 1);
  assert.deepEqual([...linhas[0].cells].slice(0, 2).map(c => c.textContent), ["x", "float"]);
  assert.equal(linhas[0].cells[5].textContent, "S1");
  assert.match(ui.$("contagem-simbolos").textContent, /1 de 2/);
  linhas[0].querySelector(".localizar-simbolo").click();
  assert.equal(ui.$("arvore-ast").querySelector(".ast-relacionado").dataset.noAst, "/comandos/1/comandos/0");
});

test("erro semântico tem fase, regra, localização, sugestão e tabela preservada", async () => {
  const ui = await montar("erro");
  assert.ok(ui.saida.querySelector(".msg.semantico"));
  assert.match(ui.$("estado-semantica").textContent, /\[!\].*com erros/);
  assert.match(ui.$("erros-semanticos").textContent, /VARIAVEL_NAO_INICIALIZADA/);
  assert.match(ui.$("erros-semanticos").textContent, /IDENTIFICADOR_NAO_DECLARADO/);
  assert.match(ui.$("erros-semanticos").textContent, /Sugestão:/);
  assert.equal(ui.$("tabela-simbolos").querySelectorAll("tbody tr").length, 2);
  ui.$("erros-semanticos").querySelector("button").click();
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "x");
  assert.equal(ui.$("arvore-ast").querySelector(".ast-relacionado").dataset.noAst, "/comandos/1/inicializador");
});

for (const [nome, causa] of [["lexico", "léxicos"], ["sintatico", "sintáticos"]]) {
  test("bloqueio semântico por erros " + causa + " é comunicado sem tabela falsa", async () => {
    const ui = await montar(nome);
    assert.match(ui.$("estado-semantica").textContent, new RegExp("não executada.*" + causa));
    assert.equal(ui.$("tabela-simbolos"), null);
    assert.equal(ui.$("erros-semanticos"), null);
    assert.ok(ui.$("tabela-tokens"));
  });
}

test("semântica malformada e ligações inexistentes são rejeitadas", async () => {
  const f = fixture("valido");
  const alteracoes = [
    d => { d.semantica = null; },
    d => { d.semantica.sucesso = false; },
    d => { d.semantica.tabelaSimbolos[0].noAst = "/comandos/99"; },
    d => { d.semantica.tabelaSimbolos[0].referencias[0].noAst = "/comandos/0"; },
    d => { d.semantica.tabelaSimbolos[0].fim.coluna = 9999; },
    d => { d.semantica.tabelaSimbolos[0].tipo = "string"; },
    d => { d.semantica.tabelaSimbolos.push(structuredClone(d.semantica.tabelaSimbolos[0])); },
    d => { d.semantica.escopos[0].pai = "E99"; },
    d => { d.semantica.escopos = []; },
    d => { d.semantica.tabelaSimbolos[0].inicializado = "sim"; },
    d => { d.semantica.tabelaSimbolos[0].referencias = [null]; }
  ];
  for (const alterar of alteracoes) {
    const dados = structuredClone(f.dados); alterar(dados);
    const r = await enviarCodigo(f.codigo, async () => resposta(dados));
    assert.equal(r.tipo, "servidor"); assert.equal(r.mensagem, MSG.inesperado);
  }
});

test("mensagens e sugestões maliciosas são texto inerte", async () => {
  const f = fixture("erro"), texto = '<img src=x onerror="alert(1)">';
  f.dados.semantica.erros[0].mensagem = texto; f.dados.semantica.erros[0].sugestao = texto;
  const ui = await montar("erro", null, f.dados);
  assert.ok(ui.$("erros-semanticos").textContent.includes(texto));
  assert.equal(ui.saida.querySelector("img"), null);
});

test("editar fonte descarta também a tabela e os diagnósticos semânticos", async () => {
  const ui = await montar("erro");
  ui.$("codigo").value = "int outro=2;";
  ui.$("codigo").dispatchEvent(new ui.win.Event("input"));
  assert.equal(ui.$("tabela-simbolos"), null); assert.equal(ui.$("erros-semanticos"), null);
});

test("mudar modo visual preserva análise, seleção e fonte sem nova requisição", async () => {
  const ui = await montar();
  ui.$("tabela-simbolos").querySelector("button").click();
  const tabela = ui.$("tabela-simbolos"), arvore = ui.$("arvore-ast");
  for (const modo of ["sem-cores", "contraste", "padrao"]) {
    ui.$("modo-visual").value = modo;
    ui.$("modo-visual").dispatchEvent(new ui.win.Event("change"));
    assert.equal(ui.win.document.documentElement.dataset.visual, modo);
    assert.equal(ui.win.localStorage.getItem("mini-c.visual"), modo);
    assert.equal(ui.$("tabela-simbolos"), tabela); assert.equal(ui.$("arvore-ast"), arvore);
    assert.equal(ui.$("codigo-analisado").textContent, ui.fonte);
    assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "x");
  }
  assert.equal(ui.chamadas(), 1);
});

test("preferência visual válida é carregada e valor desconhecido volta ao padrão", async () => {
  for (const [salvo, esperado] of [["sem-cores", "sem-cores"], ["contraste", "contraste"], ["injetado", "padrao"]]) {
    const ui = await montar("valido", win => win.localStorage.setItem("mini-c.visual", salvo));
    assert.equal(ui.$("modo-visual").value, esperado);
    assert.equal(ui.win.document.documentElement.dataset.visual, esperado);
  }
});

test("modo continua funcional quando armazenamento local é indisponível", async () => {
  const ui = await montar("valido", win => Object.defineProperty(win, "localStorage", { get() { throw new Error("bloqueado"); } }));
  ui.$("modo-visual").value = "sem-cores"; ui.$("modo-visual").dispatchEvent(new ui.win.Event("change"));
  assert.equal(ui.win.document.documentElement.dataset.visual, "sem-cores");
  assert.ok(ui.$("tabela-simbolos"));
});

test("legenda oferece seis categorias por texto e padrões, com rótulo no seletor", async () => {
  const ui = await montar();
  assert.equal(ui.win.document.querySelectorAll(".legenda-tokens li").length, 6);
  assert.match(ui.$("legenda-visual").textContent, /duplo.*simples.*pontilhado.*tracejado.*ondulado.*negrito/s);
  assert.ok(ui.win.document.querySelector('label[for="modo-visual"]'));
  assert.equal(ui.$("estado-visual").getAttribute("role"), "status");
});
