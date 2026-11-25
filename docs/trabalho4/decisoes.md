# Trabalho 4 — decisões de implementação

Definição em 24/11/2026, **antes da implementação e da primeira execução do parser**. Base: `0424376`; protocolo acadêmico 1.0 de 18/11/2026 preservado em `docs/etapa4/`.

## Protocolo de implementação 1.1

- Manter integralmente o scanner e a gramática proposta. Usar descida recursiva manual em Python, sem gerador ou dependência nova. Blocos obrigatórios em `if`/`else`; programa contém pelo menos um item; `{}` é válido.
- Manter todos os campos e significados da API da Etapa 3. Acrescentar `sintatica` com `estado`, `sucesso`, `ast` e `erros`. O booleano interno complementa o estado previsto no artigo: `null` quando não executada, `true` no sucesso e `false` no erro.
- Não chamar o parser quando houver erro léxico. Não retornar AST parcial como válida. Recuperar erros de gramática em `;` ou `}`, sempre avançando ou devolvendo a chave ao bloco que a abriu.
- Todos os nós têm início inclusivo e fim exclusivo, com linha/coluna a partir de 1, Unicode por ponto de código e quebras normalizadas como no scanner. Folhas apontam para seus lexemas. Parênteses não geram nós; um nó pai cobre também o agrupamento usado por seu operando. Programa cobre do primeiro ao último item, excluindo comentários externos.
- Preservar o limite herdado de 10.000 caracteres e o limite planejado de 64 níveis estruturais ativos (blocos, parênteses e sinais unários). Acrescentar **antes dos testes** limites de 2.000 nós construídos e altura 128 da AST: tamanho de texto não limita a altura de cadeias associativas nem o custo de serialização/renderização. Excedê-los produz diagnóstico controlado, sem AST, e não HTTP 500. Limites são de engenharia, não produções da gramática.
- Reutilizar os 33 casos aplicáveis e os três oráculos independentes do plano, sem modificar entradas ou resultados esperados após observar o parser. Copiar as fixtures congeladas para `backend/tests/fixtures/` para que os testes funcionem dentro do contexto de build Docker; verificar identidade com os originais. Os três casos semânticos só confirmarão aceitação sintática, sem simular avaliação semântica.
- Acrescentar testes de recuperação, posições com CRLF/Unicode/tabulação, limites em 64/65 níveis, altura e quantidade de nós, expressões longas e igualdade dos tokens com o scanner original. Os novos esperados derivam da gramática e dos limites acima.
- Interface: árvore hierárquica com controles nativos de expansão, seleção com destaque do intervalo no mesmo código analisado, exportação JSON e indicação separada das duas análises. Navegação de tokens permanece disponível. Não apresentar a navegação pela AST pronta como animação da construção ou derivação passo a passo.
- Porta externa da API configurável por `COMPILADORES_API_PORT`, mantendo 8000 como padrão local. Usar 18000 neste ambiente para evitar portas reservadas da plataforma; serviço interno e proxy continuam usando 8000. Não alterar a configuração publicada do ambiente.

## Critérios de conclusão

Passar regressões anteriores, testes novos de parser/API/interface, os 33 casos aplicáveis e os oráculos; realizar build sem cache, smoke nginx/API e navegador Chromium real em desktop e viewport móvel. Registrar contagens, falhas/correções e limitações em `docs/registro-de-testes.md`. Sem estudo com participantes ou alegação de aprendizagem medida.

Alterações necessárias após observar resultados serão registradas abaixo, com a falha e a razão da correção. O artigo entregue permanece como plano histórico; a documentação do Trabalho 4 descreve a implementação atual.

- Primeira rodada do backend: 228 aprovados. Primeira rodada da interface: 40 aprovados e 1 reprovado. O seletor CSS do teste de precedência alcançava o resumo da própria adição em vez do resumo da multiplicação filha. Corrigido o seletor com `:scope > .ast-filhos`; preservados o esperado matemático e a árvore de referência. Nenhuma produção da gramática ou resultado planejado foi alterado.
