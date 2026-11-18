# Histórico de decisões — protocolo 1.0

| Data | Decisão | Justificativa / estado |
|---|---|---|
| 18/11/2026 | Fixar a versão 1.0 antes de implementar o parser | Nenhum teste novo de parser ou estudo com participantes executado |
| 18/11/2026 | Conferir os nove textos completos | Reclassificar NI incorretos e corrigir referências sem usar tabelas de colegas como prova |
| 18/11/2026 | Manter scanner, API e interface da Etapa 3 | Mudança atual é documental e de fixtures de planejamento |
| 18/11/2026 | Propor parser recursivo e AST JSON | Escopo pequeno, rastreabilidade entre regras, funções e estrutura esperada |
| 18/11/2026 | Não executar parser após erro léxico | Evitar árvore aparentemente válida baseada em tokens incompletos |
| 18/11/2026 | Não apresentar AST parcial como válida | Em erro sintático, retornar árvore nula e diagnósticos separados |
| 18/11/2026 | Preservar semântica dos campos existentes da API | `sucesso` continua léxico; extensão `sintatica` foi proposta aditivamente |
| 18/11/2026 | Limites: 10.000 caracteres e profundidade proposta 64 | Tamanho é herdado; limite de aninhamento é decisão de engenharia a implementar |
| 18/11/2026 | Registrar 36 casos e três oráculos de expressão | 33 casos da Etapa 4 e três futuros; resultados observados vazios |
| 18/11/2026 | Adotar formulário próprio com itens 1–5 e não aplicável | Inspirado na literatura; não apresentado como escala validada de aprendizagem |

Mudanças futuras: registrar data, item alterado, motivo, versão do protocolo e quais resultados já eram conhecidos. Não alterar retrospectivamente o resultado esperado para fazer um teste reprovado parecer aprovado.
