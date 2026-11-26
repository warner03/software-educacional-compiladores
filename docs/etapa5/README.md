# Tarefa 5 — estratégia de implementação e avaliação

Preparação em 26/11/2026. **Estado: versão para coleta; avaliação com colegas ainda não aplicada.** A Tarefa 5 só estará concluída depois de incorporar respostas e observações reais. Código funcional examinado: `7fcb5ca`; o Trabalho 5 prático não foi implementado nesta alteração.

## Materiais

- [Artigo atualizado, identificado para a disciplina](tarefa5.md)
- [Comece aqui: aplicação e conclusão](COMECE-AQUI.md)
- [Matriz com nove estudos e o próprio projeto](matriz-atualizada.md) — [CSV](matriz-atualizada.csv) — [JSON](matriz-atualizada.json)
- [Duas novas fontes sobre avaliação](fontes-avaliacao.md) — [referências estruturadas](novas-referencias.json)
- [Protocolo versão 2.0](protocolo.md)
- [Instrumentos e instruções](instrumentos/LEIA-ME.md)
- [Perguntas prontas para Google Forms](instrumentos/formulario-texto.md) — [gerador opcional, não executado](instrumentos/criar_formulario.gs)
- [Guia para colegas, sem gabarito](instrumentos/guia-para-colegas.md)
- [Resultados funcionais observados](resultados/resumo-resultados.md) — [casos individuais CSV](resultados/casos_funcionais.csv)
- [Estado da coleta: sem respostas](resultados/estado-coleta.json)
- [Conferência e correções da preparação](revisao-metodologica.md)
- [Enquadramento na chamada SBSC 2027](enquadramento-sbsc2027.md)
- [Fundamentação complementar da atividade em duplas](fundamentacao-colaboracao.md)

Os PDFs acadêmicos e os dois artigos integrais acompanham o pacote entregue no chat. Os PDFs de terceiros não são republicados neste repositório; as referências mantêm os links oficiais. A existência de download público não foi tratada como licença de redistribuição irrestrita.

## Comparação e contribuição

As 135 classificações dos nove estudos anteriores foram preservadas e 15 células próprias acrescentadas. A linha descreve a versão implementada; não marca semântica, geração de código, estudo com estudantes ou aprendizagem como presentes. Navegar por artefatos prontos não foi reclassificado como animação dos passos do algoritmo. NI continua diferente de ausência.

A contribuição proposta é organizar e avaliar a exploração integrada de fonte, tokens, AST simplificada e diagnósticos em tarefas de interpretação. A atividade em dupla utiliza explicação e alternância de papéis externas ao software; não há colaboração multiusuário implementada. Exclusividade técnica e melhora de aprendizagem não foram demonstradas.

## Resultados técnicos desta rodada

229 testes de backend, 41 de interface, 60 cenários de navegador e integração aprovados. O protocolo congelado teve 33/33 casos aplicáveis aprovados via API real; eles já pertencem à suíte e não são somados como novos testes independentes. M01–M03 só tiveram aceitação sintática verificada; semântica permanece 0/3 executada e três pendentes. Cobertura de código não foi medida.

## Reprodução e análise

Na raiz, depois de iniciar os serviços:

```bash
python3 scripts/avaliar_plano_funcional.py --saida /tmp/mini-c-tarefa5-nova-rodada
```

O script aceita `--raiz`, `--saida` e `--url`. Os esperados vêm das fixtures anteriores ao parser. A versão portável adapta os caminhos do executor usado na coleta técnica, preservando as verificações. Os logs desta rodada estão em `resultados/`.

Após coletar dados reais, no diretório dos instrumentos:

```bash
python3 analisar_respostas.py respostas-reais.csv --saida analise-respostas.json
```

Esse CSV de respostas reais ainda não existe nesta entrega. O arquivo de cabeçalho contém zero registros; sua análise não calcula estatísticas. A análise é descritiva, separada por modo/perfil, com N/A fora do denominador de cada item. Não há escore SUS ou nota global de aprendizagem. L05 só se aplica ao modo Em dupla.

Quatro testes técnicos do analisador, com **APENAS DADOS SINTÉTICOS DE TESTE**, passaram. Eles não geram respostas de participantes:

```bash
cd docs/etapa5/instrumentos
python3 -m unittest -v test_analise_instrumento.py
```

## Pendências concretas

Criar/revisar o formulário na conta Google do autor, aplicar o protocolo a colegas voluntários e incorporar as respostas/observações reais. O gerador foi conferido estaticamente, sem execução no Google; nenhum link foi publicado ou enviado. Antes de uma futura submissão ao SBSC, escolher a trilha com o professor, consolidar evidências, adequar tamanho e anonimizar o texto e os artefatos.
