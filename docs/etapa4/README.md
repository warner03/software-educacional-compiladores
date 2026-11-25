# Tarefa 4 — Materiais e Métodos

**Registro histórico do planejamento entregue em 18/11/2026.** O Trabalho 4 foi implementado posteriormente; consulte a [documentação atual](../trabalho4/README.md), a [gramática implementada](../gramatica.md) e o [registro de testes](../registro-de-testes.md). As declarações de estado abaixo se referem à versão original da tarefa teórica.

Plano de avaliação **versão 1.0**, definido em 18/11/2026. Base técnica examinada: commit `040b296` (Etapa 3).

O scanner e a interface léxica estão implementados. Parser, AST e diagnósticos sintáticos são **propostas para o Trabalho 4**, ainda não implementadas nesta alteração. Semântica e tabela de símbolos são futuras, para a Etapa 5.

## Artefatos

- [Texto acadêmico completo](tarefa4.md)
- [Materiais e Métodos](materiais-e-metodos.md)
- [Gramática EBNF](gramatica.ebnf)
- [Fluxograma](figuras/fluxograma.png) — [SVG](figuras/fluxograma.svg) — [fonte Graphviz](figuras/fluxograma.dot)
- [Arquitetura](figuras/arquitetura.png) — [fonte Graphviz](figuras/arquitetura.dot)
- [Casos de teste](casos-de-teste.md) — [CSV](casos-de-teste.csv)
- [Matriz com evidências por célula](matriz-evidencias.csv) — [JSON](matriz-evidencias.json)
- [Instrumento de avaliação por pares](formulario-avaliacao.md)
- [Histórico das decisões](historico-decisoes.md)
- [Fontes e versões consultadas](fontes-consultadas.md)
- [Fixtures e referências iniciais de AST](../../tests/planejamento/README.md)

## Novas fontes e revisão

Foram acrescentados VERTO (Schneider et al., 2005; DOI 10.22456/1679-1916.13949) e A Generic Tool for Teaching Compilers (Jabri, 2013; DOI 10.5539/cis.v6n2p134). Os sete estudos anteriores foram preservados e relidos; a matriz não usa o resumo de uma etapa anterior como fonte de comprovação.

Os PDFs dos dois artigos novos acompanham a entrega acadêmica, não são dependências do software. O documento identifica versões e páginas dos textos originais, distingue AST de árvore de derivação e corrige os DOI antigos de Borela, Santini e VCOCO.

## Estado do plano

Há 33 casos aplicáveis à Etapa 4 ainda pendentes e três casos semânticos futuros. Não há resultados de parser ou avaliação com participantes nesta tarefa. Os testes da Etapa 3 continuam em seus diretórios e seu registro histórico não foi substituído.

Para gerar as figuras a partir do fonte, quando Graphviz estiver instalado: `dot -Tpng figuras/fluxograma.dot -o figuras/fluxograma.png` (nesta pasta).
