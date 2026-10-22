const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { JSDOM } = require("jsdom");
const { MSG, iniciar } = require("../app.js");

const HTML = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf-8");
const esperar = () => new Promise((r) => setTimeout(r, 10));

function montar(fetchMock) {
  const dom = new JSDOM(HTML); // scripts não executam; ligamos app.js manualmente
  const win = dom.window;
  win.fetch = fetchMock || (async () => { throw new Error("fetch não deveria ser chamado"); });
  iniciar(win.document, win);
  const $ = (id) => win.document.getElementById(id);
  return { win, $, campo: $("codigo"), seletor: $("exemplos"), botao: $("btn-analisar"), saida: $("resultado") };
}
const resp = (status, dados) => ({ status, json: async () => dados });

function escolher(ui, valor) {
  ui.seletor.value = valor;
  ui.seletor.dispatchEvent(new ui.win.Event("change"));
}
const valoresExemplos = (ui) => [...ui.seletor.options].map((o) => o.value).filter(Boolean);

test("tela tem os elementos obrigatórios", () => {
  const ui = montar();
  assert.match(ui.$("titulo").textContent, /Visualizador Educacional de Compiladores/);
  assert.match(ui.$("linguagem").textContent, /Mini-C/);
  assert.equal(ui.campo.tagName, "TEXTAREA");
  assert.equal(ui.botao.tagName, "BUTTON");
  assert.equal(ui.seletor.tagName, "SELECT");
  assert.ok(ui.saida);
});

test("há ao menos três exemplos e todos têm código", () => {
  const ui = montar();
  const ids = valoresExemplos(ui);
  assert.ok(ids.length >= 3);
  for (const o of ui.seletor.options) if (o.value) assert.ok(o.dataset.codigo.trim().length > 0);
});

test("cada exemplo é carregado no campo de código", () => {
  const ui = montar();
  for (const o of [...ui.seletor.options].filter((x) => x.value)) {
    escolher(ui, o.value);
    assert.equal(ui.campo.value, o.dataset.codigo);
  }
});

test("novo exemplo substitui o anterior e o código continua editável", () => {
  const ui = montar();
  const [a, b] = valoresExemplos(ui);
  escolher(ui, a);
  escolher(ui, b);
  assert.equal(ui.campo.value, [...ui.seletor.options].find((o) => o.value === b).dataset.codigo);
  ui.campo.value += "\nint z;";
  assert.ok(ui.campo.value.endsWith("int z;"));
});

test("entrada vazia mostra mensagem e não chama o backend", async () => {
  const ui = montar();
  ui.campo.value = "";
  ui.botao.click();
  await esperar();
  assert.equal(ui.saida.textContent.trim(), MSG.vazio);
});

test("entrada só com espaços mostra mensagem e não chama o backend", async () => {
  const ui = montar();
  ui.campo.value = "   \n  ";
  ui.botao.click();
  await esperar();
  assert.equal(ui.saida.textContent.trim(), MSG.espacos);
});

test("envio válido exibe a resposta do backend e preserva o código", async () => {
  let enviado;
  const ui = montar(async (url, op) => {
    enviado = JSON.parse(op.body);
    return resp(200, { recebido: true, mensagem: "Código recebido com sucesso.", total_caracteres: 16, total_linhas: 1 });
  });
  ui.campo.value = "int numero = 10;";
  ui.botao.click();
  await esperar();
  assert.deepEqual(enviado, { codigo: "int numero = 10;" });
  assert.match(ui.saida.textContent, /Código recebido com sucesso\./);
  assert.match(ui.saida.textContent, /Caracteres: 16/);
  assert.equal(ui.campo.value, "int numero = 10;");
  assert.equal(ui.botao.disabled, false);
});

test("erro de validação do backend é mostrado ao usuário", async () => {
  const ui = montar(async () => resp(400, { recebido: false, erro: "entrada_invalida", mensagem: "Mensagem do backend." }));
  ui.campo.value = "int x;";
  ui.botao.click();
  await esperar();
  assert.match(ui.saida.textContent, /Mensagem do backend\./);
});

test("falha de comunicação mostra mensagem e mantém a interface consistente", async () => {
  const ui = montar(async () => { throw new TypeError("Failed to fetch"); });
  ui.campo.value = "int x;";
  ui.botao.click();
  await esperar();
  assert.equal(ui.saida.textContent.trim(), MSG.comunicacao);
  assert.equal(ui.campo.value, "int x;");
  assert.equal(ui.botao.disabled, false);
});

test("o texto da resposta nunca é interpretado como HTML", async () => {
  const ui = montar(async () => resp(400, { mensagem: "<img src=x onerror=alert(1)>" }));
  ui.campo.value = "int x;";
  ui.botao.click();
  await esperar();
  assert.equal(ui.saida.querySelector("img"), null);
});
