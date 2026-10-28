# Registro de testes — Etapa 3

Execução: 28/10/2026 13:12 -03. Resultados abaixo pertencem a esta rodada; ausência de testes ou erro de execução não é tratado como aprovação.

| Módulo | Comando | Aprovados | Reprovados | Pulados | Resultado |
|---|---|---|---|---|---|
| Backend: scanner, validações e endpoints | `docker compose run --rm backend pytest -q` | 114 | 0 | 0 | Aprovado |
| Frontend: lógica e interface jsdom | `docker compose run --rm testes-frontend` | 29 | 0 | 0 | Aprovado |
| Integração nginx/API/scanner | `bash scripts/smoke_test.sh` | - | - | - | Aprovado |
| Navegador real: desktop e viewport móvel | `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/teste_navegador.py --chromium /usr/bin/chromium` | 24 | 0 | 0 | Aprovado |

## Ambiente e reprodução

- Docker Compose, backend Python 3.12, frontend de testes Node 20 e jsdom 24.1.0.
- Em rede com proxy TLS, utilizar o bundle confiável da máquina e o override documentado em `docs/execucao-nuvem.md`. Não desativar TLS.
- A execução em navegador usa Playwright; o viewport móvel simula 390px com toque, não um aparelho físico.
- Pré-requisito: reconstruir todas as imagens após alterar código (`docker compose build backend frontend testes-frontend`).
- Histórico da Etapa 2 preservado em [registro-de-testes-etapa2.md](registro-de-testes-etapa2.md).

## Falhas encontradas e correções

- Primeira rodada do scanner: 107 testes passaram e 7 falharam. Um operador simples no fim do arquivo entrava no caminho de operadores de dois caracteres. Correção: exigir comprimento 2 nesse caminho; os casos de borda permanecem na regressão.
- Na preparação inicial do ambiente, arquivos estáticos com permissão 600 não eram legíveis pelo nginx. O Dockerfile agora define leitura 644 dentro da imagem, independentemente da permissão do checkout.
- O healthcheck wget tentava usar o proxy externo para loopback. A consulta local agora usa `-Y off`; o tráfego externo de instalação continua usando o proxy e TLS verificado.
- Os testes de resposta da Etapa 2 foram atualizados para o contrato léxico, mantendo verificações de exemplos, edição, validação e comunicação. A mensagem de recebimento foi substituída pelo resultado da análise.
- Na primeira execução conjunta do registrador, o navegador foi iniciado após o smoke já ter encerrado os serviços e falhou por conexão recusada. O registrador agora reinicia e aguarda os serviços imediatamente antes do E2E; a sequência completa foi reexecutada.

## Limitações

- O pytest informa um aviso de depreciação da integração Starlette/AnyIO; os testes completam sem falha. Não se trata de erro do scanner.
- Não há parser, análise semântica ou AST nesta etapa.
- Não foram realizados estudo com estudantes, medição de aprendizagem ou auditoria completa de acessibilidade.
- A ausência de erro léxico não implica validade sintática ou semântica.
