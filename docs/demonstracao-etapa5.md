# Demonstração — Trabalho 5

Na pasta do projeto atualizado, abra **Abrir no Console/Terminal** no Linux e execute `docker compose up --build -d --wait`. Abra `http://localhost:8501`. Se extraiu uma pasta nova e a versão anterior estiver ativa, encerre-a com `docker compose down` na pasta antiga primeiro. Use o mesmo endereço da interface; a atualização é do código/imagem.

## 1. Mostrar as três fases

Selecione o exemplo 1 e analise. Os estados Léxica, Sintática e Semântica devem indicar sucesso. A tabela mostra a variável declarada, tipo, posição e escopo. Os tokens e a AST continuam disponíveis. O software analisa as regras; não calcula ou executa o programa.

## 2. Escopos, símbolos e ligação ao fonte

Selecione o exemplo 10. Há um `x` global e outro `x` dentro do bloco, além de `y`. Filtre `E1` e compare o `x` interno com o global em `E0`. A coluna Sombreia informa a ligação. Selecione **Localizar declaração**: o nome é destacado no fonte e o nó Declaracao recebe contorno na AST. Use **Ver trecho destacado no código** para ir diretamente ao resultado.

Abra Referências e selecione uma leitura/atribuição. A ligação usa o símbolo visível correto, mesmo com nomes iguais. **Destacar token atual** retoma a navegação de tokens.

## 3. Distinguir os erros

| Exemplo | O que mostrar |
|---|---|
| 6 | Erro léxico; sintática e semântica não executadas |
| 8 | Léxico sem erros, erro sintático; semântica não executada |
| 9 | Estrutura válida, mas `total` não declarado; erro semântico, AST preservada |
| 11 | `float` em variável `int`, com regra e sugestão |
| 12 | Leitura de variável sem inicialização garantida |
| 14 | Este Mini-C exige uma comparação no `if`; `if(valor)` numérico é rejeitado |

No exemplo 9, localize o erro: `total` deve ser destacado e o alvo da atribuição marcado na AST. A tabela mantém as declarações reconhecidas durante a análise com erros.

## 4. Inicialização e fluxo

Analise o exemplo 13: `valor` recebe uma atribuição nos dois ramos e pode ser lido depois. Remova o `else` e analise novamente. A leitura final deixa de ter inicialização garantida. Condições constantes não são executadas pela análise: os dois caminhos são considerados.

Uma declaração sem leitura, como `int x;`, é válida mesmo com inicialização não garantida. O atributo mostrado é a garantia no fim do escopo, não uma simulação do valor a cada passo.

## 5. Apoio ao daltonismo

No seletor inicial, escolha **Sem cores — padrões e rótulos**. Abra a legenda e observe os sublinhados distintos. Navegue pelos tokens: nomes/tipos e contorno permitem acompanhar os resultados sem depender da cor. Alterne para **Alto contraste**. A análise e a seleção permanecem. Recarregue a página para conferir a preferência visual; o código do editor não é salvo nessa preferência.

Explique a contribuição como recurso de acessibilidade implementado e tecnicamente testado. As emulações do navegador não são avaliação com pessoas daltônicas ou certificação WCAG integral. O artigo e o formulário curto estão revisados na Tarefa 5; a experiência com colegas ainda será avaliada com dados reais.

## Evidências

O registro contém 322 testes de backend, 55 de interface e 134 cenários de navegador aprovados, além da integração e 30/30 casos semânticos pela API. As capturas e medidas estão em `docs/trabalho5/capturas/`; os 30 casos já estão na suíte e não devem ser somados como novos testes independentes.
