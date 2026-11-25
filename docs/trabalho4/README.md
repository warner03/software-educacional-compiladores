# Trabalho 4 — implementação prática

Parser e AST integrados ao projeto existente, a partir da versão `0424376`. A análise semântica permanece para a Etapa 5.

- [Gramática e estratégia do parser](../gramatica.md)
- [Estrutura e visualização da AST](../ast.md)
- [Contrato compatível da API](../contrato-api.md)
- [Decisões registradas antes da execução](decisoes.md)
- [Rastreabilidade dos entregáveis](entrega.md)
- [Fluxograma atual](fluxograma.png) — [SVG](fluxograma.svg) — [Graphviz](fluxograma.dot)
- [Demonstração](../demonstracao-etapa4.md)
- [Testes e limitações](../registro-de-testes.md)
- [Capturas e JSON exportado](capturas/)
- [Saídas completas da validação](evidencias/)

## Relação com Materiais e Métodos

O [artigo da Tarefa 4](../etapa4/README.md) preserva o plano definido em 18/11/2026, antes do parser. Não foram reescritas suas expectativas ou classificações bibliográficas após observar resultados. O scanner original e os campos léxicos da API continuam iguais.

Realizaram-se as escolhas previstas: Mini-C, Python/FastAPI, parser recursivo, AST JSON com posições, bloqueio do parser diante de erro léxico e ausência de AST parcial na resposta. O protocolo 1.1 acrescenta indicador booleano dentro de `sintatica`, limites de nós/altura e decisões de interface/infraestrutura antes da primeira execução. A gramática não mudou.

As nove fontes e a matriz revisada, inclusive os estudos sobre parser/geração e visualização, continuam em [fontes-consultadas.md](../etapa4/fontes-consultadas.md) e na [matriz com evidências](../etapa4/matriz-evidencias.csv). Esta implementação usa essas fontes como fundamentação, sem alterar a comparação ou atribuir ausência de recurso não comprovada nos artigos.

Para a futura seção de resultados, usar as contagens do registro executado, distinguir avaliação funcional de aprendizagem e explicar o teste em viewport móvel como simulação. A visualização implementa navegação, regras e destaque do fonte; não implementa construção animada. O formulário para avaliação por pares continua como instrumento planejado, sem participantes ou respostas coletadas nesta etapa.

## Gerar as figuras

Na raiz do repositório, com Graphviz instalado:

```bash
dot -Tpng docs/trabalho4/fluxograma.dot -o docs/trabalho4/fluxograma.png
dot -Tsvg docs/trabalho4/fluxograma.dot -o docs/trabalho4/fluxograma.svg
```

O fluxo principal representa implementação atual; a extensão semântica está tracejada e explicitamente identificada como futura. A figura original do artigo permanece em `docs/etapa4/figuras/` como registro histórico.
