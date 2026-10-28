# Contrato da API — Etapa 3

## Rotas

- `GET /saude`: HTTP 200, `{"status":"ok"}`.
- `POST /analisar`: análise direta no FastAPI.
- `POST /api/analisar`: mesma operação pelo nginx, usada pelo navegador.

Requisição: JSON com `codigo` string, não vazia e com no máximo 10.000 caracteres. Não há autenticação, banco ou credenciais exigidos nesta aplicação educacional.

```json
{"codigo":"int numero = 10;"}
```

## Resposta processada — HTTP 200

Sempre inclui:

| Campo | Significado |
|---|---|
| `recebido` | `true`: solicitação recebida e processada; não indica ausência de erros léxicos |
| `sucesso` | `true` se e somente se `erros` está vazio |
| `mensagem` | Resumo didático; não deve ser usado como discriminador lógico |
| `total_caracteres` | Tamanho da string recebida em caracteres Unicode |
| `total_linhas` | Quantidade de linhas segundo `str.splitlines()` do Python, preservando a métrica da Etapa 2 |
| `tokens` | Lista em ordem de leitura dos tokens válidos |
| `erros` | Lista em ordem de leitura dos erros léxicos |

Token: `{"tipo":"IDENTIFICADOR","lexema":"numero","linha":1,"coluna":5}`.

Tipos: `PALAVRA_RESERVADA`, `IDENTIFICADOR`, `LITERAL_INTEIRO`, `LITERAL_REAL`, `OPERADOR`, `DELIMITADOR`. Não há token EOF na resposta nem tokens de comentários/espaços.

Erro: `{"tipo":"ERRO_LEXICO","lexema":"@","linha":2,"coluna":1,"mensagem":"Caractere não reconhecido: '@'. Verifique o subconjunto Mini-C suportado."}`.

Linha e coluna são inteiros positivos e iniciam em 1; tab conta uma coluna. CRLF/CR são normalizados para LF no scanner. A contagem de linhas é uma métrica informativa herdada, não um índice do último token; um arquivo terminado em quebra não recebe uma linha adicional nessa métrica.

### Sem erros

```json
{
  "recebido": true,
  "sucesso": true,
  "mensagem": "Análise léxica concluída sem erros.",
  "total_caracteres": 6,
  "total_linhas": 1,
  "tokens": [
    {"tipo":"PALAVRA_RESERVADA","lexema":"int","linha":1,"coluna":1},
    {"tipo":"IDENTIFICADOR","lexema":"x","linha":1,"coluna":5},
    {"tipo":"DELIMITADOR","lexema":";","linha":1,"coluna":6}
  ],
  "erros": []
}
```

### Com erro léxico

Entrada `{"codigo":"@ x"}`:

```json
{
  "recebido": true,
  "sucesso": false,
  "mensagem": "Análise léxica concluída com erros. Revise os trechos indicados.",
  "total_caracteres": 3,
  "total_linhas": 1,
  "tokens": [{"tipo":"IDENTIFICADOR","lexema":"x","linha":1,"coluna":3}],
  "erros": [{
    "tipo":"ERRO_LEXICO","lexema":"@","linha":1,"coluna":1,
    "mensagem":"Caractere não reconhecido: '@'. Verifique o subconjunto Mini-C suportado."
  }]
}
```

Erro léxico é resultado da análise, por isso retorna HTTP 200 com `sucesso:false`. Não retorna HTTP 500 nem descarta tokens recuperados. Entradas apenas com comentários podem ter `sucesso:true`, `tokens:[]`, `erros:[]`.

## Falhas de entrada e servidor

Mantêm o formato da Etapa 2:

| Situação | HTTP | Campo `erro` |
|---|---|---|
| JSON inválido, corpo não objeto, `codigo` ausente | 400 | `requisicao_invalida` |
| Tipo errado, vazio, só espaços ou acima de 10.000 caracteres | 400 | `entrada_invalida` |
| Exceção interna | 500 | `erro_interno` |

```json
{"recebido":false,"erro":"entrada_invalida","mensagem":"Informe um código-fonte antes de solicitar a análise."}
```

Nessas falhas não há resultado de scanner (`sucesso`, `tokens` e `erros` não são incluídos). HTTP 500 apresenta somente mensagem genérica, sem detalhes internos. O frontend distingue falha de comunicação, entrada inválida, erro léxico e falha interna; valida a estrutura das listas antes de renderizar.

## Compatibilidade e limites

Os campos `recebido`, contagens e rota da Etapa 2 foram preservados; a mensagem de sucesso agora descreve a análise léxica. Clientes devem usar `sucesso` para o resultado léxico, não apenas `recebido`. Nenhum resultado desta etapa comprova estrutura sintática ou significado corretos. O contrato do parser será especificado na Etapa 4.
