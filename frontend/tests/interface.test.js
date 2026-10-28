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
    return resp(200, { recebido: true, sucesso: true, tokens: [], erros: [], mensagem: "Análise léxica concluída sem erros.", total_caracteres: 16, total_linhas: 1 });
  });
  ui.campo.value = "int numero = 10;";
  ui.botao.click();
  await esperar();
  assert.deepEqual(enviado, { codigo: "int numero = 10;" });
  assert.match(ui.saida.textContent, /Análise léxica concluída sem erros\./);
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

const token = (tipo, lexema, linha, coluna) => ({ tipo, lexema, linha, coluna });
const tokensExemplo = [
  token("PALAVRA_RESERVADA", "int", 1, 1), token("IDENTIFICADOR", "numero", 1, 5),
  token("OPERADOR", "=", 1, 12), token("LITERAL_INTEIRO", "10", 1, 14), token("DELIMITADOR", ";", 1, 16)
];
const analise = (tokens = tokensExemplo, erros = []) => ({
  recebido: true, sucesso: erros.length === 0, tokens, erros,
  mensagem: erros.length ? "Análise léxica com erros." : "Análise léxica concluída sem erros.",
  total_caracteres: 16, total_linhas: 1
});
async function analisarUI(ui, codigo = "int numero = 10;") {
  ui.campo.value = codigo;
  ui.botao.click();
  await esperar();
}

test("exibe tipos, lexemas, posições e contagem por categoria", async () => {
  const ui = montar(async () => resp(200, analise()));
  await analisarUI(ui);
  const linhas = [...ui.$("tabela-tokens").querySelectorAll("tbody tr")];
  assert.equal(linhas.length, 5);
  assert.deepEqual([...linhas[1].cells].map(c => c.textContent), ["Identificador", "numero", "1", "5"]);
  assert.match(ui.$("contagem-tokens").textContent, /Palavra reservada: 1/);
  assert.match(ui.saida.textContent, /Tokens: 5/);
  assert.match(ui.saida.textContent, /não comprova que o programa esteja correto/);
  assert.equal(ui.$("codigo-analisado").textContent, "int numero = 10;");
});

test("navegação destaca o lexema e respeita os limites da sequência", async () => {
  const ui = montar(async () => resp(200, analise()));
  await analisarUI(ui);
  assert.equal(ui.$("token-anterior").disabled, true);
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "int");
  ui.$("token-proximo").click();
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "numero");
  assert.match(ui.$("passo-token").textContent, /Token 2 de 5/);
  assert.equal(ui.$("tabela-tokens").querySelectorAll(".token-atual").length, 1);
  ui.$("token-anterior").click();
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "int");
  for (let i = 0; i < 8; i++) ui.$("token-proximo").click();
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, ";");
  assert.equal(ui.$("token-proximo").disabled, true);
});

test("mostra erros localizados e também os tokens recuperados", async () => {
  const erros = [{ tipo: "ERRO_LEXICO", lexema: "@", linha: 1, coluna: 1, mensagem: "Caractere não reconhecido: '@'." }];
  const ui = montar(async () => resp(200, analise([token("IDENTIFICADOR", "x", 1, 3)], erros)));
  await analisarUI(ui, "@ x");
  assert.match(ui.$("erros-lexicos").textContent, /Linha 1, coluna 1/);
  assert.match(ui.$("erros-lexicos").textContent, /Caractere não reconhecido/);
  assert.equal(ui.$("tabela-tokens").querySelectorAll("tbody tr").length, 1);
  assert.equal(ui.$("codigo-analisado").textContent, "@ x");
  assert.equal(ui.campo.value, "@ x");
  assert.equal(ui.botao.disabled, false);
});

test("lexemas e mensagens maliciosos são exibidos como texto", async () => {
  const texto = '<img src=x onerror="alert(1)">';
  const erros = [{ tipo: "ERRO_LEXICO", lexema: texto, linha: 1, coluna: 1, mensagem: texto }];
  const ui = montar(async () => resp(200, analise([], erros)));
  await analisarUI(ui, texto);
  assert.equal(ui.saida.querySelector("img"), null);
  assert.match(ui.$("erros-lexicos").textContent, /<img/);
  assert.equal(ui.$("codigo-analisado").textContent, texto);
});

test("apenas comentários e apenas erros não quebram a apresentação vazia", async () => {
  for (const [codigo, erros] of [["/* ok */", []], ["@", [{ tipo: "ERRO_LEXICO", lexema: "@", linha: 1, coluna: 1, mensagem: "Caractere inválido." }]]]) {
    const ui = montar(async () => resp(200, analise([], erros)));
    await analisarUI(ui, codigo);
    assert.equal(ui.$("tabela-tokens").querySelectorAll("tbody tr").length, 0);
    assert.match(ui.saida.textContent, /Nenhum token reconhecido/);
    assert.equal(ui.$("token-proximo"), null);
    assert.equal(ui.botao.disabled, false);
  }
});

test("destaque usa caracteres Unicode e linhas, não bytes ou unidades UTF-16", async () => {
  const ui = montar(async () => resp(200, analise([
    token("IDENTIFICADOR", "x", 1, 3), token("IDENTIFICADOR", "y", 2, 2)
  ], [{ tipo: "ERRO_LEXICO", lexema: "😀", linha: 1, coluna: 1, mensagem: "Fora do recorte." }])));
  await analisarUI(ui, "😀 x\n y");
  assert.equal(ui.$("codigo-analisado").textContent, "😀 x\n y");
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "x");
  ui.$("token-proximo").click();
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "y");
});

test("alteração de código invalida resultados e respostas de solicitações anteriores", async () => {
  let concluir;
  const ui = montar(() => new Promise(resolve => { concluir = resolve; }));
  ui.botao.click();
  ui.campo.value = "float novo;";
  ui.campo.dispatchEvent(new ui.win.Event("input"));
  concluir(resp(200, analise()));
  await esperar();
  assert.equal(ui.$("tabela-tokens"), null);
  assert.match(ui.saida.textContent, /Código alterado/);
  assert.equal(ui.campo.value, "float novo;");
  assert.equal(ui.botao.disabled, false);
});

test("trocar exemplo durante envio descarta a resposta antiga", async () => {
  let concluir;
  const ui = montar(() => new Promise(resolve => { concluir = resolve; }));
  ui.botao.click();
  escolher(ui, "ex4");
  concluir(resp(200, analise()));
  await esperar();
  assert.equal(ui.$("tabela-tokens"), null);
  assert.match(ui.campo.value, /float media/);
});

test("resposta malformada não cria uma tabela incorreta", async () => {
  const ui = montar(async () => resp(200, { recebido: true, sucesso: true, tokens: [null], erros: [] }));
  await analisarUI(ui);
  assert.equal(ui.saida.textContent.trim(), MSG.inesperado);
  assert.equal(ui.botao.disabled, false);
});
