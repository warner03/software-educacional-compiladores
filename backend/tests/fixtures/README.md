# Fixtures independentes

Os dois JSON desta pasta são cópias exatas dos originais de `tests/planejamento/`, fixados na Tarefa 4 em 18/11/2026, antes da implementação. A cópia permite executar pytest no contexto Docker `backend/` sem montar arquivos externos. Os campos históricos `pendente`, `parser_implementado: false` e `resultado_observado: null` descrevem o **planejamento original**, não o estado atual. Resultados atuais: `docs/registro-de-testes.md`.

Não gerar os esperados com o parser avaliado. Verificação de identidade, a partir da raiz do repositório:

```bash
cmp tests/planejamento/etapa4-casos.json backend/tests/fixtures/etapa4-casos.json
cmp tests/planejamento/etapa4-ast-referencias.json backend/tests/fixtures/etapa4-ast-referencias.json
```
