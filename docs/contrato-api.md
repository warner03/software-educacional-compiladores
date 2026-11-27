# Contrato da API — Etapa 5

## Rotas e entrada

`GET /saude` retorna HTTP 200 e `{"status":"ok"}`. `POST /analisar` é a rota FastAPI; `POST /api/analisar` é a mesma operação via nginx, usada pela interface. Entrada: objeto JSON com `codigo` string não vazia, não só espaços e com até 10.000 caracteres Unicode.

```json
{"codigo":"int x;"}
```

## Campos preservados e extensão aditiva

| Campo | Significado |
|---|---|
| `recebido` | Solicitação processada; não significa programa sem erros |
| `sucesso` | **Somente resultado léxico**, preservado por compatibilidade |
| `mensagem` | Resumo léxico; não usar como discriminador das outras fases |
| `total_caracteres` | Comprimento original em pontos de código Unicode |
| `total_linhas` | `len(codigo.splitlines())`, métrica herdada da Etapa 2 |
| `tokens` | Mesmos tokens válidos do scanner, em ordem de leitura |
| `erros` | Somente erros léxicos |
| `sintatica` | Objeto da Etapa 4, com `estado`, `sucesso`, `ast` e `erros` |
| `semantica` | Novo objeto da Etapa 5, com `estado`, `sucesso`, `tabelaSimbolos`, `escopos` e `erros` |

A API não renomeia `sintatica` para o `sintatico` ilustrativo do enunciado. Usa `semantica` de forma consistente. Clientes antigos continuam recebendo os campos originais; a interface também aceita respostas de etapas anteriores, indicando as fases indisponíveis.

## Estados e bloqueio de fases

| Situação | Léxico superior | Sintática | Semântica |
|---|---|---|---|
| Programa válido nas regras atuais | `sucesso: true` | Sucesso, AST completa | Sucesso e tabela/escopos |
| Erro semântico | `sucesso: true` | Sucesso, AST preservada | Erro, tabela das declarações reconhecidas e diagnósticos |
| Erro sintático | `sucesso: true` | Erro, AST nula | Não executada, motivo `erros_sintaticos` |
| Erro léxico | `sucesso: false` | Não executada, motivo `erros_lexicos` | Não executada, motivo `erros_lexicos` |

Em qualquer fase, `estado` é `sucesso`, `erro` ou `nao_executada`. O booleano `sucesso` é respectivamente `true`, `false` ou `null`. A AST permanece no objeto sintático; a semântica não a altera nem acrescenta campos aos nós.

Objeto semântico bloqueado por erro sintático:

```json
{"estado":"nao_executada","sucesso":null,"motivo":"erros_sintaticos","tabelaSimbolos":[],"escopos":[],"erros":[]}
```

Por erro léxico, muda somente `motivo` para `erros_lexicos`. Não chamar a semântica após erro sintático/léxico é uma decisão testada com substituição da função por uma que falharia se fosse chamada.

## Resposta completa: declaração sem leitura

`int x;` é válido semanticamente; o símbolo termina o escopo com `inicializado: false`, pois não foi atribuído nem lido. Isso não é, por si só, uma violação. Exemplo produzido pelas funções reais da aplicação:

```json
{
  "recebido": true,
  "mensagem": "Análise léxica concluída sem erros.",
  "total_caracteres": 6,
  "total_linhas": 1,
  "sucesso": true,
  "tokens": [
    {
      "tipo": "PALAVRA_RESERVADA",
      "lexema": "int",
      "linha": 1,
      "coluna": 1
    },
    {
      "tipo": "IDENTIFICADOR",
      "lexema": "x",
      "linha": 1,
      "coluna": 5
    },
    {
      "tipo": "DELIMITADOR",
      "lexema": ";",
      "linha": 1,
      "coluna": 6
    }
  ],
  "erros": [],
  "sintatica": {
    "estado": "sucesso",
    "sucesso": true,
    "ast": {
      "tipo": "Programa",
      "inicio": {
        "linha": 1,
        "coluna": 1
      },
      "fim": {
        "linha": 1,
        "coluna": 7
      },
      "comandos": [
        {
          "tipo": "Declaracao",
          "inicio": {
            "linha": 1,
            "coluna": 1
          },
          "fim": {
            "linha": 1,
            "coluna": 7
          },
          "tipoDado": "int",
          "nome": "x",
          "inicializador": null
        }
      ]
    },
    "erros": []
  },
  "semantica": {
    "estado": "sucesso",
    "sucesso": true,
    "tabelaSimbolos": [
      {
        "id": "S1",
        "nome": "x",
        "tipo": "int",
        "escopo": "E0",
        "linha": 1,
        "coluna": 5,
        "fim": {
          "linha": 1,
          "coluna": 6
        },
        "noAst": "/comandos/0",
        "inicializado": false,
        "sombreia": null,
        "referencias": []
      }
    ],
    "escopos": [
      {
        "id": "E0",
        "nome": "Global",
        "pai": null,
        "inicio": {
          "linha": 1,
          "coluna": 1
        },
        "fim": {
          "linha": 1,
          "coluna": 7
        },
        "noAst": ""
      }
    ],
    "erros": []
  }
}
```

## Exemplo de erro semântico

Para `x=1;`, léxico e sintático têm sucesso, e `semantica` é:

```json
{
  "estado": "erro",
  "sucesso": false,
  "tabelaSimbolos": [],
  "escopos": [
    {
      "id": "E0",
      "nome": "Global",
      "pai": null,
      "inicio": {
        "linha": 1,
        "coluna": 1
      },
      "fim": {
        "linha": 1,
        "coluna": 5
      },
      "noAst": ""
    }
  ],
  "erros": [
    {
      "tipo": "ERRO_SEMANTICO",
      "regra": "IDENTIFICADOR_NAO_DECLARADO",
      "lexema": "x",
      "linha": 1,
      "coluna": 1,
      "fim": {
        "linha": 1,
        "coluna": 2
      },
      "noAst": "/comandos/0/alvo",
      "simboloId": null,
      "mensagem": "O identificador 'x' não foi declarado antes deste uso no escopo atual nem nos escopos externos.",
      "sugestao": "Declare a variável antes de usá-la e confira se ela está visível neste bloco."
    }
  ]
}
```

`regra` identifica uma das sete regras documentadas em [semantica.md](semantica.md). Mensagens/sugestões são textos didáticos; clientes devem usar discriminadores, não comparar toda a redação. `noAst` é um caminho para a construção na AST original; raiz vazia, por exemplo `/comandos/0/alvo`. `simboloId` é o ID conhecido ou `null`. `lexema` é o nome/operador associado, não necessariamente todo o intervalo de uma expressão composta.

A tabela usa IDs estáveis na análise, nome, tipo, escopo, posição do identificador declarado, garantia de inicialização ao fim do escopo, vínculo de sombreamento e referências. Escopos informam pai e intervalo. Posições são baseadas em 1, fim exclusivo, CRLF/CR normalizados para LF e Unicode por ponto de código; tab conta uma coluna. O fonte é mantido para seleção coerente.

## HTTP e falhas

| Situação | HTTP | Campo `erro` |
|---|---|---|
| Corpo não JSON/objeto ou `codigo` ausente | 400 | `requisicao_invalida` |
| Tipo errado, vazio, só espaços ou acima do limite | 400 | `entrada_invalida` |
| Programa analisado, com ou sem erro léxico/sintático/semântico | 200 | Resultados por fase |
| Exceção interna inesperada | 500 | `erro_interno`, mensagem genérica |

Falhas de entrada/servidor preservam `{"recebido":false,"erro":"...","mensagem":"..."}` sem resultados de análises. Stack traces ficam fora da resposta. Comentários sozinhos geram erro sintático de programa vazio; `{}` é válido e não declara símbolos. EOF permanece interno ao parser, ausente da lista pública de tokens.

Os limites do parser (64 níveis, 2.000 nós, altura 128) geram diagnóstico sintático controlado e bloqueiam a semântica. As regras atuais não equivalem a C completo, execução ou geração de código. A representação semântica ampliada fica para a Etapa 6.
