# Rastreabilidade — Trabalho 5

| Exigência | Artefato e verificação |
|---|---|
| Escopo antes de programar | `decisoes.md`; 30 esperados em `backend/tests/fixtures/etapa5-semantica.json` |
| Estratégia justificada | `backend/app/semantica.py`, percurso único, pilha de escopos e conjunto de inicialização; `docs/semantica.md` |
| Tabela de símbolos | IDs, nome/tipo, escopo, posições, sombreamento, referências e garantia ao fim do escopo |
| Integração preservando etapas anteriores | `main.py` acrescenta `semantica`; `sucesso` superior mantém significado léxico; scanner/parser/AST preservados |
| Bloqueio por erro anterior | Semântica não é chamada após erro léxico/sintático; testes substituem função para comprovar |
| Mensagens didáticas | Sete códigos de regra, localização, explicação e sugestão; ausência de tipo propaga sem cascata artificial |
| Interface | Estados das três fases por texto, tabela filtrável, destaque de símbolos/erros/referências e construção na AST |
| Diferencial de acessibilidade | Sem cores com padrões/rótulos e Alto contraste; preferência visual, foco e seleção preservada |
| Testes positivos/negativos | Testes de política, fluxo, tipos, escopos, posições, contrato e DOM; esperados independentes do analisador |
| Consistência entre visualizações | Ligações de símbolos a declarações/referências e diagnósticos a nós/intervalos reais; AST/tokens imutáveis |
| Regressão | Testes anteriores, integração e navegador reexecutados; históricos preservados |
| Docker reproduzível | Build sem cache e smoke aprovados; logs em `evidencias/` |
| Logs para depuração | Resumo de fases/contagens no backend; `docker compose logs --tail=80 backend frontend` |
| Documentação e fluxograma | README, contrato, semântica, acessibilidade, demonstração e figura editável |
| Artigo e pergunta da contribuição | Registros técnicos preparados; artigo/matriz e formulário curto revisados posteriormente na Tarefa 5, com aplicação ainda pendente |
| Demonstração | Roteiro atual, capturas padrão/sem cores/alto contraste, erros e medidas de contraste |

As contagens/resultados são os do registro, sem tratar casos repetidos pela API como novos cenários independentes. Validação com pessoas e ganho de aprendizagem permanecem pendentes; não foram produzidos dados humanos nesta entrega.
