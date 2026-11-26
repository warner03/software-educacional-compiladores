# Instrumentos da Tarefa 5

**Situação real:** não houve coleta com colegas nesta entrega. Não há link Google Forms criado. Os dois CSV contêm somente cabeçalhos. Os testes do analisador usam exclusivamente dados sintéticos dentro do código de teste, sem produzir uma tabela de resultados de participantes.

## Arquivos e destinatários

- `guia-para-colegas.md`: instruções aos participantes, sem gabarito.
- `formulario-texto.md`: perguntas e opções prontas para copiar ao Google Forms.
- `criar_formulario.gs`: gerador opcional a executar pelo usuário na sua conta Google; cria formulário fechado para respostas.
- `instrumento.json`: mesma definição das questões, sem respostas corretas.
- `roteiro-aplicacao.md`: protocolo do facilitador para duplas com alternância e piloto individual separado.
- `gabarito-facilitador.md`: reservado ao facilitador; não entregar antes das tarefas.
- `observacoes-cabecalho.csv`: somente cabeçalho de registro das sessões, sem identidades ou vínculo com formulários.
- `respostas-cabecalho.csv`: somente cabeçalho do CSV individual, sem linhas de respostas.
- `analisar_respostas.py`: análise descritiva de CSV; contém gabarito técnico para correção e é arquivo do facilitador.
- `test_analise_instrumento.py`: quatro testes técnicos, APENAS DADOS SINTÉTICOS DE TESTE.
- `preparar_instrumento.py`: regenera texto, JSON, gerador .gs e cabeçalho a partir da mesma definição. Não conecta ao Google.

## Criar o formulário em sua conta

1. Abra https://script.google.com/ e escolha Novo projeto.
2. No editor, substitua o código pelo conteúdo de `criar_formulario.gs` e salve.
3. Escolha a função `criarFormularioMiniCTarefa5` e clique em Executar. Revise as permissões de criar/editar formulário na sua conta.
4. Abra o Registro de execução e copie a URL de **edição** mostrada. O formulário está fechado para respostas.
5. Revise as configurações: sem e-mail, sem nome/matrícula, sem login obrigatório, sem quiz ou resumo público. Teste o encaminhamento do consentimento Sim/Não; confira limitações de contas institucionais.
6. Após a revisão e orientações aplicáveis, disponibilize/publique manualmente o formulário e abra as respostas. Só então copie o link para participantes. Esta entrega não publicou nem enviou convite a ninguém.

O gerador foi conferido estaticamente; não foi executado nem validado dentro do Google Forms. O responsável deve testar o formulário real antes da coleta.

## Analisar respostas reais

Baixe as respostas em CSV do Google Forms ou da planilha associada. Se o Google entregar um ZIP, extraia o CSV. Mantenha os prefixos C01, M01, P01, Q01–Q04, L01–L06 e A01–A02 nos títulos das questões. As colunas adicionais de data/hora/e-mail não são usadas na análise.

No Linux, dentro da pasta dos instrumentos:

```bash
python3 analisar_respostas.py respostas-reais.csv --saida analise-respostas.json
```

O nome `respostas-reais.csv` representa o arquivo que será exportado após a aplicação; ele ainda não existe como base coletada nesta entrega.

O analisador exclui respostas sem consentimento/elegibilidade, mantém Em dupla e Individual separados e apresenta também estratos de perfil amplo. Corrige os quatro itens objetivos separadamente, com denominador explícito; Não sei é válido e não correto. Para os seis itens próprios de percepção, apresenta frequências e medianas; N/A, valores ausentes e inválidos não entram no denominador. L05 é aplicável somente quando M01 confirma Em dupla. No modo Individual ele é não aplicável; modo ausente/inválido fica em estrato separado com aplicabilidade indeterminada. Ambos ficam fora das estatísticas desse item, com contadores explícitos. Valores numéricos indevidos são contados como inconsistências de modo, sem produzir mediana. Não calcula SUS, soma Likert, nota global ou ganho de aprendizagem.

O programa emite somente contagens de preenchimento dos campos abertos. Não reproduz comentários, nomes, e-mails, horários ou categorias livres que possam identificar alguém. Observações de sessão devem ser analisadas separadamente, agregadas e sem associá-las aos formulários individuais. A observação presencial não é anônima para o facilitador; os registros são minimizados. Revisar estratos pequenos antes de publicação.

Com o CSV de cabeçalho vazio, este comando retorna `sem_respostas` e `estatisticas_por_modo: null`:

```bash
python3 analisar_respostas.py respostas-cabecalho.csv
```

## Verificação técnica do analisador

```bash
python3 -m unittest -v test_analise_instrumento.py
```

Foram executados **quatro testes, todos aprovados**, somente com dados sintéticos de teste: (1) exclusão por consentimento, estratificação, frequência/mediana e ausência de exposição de identificadores; (2) N/A, valores ausentes/inválidos e L05 no modo individual; (3) cabeçalho sem registros ou todos sem consentimento resultam em estatísticas nulas; (4) modo ausente/inválido e L05 = 5 não produzem frequência/mediana e ficam rastreados como aplicabilidade indeterminada. Esses testes verificam o código de análise, não constituem avaliação educacional ou dados de participantes.

## Correção identificada na revisão independente

A primeira versão excluía L05 somente no modo Individual e ainda calculava o item em modo ausente/inválido. Corrigiu-se a aplicabilidade para exigir Em dupla, com contadores específicos e um quarto teste de regressão. Não houve dados humanos envolvidos nem alteração do texto da pergunta L05.
