# Tarefa 5 — revisão após o Trabalho 5

Versão de 26/11/2026, atualizada com análise semântica, tabela de símbolos e apoio ao daltonismo já implementados. **Texto, matriz e instrumento estão revisados; a exigência de resultados com colegas depende de aplicar o formulário.** Não existem respostas humanas nesta entrega.

## Arquivos principais

- [Artigo completo](tarefa5.md)
- [Comece aqui](COMECE-AQUI.md)
- [Matriz: nove estudos e seu software, 17 critérios](matriz-atualizada.md) — [CSV](matriz-atualizada.csv) — [JSON](matriz-atualizada.json)
- [Auditoria dos critérios novos de acessibilidade](auditoria-acessibilidade.md)
- [Síntese dos dois artigos metodológicos](fontes-avaliacao.md)
- [Protocolo curto v3](protocolo.md)
- [Formulário: seis perguntas](instrumentos/formulario-texto.md)
- [Guia dos colegas](instrumentos/guia-para-colegas.md)
- [Roteiro do facilitador](instrumentos/roteiro-aplicacao.md) — [gabarito separado](instrumentos/gabarito-facilitador.md)
- [Resultados técnicos atuais](resultados/resumo-resultados.md) — [estado da coleta](resultados/estado-coleta.json)
- [Relação com a chamada SBSC 2027](enquadramento-sbsc2027.md)
- [Conferências desta revisão](revisao-metodologica.md)
- [Correspondência com as exigências da tarefa](entrega.md)
- [Histórico anterior ao Trabalho 5](historico/versao2/LEIA-ME.md)

## O diferencial

**Exploração de tokens, AST, símbolos e diagnósticos com modos Sem cores e Alto contraste, usando padrões/rótulos e contornos para reduzir a dependência de cores.** O recurso é implementado e tecnicamente verificado. NI nos artigos comparados não demonstra ausência ou exclusividade; não houve avaliação com pessoas daltônicas.

A linha própria passa a confirmar semântica e símbolos. Continuam fora do escopo geração de código, árvore de derivação e animação das transformações do algoritmo. As colunas de aplicação com estudantes e aprendizagem continuam negativas porque a coleta não ocorreu. A matriz não é um ranking por número de marcas.

## Fundamentação e resultados

Os dois artigos novos continuam sendo **Pontes et al. (2019), Avaliação de Ferramentas para Ensino de Programação para Crianças e Adolescentes**, e **Veras et al. (2020), Desenvolvimento e Avaliação da Usabilidade em Aplicativo Desktop para o Ensino da Programação Orientada a Objetos**. Os PDFs integrais acompanham a versão acadêmica com anexos entregue no chat; o repositório mantém referências e links oficiais.

A rodada do Trabalho 5 registrou 322 testes de backend, 55 de interface, 134 cenários de navegador, integração e 30/30 casos semânticos aprovados. A revisão teórica reutiliza esses registros identificados por hashes; não representa uma nova execução. Os trinta casos já integram a suíte e não são somados como novos testes independentes.

## Formulário e coleta

O instrumento v3 possui duas questões objetivas, três afirmações e uma sugestão opcional, além de aceite e modo de uso. **L02:** “No modo Sem cores, consegui identificar os resultados sem depender das cores.” Não coleta nome, e-mail, matrícula ou condição de saúde.

Nenhum Google Forms foi criado/publicado. Copie o texto para sua conta ou utilize o gerador opcional. Depois da coleta, exporte o CSV e use:

```bash
python3 docs/etapa5/instrumentos/analisar_respostas.py respostas-reais.csv --saida analise-respostas.json
```

Para conferir os quatro testes do analisador (apenas dados sintéticos de código):

```bash
cd docs/etapa5/instrumentos
python3 -m unittest -v test_analise_instrumento.py
```

Não misture respostas dos instrumentos v2 e v3; os itens e gabaritos mudaram. Uma planilha vazia produz estatísticas nulas. Sem os dados reais, o artigo não declara a avaliação por pares concluída. A versão ampliada da disciplina também exige adaptação antes de uma eventual submissão ao SBSC.
