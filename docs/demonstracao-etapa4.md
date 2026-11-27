# Demonstração do Trabalho 4

Este é o roteiro histórico da Etapa 4. Para a aplicação atual, use a [demonstração da Etapa 5](demonstracao-etapa5.md), com símbolos, diagnósticos semânticos e modos visuais.

Execute `docker compose up --build -d --wait` e abra `http://localhost:8501`. Para a demonstração automática: veja os comandos Playwright do README. As capturas geradas pelo registrador ficam em `docs/trabalho4/capturas/`.

## 1. Programa válido e precedência

Digite:

```c
int resultado = 10 + 5 * 2;
```

Analise. Mostre os dois estados sem erros e os nove tokens na tabela. Expanda a AST: `Programa → Declaracao → Binario +`, com `Literal 10` à esquerda e `Binario *` à direita. A multiplicação tem dois literais, 5 e 2. Ela não foi calculada: a árvore registra sua estrutura.

Selecione **Localizar Operação binária · \***. O código destaca `5 * 2`, e a indicação mostra linha 1, coluna 22 até coluna 27, fim exclusivo. Selecione um literal e compare a coluna com a tabela de tokens. **Destacar token atual** retoma a sequência léxica. Baixe o JSON e confira os mesmos nós e intervalos.

Use também o exemplo 7. Em `(10 + 5) * 2`, a multiplicação passa à raiz da expressão; em `20 - 5 - 3`, a subtração da esquerda é filha da última: `(20 - 5) - 3`.

## 2. Combinação de construções

Selecione o exemplo 4: declaração `float` e `if/else`. Localize na árvore `Se`, `condicao`, `entao` e `senao`, e mostre as atribuições dentro dos blocos. As chaves são obrigatórias. O software reconhece estrutura, sem checar compatibilidade de tipos ou executar o programa.

## 3. Erros sintáticos e recuperação

Selecione o exemplo 8 ou digite:

```c
int numero = ;
float media;
media = ;
```

Os tokens são reconhecidos; a análise léxica fica sem erros. A sintática aponta dois operandos ausentes, nas linhas 1 e 3. A AST é nula. A recuperação passa por `;`, permitindo detectar o segundo problema.

Teste `int x`: erro no fim da entrada, linha 1, coluna 6; esperado `;`. Teste `if (x > 0 { x = 1; }`: esperado `)` em 1:11. Teste `{ int x;`: o diagnóstico informa o bloco aberto e a chave ausente. Teste `else {}`: `else` sem `if`.

## 4. Erro léxico

Selecione o exemplo 6. Mostre os trechos inválidos e os tokens recuperados. A sintática deve dizer **não executada**, porque o parser não recebe sequência com erro léxico. Não há AST nem diagnósticos sintáticos em cascata.

## 5. Explicar o alcance

`x = 1;` é aceito sintaticamente: verificar se `x` foi declarado ficará para a Etapa 5. Comentários sozinhos não constituem programa; `{}` é um bloco válido. Não há árvore de derivação ou construção animada: os controles navegam pela AST pronta.

O registrador automatiza os testes de desktop e viewport móvel, incluindo os limites e o download real do JSON. As capturas demonstram funcionamento, sem substituir o repositório, os testes ou uma eventual exigência específica do SIGAA.
