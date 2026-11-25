# Registro de testes — Etapa 4

Execução: 24/11/2026 23:29 -03. Resultados abaixo pertencem a esta rodada; ausência de testes ou erro de execução não é tratado como aprovação.

| Módulo | Comando | Aprovados | Reprovados | Pulados | Resultado |
|---|---|---|---|---|---|
| Backend: scanner, parser, validações e endpoints | `docker compose run --rm backend pytest -q` | 229 | 0 | 0 | Aprovado |
| Frontend: lógica e interface jsdom | `docker compose run --rm testes-frontend` | 41 | 0 | 0 | Aprovado |
| Integração nginx/API/scanner/parser | `bash scripts/smoke_test.sh` | - | - | - | Aprovado |
| Navegador real: desktop e viewport móvel | `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/teste_navegador.py --capturas docs/trabalho4/capturas --chromium /usr/bin/chromium` | 60 | 0 | 0 | Aprovado |

## Ambiente e reprodução

- Docker Compose, backend Python 3.12, frontend de testes Node 20 e jsdom 24.1.0.
- Em rede com proxy TLS, utilizar o bundle confiável da máquina e o override documentado em `docs/execucao-nuvem.md`. Não desativar TLS.
- A execução em navegador usa Playwright; o viewport móvel simula 390px com toque, não um aparelho físico.
- Pré-requisito: reconstruir todas as imagens após alterar código (`docker compose build backend frontend testes-frontend`).
- Histórico da Etapa 2 preservado em [registro-de-testes-etapa2.md](registro-de-testes-etapa2.md).
- Histórico da Etapa 3 preservado em [registro-de-testes-etapa3.md](registro-de-testes-etapa3.md).
- Saídas completas desta rodada em [trabalho4/evidencias/](trabalho4/evidencias/); capturas em `docs/trabalho4/capturas`.
- Neste ambiente: `COMPILADORES_API_PORT=18000`, `COMPOSE_FILE=docker-compose.yml:compose.cloud.yaml` e `CLOUD_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt`. Porta padrão local permanece 8000.

## Casos e referências anteriores à implementação

- Os 33 casos aplicáveis fixados na Tarefa 4 são parametrizados em `test_api_sintatica.py`, com os mesmos códigos e resultados esperados. Os três oráculos V04–V06 são comparados estruturalmente em `test_parser.py`; posições são verificadas separadamente.
- Fixtures Docker são cópias binárias dos originais do planejamento. O scanner não foi alterado; sua suíte original e sua saída completa continuam verificadas.
- M01–M03 confirmam somente aceitação sintática; a avaliação semântica desses casos permanece pendente para a Etapa 5.
- Testes adicionais cobrem todas as construções, precedência, associação, recuperação, EOF, posições Unicode/CRLF/tab, limites em 64/65 níveis, altura e quantidade de nós, API, seleção/exportação e respostas incoerentes.
- Critérios, limites e decisões foram registrados antes da primeira execução em [trabalho4/decisoes.md](trabalho4/decisoes.md). O teste da UI usa referência manual; não gera o esperado com o parser.

## Falhas encontradas e correções

- Primeira rodada do backend: 228 aprovados, sem falhas. A suíte léxica e os testes anteriores da API/validação foram mantidos sem alteração.
- Primeira rodada da interface: 40 aprovados e um reprovado. O seletor do novo teste de hierarquia alcançava o resumo da própria adição em vez da multiplicação filha. Correção apenas no seletor, usando `:scope > .ast-filhos`; esperado matemático preservado.
- A apresentação do destaque foi ajustada para informar quando a AST está selecionada, evitando confundir o trecho da árvore com o token corrente da navegação.
- Correções históricas do scanner/infraestrutura permanecem descritas no registro da Etapa 3. Nenhum limite de recursos foi criado depois de observar resultados para fazer um caso planejado passar.

## Limitações

- O pytest pode informar aviso de depreciação da integração Starlette/AnyIO; verificar contagens/estado da rodada acima.
- Semântica, tabela de símbolos, execução e geração de código ainda não foram implementadas.
- Não foram realizados estudo com estudantes, medição de aprendizagem ou auditoria completa de acessibilidade.
- A ausência de erro sintático não implica validade semântica. A recuperação pode descartar comandos e não garante enumerar todos os erros.
- Tempos de resposta/renderização impressos pelo E2E são observações desta máquina, não comparação de desempenho ou benchmark controlado.
