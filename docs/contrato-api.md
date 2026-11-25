# Contrato da API — Etapa 4

## Rotas e entrada

- `GET /saude`: HTTP 200, `{"status":"ok"}`.
- `POST /analisar`: FastAPI direto; `POST /api/analisar`: mesma operação pelo nginx.
- Requisição: objeto JSON com `codigo` string não vazia, não composta somente por espaços, com no máximo 10.000 caracteres Unicode. Sem autenticação/banco/credenciais exigidas.

```json
{"codigo":"int x;"}
```

## Resposta processada — HTTP 200

Campos das etapas anteriores preservados, com o mesmo significado:

| Campo | Significado |
|---|---|
| `recebido` | Solicitação processada; não indica correção do programa |
| `sucesso` | **Somente léxico:** `true` se e somente se `erros` está vazio |
| `mensagem` | Resumo da análise léxica, preservado por compatibilidade; não usar como discriminador lógico |
| `total_caracteres` | Tamanho original da string em pontos de código Unicode |
| `total_linhas` | `len(codigo.splitlines())`, métrica informativa herdada da Etapa 2 |
| `tokens` | Tokens válidos em ordem de leitura, sem alteração pelo parser |
| `erros` | Erros **léxicos**, sem mistura com diagnósticos sintáticos |
| `sintatica` | Novo objeto com estado, sucesso, AST e erros sintáticos |

Token: `{"tipo":"IDENTIFICADOR","lexema":"x","linha":1,"coluna":5}`. Tipos: `PALAVRA_RESERVADA`, `IDENTIFICADOR`, `LITERAL_INTEIRO`, `LITERAL_REAL`, `OPERADOR`, `DELIMITADOR`. EOF é interno ao parser e nunca aparece nessa lista. Comentários/espaços também não aparecem.

Linha/coluna começam em 1; tab conta uma coluna; CRLF/CR são normalizados para LF pelos analisadores. A métrica `total_linhas` preserva `splitlines()` e pode diferir da posição EOF de um texto terminado em quebra; use as posições dos tokens/nós para localizar trechos.

### Sucesso léxico e sintático

Resposta completa para `int x;`:

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
  "erros": [],
  "sintatica": {
    "estado": "sucesso",
    "sucesso": true,
    "ast": {
      "tipo": "Programa",
      "inicio": {"linha":1,"coluna":1},
      "fim": {"linha":1,"coluna":7},
      "comandos": [{
        "tipo": "Declaracao",
        "inicio": {"linha":1,"coluna":1},
        "fim": {"linha":1,"coluna":7},
        "tipoDado": "int", "nome": "x", "inicializador": null
      }]
    },
    "erros": []
  }
}
```

### Falha sintática

Para `int x`, os campos léxicos continuam com `sucesso: true`, dois tokens e `erros: []`. O novo campo é:

```json
{
  "estado": "erro",
  "sucesso": false,
  "ast": null,
  "erros": [{
    "tipo": "ERRO_SINTATICO",
    "codigo": "gramatica",
    "lexema": "",
    "linha": 1, "coluna": 6,
    "esperado": [";"],
    "encontrado": "EOF",
    "mensagem": "Era esperado ';' ao final da declaração. Declare uma variável por instrução. Encontrado: o fim do código."
  }]
}
```

`encontrado` guarda o **tipo** do token; `lexema` guarda seu texto, vazio no EOF; `esperado` é uma lista de lexemas ou nomes de categorias. `codigo` pode ser `gramatica`, `limite_profundidade`, `limite_nos` ou `limite_altura`. Mensagens são texto didático e podem melhorar sem mudar os discriminadores. AST parcial nunca é devolvida como válida.

### Falha léxica: parser não executado

Para `@ int x;`, os tokens válidos permanecem e o nível superior tem `sucesso: false` e erro léxico `@` em 1:1. `sintatica` é exatamente:

```json
{
  "estado": "nao_executada",
  "sucesso": null,
  "motivo": "erros_lexicos",
  "ast": null,
  "erros": []
}
```

O parser não é chamado: tokens recuperados podem estar incompletos e não devem produzir diagnósticos ou uma AST enganosa. Comentários sozinhos são lexicalmente válidos, mas geram erro **sintático** de programa vazio. Um bloco vazio `{}` é sintaticamente válido.

## Falhas de entrada e servidor

| Situação | HTTP | Campo `erro` |
|---|---|---|
| JSON inválido, corpo não objeto, `codigo` ausente | 400 | `requisicao_invalida` |
| Tipo errado, vazio, só espaços ou acima de 10.000 caracteres | 400 | `entrada_invalida` |
| Falha interna inesperada | 500 | `erro_interno` |

```json
{"recebido":false,"erro":"entrada_invalida","mensagem":"Informe um código-fonte antes de solicitar a análise."}
```

Nesses casos não há resultado de scanner/parser. HTTP 500 retorna mensagem genérica, sem stack trace ou caminhos internos. Erros no programa e limites sintáticos são resultados processados com HTTP 200, não falhas do servidor. A interface distingue comunicação, entrada, léxico e sintático.

## Compatibilidade e limites

Usa-se o nome `sintatica`, conforme a proposta da Tarefa 4; o `sintatico` do enunciado era ilustrativo. A extensão é aditiva: clientes da Etapa 3 podem ignorá-la e continuam recebendo seus campos originais. O frontend aceita respostas antigas sem esse objeto e informa que a sintaxe está indisponível; a API atual sempre o envia após análise válida da entrada.

A API e a AST não comprovam significado correto. Limites de 64 níveis estruturais, 2.000 nós e altura 128, recuperação e construções aceitas estão em [gramatica.md](gramatica.md). Nós e convenções de intervalo estão em [ast.md](ast.md). A semântica será implementada na Etapa 5.
