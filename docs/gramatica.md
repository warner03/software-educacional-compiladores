# Mini-C — gramática e parser da Etapa 4

Gramática implementada sem alterar o recorte proposto na Tarefa 4. Símbolo inicial: **`programa`**. A [EBNF original](etapa4/gramatica.ebnf) permanece como registro histórico; a versão executada é:

```ebnf
programa       = item, { item }, EOF ;
item           = declaracao | atribuicao | condicional | bloco ;
declaracao     = tipo, IDENTIFICADOR, [ "=", expressao ], ";" ;
tipo           = "int" | "float" ;
atribuicao     = IDENTIFICADOR, "=", expressao, ";" ;
condicional    = "if", "(", expressao, ")", bloco, [ "else", bloco ] ;
bloco          = "{", { item }, "}" ;
expressao      = igualdade ;
igualdade      = relacional, { ( "==" | "!=" ), relacional } ;
relacional     = aditiva, { ( "<" | ">" | "<=" | ">=" ), aditiva } ;
aditiva        = multiplicativa, { ( "+" | "-" ), multiplicativa } ;
multiplicativa = unaria, { ( "*" | "/" ), unaria } ;
unaria         = ( "+" | "-" ), unaria | primaria ;
primaria       = IDENTIFICADOR | LITERAL_INTEIRO | LITERAL_REAL
               | "(", expressao, ")" ;
```

Aspas representam terminais literais; `,` fora das aspas significa concatenação; `{ ... }` significa zero ou mais repetições; `[ ... ]`, parte opcional; `|`, alternativa. Chaves e parênteses **entre aspas** são caracteres do programa. Todos os nomes minúsculos à esquerda de `=` são não terminais. EOF representa o fim da entrada.

## Correspondência com o scanner

O parser recebe a **mesma lista** produzida por `analisar_lexico`, sem adicionar ou modificar tokens. Distingue símbolos pelo lexema e identificadores/números pelo tipo. O marcador EOF é criado somente dentro do parser, na posição após o último caractere do fonte normalizado, incluindo comentários/espaços finais.

| Terminal da gramática | Tipo de token JSON da Etapa 3 | Distinção |
|---|---|---|
| `int`, `float`, `if`, `else` | `PALAVRA_RESERVADA` | Lexema exato, minúsculo |
| `IDENTIFICADOR` | `IDENTIFICADOR` | Mesmo identificador ASCII do scanner |
| `LITERAL_INTEIRO` | `LITERAL_INTEIRO` | `[0-9]+` |
| `LITERAL_REAL` | `LITERAL_REAL` | `[0-9]+\.[0-9]+` |
| `=`, `+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, `<=`, `>=` | `OPERADOR` | Lexema exato |
| `(`, `)`, `{`, `}`, `;` | `DELIMITADOR` | Lexema exato |
| EOF | Marcador interno `EOF` | Ausente de `tokens` na API |

A vírgula continua sendo um `DELIMITADOR` reconhecido lexicalmente, mas **não pertence às produções sintáticas**: `int x, y;` é rejeitado. Comentários e espaços não produzem tokens. Nenhuma mudança foi necessária em `scanner.py`.

## Precedência e associatividade

| Da maior à menor precedência | Operadores | Associatividade |
|---|---|---|
| Agrupamento | `( expressão )` | Determinado pelos parênteses |
| Unários | `+`, `-` | Direita |
| Multiplicação/divisão | `*`, `/` | Esquerda |
| Adição/subtração | `+`, `-` | Esquerda |
| Relações | `<`, `>`, `<=`, `>=` | Esquerda |
| Igualdade | `==`, `!=` | Esquerda |

`=` é parte da declaração ou atribuição, não operador de expressão. Relações encadeadas são aceitas segundo a associação acima, sem avaliar seu significado ou recomendar seu uso.

| Entrada | Estrutura esperada da expressão |
|---|---|
| `int x = 10 + 5 * 2;` | `+(10, *(5, 2))` |
| `int x = 20 - 5 - 3;` | `-(-(20, 5), 3)` |
| `int x = (10 + 5) * 2;` | `*(+(10, 5), 2)` |
| `int x = - +2 * 3;` | `*(unário-(unário+(2)), 3)` |

Os exemplos são oráculos estruturais, não execução numérica do programa.

## Construções e limites

Aceita declarações de **uma** variável `int` ou `float`, com inicialização opcional; atribuições a identificadores; expressões; `if` com `else` opcional; blocos vazios ou com itens; combinações aninhadas dessas construções. Chaves são obrigatórias em ambos os ramos. Um programa precisa de ao menos um item: comentários sozinhos geram diagnóstico de programa vazio; `{}` é válido.

Não aceita funções, chamadas, `return`, laços, vetores, ponteiros, strings, operadores lógicos, incremento, atribuição composta ou dentro de expressão, declarações múltiplas, comando vazio `;` ou `else if` sem bloco intermediário. `while` e `return` são identificadores lexicalmente; seus comandos não são reconhecidos. O nome `while` ainda pode ser usado como variável nesse recorte.

Limites operacionais, definidos no [protocolo 1.1](trabalho4/decisoes.md):

- Entrada de até **10.000 caracteres Unicode**, validada antes do scanner (HTTP 400 se excedida).
- Até **64** níveis simultâneos de blocos, parênteses ou sinais unários. Parênteses da condição de `if` também contam durante a condição.
- Até **2.000 nós construídos**, incluindo raiz, e altura da AST de até **128** nós no maior caminho. Agrupamentos não adicionam nós; cadeias binárias aumentam a altura.

Ultrapassar um limite sintático retorna HTTP 200, `sintatica.estado: "erro"`, AST nula e diagnóstico com `codigo` iniciado por `limite_`. Os tokens continuam disponíveis. Não se trata de alteração na gramática abstrata; são limites de segurança de execução/serialização/interface.

## Estratégia, tecnologia e recuperação

Implementação manual em [parser.py](../backend/app/parser.py), com descida recursiva e um token de antecipação. Cada família de construções tem uma função; laços por nível de expressão eliminam recursão à esquerda e constroem operadores binários pela esquerda. Sinais unários são coletados iterativamente e aplicados de trás para frente. Não há gerador de parser nem dependências novas.

Essa estratégia permite relacionar EBNF, funções e nós de forma direta, usando o Python/FastAPI existente. Exige manutenção manual das regras e diagnósticos; não produz tabelas FIRST/FOLLOW, árvore de derivação ou animação dos passos do algoritmo.

O endpoint só chama o parser quando a lista de erros léxicos está vazia. Tokens recuperados após erro léxico continuam sendo apresentados, mas não geram uma árvore potencialmente enganosa. Em qualquer erro sintático, a resposta contém **AST nula**; a estrutura parcial interna é descartada.

O modo pânico descarta tokens até `;` (consumido) ou `}`. Dentro de bloco, a chave fica para a função que o abriu; no nível superior, a chave avulsa é consumida. EOF termina a recuperação. Isso garante avanço, permite apontar erros independentes e evita loops. Não garante listar todos os problemas: uma instrução correta pode ser descartada junto da defeituosa, e delimitadores ausentes podem causar diagnósticos adicionais. Limites de recursos encerram imediatamente a análise.

| Entrada inválida | Primeiro diagnóstico esperado |
|---|---|
| `int x` | EOF, coluna 6; esperado `;` |
| `if (x > 0 { x = 1; }` | `{`, coluna 11; esperado `)` |
| `{ int x;` | EOF; esperado `}` e indicação do bloco aberto |
| `int x = ;` | `;`, coluna 9; esperado operando |
| `else {}` | `else` sem `if` correspondente |
| `int x = 1 + * 2;` | `*` onde deveria haver operando |
| `int if;` | Palavra reservada onde deveria haver identificador |

`int a = ;\nint b;\nb = ;` gera dois erros independentes em 1:9 e 3:5. Mensagens trazem encontrado, esperado e localização; detalhes internos ficam fora da resposta.

## Fronteira semântica

`x = 1;`, `int x; int x;` e `int x; x = 2.5;` continuam sintaticamente válidos. A [semântica da Etapa 5](semantica.md) agora identifica, respectivamente, nome não declarado, redeclaração e tipos incompatíveis. O parser permanece responsável somente pela estrutura; sua AST não é alterada pelo analisador semântico. Condições numéricas podem ser reconhecidas sintaticamente e rejeitadas pela política semântica, que exige resultado `bool`.
