# Mini-C — análise semântica da Etapa 5

Implementação em `backend/app/semantica.py`: percurso único da AST válida, com pilha de dicionários de escopos, conjunto de variáveis definitivamente inicializadas e listas de símbolos/escopos para apresentação. O scanner, o parser e a AST das etapas anteriores não foram alterados. A política foi fixada antes do código em [decisoes.md](trabalho5/decisoes.md).

## Regras implementadas

| Regra | Verificação e diagnóstico |
|---|---|
| Declaração antes do uso | Busca do bloco atual para os externos. Ausência: `IDENTIFICADOR_NAO_DECLARADO` |
| Redeclaração | Nome repetido no mesmo escopo: `REDECLARACAO_NO_ESCOPO`; manter símbolo anterior |
| Escopos e sombreamento | Cada `{}` abre escopo; nomes locais saem de visibilidade ao fechar. Nome interno pode sombrear externo |
| Inicialização na leitura | Exigir atribuição/inicialização válida antes da leitura: `VARIAVEL_NAO_INICIALIZADA` |
| Compatibilidade | Tipos iguais ou promoção de `int` para `float`; rejeitar outros casos: `TIPOS_INCOMPATIVEIS` |
| Aritmética e unários | `+ - * /` e sinais unários exigem números: `OPERANDOS_NAO_NUMERICOS` |
| Comparações | Relações ordenadas exigem números; igualdade também aceita dois `bool`: `TIPOS_NAO_COMPARAVEIS` |
| Condição | `if` exige resultado `bool`: `CONDICAO_NAO_BOOLEANA` |

Os tipos declarados são `int` e `float`. Comparações produzem o tipo interno `bool`, que não foi acrescentado à gramática como tipo de variável. Operações numéricas com um `float` produzem `float`; dois `int` produzem `int`, inclusive em divisão. Isso é inferência de **tipo**, não cálculo do valor.

Este Mini-C exige comparação na condição: `if (x != 0) {}` é válido quando `x` está declarado/inicializado. `if (x) {}` é sintaticamente reconhecido, mas semanticamente rejeitado para `int`/`float`. Essa escolha é explícita e difere da conversão numérica de C completo. `int x = 1 < 2;` também é rejeitado: não há conversão implícita de `bool` para número.

## Inicialização e fluxo

Uma declaração sem inicializador é válida se não houver leitura prematura. O nome entra no escopo antes do seu inicializador: `int x = x;` refere-se ao próprio `x`, ainda não inicializado. Em um bloco que sombreia um `x` externo, o inicializador também enxerga o novo nome local.

Uma atribuição compatível acrescenta o símbolo ao conjunto inicializado. Expressões inválidas não inicializam uma variável nova. Atribuir a uma variável não exige valor anterior; ler o seu lado direito exige. Exemplos:

```c
int x; x = 1; int y = x; // válido
int a; int b = a;        // leitura sem inicialização
```

Nos ramos do `if`, cada caminho parte do estado anterior. Depois, conserva-se a interseção dos estados de saída; sem `else`, o caminho que não entra no bloco também é considerado. Blocos comuns propagam atribuições a nomes externos. IDs de variáveis locais são retirados do estado ao fechar o escopo; suas informações continuam arquivadas na tabela.

```c
int x;
if (1 < 2) { x = 1; } else { x = 2; }
int y = x; // inicialização garantida nos dois caminhos
```

Sem `else`, essa leitura é rejeitada. Condições constantes não são avaliadas; a análise é conservadora. O campo `inicializado` apresentado na tabela indica a garantia ao **fim do escopo que declarou o símbolo**, não o estado em cada ponto intermediário nem o valor em execução.

## Tabela de símbolos e escopos

`semantica.escopos` contém `id`, `nome`, `pai`, `inicio`, `fim` e `noAst`. O global é `E0`; cada bloco recebe outro ID determinístico. O filtro da interface mostra todos os escopos ou um escolhido, inclusive blocos já fechados, para estudo.

Cada item de `semantica.tabelaSimbolos` contém:

| Campo | Significado |
|---|---|
| `id` | ID determinístico `S1`, `S2`, ... |
| `nome`, `tipo`, `escopo` | Nome declarado, `int`/`float` e ID do escopo |
| `linha`, `coluna`, `fim` | Intervalo do **identificador declarado**, não da palavra `int`/`float` |
| `noAst` | Caminho do nó `Declaracao` na AST original |
| `inicializado` | Garantia ao fim do escopo, conforme a análise de caminhos |
| `sombreia` | ID do símbolo externo sombreado ou `null` |
| `referencias` | Leituras/atribuições com linha, coluna, fim, `noAst` e `contexto` |

A posição do nome declarado vem dos tokens originais: a AST guarda o nome como atributo de `Declaracao`. Não foi necessário modificar seu esquema. As referências apontam para folhas `Identificador`; nomes iguais em escopos diferentes são ligados ao ID visível correto.

Os caminhos `noAst` usam raiz vazia e componentes como `/comandos/0` ou `/comandos/1/valor/esquerda`. São metadados de ligação, não uma nova árvore anotada da Etapa 6. Todos os intervalos seguem início inclusivo/fim exclusivo, linha/coluna baseadas em 1, CRLF/CR normalizados para LF e Unicode por ponto de código; tab conta uma coluna.

## Erros, sugestões e preservação das fases

Semântica só é chamada se o scanner e o parser tiverem sucesso. Quando bloqueada, a API informa `nao_executada`, causa léxica/sintática e listas vazias. Entrada inválida continua HTTP 400; análise concluída com erro da linguagem continua HTTP 200. `sucesso` superior permanece léxico; o novo resultado está em `semantica`.

Cada diagnóstico contém `tipo: ERRO_SEMANTICO`, `regra`, `lexema` associado (nome/operador), `linha`, `coluna`, `fim`, `noAst`, `simboloId` quando identificado, `mensagem` e `sugestao`. A seleção destaca o intervalo do problema e marca a construção correspondente. Um link permite ir diretamente ao código destacado.

As violações independentes são acumuladas. Um identificador inexistente ou leitura inválida propaga tipo desconhecido, evitando inventar incompatibilidades adicionais em seus pais. Redeclarações não substituem o primeiro símbolo; o inicializador duplicado ainda é inspecionado para outros problemas.

Uma análise semântica com erro preserva tokens e AST reconhecidos. A tabela contém as declarações válidas reconhecidas durante o percurso e é identificada como resultado de análise com erros; não prova que o programa seja semanticamente válido ou executável.

## Exemplos

| Entrada | Resultado semântico |
|---|---|
| `int x=1; float y=x+2.5;` | Válido; promoção numérica |
| `int x;` | Válido, sem leitura; inicialização não garantida |
| `x=1;` | Identificador não declarado |
| `int x; int x;` | Redeclaração no mesmo escopo |
| `int x; x=2.5;` | `float` incompatível com `int` |
| `int x; int y=x;` | Leitura sem inicialização |
| `{int x=1;} x=2;` | Nome fora de visibilidade |
| `int x=1; {float x=2.0;}` | Sombreamento válido |
| `int x=(1<2)+3;` | Operando `bool` em aritmética |

## Limites e continuidade

Não há funções, argumentos/retorno, laços, vetores, ponteiros, casts, avaliação de valores, divisão por zero, overflow, execução ou geração de código. O fluxo verificado é somente o permitido pela gramática atual, incluindo `if/else` e blocos; não é uma análise geral de fluxo arbitrário. Os limites herdados (10.000 caracteres, 64 níveis, 2.000 nós, altura 128) continuam aplicados antes da semântica.

A representação semântica ampliada e outras experiências didáticas ficam para a Etapa 6. Casos, comandos, resultados e limites da validação estão em [registro-de-testes.md](registro-de-testes.md); acessibilidade em [acessibilidade.md](acessibilidade.md).
