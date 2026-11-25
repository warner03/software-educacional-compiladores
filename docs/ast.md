# AST — formato e visualização

A sequência de tokens registra unidades em ordem de leitura. Uma árvore de derivação registraria terminais e não terminais das produções. A **árvore sintática abstrata (AST)** desta aplicação guarda construções e relações essenciais: não tem nós de pontuação, comentários ou parênteses, nem nós intermediários `aditiva`/`multiplicativa`.

## Esquema JSON

Todo nó contém `tipo`, `inicio` e `fim`. Posições usam `{ "linha": 1, "coluna": 1 }`, com início inclusivo e fim exclusivo, a partir de 1. CRLF e CR são normalizados para LF; Unicode conta por ponto de código; tab conta uma coluna. São as mesmas convenções do scanner, não índices UTF-16 do JavaScript.

| `tipo` | Atributos específicos e filhos |
|---|---|
| `Programa` | `comandos`: lista ordenada, não vazia, de itens |
| `Declaracao` | `tipoDado`: `int`/`float`; `nome`: string; `inicializador`: expressão ou `null` |
| `Atribuicao` | `alvo`: nó `Identificador`; `valor`: expressão |
| `Bloco` | `comandos`: lista ordenada de itens, possivelmente vazia |
| `Se` | `condicao`: expressão; `entao`: `Bloco`; `senao`: `Bloco` ou `null` |
| `Binario` | `operador`; `esquerda` e `direita`: expressões |
| `Unario` | `operador`: `+`/`-`; `operando`: expressão |
| `Identificador` | `nome`: string |
| `Literal` | `categoria`: `inteiro`/`real`; `lexema`: string original, por exemplo `7.50` |

Itens são `Declaracao`, `Atribuicao`, `Se` e `Bloco`; expressões são `Binario`, `Unario`, `Identificador` e `Literal`. Filhos opcionais usam `null`; listas vazias usam `[]`. Números não são convertidos nem avaliados: preserva-se o texto, inclusive zeros iniciais. O nome declarado é atributo de `Declaracao`, e o alvo de atribuição é um nó explícito, como no plano da Tarefa 4.

Uma declaração e uma atribuição abrangem até depois de `;`; um bloco abrange suas chaves; `Se` abrange do `if` até depois da última chave. Programa abrange do primeiro ao último item, sem comentários externos. Folhas apontam para o lexema exato da tabela de tokens. Ao usar uma expressão agrupada como operando, o intervalo do **pai** inclui os parênteses, sem criar um nó extra ou mudar a posição das folhas. Assim, em `(1 + 2) * 3`, a multiplicação cobre a expressão inteira e a folha `1` continua apontando somente para `1`.

Exemplo completo, entrada `int x = 5;`:

```json
{
  "tipo": "Programa",
  "inicio": {"linha": 1, "coluna": 1},
  "fim": {"linha": 1, "coluna": 11},
  "comandos": [{
    "tipo": "Declaracao",
    "inicio": {"linha": 1, "coluna": 1},
    "fim": {"linha": 1, "coluna": 11},
    "tipoDado": "int",
    "nome": "x",
    "inicializador": {
      "tipo": "Literal",
      "inicio": {"linha": 1, "coluna": 9},
      "fim": {"linha": 1, "coluna": 10},
      "categoria": "inteiro",
      "lexema": "5"
    }
  }]
}
```

Referência estrutural simplificada para `int resultado = 10 + 5 * 2;` (as posições continuam presentes no JSON real):

```text
Programa
└── Declaracao: int resultado
    └── Binario: +
        ├── Literal inteiro: 10
        └── Binario: *
            ├── Literal inteiro: 5
            └── Literal inteiro: 2
```

Três subárvores de referência independentes foram fixadas antes do parser em `tests/planejamento/etapa4-ast-referencias.json`; os testes comparam estrutura sem posições e verificam posições separadamente. Os esperados não foram gerados pelo parser avaliado.

## Interface e acessibilidade

A interface usa árvore hierárquica com `details`/`summary` nativos, rótulos por escrito e cores auxiliares. Enter ou Espaço abre/fecha um resumo focado; botões usam navegação padrão por Tab. Há controles para expandir/recolher tudo e baixar `mini-c-ast.json`. As regras exibidas explicam os tipos de construção; não representam um registro completo da derivação.

`Localizar` marca o intervalo do nó no **mesmo fonte enviado** e anuncia início/fim. A tabela continua mostrando os tokens originais. `Destacar token atual`, `Token anterior` ou `Próximo token` retomam o destaque individual. Editar o fonte ou trocar o exemplo elimina resultados antigos e descarta respostas de solicitações anteriores.

A árvore e a tabela têm rolagem própria; telas pequenas usam uma coluna. A entrada e a AST têm os limites documentados na gramática. O frontend valida o formato, tipos de nó, posições e limites antes de renderizar. Todo texto é inserido como texto, sem interpretação HTML. Respostas antigas da Etapa 3 ainda exibem os tokens e informam explicitamente a ausência da análise sintática.

Essa visualização percorre uma AST **já construída**. Não há animação de construção, filtro por tipo de nó, árvore de derivação ou simulação passo a passo do parser. Não houve avaliação de aprendizagem com participantes nem auditoria completa de acessibilidade.
