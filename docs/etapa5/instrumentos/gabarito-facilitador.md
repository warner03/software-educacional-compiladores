# Gabarito — uso exclusivo do facilitador

Não entregue aos colegas antes das tarefas. Instrumento v3.0; entradas/gabaritos mudaram em relação à versão 2.

## A1 — símbolos e fonte

Em `int x = 1; float y = x + 2.5;`, as três fases têm sucesso. Há dois símbolos no escopo global E0: x do tipo int e y do tipo float; ambos terminam inicializados. A declaração de x e sua leitura no inicializador de y podem ser localizadas pela tabela, com destaque no fonte e nó correspondente da AST. No guia a entrada tem duas linhas; as linhas/colunas mudam em relação à versão em uma linha, sem mudar os símbolos ou a regra.

**Conclusão:** localizar a declaração e a leitura de x e distinguir verbalmente onde foi declarada/usada. Somente dizer o nome do símbolo não basta. Registrar ajuda, se houve.

## A2 — significado

Em `int x = 1; total = x + 2;`, o léxico e a sintática têm sucesso. Há erro **semântico**, regra IDENTIFICADOR_NAO_DECLARADO para total. A AST continua disponível. A tabela reconhece x; total não vira declaração. A sugestão orienta declarar antes de usar. No guia, total começa na segunda linha; na versão em uma linha, está na coluna 12.

**Conclusão:** indicar a fase semântica e localizar total; explicar que falta declaração visível anterior. Q01: **C) Semântico.**

## A3 — apresentação sem dependência de cores

Em `int x = ;`, o léxico não tem erro, a sintática acusa falta de expressão e a semântica não é executada. Em `@ int x;`, há erro léxico para @ e sintática/semântica não executadas. Os rótulos identificam fases/estados em Sem cores e Alto contraste. A legenda informa os padrões, sem depender de distinguir matizes.

**Conclusão:** selecionar Sem cores, identificar o erro sintático e comparar o bloqueio com a entrada léxica inválida; experimentar Alto contraste. Anotar se a pessoa efetivamente usou rótulos/padrões e qualquer ajuda. Q02: **B) Sintática.** A tarefa examina apenas parte da interface, sem comprovar eficácia geral de acessibilidade.

## Formulário

L01–L03 não têm resposta correta; N/A deve ser aceito sem pressão. A01 é opcional. Não corrigir ou induzir a opinião durante o preenchimento. Os acertos objetivos são realização apoiada pela interface, sem prova de ganho de aprendizagem.
