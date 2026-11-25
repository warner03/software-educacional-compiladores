# Conferência dos entregáveis — Trabalho 4

| Exigência do enunciado | Implementação / evidência |
|---|---|
| Gramática formal coerente com scanner | [gramatica.md](../gramatica.md); mesma EBNF da Tarefa 4; tabela de terminais/tokens |
| Estratégia justificada | Descida recursiva manual em [parser.py](../../backend/app/parser.py); justificativa e limites na gramática |
| AST consistente, com posições | [ast.md](../ast.md); nove tipos de nó; fim exclusivo |
| API ampliada sem regressão | [contrato-api.md](../contrato-api.md); extensão `sintatica`; campos léxicos preservados |
| Política diante de erro léxico | Parser não chamado; teste com substituição da função confirma o bloqueio |
| Visualização didática | Árvore nativa expansível, rótulos e regras, seleção/destaque e download JSON |
| Erros localizados e recuperação | Encontrado/esperado/posição; sincronização em `;`/`}`; AST nula em erro |
| Testes do parser e oráculos | `backend/tests/test_parser.py`; referências V04–V06 anteriores à implementação |
| Casos planejados e endpoints | 33 casos em `test_api_sintatica.py`; fixtures originais preservadas |
| Regressão das etapas anteriores | Testes originais do scanner/API/validação/interface mantidos; scanner inalterado |
| Interface e consistência | Testes jsdom e Playwright verificam estrutura, destaque, posições, tokens, download e estados |
| Docker reproduzível | Build sem cache e smoke com nginx/API; comandos e saídas no registro |
| Artigo e fluxograma | [decisões](decisoes.md), [fontes anteriores](../etapa4/fontes-consultadas.md), [fluxograma atual](fluxograma.png) |
| Demonstração | [roteiro](../demonstracao-etapa4.md), capturas e AST JSON exportada em `capturas/` |
| Limitações e Etapa 5 | Semântica futura, limites operacionais e ausência de estudo com participantes explicitados |

Os resultados da execução e as pendências estão no [registro de testes](../registro-de-testes.md). A aprovação funcional não comprova correção semântica ou ganho de aprendizagem. O GitHub é a entrega do código; as capturas são evidência complementar.
