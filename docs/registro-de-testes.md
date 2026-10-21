# Registro de testes

> Preencha esta tabela **depois de executar** cada comando, com os números reais exibidos pelo pytest.

| Data | Módulo | Tipo | Comando | Aprovados | Reprovados | Observações |
|---|---|---|---|---|---|---|
| __/__/____ | Backend: validações e endpoints | Unitário + endpoint | `docker compose run --rm backend pytest -v` | | | |
| __/__/____ | Frontend: cliente HTTP, exemplos e interface | Unitário + interface | `docker compose run --rm frontend pytest -v` | | | |
| __/__/____ | Implantação e integração frontend↔backend | Implantação / integração | `./scripts/smoke_test.sh` | | | |

## Falhas encontradas e correções
(nenhuma registrada ainda)

## Limitações / testes pendentes
- Sem testes de ponta a ponta com navegador real (ex.: Playwright).
- Análises léxica, sintática e semântica ainda não implementadas (etapas seguintes).
