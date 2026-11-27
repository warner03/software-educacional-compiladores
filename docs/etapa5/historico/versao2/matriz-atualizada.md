# Matriz atualizada — nove estudos e o projeto Mini-C

Auditoria de estado em 26/11/2026. Base de código `7fcb5ca`. Preservam-se as 135 classificações e evidências da Tarefa 4. Acrescentam-se 15 células para **Este trabalho**, totalizando 150. Esta matriz descreve o estado implementado até o Trabalho 4; a estratégia teórica da Tarefa 5 não é tratada como software pronto.

**Legenda:** ✓ = presença confirmada; ✗ = ausência documentada na versão; NI = informação insuficiente, sem inferir ausência; N/A = critério não aplicável ao objeto. Nenhuma coluna separada de ano ou nome de software foi criada.

## Interface, entrada e estruturas

| Referência | Web | Entrada | Exemplos | Léxica | Sintática | AST | Derivação |
|---|---|---|---|---|---|---|---|
| Graciano Junior et al. (2022) | ✓ | ✓ | NI | ✓ | ✓ | NI | ✓ |
| Borela et al. (2025) | ✓ | ✓ | ✓ | ✓ | ✓ | NI | ✓ |
| Santini et al. (2022) | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Mernik e Žumer (2003) | NI | ✓ | ✓ | ✓ | ✓ | NI | ✓ |
| Resler e Deaver (1998) | NI | ✓ | NI | ✓ | ✓ | NI | NI |
| Rodger et al. (2009) | NI | N/A | ✓ | NI | ✓ | NI | ✓ |
| Moreno et al. (2004) | NI | ✓ | NI | NI | NI | NI | NI |
| Schneider et al. (2005) | NI | ✓ | NI | ✓ | ✓ | NI | NI |
| Jabri (2013) | NI | N/A | NI | ✓ | ✓ | NI | NI |
| **Este trabalho — Mini-C (estado implementado)** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |

## Processamento e apoio didático

| Referência | Semânt. | Símb. | Geração | Passos | Diag. | Explic. |
|---|---|---|---|---|---|---|
| Graciano Junior et al. (2022) | ✗ | NI | ✗ | ✓ | ✓ | ✓ |
| Borela et al. (2025) | ✓ | ✓ | ✓ | ✗ | NI | ✓ |
| Santini et al. (2022) | N/A | N/A | N/A | N/A | N/A | N/A |
| Mernik e Žumer (2003) | ✓ | NI | ✓ | ✓ | ✓ | NI |
| Resler e Deaver (1998) | NI | NI | NI | ✓ | NI | NI |
| Rodger et al. (2009) | NI | NI | NI | ✓ | NI | ✓ |
| Moreno et al. (2004) | NI | NI | NI | ✓ | ✓ | ✓ |
| Schneider et al. (2005) | ✓ | ✓ | ✓ | NI | NI | ✓ |
| Jabri (2013) | NI | NI | NI | NI | ✓ | NI |
| **Este trabalho — Mini-C (estado implementado)** | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |

## Evidências de avaliação

| Referência | Estudantes | Aprendizagem |
|---|---|---|
| Graciano Junior et al. (2022) | ✓ | NI |
| Borela et al. (2025) | ✓ | NI |
| Santini et al. (2022) | N/A | N/A |
| Mernik e Žumer (2003) | ✓ | ✓ |
| Resler e Deaver (1998) | NI | NI |
| Rodger et al. (2009) | ✓ | ✓ |
| Moreno et al. (2004) | ✗ | ✗ |
| Schneider et al. (2005) | NI | NI |
| Jabri (2013) | ✓ | ✓ |
| **Este trabalho — Mini-C (estado implementado)** | ✗ | ✗ |

## Evidências da linha própria

| Critério | Estado | Evidência verificável | Delimitação |
|---|---|---|---|
| Web | ✓ | frontend/index.html:1–16; frontend/nginx.conf; docker-compose.yml: frontend/backend. Interface HTML/CSS/JavaScript executada em navegador. | Confirma uso web; não implica implantação pública ou serviço colaborativo multiusuário. |
| Entrada | ✓ | frontend/index.html:31–35; frontend/app.js: envio do conteúdo do editor a /api/analisar. | Editor de programa-fonte Mini-C. |
| Exemplos | ✓ | frontend/index.html:23–30: oito opções com data-codigo, incluindo programas válidos e erros intencionais. | Exemplos integram a interface e podem ser editados; não são apenas listagens impressas no artigo. |
| Léxica | ✓ | backend/app/scanner.py; backend/app/main.py:47; backend/tests/test_scanner.py. | Scanner original da Etapa 3, tokens e diagnósticos com posições. |
| Sintática | ✓ | backend/app/parser.py; backend/app/main.py:48; backend/tests/test_parser.py e test_api_sintatica.py. | Descida recursiva manual, EBNF explícita, precedência e recuperação em ; ou }. |
| AST | ✓ | backend/app/parser.py:23–28 e construção dos nós; docs/ast.md:5–61; frontend/app.js:154–232. | AST simplificada com nove tipos de nó, posições, seleção, destaque no fonte e exportação JSON. |
| Derivação | ✗ | docs/ast.md:3,71; docs/gramatica.md:81; frontend/app.js:179. | A interface não exibe árvore de derivação. A AST não é reclassificada como derivação para preencher a coluna. |
| Semânt. | ✗ | backend/app/parser.py:4; docs/gramatica.md:99–101; frontend/index.html:53. | Análise semântica permanece futura para Trabalho 5; protocolo teórico não comprova implementação. |
| Símb. | ✗ | README.md: última seção; docs/registro-de-testes.md: limitações; contrato docs/contrato-api.md e resposta backend/app/main.py:51–58. | Sem tabela de símbolos ou verificações de declaração/tipos na versão examinada. |
| Geração | ✗ | README.md: limitações; backend/app/parser.py:4; docs/registro-de-testes.md: limitações. | Nenhuma execução do programa, código intermediário didático ou código-alvo é produzido. |
| Passos | ✗ | docs/ast.md:71; frontend/index.html:44; frontend/app.js:179. | Há navegação sobre tokens e AST prontos. O critério herdado exige acompanhamento controlado/animado das transformações do algoritmo; não foi implementado. |
| Diag. | ✓ | backend/app/parser.py:61–69; backend/app/scanner.py; backend/app/main.py:47–50; frontend/app.js:161–176. | Diagnósticos separados por fase; linha/coluna, esperado/encontrado; não executar parser após erro léxico; AST nula em erro. |
| Explic. | ✓ | frontend/index.html:38–55: guia inicial; frontend/app.js:17–26 e visualização de regras; docs/gramatica.md e docs/ast.md. | Guia e explicações por tipo de construção já presentes; não se trata de rastro completo de derivação. |
| Estudantes | ✗ | docs/trabalho4/README.md: seção Relação com Materiais e Métodos; docs/registro-de-testes.md: limitações. | Nenhuma aplicação formal com colegas e respostas reais foi localizada na base auditada. Testes automatizados e apresentação ao professor não constituem estudo com participantes. |
| Aprendizagem | ✗ | docs/registro-de-testes.md: limitações; docs/trabalho4/README.md: Relação com Materiais e Métodos. | Sem pré/pós-teste, medida de conhecimento ou avaliação humana concluída. Não converter aprovação de testes em ganho de aprendizagem. |

## Leitura responsável da comparação

As nove referências foram conservadas com os mesmos critérios. Santini et al. (2022) continuam como estudo secundário, sem somar funcionalidades dos nove jogos em uma ferramenta imaginária. Os dois novos artigos metodológicos da Tarefa 5 devem fundamentar a avaliação; se não descrevem uma ferramenta concorrente comparável, devem ser sintetizados em quadro metodológico separado, e não forçados a receber marcações de funcionalidades.

Não há base para declarar que Mini-C preenche todas as colunas. Na versão auditada estão ausentes árvore de derivação, semântica, tabela de símbolos, geração, passos do algoritmo, estudo com estudantes e medida de aprendizagem. Isso não impede uma contribuição: uma escolha de escopo ou representação pode ser adequada ao objetivo didático sem reproduzir todas as fases de um compilador completo.

“Passos” mantém a definição operacional do artigo anterior. Selecionar o próximo token e expandir uma AST pronta não comprova execução passo a passo do scanner/parser. “Estudantes” exige aplicação real do instrumento com participantes. “Aprendizagem” exige evidência pertinente; opiniões e funcionamento correto não são substitutos.

As marcas NI de AST nos estudos anteriores não podem ser convertidas em ✗ para proclamar exclusividade da AST do projeto. O texto de Borela et al. já associa tokens/nós a trechos do fonte; Graciano Junior et al. já documentam processamento visual e controles; ajuda/documentação também ocorre em outros estudos. A própria Tarefa 4 (§2.6) identifica essas sobreposições.

## Diferencial operacional avaliável

**Formulação pronta:** Este trabalho investiga uma sequência de exploração de Mini-C que integra tokens localizados, AST simplificada com intervalos e explicações por tipo de construção, seleção do trecho-fonte e diagnósticos separados por fase. A contribuição proposta é organizar e avaliar essa experiência para tarefas de interpretação de agrupamentos e de localização/classificação de erros no contexto da disciplina. Sua exclusividade técnica ou superioridade frente às outras ferramentas não foi demonstrada.

**Questão de avaliação:** Ao usar a ligação entre nós da AST e trechos do código, os participantes conseguem identificar o agrupamento de uma expressão e localizar a construção correspondente? Como avaliam a clareza desse apoio?

**Questão explícita para formulário (percepção específica):** “A seleção de um nó da AST, acompanhada do destaque no código e da explicação da construção, ajudou você a compreender como os operandos da expressão estão agrupados?” Respostas: 1 Discordo totalmente; 2 Discordo; 3 Nem concordo nem discordo; 4 Concordo; 5 Concordo totalmente; Não utilizei/não consigo avaliar.

**Tarefa observável relacionada:** Em `int resultado = 10 + 5 * 2;`, indicar o operador que organiza a expressão inteira, seus dois operandos e selecionar o trecho correspondente ao operando direito. Resposta de referência: raiz `+`, operando esquerdo `10`, operando direito `5 * 2`. Repetir com `int resultado = (10 + 5) * 2;`: raiz `*`, operandos `(10 + 5)` e `2`. Registrar acerto, necessidade de ajuda e justificativa, sem revelar o gabarito durante a tarefa.

Um estudo descritivo por tarefas pode registrar sucesso e percepção de apoio. Sem comparação adequada, pré/pós-teste e controle de fatores, não permite atribuir melhora de aprendizagem ou efeito causal ao realce da AST. Uma resposta Likert favorável é percepção, não prova de conhecimento.

## Para afirmar exclusividade de uma combinação

É necessário definir antes os critérios exatos, delimitar as versões e a busca, examinar recursos equivalentes por evidência e confirmar ausências relevantes nas ferramentas comparadas. Uma combinação com vários NI não estabelece exclusividade. A relação entre seleção AST, realce e explicação poderia virar um critério mais específico em revisão futura, mas precisaria ser verificada de novo para todas as referências. Não se deve escolher colunas depois de ver os resultados apenas para deixar uma única linha toda verde.

## Relação com colaboração / SBSC

O código auditado é uma ferramenta de uso individual em navegador. Avaliação por pares e atividade cooperativa de interpretação são desenhos de uso/estudo a definir; não significam edição compartilhada, chat, coautoria, rastreamento de pares ou colaboração síncrona implementados. Não marcar esses recursos como presentes nem afirmar aderência automática ao SBSC. Verificar chamada/trilha e explicitar qual questão de colaboração será investigada antes da coleta.

## Rastreabilidade

- Fonte das nove referências: `docs/etapa4/matriz-evidencias.csv` e `docs/etapa4/tarefa4.md`, especialmente §§2.5–2.7.
- Evidências próprias: caminhos/linhas da tabela e documentação da versão atual.
- Histórico funcional: `docs/registro-de-testes.md`, execução em 24/11/2026: 229 backend, 41 interface, 60 cenários de navegador e smoke aprovados. Esta auditoria documental não reexecutou esses testes.
- Artefatos: `matriz-atualizada.csv` e `matriz-atualizada.json`, com todas as células e suas evidências.
- Estado da coleta com pares: pendente na base examinada; atualizar somente após receber dados reais.
