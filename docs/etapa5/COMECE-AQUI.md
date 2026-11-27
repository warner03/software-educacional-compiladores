---
title: 'Tarefa 5 — o que fazer agora'
author: 'Warner Pereira Cardoso Júnior'
lang: pt-BR
geometry: margin=2.2cm
fontsize: 11pt
---

# O que já está pronto

O artigo está atualizado com o Trabalho 5. Seu software aparece nas tabelas, agora com semântica, símbolos e dois critérios de acessibilidade. Os testes reais e as medidas de contraste estão descritos. Os dois artigos novos sobre avaliação continuam anexados à versão acadêmica com artigos.

**O professor também exige aplicar o formulário e analisar as respostas. Como você ainda vai fazer isso, essa é a única parte empírica que falta.** Não inventamos resultados de colegas.

# Como explicar o diferencial

“O meu software permite explorar as fases do compilador sem depender só das cores. Ele oferece um modo Sem cores com padrões e rótulos e outro de Alto contraste. Esses modos funcionam junto com os tokens, a árvore sintática e a tabela de símbolos: ao selecionar uma variável ou erro, o trecho aparece no código e na árvore. Os recursos já foram testados tecnicamente; agora vou avaliar com colegas se ajudam na interpretação.”

Você não precisa afirmar que é o único software com esses recursos. Nas publicações em que eles não foram confirmados, a tabela mostra NI, que significa informação insuficiente.

# 1. Crie o formulário curto

Abra https://forms.google.com na sua conta e crie um formulário em branco. Copie o título, a descrição e as perguntas de **formulario_avaliacao_simples.pdf**. São seis perguntas de avaliação, mais aceite e indicação se a pessoa usou sozinha ou em dupla.

Não ative coleta de e-mail, login obrigatório ou modo teste. Não peça nome ou matrícula. Configure o aceite em uma primeira seção: Sim segue para as perguntas; Não encerra. As perguntas fechadas são obrigatórias, com Não sei/N/A; a sugestão é opcional. Faça um teste da navegação e mantenha os testes técnicos separados das respostas dos colegas.

Há um gerador opcional criar_formulario.gs para Apps Script, caso prefira. Ele não foi executado na sua conta e nenhum link de Forms foi criado nesta entrega. A opção manual é suficiente.

# 2. Convide os colegas e faça as atividades

Combine com o professor as condições de participação e uso dos dados. No computador com o projeto atualizado, abra **Abrir no Console/Terminal** na pasta e execute:

```bash
docker compose up --build -d --wait
```

Abra **http://localhost:8501**. Esse endereço funciona no computador que executa o Docker. O link do Google Forms é separado.

Entregue aos colegas o **guia_para_colegas.pdf** e o link de responder ao formulário. Fique com o gabarito. A atividade tem três partes, leva aproximadamente 10–15 minutos e pode ser feita em dupla, alternando quem opera. Depois, cada pessoa responde ao formulário em cerca de três minutos. Registre somente sessão, ajuda e dificuldades, sem nomes.

Não é necessário um estudo longo ou perguntas complexas. A meta de duplas no protocolo é uma previsão: registre a quantidade real que conseguir, inclusive dificuldades e não conclusões.

# 3. Incorpore as respostas ao artigo

No Forms, abra **Respostas** e baixe o CSV. Se vier um ZIP, extraia o CSV. Confira que não há nomes, e-mails ou outros identificadores antes de compartilhar. Traga o CSV e o registro das sessões sem nomes; informe também o número de sessões, se foram individuais/em dupla e qualquer mudança de versão.

Esses dados permitem completar a seção 6.3 com resultados reais e discutir as dificuldades. Até lá, use o PDF como **versão revisada com validação técnica e coleta pendente**, sem dizer que o requisito de resultados de colegas já foi cumprido.

# Sobre o SBSC

O texto entregue é a versão ampliada da disciplina. Para o evento, o professor ainda precisa definir a trilha; será necessário ajustar tamanho, anonimato e evidências. A chamada consultada informa 15/12/2026 para Pesquisa, Desenho e IIRE. Nenhuma submissão foi feita.
