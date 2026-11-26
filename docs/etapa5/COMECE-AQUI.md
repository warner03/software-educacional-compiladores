---
title: 'Tarefa 5 — próximos passos para Warner'
subtitle: 'Guia de aplicação e conclusão da avaliação'
lang: pt-BR
geometry: margin=2.2cm
fontsize: 11pt
---

# O que está pronto

O artigo foi atualizado com seu projeto na matriz, dois novos artigos de avaliação, método fundamentado, pergunta específica da contribuição, resultados funcionais reais e limitações. O software continua na versão prática da Etapa 4; o Trabalho 5 prático será tratado depois de receber suas instruções.

**O que falta para concluir a Tarefa 5:** criar/revisar o Google Forms na sua conta, aplicar a avaliação com colegas e incorporar as respostas reais. O arquivo do artigo está identificado como **versão para coleta**, porque não há dados humanos ainda. A versão identificada da disciplina também não é o PDF de uma submissão ao SBSC.

# 1. Confira o protocolo com o professor

O método proposto é uma avaliação formativa: tarefas com respostas de referência, observação, perguntas objetivas, seis itens de percepção e comentários. Não foi escolhida uma SUS adaptada. A pergunta L02 trata diretamente do apoio da AST para explicar o efeito dos parênteses; Q01 e Q02 conferem respostas sobre a estrutura.

O modo principal é atividade em duplas no mesmo computador, com alternância entre quem opera e quem explica. Meta inicial: 4–6 duplas, caso viável, sem inventar uma amostra mínima. Se houver menos colegas, registrar a quantidade real. Um piloto individual é possível e ficará separado. Combine as condições de participação e uso dos dados com o professor antes de aplicar.

# 2. Crie o formulário na sua conta Google

**Opção manual:** abra https://forms.google.com, crie um formulário em branco e copie as perguntas de `instrumentos/formulario-texto.md` ou do PDF do formulário. Preserve os códigos C01, M01, P01, Q01–Q04, L01–L06 e A01–A02 nos títulos. O texto também informa a configuração das seções e da saída por consentimento.

**Opção automatizada, se preferir:**

1. Acesse https://script.google.com com sua conta Google e escolha Novo projeto.
2. Abra `instrumentos/criar_formulario.gs` em um editor de texto e copie todo o conteúdo para o editor do Apps Script, substituindo o exemplo que estiver lá.
3. Salve. Selecione a função `criarFormularioMiniCTarefa5` e clique em Executar.
4. Revise as permissões de criação do formulário solicitadas na sua conta. Esse código não foi executado no serviço Google nesta entrega.
5. O registro de execução mostrará um endereço de **edição** do formulário. Abra esse endereço. Ele é criado fechado para respostas.
6. Revise as questões e configurações. Faça testes técnicos da navegação Sim/Não separados da coleta e remova apenas as respostas desses testes identificados antes da aplicação.
7. Depois da revisão, libere o formulário para os respondentes pelos controles do próprio Google Forms e copie o link de **responder**, que é o link destinado aos colegas.

O formulário deve ficar sem coleta de e-mail, nome ou matrícula, sem resumo público e sem modo quiz. Não configure restrição de login ou domínio para identificar quem respondeu. A saída Não no consentimento encerra o formulário. As perguntas abertas são opcionais. Se sua organização impedir alguma configuração, confira a alternativa com o professor.

**Nenhum link de Google Forms foi criado ou publicado nesta sessão.** Os arquivos são o conteúdo e o gerador para você usar na sua conta.

# 3. Aplique a atividade

No computador da atividade, inicie o software na pasta do projeto:

```bash
docker compose up -d --wait
```

Abra `http://localhost:8501`. Esse endereço funciona no computador onde os serviços estão rodando. Para a atividade presencial em dupla, os dois colegas usam essa mesma tela. O link do formulário Google é separado do endereço local do software.

Use `instrumentos/roteiro-aplicacao.md` como facilitador. Entregue aos colegas somente `instrumentos/guia-para-colegas.md` e o link do formulário. O gabarito e o artigo completo ficam com você durante a coleta para evitar apresentar as respostas de referência antes das tarefas.

A duração total estimada é 20–30 minutos. Explique os controles, obtenha concordância voluntária antes das tarefas e siga as quatro atividades. As pessoas alternam quem opera e quem explica, depois respondem ao formulário individualmente. Use `observacoes-cabecalho.csv` para anotar somente sessões, conclusão, ajuda e dificuldades, sem nomes ou ligação individual com o Forms.

A observação presencial é conhecida pelo facilitador e pela dupla; o compromisso é minimizar os registros e apresentar resultados agregados. O formulário não solicita identificadores diretos. Preserve os dados de forma restrita e combine o prazo de guarda com o professor.

# 4. Exporte as respostas e conclua o artigo

No Google Forms, abra Respostas e baixe as respostas em CSV. Se o download vier em ZIP, extraia o CSV. Confira que não há nomes, e-mails, matrícula ou outros identificadores antes de compartilhar o arquivo; mantenha os prefixos das perguntas. Os metadados de data/hora não são necessários para a análise agregada.

Envie aqui o CSV das respostas reais e o registro das sessões sem identificadores. Informe também quantas sessões ocorreram, se houve aplicação individual ou em dupla e se houve mudanças de versão ou ajuda fora do roteiro. Com esses dados será possível completar a seção de resultados, discutir limitações e atualizar a matriz de avaliação com estudantes.

O arquivo `respostas-cabecalho.csv` está vazio de propósito: é um modelo de estrutura, não resultado. O analisador mantém as estatísticas nulas enquanto não há respostas elegíveis.

# 5. Artigos escolhidos e SBSC

Os dois artigos novos de método são:

- Pontes et al. (2019): *Avaliação de Ferramentas para Ensino de Programação para Crianças e Adolescentes*.
- Veras et al. (2020): *Desenvolvimento e Avaliação da Usabilidade em Aplicativo Desktop para o Ensino da Programação Orientada a Objetos*.

Os PDFs oficiais acompanham a entrega acadêmica. Uma fonte complementar sobre o Modelo 3C fundamenta o desenho da atividade em dupla. Nenhuma fonte comprova antecipadamente aprendizagem no Mini-C.

A chamada SBSC 2027 informa prazo de 15/12/2026 para Pesquisa, Desenho de Pesquisa e IIRE. O enquadramento provisório mais próximo de um estudo ainda em planejamento é Desenho de Pesquisa; a escolha final depende do professor, da atividade colaborativa concretizada e dos resultados disponíveis. A nota no pacote explica páginas, anonimato e declaração de IA. Não houve submissão ao evento.
