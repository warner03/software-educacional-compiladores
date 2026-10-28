# Mini-C — Especificação léxica da Etapa 3

## Objetivo e tecnologia

Scanner manual em Python, módulo `backend/app/scanner.py`, função `analisar_lexico(codigo)`. Recebe uma string e retorna `sucesso`, `tokens` e `erros`. Não há bibliotecas novas na aplicação. Um percurso explícito facilita ensinar classificação, precedência de reconhecimento, posição e recuperação, reutilizando FastAPI em vez de introduzir outra tecnologia.

A função é robusta a string vazia, espaços e comentários; o endpoint aplica antes as validações da Etapa 2 e rejeita texto vazio ou só espaços. Um texto com apenas comentários é válido lexicalmente e produz zero tokens.

## Categorias reconhecidas

| Tipo JSON | Formação | Exemplos |
|---|---|---|
| `PALAVRA_RESERVADA` | Correspondência exata, minúscula | `int float if else` |
| `IDENTIFICADOR` | `[A-Za-z_][A-Za-z0-9_]*` | `x _x1 numero media2` |
| `LITERAL_INTEIRO` | `[0-9]+` | `0 42 001` |
| `LITERAL_REAL` | `[0-9]+\.[0-9]+` | `7.5 0.0 12.003` |
| `OPERADOR` | Aritmético, atribuição ou relacional do recorte | `+ - * / = == != < > <= >=` |
| `DELIMITADOR` | Símbolos listados, reconhecidos isoladamente | `( ) { } ; ,` |
| `ERRO_LEXICO` | Trecho não reconhecido ou explicitamente fora do recorte | `@`, `12abc`, `/* sem fechamento` |

Reservadas exigem palavra inteira: `ifelse` e `INT` são identificadores. Nomes como `while`, `return` e `printf` também são identificadores; o scanner não conhece declarações nem restringe nomes pela semântica. Reconhecê-los não significa implementar comandos ou funções de C.

## Ordem de reconhecimento

1. Ignorar espaços e comentários.
2. Agrupar identificadores e distinguir as quatro palavras reservadas.
3. Agrupar candidatos a número e verificar o formato completo.
4. Agrupar literais entre aspas como erros (fora do recorte).
5. Identificar operadores compostos explicitamente não suportados.
6. Reconhecer operadores de dois caracteres antes dos simples.
7. Reconhecer delimitadores; reportar outros caracteres como erro.

Comentários têm prioridade sobre `/`; divisão não é confundida com comentário. Operadores compostos reconhecidos usam o maior comprimento disponível: `>=` é um token, não dois. `-10` resulta em `-` e `10`, pois o sinal será interpretado pelo parser.

## Números malformados e limites

Inteiros com zeros iniciais não são interpretados como octais; nesta etapa apenas se registra o lexema. Não há expoentes, sufixos, hexadecimal, `.5` ou `1.`. `12abc`, `1.2.3`, `1e-3` e `0x10` geram um erro por candidato numérico, e não tokens que ocultariam o problema. Letras ASCII, dígitos, `_` e pontos adjacentes são consumidos como parte desse candidato; um sinal imediatamente depois de `e` ou `E` também é consumido para reportar a tentativa de expoente em conjunto.

O scanner reconhece explicitamente como fora do recorte os operadores `++ -- += -= *= /= %= && || << >> -> &= |= ^=`. Por exemplo, `x++` produz um erro para `++`; `x + + 1` possui dois operadores separados e não gera erro léxico, embora sua estrutura ainda dependa do parser. `!` isolado, `%`, `&`, `|`, `^`, `~`, `.` isolado e colchetes são caracteres não reconhecidos. O fato de um símbolo pertencer à linguagem C completa não o torna parte desta Mini-C.

## Comentários e posições

- `//` ignora até LF ou fim do arquivo; a quebra continua sendo contada.
- `/* ... */` ignora até o primeiro fechamento. Não há aninhamento.
- Espaços ASCII, tabs, LF, tab vertical e form feed não geram tokens.
- CRLF e CR são normalizados para LF pelo scanner. Trechos de erro que abrangem linhas são apresentados com essa normalização.
- Linha e coluna começam em 1; coluna representa caracteres Unicode, não bytes. Tab conta uma coluna (não a distância visual de um editor).
- As posições contam também caracteres ignorados, inclusive os de comentários. A interface usa a mesma normalização para localizar os tokens.
- Caracteres Unicode não ASCII em identificadores ou fora de comentários/aspas produzem erro. Uma string Unicode inválida pode produzir mais de um erro; nomes válidos ao redor continuam reconhecidos.

## Recuperação e mensagens

- Símbolo desconhecido: registrar sua localização e consumir um caractere.
- Operador não suportado ou número malformado: registrar o trecho agrupado, depois continuar a partir do próximo caractere não consumido.
- Aspas: strings e literais de caractere não são suportados. Consome-se até a aspa correspondente, quebra de linha ou EOF; escapes são atravessados apenas para localizar o fim, não para aceitar o literal. O trecho gera um erro didático e a leitura continua.
- Comentário de bloco sem fechamento: registrar um erro desde `/*` até EOF; não é possível decidir com segurança se os trechos seguintes eram código ou comentário.

Mensagem e localização são dados de usuário apresentados como texto, não como HTML. A API não devolve stack traces; falhas internas geram a mensagem genérica da Etapa 2. A resposta conserva todos os tokens válidos reconhecidos e a lista de erros.

## Exemplo completo

Entrada:

```c
int numero = 10;
```

| Tipo | Lexema | Linha | Coluna |
|---|---|---|---|
| PALAVRA_RESERVADA | int | 1 | 1 |
| IDENTIFICADOR | numero | 1 | 5 |
| OPERADOR | = | 1 | 12 |
| LITERAL_INTEIRO | 10 | 1 | 14 |
| DELIMITADOR | ; | 1 | 16 |

Entrada com erro e recuperação:

```c
int x=12abc;
@ float y=7.5;
```

Erros: `12abc` na linha 1, coluna 7, e `@` na linha 2, coluna 1. A saída também contém `int`, `x`, `=`, `;`, `float`, `y`, `=`, `7.5` e `;`, em ordem.

## Fronteira com a Etapa 4

`int = ;` não tem erro léxico: suas unidades são reconhecidas. Declarações, uso de vírgula, balanceamento de delimitadores, precedência, tipo de expressão em condicionais e ordem de comandos serão definidos e verificados pela gramática e pelo parser. Nesta etapa não há tabela de símbolos, checagem de tipos, AST ou execução. Os tokens já preservam posições para futuros diagnósticos sintáticos.
