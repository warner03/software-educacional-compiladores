# Modos visuais e apoio ao daltonismo

O seletor **Visualização e acessibilidade**, no início da interface, oferece três modos:

| Modo | Comportamento |
|---|---|
| Padrão | Cores de categorias, com nomes, fases e estados também escritos |
| Sem cores | Tons de cinza, padrões de sublinhado, rótulos e contornos; apoio para estudar sem depender da distinção de cores |
| Alto contraste | Fundo escuro, texto claro, controles contrastantes e os mesmos padrões/rótulos |

A troca de modo preserva o fonte, o resultado, as expansões e as seleções. A escolha é gravada apenas como preferência visual local quando o navegador permite; se o armazenamento estiver indisponível, o controle continua funcionando na sessão. Não são armazenados código ou respostas de avaliação nessa preferência.

## Como a informação permanece identificável

- Estados indicam o nome da fase e texto explícito: sem erros, com erros ou não executada. A indicação léxica/semântica também usa `[OK]`, `[!]` e `[—]`. Contornos sólidos/tracejados/duplos ajudam a distinguir avisos sem depender da cor do fundo.
- A tabela de tokens informa o tipo por escrito em todos os modos. A legenda explica os padrões do modo Sem cores/Alto contraste: palavra reservada com sublinhado duplo; identificador com simples; inteiro com pontilhado; real com tracejado; operador com ondulado; delimitador em negrito.
- Trechos selecionados têm contorno; a navegação anuncia tipo/posição. Seleções na tabela semântica marcam o fonte e o nó relacionado por contorno duplo. Botões selecionáveis expõem `aria-pressed`.
- A AST conserva rótulos, relações Esquerda/Direita/Então/Senão e controles nativos `details`/`summary`. Padrões nas bordas reforçam categorias. A tabela de símbolos separa escopo, tipo, posição e garantia de inicialização por texto.
- Há foco visível, link para ir ao editor e links dos resultados ao código destacado. Controles usam a navegação padrão por teclado. Tabelas/AST têm regiões roláveis; telas estreitas usam uma coluna.

No destaque de uma construção inteira, o trecho é selecionado como unidade; a tabela continua sendo a referência textual de cada token. A navegação de tokens retoma seus destaques e padrões individuais.

## Critérios e validação técnica

O desenho se orienta pelos critérios de [uso de cor](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html), [contraste mínimo](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [contraste não textual](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) e [foco visível](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html) da WCAG 2.2.

O teste em Chromium examina os três modos em estados válido, erro léxico, sintático e semântico, em desktop e viewport móvel. Mede luminância relativa sRGB das cores computadas do texto e dos fundos/gradientes, exigindo pelo menos **4,5:1** para os elementos textuais medidos, e **3:1** para foco/contorno de seleção. Controles desabilitados são excluídos do cálculo. Não se presume que o simples nome de uma paleta garanta contraste.

Também confere padrões, manutenção dos dados/seleção ao alternar modo, preferência após recarga, operação por teclado e largura da página. São realizadas inspeções sob emulação Chromium de protanopia, deuteranopia, tritanopia e acromatopsia, com capturas. Resultados numéricos ficam em `docs/trabalho5/capturas/contraste-medido.json` e comandos no [registro de testes](registro-de-testes.md).

Essas verificações são técnicas: não houve estudo com pessoas daltônicas, teste em aparelho físico ou auditoria completa de todos os critérios WCAG. A medição usa estilos computados antes das emulações, não limiares clínicos da percepção de cada pessoa. Não há filtro anunciado como correção da visão de cores ou garantia médica. O desempenho real nas tarefas deve ser avaliado com usuários, com respeito a suas preferências.

## Contribuição proposta e avaliação futura

A contribuição implementada é disponibilizar uma forma de explorar tokens, AST, símbolos e diagnósticos com padrões/rótulos, seleção rastreável e preferência de contraste, integrada ao objetivo didático de Compiladores. Sua exclusividade frente às ferramentas relacionadas não foi demonstrada.

Uma pergunta simples para a revisão posterior do formulário é: **“Consegui identificar os tipos de token e os erros sem depender das cores.”** Uma segunda pode investigar a localização de um símbolo/erro no fonte. As perguntas ainda serão simplificadas e aplicadas na revisão da Tarefa 5; não existem respostas humanas nesta entrega prática.
