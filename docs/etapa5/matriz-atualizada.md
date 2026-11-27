# Matriz comparativa — revisão após o Trabalho 5

Base de código `2b535d1`. Dez linhas e 17 critérios: 170 classificações rastreáveis. As 135 células dos nove estudos da Tarefa 4 são preservadas. Acrescentam-se dois critérios de acessibilidade para todos os estudos e atualiza-se a linha própria.

**Legenda:** ✓ presença confirmada; ✗ ausência documentada; NI informação insuficiente; N/A não aplicável. Não há colunas separadas de ano ou nome de software. Os critérios novos não foram usados para produzir um ranking ou atribuir ausência aos demais.

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
| **Este trabalho — Mini-C (estado implementado)** | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ |

## Acessibilidade visual e avaliação

| Referência | Sem cores | Alto contraste | Estudantes | Aprendizagem |
|---|---|---|---|---|
| Graciano Junior et al. (2022) | NI | NI | ✓ | NI |
| Borela et al. (2025) | NI | NI | ✓ | NI |
| Santini et al. (2022) | N/A | N/A | N/A | N/A |
| Mernik e Žumer (2003) | NI | NI | ✓ | ✓ |
| Resler e Deaver (1998) | NI | NI | NI | NI |
| Rodger et al. (2009) | NI | NI | ✓ | ✓ |
| Moreno et al. (2004) | NI | NI | ✗ | ✗ |
| Schneider et al. (2005) | NI | NI | NI | NI |
| Jabri (2013) | NI | NI | ✓ | ✓ |
| **Este trabalho — Mini-C (estado implementado)** | ✓ | ✓ | ✗ | ✗ |

## Definições e leitura

“Entrada” significa edição do programa-alvo; “AST” não equivale a árvore de derivação; “Passos” exige acompanhamento das transformações do algoritmo, não navegação por resultados prontos. “Símb.” confirma identificadores e atributos, sem exigir que todas as ferramentas tenham a mesma interação.

“Sem cores” exige modo selecionável que preserve a distinção dos resultados por padrões/rótulos, sem depender da cor; “Alto contraste” exige modo visual alternativo explicitamente documentado. Uma figura em preto e branco, realce colorido ou simples interface textual não confirma esses modos. Os critérios derivam da demanda de acessibilidade e dos princípios W3C de redundância da informação e contraste; não são requisitos universais de todas as ferramentas.

“Estudantes” exige aplicação com participantes. “Aprendizagem” exige evidência pertinente de conhecimento/desempenho, a interpretar segundo o desenho do estudo. Mini-C continua sem resultados humanos; a aprovação dos testes não muda essas duas marcações.

O diferencial implementado combina modos Sem cores/Alto contraste com exploração de tokens, AST, símbolos e diagnósticos localizados. NI nas outras linhas impede concluir exclusividade ou superioridade. Os dois novos artigos metodológicos, Pontes et al. (2019) e Veras et al. (2020), fundamentam o protocolo e são sintetizados separadamente no artigo.

## Evidências próprias

| Critério | Estado | Evidência e limite |
|---|---|---|
| Web | ✓ | frontend/index.html; frontend/nginx.conf; docker-compose.yml. Interface web executada em navegador; não implica serviço público nem colaboração multiusuário. |
| Entrada | ✓ | frontend/index.html: editor codigo; frontend/app.js: envio para /api/analisar. Edição de programa Mini-C. |
| Exemplos | ✓ | frontend/index.html: seletor com 14 opções data-codigo. Exemplos editáveis válidos e com erros intencionais das três fases. |
| Léxica | ✓ | backend/app/scanner.py; backend/tests/test_scanner.py. Scanner preservado da versão anterior; tokens/lexemas/posições. |
| Sintática | ✓ | backend/app/parser.py; backend/tests/test_parser.py. Parser descendente recursivo preservado, com precedência e recuperação. |
| AST | ✓ | backend/app/parser.py; docs/ast.md; frontend/app.js: mostrarSintatica e filhosAST. AST simplificada, navegação, intervalos, ligação ao fonte e exportação JSON. |
| Derivação | ✗ | docs/ast.md; docs/gramatica.md. A representação implementada é AST, sem árvore de derivação. |
| Semânt. | ✓ | backend/app/semantica.py; backend/app/main.py; backend/tests/test_semantica.py; docs/semantica.md. Declaração, redeclaração, escopos, tipos, condição bool e inicialização definida; não C completo. |
| Símb. | ✓ | backend/app/semantica.py: simbolos/escopos; frontend/app.js: tabela-simbolos; frontend/tests/semantica.test.js. Tabela filtrável por escopo, nome/tipo/posição/inicialização, sombreamento e referências; seleção liga fonte e AST. |
| Geração | ✗ | docs/semantica.md: fora do recorte; README.md. Sem execução, código intermediário ou código-alvo. |
| Passos | ✗ | docs/ast.md; README.md: continuidade. Navegação por artefatos prontos não é animação das transformações do algoritmo. |
| Diag. | ✓ | backend/app/main.py; backend/app/semantica.py; frontend/app.js: mostrarSemantica. Três fases, localização, regra e sugestão; fase anterior inválida bloqueia as posteriores. |
| Explic. | ✓ | frontend/app.js: REGRAS_SEMANTICAS e explicações da AST; frontend/index.html: guia/legenda. Explicações em português e sugestões determinísticas, sem IA em tempo de uso. |
| Sem cores | ✓ | frontend/index.html: modo-visual; frontend/style.css: data-visual=sem-cores e padrões por categoria; frontend/app.js: aplicarVisual; docs/trabalho5/capturas/tokens-sem-cores-desktop.png. Modo selecionável com padrões/rótulos, contornos e legenda. Confirma implementação; não comprova eficácia com pessoas daltônicas. |
| Alto contraste | ✓ | frontend/style.css: data-visual=contraste; docs/trabalho5/capturas/contraste-medido.json; scripts/teste_navegador.py. Modo selecionável. Menores razões observadas: texto 16,275:1, foco 13,584:1, seleção 4,217:1, somente nos elementos medidos. |
| Estudantes | ✗ | docs/etapa5/resultados/estado-coleta.json; informação do autor: avaliação ainda será aplicada. Não existem respostas reais de colegas. Testes técnicos não substituem aplicação com pessoas. |
| Aprendizagem | ✗ | docs/etapa5/protocolo.md; docs/etapa5/resultados/estado-coleta.json. Sem medida humana concluída. Nem percepção futura nem testes de software demonstram ganho de aprendizagem. |

[Auditoria dos critérios novos](auditoria-acessibilidade.md) · [CSV com todas as evidências](matriz-atualizada.csv) · [JSON](matriz-atualizada.json)
