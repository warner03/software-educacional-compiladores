# Registro de testes

| Data | Módulo | Tipo | Comando | Aprovados | Reprovados | Observações |
|---|---|---|---|---|---|---|
| 22/10/2026 | Backend: validações e endpoints | Unitário + endpoint | `docker compose run --rm backend pytest -v` | 26 | 0 | Todos aprovados |
| 22/10/2026 | Frontend: lógica, exemplos e interface (jsdom) | Unitário + interface | `docker compose run --rm testes-frontend` | 17 | 0 | Todos aprovados |
| - | Implantação e integração frontend↔backend | Implantação / integração | `./scripts/smoke_test.sh` | - | - | Não executado |

## Falhas encontradas e correções
- Correção após avaliação do professor: o frontend em Streamlit só montava a tela via JavaScript, e o HTML
  inicial não continha campo de texto, botão nem exemplos. Foi substituído por uma página HTML/JS servida
  pelo nginx, com os elementos presentes no HTML puro e comunicação via proxy `/api`.

## Limitações / testes pendentes
- Sem testes de ponta a ponta com navegador real (ex.: Playwright).
- Análises léxica, sintática e semântica ainda não implementadas (etapas seguintes).
