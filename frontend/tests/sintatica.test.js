const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { JSDOM } = require("jsdom");
const { iniciar, enviarCodigo, MSG } = require("../app.js");

const HTML = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf-8");
const esperar = () => new Promise(resolve => setTimeout(resolve, 10));
const codigo = "int x = 1 + 2 * 3;";
const p = coluna => ({ linha: 1, coluna });
const numero = (lexema, coluna) => ({ tipo: "Literal", categoria: "inteiro", lexema, inicio: p(coluna), fim: p(coluna + lexema.length) });
// Referência manual: multiplicação sob a adição, com posições contadas no fonte.
const AST = {
  tipo: "Programa", inicio: p(1), fim: p(19), comandos: [{
    tipo: "Declaracao", tipoDado: "int", nome: "x", inicio: p(1), fim: p(19), inicializador: {
      tipo: "Binario", operador: "+", inicio: p(9), fim: p(18), esquerda: numero("1", 9), direita: {
        tipo: "Binario", operador: "*", inicio: p(13), fim: p(18), esquerda: numero("2", 13), direita: numero("3", 17)
      }
    }
  }]
};
const tokens = [
  ["PALAVRA_RESERVADA", "int", 1], ["IDENTIFICADOR", "x", 5], ["OPERADOR", "=", 7],
  ["LITERAL_INTEIRO", "1", 9], ["OPERADOR", "+", 11], ["LITERAL_INTEIRO", "2", 13],
  ["OPERADOR", "*", 15], ["LITERAL_INTEIRO", "3", 17], ["DELIMITADOR", ";", 18]
].map(([tipo, lexema, coluna]) => ({ tipo, lexema, linha: 1, coluna }));
const erro = { tipo: "ERRO_SINTATICO", codigo: "gramatica", linha: 1, coluna: 9, lexema: ";", encontrado: "DELIMITADOR", esperado: ["IDENTIFICADOR", "LITERAL_INTEIRO"], mensagem: "Era esperado um operando. Encontrado: ';'." };
const dados = () => ({ recebido: true, sucesso: true, tokens: structuredClone(tokens), erros: [], total_caracteres: codigo.length, total_linhas: 1,
  sintatica: { estado: "sucesso", sucesso: true, ast: structuredClone(AST), erros: [] } });
const resp = d => ({ status: 200, json: async () => d });

async function montar(d = dados(), fonte = codigo) {
  const dom = new JSDOM(HTML);
  const win = dom.window;
  win.fetch = async () => resp(d);
  iniciar(win.document, win);
  const $ = id => win.document.getElementById(id);
  $("codigo").value = fonte; $("btn-analisar").click();
  await esperar();
  return { win, $, saida: $("resultado") };
}

test("sucesso sintático tem estados separados, AST legível e tokens preservados", async () => {
  const ui = await montar();
  assert.match(ui.$("estado-lexico").textContent, /sem erros/);
  assert.match(ui.$("estado-sintatica").textContent, /sem erros/);
  assert.equal(ui.$("tabela-tokens").querySelectorAll("tbody tr").length, 9);
  assert.match(ui.$("arvore-ast").textContent, /Declaração · int x/);
  const soma = ui.$("arvore-ast").querySelector('details[data-tipo="Binario"]');
  assert.match(soma.querySelector("summary").textContent, /\+/);
  assert.match(soma.querySelector(':scope > .ast-filhos details[data-tipo="Binario"] > summary').textContent, /\*/);
  assert.match(ui.saida.textContent, /árvore de derivação/);
  assert.match(ui.saida.textContent, /Etapa 5/);
});

test("expandir e recolher alteram todos os nós, incluindo folhas", async () => {
  const ui = await montar();
  const nos = [...ui.$("arvore-ast").querySelectorAll("details")];
  assert.equal(nos.length, 7);
  assert.ok(nos.some(n => !n.open));
  ui.$("ast-expandir").click(); assert.ok(nos.every(n => n.open));
  ui.$("ast-recolher").click(); assert.ok(nos.every(n => !n.open));
});

test("seleção de operação destaca expressão inteira, com fim exclusivo", async () => {
  const ui = await montar();
  const soma = ui.$("arvore-ast").querySelector('details[data-tipo="Binario"]');
  const selecionar = soma.querySelector(".ast-localizar");
  selecionar.click();
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "1 + 2 * 3");
  assert.equal(ui.$("codigo-analisado").textContent, codigo);
  assert.equal(selecionar.getAttribute("aria-pressed"), "true");
  assert.match(ui.$("posicao-ast").textContent, /coluna 9.*coluna 18/);
  assert.equal(ui.$("tabela-tokens").querySelectorAll(".token-atual").length, 0);
  const folha = ui.$("arvore-ast").querySelector('details[data-tipo="Literal"] .ast-localizar');
  folha.click();
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "1");
  assert.equal(selecionar.getAttribute("aria-pressed"), "false");
  ui.$("token-destacar").click();
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "int");
  assert.equal(folha.getAttribute("aria-pressed"), "false");
});

test("navegação de tokens retoma destaque individual depois de selecionar AST", async () => {
  const ui = await montar();
  ui.$("arvore-ast").querySelector(".ast-localizar").click();
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, codigo);
  ui.$("token-proximo").click();
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "x");
  assert.match(ui.$("posicao-ast").textContent, /Destaque por token/);
});

test("erro sintático preserva sucesso léxico, localiza erro e não mostra AST", async () => {
  const d = dados();
  d.sintatica = { estado: "erro", sucesso: false, ast: null, erros: [erro] };
  const ui = await montar(d);
  assert.ok(ui.saida.querySelector(".msg.sintatico"));
  assert.match(ui.$("estado-lexico").textContent, /sem erros/);
  assert.match(ui.$("estado-sintatica").textContent, /com erros/);
  assert.match(ui.$("erros-sintaticos").textContent, /Linha 1, coluna 9/);
  assert.match(ui.$("erros-sintaticos").textContent, /Esperado: IDENTIFICADOR, LITERAL_INTEIRO/);
  assert.equal(ui.$("arvore-ast"), null);
  assert.ok(ui.$("tabela-tokens"));
});

test("erro léxico explica por que parser não foi executado", async () => {
  const d = dados(); d.sucesso = false;
  d.erros = [{ tipo: "ERRO_LEXICO", lexema: "@", linha: 1, coluna: 1, mensagem: "Caractere não reconhecido." }];
  d.sintatica = { estado: "nao_executada", sucesso: null, motivo: "erros_lexicos", ast: null, erros: [] };
  const ui = await montar(d);
  assert.match(ui.$("estado-sintatica").textContent, /não executada.*erros léxicos/);
  assert.ok(ui.$("erros-lexicos"));
  assert.equal(ui.$("arvore-ast"), null);
  assert.equal(ui.$("erros-sintaticos"), null);
});

test("erro em EOF é descrito como fim do código, sem lexema vazio confuso", async () => {
  const d = dados();
  d.sintatica = { estado: "erro", sucesso: false, ast: null, erros: [{ ...erro, lexema: "", encontrado: "EOF", esperado: [";"], coluna: 19 }] };
  const ui = await montar(d);
  assert.match(ui.$("erros-sintaticos").textContent, /fim do código \(EOF\)/);
});

test("texto vindo de nós e diagnósticos é inerte, sem criar HTML", async () => {
  const d = dados(), malicioso = '<img src=x onerror="alert(1)">';
  d.sintatica.ast.comandos[0].nome = malicioso;
  const ui = await montar(d);
  assert.equal(ui.saida.querySelector("img"), null);
  assert.ok(ui.$("arvore-ast").textContent.includes(malicioso));
  d.sintatica = { estado: "erro", sucesso: false, ast: null, erros: [{ ...erro, mensagem: malicioso, esperado: [malicioso] }] };
  const erroUI = await montar(d);
  assert.equal(erroUI.saida.querySelector("img"), null);
  assert.ok(erroUI.$("erros-sintaticos").textContent.includes(malicioso));
});

test("exportação baixa JSON da AST completa, sem incluir código ou tokens", async () => {
  const ui = await montar();
  let blob, nome, objetoRevogado;
  ui.win.URL.createObjectURL = b => { blob = b; return "blob:teste"; };
  ui.win.URL.revokeObjectURL = url => { objetoRevogado = url; };
  ui.win.setTimeout = f => f();
  ui.win.HTMLAnchorElement.prototype.click = function () { nome = this.download; };
  ui.$("ast-exportar").click();
  assert.equal(nome, "mini-c-ast.json");
  assert.equal(blob.type, "application/json;charset=utf-8");
  const texto = await new Promise(resolve => { const leitor = new ui.win.FileReader(); leitor.onload = () => resolve(leitor.result); leitor.readAsText(blob); });
  assert.deepEqual(JSON.parse(texto), AST);
  assert.equal(objetoRevogado, "blob:teste");
});

test("seleção por Unicode e CRLF usa as mesmas colunas do scanner", async () => {
  const fonte = "/* 😀 */\r\n\tint x = 1;", d = dados();
  d.tokens = [{ tipo: "PALAVRA_RESERVADA", lexema: "int", linha: 2, coluna: 2 }];
  d.sintatica.ast = { tipo: "Programa", inicio: { linha: 2, coluna: 2 }, fim: { linha: 2, coluna: 12 }, comandos: [{
    tipo: "Declaracao", tipoDado: "int", nome: "x", inicio: { linha: 2, coluna: 2 }, fim: { linha: 2, coluna: 12 },
    inicializador: { tipo: "Literal", categoria: "inteiro", lexema: "1", inicio: { linha: 2, coluna: 10 }, fim: { linha: 2, coluna: 11 } }
  }] };
  const ui = await montar(d, fonte);
  ui.$("arvore-ast").querySelector('details[data-tipo="Literal"] .ast-localizar').click();
  assert.equal(ui.$("codigo-analisado").querySelector("mark").textContent, "1");
  assert.equal(ui.$("codigo-analisado").textContent, fonte.replace(/\r\n/g, "\n"));
});

test("editar código elimina a árvore, evitando destaque baseado em fonte antigo", async () => {
  const ui = await montar();
  assert.ok(ui.$("arvore-ast"));
  ui.$("codigo").value = "int novo;";
  ui.$("codigo").dispatchEvent(new ui.win.Event("input"));
  assert.equal(ui.$("arvore-ast"), null);
  assert.match(ui.saida.textContent, /Código alterado/);
});

test("contratos sintáticos incoerentes ou posições impossíveis são rejeitados", async () => {
  const invalidos = [
    null, { estado: "sucesso", sucesso: true, ast: null, erros: [] },
    { estado: "erro", sucesso: true, ast: null, erros: [erro] },
    { estado: "erro", sucesso: false, ast: AST, erros: [erro] },
    { estado: "erro", sucesso: false, ast: null, erros: [] },
    { estado: "nao_executada", sucesso: null, ast: null, erros: [] },
    { estado: "erro", sucesso: false, ast: null, erros: [{ ...erro, esperado: null }] }
  ];
  const posicaoInvalida = structuredClone(AST); posicaoInvalida.fim.coluna = 999;
  const noDesconhecido = structuredClone(AST); noDesconhecido.comandos[0].tipo = "ComandoInventado";
  const filhoAusente = structuredClone(AST); filhoAusente.comandos[0].inicializador.esquerda = null;
  for (const ast of [posicaoInvalida, noDesconhecido, filhoAusente]) invalidos.push({ estado: "sucesso", sucesso: true, ast, erros: [] });
  for (const sintatica of invalidos) {
    const r = await enviarCodigo(codigo, async () => resp({ ...dados(), sintatica }));
    assert.equal(r.tipo, "servidor"); assert.equal(r.mensagem, MSG.inesperado);
  }
});
