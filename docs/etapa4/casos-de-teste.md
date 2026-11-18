# Casos de teste — protocolo 1.0, Etapa 4

Todos os casos são de elaboração do projeto a partir da gramática e dos requisitos. **Nenhum resultado observado foi preenchido.** V01–V12, L01–L03, S01–S10 e B01–B08 estão pendentes para a implementação; M01–M03 são futuros, fora da aceitação da Etapa 4. Para entradas representadas por instrução de geração, a fixture JSON preserva quantidade e conteúdo, evitando alterações na montagem.

## Programas válidos

| ID | Entrada ou construção | Resultado esperado |
|:--|:--|:--|
| V01 | `int x;` | Aceitar; Programa com Declaracao sem inicializador. |
| V02 | `float x = 7.5;` | Aceitar; inicializador Literal real com lexema 7.5. |
| V03 | `int x; x = 10;` | Aceitar; Declaracao e Atribuicao em ordem. |
| V04 | `int x = 1 + 2 * 3;` | Aceitar; Binario + na raiz da expressão, * no ramo direito. |
| V05 | `int x = (1 + 2) * 3;` | Aceitar; Binario * na raiz da expressão, + no ramo esquerdo. |
| V06 | `int x = 8 - 3 - 1;` | Aceitar; associatividade à esquerda: (8 - 3) - 1. |
| V07 | `int x = -2 * +3;` | Aceitar; sinais unários separados dos literais. |
| V08 | `int x; if (x >= 0) { x = 1; }` | Aceitar; Se com bloco e sem alternativa. |
| V09 | `int x; if (x != 0) { x = 1; } else { x = 2; }` | Aceitar; Se com dois blocos. |
| V10 | `{ int x; { float y; } }` | Aceitar; dois níveis de Bloco. |
| V11 | `/* início */ int x; // fim` | Aceitar; comentário não aparece como nó. |
| V12 | `{}` | Aceitar um bloco vazio como item do programa. |

## Erros léxicos

| ID | Entrada ou construção | Resultado esperado |
|:--|:--|:--|
| L01 | `@ int x;` | Erro léxico @ em 1:1; recuperar tokens; parser não executado e AST nula. |
| L02 | `int x=1.2.3;` | Um erro pelo literal 1.2.3 em 1:7; parser não executado. |
| L03 | `int x; /* aberto` | Erro de comentário não fechado em 1:8; parser não executado. |

## Erros sintáticos

| ID | Entrada ou construção | Resultado esperado |
|:--|:--|:--|
| S01 | `int x` | Erro em EOF (1:6): esperado ;, ou complemento compatível da declaração; AST nula. |
| S02 | `if (x > 0 { x = 1; }` | Erro em { (1:11): esperado ); AST nula. |
| S03 | `{ int x;` | Erro em EOF: esperado }; AST nula. |
| S04 | `int x = ;` | Erro em ;: esperado operando; AST nula. |
| S05 | `else { int x; }` | Erro em else: não inicia item da gramática; AST nula. |
| S06 | `int x = 1 + * 2;` | Erro em *: esperado operando; AST nula. |
| S07 | `int if;` | Erro em if (1:5): esperado identificador; AST nula. |
| S08 | `int x =` | Erro em EOF: esperado operando; AST nula. |
| S09 | `int x, y;` | Declaração múltipla fora da gramática: erro na vírgula; AST nula. |
| S10 | `while (x) { x = 1; }` | while é identificador no scanner; construção é rejeitada pelo parser. |

## Casos de borda

| ID | Entrada ou construção | Resultado esperado |
|:--|:--|:--|
| B01 | `String vazia` | HTTP 400, validação; scanner/parser não executados. |
| B02 | ` [TAB][LF] ` | HTTP 400, validação; scanner/parser não executados. |
| B03 | `/* apenas comentário */` | Sucesso léxico com zero tokens; parser informa programa vazio; AST nula. |
| B04 | 9994 espaços + int x; | 10.000 caracteres: aceitar; declaração válida. |
| B05 | 9995 espaços + int x; | 10.001 caracteres: HTTP 400 por limite de entrada. |
| B06 | 64 chaves de abertura + int x; + 64 chaves de fechamento | Aceitar no limite proposto de profundidade estrutural 64. |
| B07 | 65 chaves de abertura + int x; + 65 chaves de fechamento | Diagnóstico controlado por profundidade; sem stack trace e sem AST válida. |
| B08 | `@ int x; x = 1;` | Erro léxico; tokens válidos preservados; parser não executado apesar do sufixo válido. |

## Casos semânticos futuros

| ID | Entrada ou construção | Resultado esperado |
|:--|:--|:--|
| M01 | `x = 1;` | Na Etapa 4: estrutura válida; sem checagem de declaração. Na Etapa 5: avaliar identificador não declarado. |
| M02 | `int x; int x;` | Na Etapa 4: estrutura válida. Redeclaração só será verificada se prevista na Etapa 5. |
| M03 | `int x; x = 2.5;` | Na Etapa 4: estrutura válida. Política de compatibilidade/conversão deverá ser definida na Etapa 5. |


No CSV, entradas com tabulação/quebra de linha usam uma string JSON escapada para leitura sem ambiguidades. As entradas executáveis já materializadas estão em `tests/planejamento/etapa4-casos.json`.
