# Entradas de contrato da interface

Os JSON são entradas do frontend obtidas das funções reais scanner/parser/semântica para os fontes indicados. Não são oráculos de correção semântica: essa correção é verificada em `backend/tests/test_semantica.py` usando a política e os casos fixados antes do analisador.

Os testes da interface usam estes dados como entrada e comparam tabelas, rótulos, posições e seleções com esperados escritos separadamente. O E2E também usa respostas reais, sem mocks, e confere a consistência fonte–tokens–AST–símbolos.
