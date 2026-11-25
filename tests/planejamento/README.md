# Estrutura inicial de testes da Etapa 4

Esta pasta preserva o **planejamento e as fixtures originais de 18/11/2026**, anteriores ao parser. Os campos abaixo são históricos e não foram sobrescritos com resultados posteriores.

- `etapa4-casos.json`: 36 casos, com entradas materializadas; 33 aplicáveis à Etapa 4 e três semânticos futuros.
- `etapa4-ast-referencias.json`: oráculos estruturais independentes para V04–V06.
- Resultados observados: `null`. Os casos não foram executados como testes de parser.
- Não foram adicionados testes que passam trivialmente ou testes artificialmente pulados para simular uma implementação.

O Trabalho 4 reutiliza cópias exatas em `backend/tests/fixtures/`, verificadas por comparação binária. A suíte executável está em `backend/tests/test_parser.py` e `test_api_sintatica.py`; os resultados atuais estão no [registro de testes](../../docs/registro-de-testes.md). Veja [o protocolo original](../../docs/etapa4/casos-de-teste.md) e [as decisões da implementação](../../docs/trabalho4/decisoes.md). Os três casos futuros confirmam somente aceitação sintática; sua avaliação semântica permanece pendente.
