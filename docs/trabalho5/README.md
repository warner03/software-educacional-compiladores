# Trabalho 5 — semântica e acessibilidade

Implementação sobre a base `0637b7d`, preservando scanner, parser, AST, validação e recursos anteriores. A semântica percorre a AST e mantém escopos, tipos e inicialização definida. A interface integra símbolos, referências e diagnósticos com fonte/AST e oferece modos Sem cores e Alto contraste.

- [Política e decisões anteriores ao analisador](decisoes.md)
- [Semântica e estrutura da tabela](../semantica.md)
- [Contrato da API](../contrato-api.md)
- [Acessibilidade e limites da validação](../acessibilidade.md)
- [Roteiro de demonstração](../demonstracao-etapa5.md)
- [Rastreabilidade dos entregáveis](entrega.md)
- [Fluxograma atual](fluxograma.png) — [SVG](fluxograma.svg) — [Graphviz](fluxograma.dot)
- [Registro de testes](../registro-de-testes.md)
- [30 casos semânticos observados](evidencias/casos-semanticos.csv) — [JSON](evidencias/casos-semanticos.json)
- [Capturas e medidas de contraste](capturas/)
- [Metadados e hashes da versão testada](evidencias/metadados.json)
- [Commit do código e conferência dos hashes](evidencias/versao-entregue.json)

## O que foi validado

322 testes de backend e 55 de interface, 134 cenários de navegador e integração real aprovados na rodada registrada. Os 30 casos semânticos congelados também foram aprovados via nginx/API; eles já pertencem à suíte e não são somados como casos independentes. Scanner, parser e testes anteriores foram mantidos. Build sem cache e saídas integrais estão em `evidencias/`.

Três modos e quatro estados de análise foram examinados em desktop e viewport estreito. As medidas de texto/foco/seleção e os limites do procedimento estão registrados; as emulações de visão de cores são inspeções técnicas. Não houve avaliação com pessoas daltônicas, auditoria WCAG completa ou medida de aprendizagem.

## Relação com o artigo

A [Tarefa 5](../etapa5/README.md) foi revisada após esta entrega prática, usando as evidências atuais. A preparação anterior está no histórico `docs/etapa5/historico/versao2/`. Os registros originais permanecem vinculados às respectivas versões; a coleta com colegas ainda será aplicada.

A contribuição implementada é a exploração com padrões/rótulos e preferências visuais, associada à tabela de símbolos interativa, diagnósticos de regras e ligações ao fonte/AST. A exclusividade frente às ferramentas estudadas não foi demonstrada. A pergunta L02 do instrumento curto da Tarefa 5 trata de identificar os resultados sem depender de cores; sua aplicação ainda está pendente.

## Figura

```bash
dot -Tpng docs/trabalho5/fluxograma.dot -o docs/trabalho5/fluxograma.png
dot -Tsvg docs/trabalho5/fluxograma.dot -o docs/trabalho5/fluxograma.svg
```

O fluxo distingue fases executadas, bloqueios e extensões futuras da Etapa 6. A semântica não executa o programa nem gera código.
