# Registro de testes

| Data | Módulo | Tipo | Comando | Aprovados | Reprovados | Observações |
|---|---|---|---|---|---|---|
| 21/10/2026 | Backend: validações e endpoints | Unitário + endpoint | `docker compose run --rm backend pytest -v` | 26 | 0 | Todos aprovados |
| 21/10/2026 | Frontend: cliente HTTP, exemplos e interface | Unitário + interface | `docker compose run --rm frontend pytest -v` | 18 | 0 | Todos aprovados |
| - | Implantação e integração frontend↔backend | Implantação / integração | `./scripts/smoke_test.sh` | - | - | Não executado |

## Falhas encontradas e correções
(nenhuma registrada)

## Limitações / testes pendentes
- Sem testes de ponta a ponta com navegador real (ex.: Playwright).
- Análises léxica, sintática e semântica ainda não implementadas (etapas seguintes).
