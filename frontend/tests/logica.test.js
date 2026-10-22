const test = require("node:test");
const assert = require("node:assert/strict");
const { MSG, validarLocalmente, enviarCodigo } = require("../app.js");

const resposta = (status, dados, jsonInvalido = false) => ({
  status,
  json: async () => { if (jsonInvalido) throw new Error("json inválido"); return dados; },
});

test("validação local: vazio, só espaços e código válido", () => {
  assert.equal(validarLocalmente(""), MSG.vazio);
  assert.equal(validarLocalmente("   \n\t "), MSG.espacos);
  assert.equal(validarLocalmente("int x;"), null);
  assert.equal(validarLocalmente('printf("ação 😀 @#$");'), null);
  assert.equal(validarLocalmente(undefined), MSG.vazio);
});

test("envio com sucesso usa POST /api/analisar com o JSON esperado", async () => {
  let chamada;
  const fakeFetch = async (url, opcoes) => {
    chamada = { url, opcoes };
    return resposta(200, { recebido: true, mensagem: "Código recebido com sucesso.", total_caracteres: 6, total_linhas: 1 });
  };
  const r = await enviarCodigo("int x;", fakeFetch);
  assert.equal(r.tipo, "sucesso");
  assert.equal(chamada.url, "/api/analisar");
  assert.equal(chamada.opcoes.method, "POST");
  assert.deepEqual(JSON.parse(chamada.opcoes.body), { codigo: "int x;" });
});

test("erro 400 do backend vira mensagem de entrada", async () => {
  const r = await enviarCodigo("x", async () => resposta(400, { recebido: false, erro: "entrada_invalida", mensagem: "msg do backend" }));
  assert.equal(r.tipo, "entrada");
  assert.equal(r.mensagem, "msg do backend");
});

test("falha de rede vira mensagem de comunicação", async () => {
  const r = await enviarCodigo("int x;", async () => { throw new TypeError("Failed to fetch"); });
  assert.equal(r.tipo, "comunicacao");
  assert.equal(r.mensagem, MSG.comunicacao);
});

test("502/503/504 (backend fora do ar) vira falha de comunicação", async () => {
  for (const status of [502, 503, 504]) {
    const r = await enviarCodigo("int x;", async () => resposta(status, null, true));
    assert.equal(r.tipo, "comunicacao");
  }
});

test("erro 500 não expõe detalhes internos", async () => {
  const r = await enviarCodigo("int x;", async () => resposta(500, { mensagem: "Traceback /etc/segredo" }));
  assert.equal(r.tipo, "servidor");
  assert.equal(r.mensagem, MSG.inesperado);
});

test("resposta que não é JSON vira erro genérico", async () => {
  const r = await enviarCodigo("int x;", async () => resposta(200, null, true));
  assert.equal(r.tipo, "servidor");
  assert.equal(r.mensagem, MSG.inesperado);
});
