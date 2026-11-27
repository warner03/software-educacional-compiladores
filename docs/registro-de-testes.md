# Registro de testes — Etapa 5

Execução: 26/11/2026 21:23 -03. Resultados abaixo pertencem a esta rodada; ausência de testes ou erro de execução não é tratado como aprovação.

| Módulo | Comando | Aprovados | Reprovados | Pulados | Resultado |
|---|---|---|---|---|---|
| Backend: scanner, parser, semântica e endpoints | `docker compose run --rm backend pytest -q` | 322 | 0 | 0 | Aprovado |
| Frontend: lógica e interface jsdom | `docker compose run --rm testes-frontend` | 55 | 0 | 0 | Aprovado |
| Integração nginx/API/scanner/parser/semântica | `bash scripts/smoke_test.sh` | - | - | - | Aprovado |
| Casos semânticos por API real | `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/avaliar_semantica.py` | 30 | 0 | 0 | Aprovado |
| Navegador real: desktop e viewport móvel | `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/teste_navegador.py --capturas docs/trabalho5/capturas --chromium /usr/bin/chromium` | 134 | 0 | 0 | Aprovado |

## Ambiente e reprodução

- Docker Compose, Python 3.12, Node 20/jsdom 24.1.0 e Chromium headless via Playwright.
- Pré-requisito: reconstruir imagens após mudanças (`docker compose build backend frontend testes-frontend`). Build sem cache desta entrega preservado em `trabalho5/evidencias/build-sem-cache.txt`.
- Na nuvem: `COMPILADORES_API_PORT=18000`, `COMPOSE_FILE=docker-compose.yml:compose.cloud.yaml`, `CLOUD_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt`. Ver [execução](execucao-nuvem.md); TLS continua verificado.
- Saídas desta rodada: [trabalho5/evidencias/](trabalho5/evidencias/). Capturas/medidas: `docs/trabalho5/capturas`.
- Históricos preservados: [Etapa 2](registro-de-testes-etapa2.md), [Etapa 3](registro-de-testes-etapa3.md) e [Etapa 4](registro-de-testes-etapa4.md). A Tarefa 5 teórica original permanece como fotografia da base anterior.

## Escopo e esperados

- Política semântica e acessibilidade definidas antes do analisador em [decisoes.md](trabalho5/decisoes.md). Trinta casos próprios em `backend/tests/fixtures/etapa5-semantica.json` fixam resultados e regras esperadas, sem gerar os esperados com a implementação avaliada.
- Declaração antes do uso, redeclaração no escopo, sombreamento, tipos/promoção, comparação, condição bool e inicialização definida, incluindo interseção dos caminhos do if/else e leituras no próprio inicializador.
- M01–M03, antes previstos como casos futuros, agora exigem os diagnósticos semânticos definidos. Aceitação sintática permanece preservada; não basta para aprovar os casos semânticos.
- AST/tokens e seus testes anteriores preservados. Dados de contrato nos testes do frontend são entradas, com esperados DOM escritos separadamente; não substituem os oráculos semânticos.
- Os 30 casos externos também pertencem à suíte; a execução por nginx verifica integração, sem somá-los como casos independentes. Cobertura de casos não é cobertura de código; linhas/ramos não foram medidos.
- O navegador verifica três fases, tabela/referências/escopos, ligações à AST e fonte, erros, limites, modos visuais, persistência, teclado e responsividade em 1366px e 390px.
- Contraste textual mínimo exigido de 4,5:1 para os elementos medidos em três modos e quatro estados. Foco/contorno de seleção exigem 3:1. As cores/fundos computados e gradientes são examinados; controles desabilitados ficam excluídos.

## Rodadas e correções

- Primeira rodada: 322 testes de backend, 55 de interface e 134 cenários de navegador aprovados, sem reprovações. O registro acima corresponde à última rodada, com as alterações finais reconstruídas.
- Conferência visual: reduzida a largura de texto nas legendas e reposicionada a captura das tabelas na sua borda esquerda, pois a seleção automática do navegador rolava a região até o botão à direita.
- Acrescentado acesso direto do resultado ao trecho destacado e conferência de foco/contorno em cada modo, mantendo a posição e os resultados ao alterar a preferência.
- O smoke encerra os serviços por padrão; o registrador inicia/aguarda os serviços antes dos casos HTTP e do E2E.
- As correções históricas das etapas anteriores continuam registradas nos documentos correspondentes. Não se alteraram regras ou esperados para transformar falha em aprovação.

## Limitações

- Nenhum estudo com pessoas daltônicas ou avaliação por pares foi executado. As simulações de protanopia/deuteranopia/tritanopia/acromatopsia são inspeções técnicas no Chromium, não resultados humanos.
- Os critérios medidos não constituem auditoria WCAG integral ou certificação. Viewport móvel não é aparelho físico; tempos impressos não são benchmark controlado.
- Sem execução do programa, valores constantes, funções, laços, conversões explícitas, otimização ou geração de código. A representação semântica ampliada fica para a Etapa 6.
- O pytest pode emitir aviso de depreciação Starlette/AnyIO; isso não é falha funcional. Estatísticas humanas e ganho de aprendizagem continuam sem dados.
