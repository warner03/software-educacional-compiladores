# Trabalho 5 — decisões anteriores à implementação

Definição em 26/11/2026, base `0637b7d`. O artigo/formulário da Tarefa 5 serão revisados depois desta entrega prática. Esta alteração implementa semântica e acessibilidade no software, sem reescrever resultados humanos ou o planejamento histórico.

## Regras Mini-C escolhidas

- Percurso único da AST em Python; scanner, parser e formato da AST preservados. A API acrescenta `semantica`, mantendo `sucesso` superior como resultado exclusivamente léxico.
- Declaração antes do uso; entrada do nome no escopo antes de analisar seu inicializador. `int x = x;` encontra `x`, mas acusa uso sem inicialização. Não permitir redeclaração no mesmo escopo; permitir sombreamento em bloco interno. Busca do escopo interno para o externo; nomes locais deixam de ser visíveis ao sair do bloco.
- Tipos declarados `int` e `float`; tipo interno `bool` produzido por comparações, sem ampliar a gramática. Aritmética/unários exigem números. Operações numéricas mistas produzem `float`; divisão de dois `int` tem tipo `int`. Relações ordenadas exigem números; igualdade aceita dois números ou dois booleanos.
- Atribuições/inicializadores aceitam tipos iguais ou promoção `int` para `float`. Rejeitar `float` para `int` e `bool` para números. Não executar cálculos, conversões, divisão ou programa.
- Condição de `if` deve ter tipo interno `bool`: usar comparação, por exemplo `x != 0`, em vez de `if (x)`. Essa escolha explícita do Mini-C difere da conversão numérica de C completo e não muda o reconhecimento sintático.
- Verificar inicialização definida na leitura. Uma atribuição válida inicializa a variável. Em `if/else`, somente inicializações presentes em ambos os caminhos permanecem garantidas depois da condicional; sem `else`, considerar também o caminho que não executa o bloco. Não inferir condições constantes. Blocos comuns propagam atribuições a variáveis externas. O atributo da tabela representa a garantia ao final do escopo que declarou o símbolo, não um valor em execução.
- Acumular violações independentes; tipo desconhecido decorrente de erro propaga sem diagnósticos de tipo em cascata. Redeclaração não substitui o símbolo anterior. Resultado com erros apresenta as declarações reconhecidas, claramente identificado como análise com erros.
- Semântica só roda após sucesso léxico e sintático. Semântica não altera nem invalida a AST já reconhecida; ela continua disponível quando há erro semântico.
- Fora do recorte: funções/argumentos/retorno, laços, arrays, ponteiros, conversões explícitas, fluxo arbitrário, valores constantes, divisão por zero, overflow, execução, otimização e geração de código. Esses recursos não pertencem à gramática atual.

## Tabela e rastreabilidade

Pilha de dicionários para busca e lista de escopos/símbolos para apresentação, inclusive blocos fechados. IDs determinísticos `E0`/`E1` e `S1`/`S2`; pai do escopo e símbolo sombreado explícitos. Cada símbolo tem nome, tipo, escopo, posição do identificador declarado, garantia de inicialização e referências de leitura/atribuição. Posições do nome declarado são obtidas dos tokens originais, pois o nó Declaracao preserva o nome como atributo, sem folha separada. Nenhum campo novo precisa ser inserido na AST.

Símbolos, referências e diagnósticos apontam para nós pelo caminho JSON `noAst` (raiz vazia e caminhos como `/comandos/0/inicializador`). Intervalos são início inclusivo/fim exclusivo e usam a mesma normalização Unicode/CRLF/tab do scanner. Seleção na tabela ou diagnóstico deve destacar o fonte e a construção correspondente na AST.

## Acessibilidade para daltonismo

Três modos: padrão, sem cores (padrões e rótulos) e alto contraste. Em todos, fases/estados/categorias são escritos por extenso; seleção tem contorno, foco visível e estado anunciado. Sem cores usa sublinhados/padrões distintos nos tokens e mantém a tabela textual/legenda. Preferência visual persistida localmente quando possível, sem alterar código, respostas ou resultados ao trocar modo.

Não usar filtro de cores como suposta correção clínica. Medir contraste dos elementos efetivamente exibidos e verificar operação por teclado, desktop e viewport estreito. Simulações de deficiências de visão de cores no Chromium são inspeções técnicas, não avaliação com pessoas daltônicas nem certificação integral WCAG. A contribuição será descrita como recurso implementado a avaliar; exclusividade perante a literatura não foi demonstrada.

## Critérios definidos antes de observar resultados

Casos próprios congelados em `backend/tests/fixtures/etapa5-semantica.json`; positivos e negativos de cada regra, escopos, sombreamento, fluxos de inicialização e cascatas. Conferir AST/tokens imutáveis, posições, ligações de símbolos/referências, bloqueio por fases anteriores e os três casos semânticos antes previstos como M01–M03.

Manter regressões existentes. Acrescentar testes da UI para estados/tabela/seleções/temas e testes reais com Docker e Chromium, inclusive contraste, simulações e persistência. O registro deve distinguir testes técnicos, casos funcionais e estudo humano ainda não aplicado. Definir esperados pela política acima, sem gerá-los com o analisador em avaliação.
