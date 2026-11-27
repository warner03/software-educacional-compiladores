/** Gerador não executado nesta entrega. Cria formulário FECHADO para respostas.
 * Revise privacidade e navegação antes de disponibilizar manualmente.
 * Não é quiz; não envia gabarito aos participantes.
 */
const INSTRUMENTO = {
  "titulo": "Avaliação formativa do Visualizador Educacional Mini-C — Tarefa 5",
  "descricao": "Convite para estudantes adultos avaliarem uma atividade com o software Mini-C. Participação voluntária, sem relação com notas. Duração estimada: 15–20 minutos de atividade e 5–8 minutos de formulário. Não são solicitados nome, e-mail, matrícula ou áudio. Durante a atividade presencial, o facilitador e seu colega veem sua participação; a observação não é anônima para eles. As anotações serão minimizadas e os resultados apresentados somente em conjunto. O formulário não solicita identificadores diretos. Você pode desistir antes de enviar. Sem identificadores, pode não ser possível localizar uma resposta específica após o envio. Os dados serão usados no trabalho acadêmico; eventual uso em publicação depende das orientações institucionais aplicáveis. Não inclua dados pessoais nos campos abertos.",
  "consentimento": {
    "id": "C01",
    "titulo": "C01 — Consentimento e elegibilidade",
    "ajuda": "Participe somente se tiver 18 anos ou mais e concordar livremente com as condições acima. A opção Não encerra o formulário sem solicitar as tarefas ou outras respostas.",
    "sim": "Sim, tenho 18 anos ou mais e aceito participar voluntariamente.",
    "nao": "Não aceito participar ou tenho menos de 18 anos."
  },
  "modo": {
    "id": "M01",
    "titulo": "M01 — Modo de realização da atividade",
    "opcoes": [
      "Em dupla",
      "Individual"
    ]
  },
  "perfil": {
    "id": "P01",
    "titulo": "P01 — Perfil amplo",
    "opcoes": [
      "Estudante cursando Compiladores",
      "Estudante que já cursou Compiladores",
      "Docente ou monitor",
      "Outro perfil ou prefiro não informar"
    ]
  },
  "objetivas": [
    {
      "id": "Q01",
      "titulo": "Q01 — Qual operador está na raiz da expressão inicializadora?",
      "ajuda": "Considere o programa int resultado = 10 + 5 * 2; Responda sobre a expressão após =, não sobre o nó Programa ou Declaracao.",
      "opcoes": [
        "A) Soma (+).",
        "B) Multiplicação (*).",
        "C) Atribuição (=).",
        "D) Não sei."
      ]
    },
    {
      "id": "Q02",
      "titulo": "Q02 — Qual operador está na raiz da expressão com parênteses?",
      "ajuda": "Considere o programa int resultado = (10 + 5) * 2; Responda sobre a expressão após =.",
      "opcoes": [
        "A) Soma (+).",
        "B) Multiplicação (*).",
        "C) Atribuição (=).",
        "D) Não sei."
      ]
    },
    {
      "id": "Q03",
      "titulo": "Q03 — Como classificar o problema deste programa?",
      "ajuda": "Considere int x = ; e os resultados das análises no software.",
      "opcoes": [
        "A) Erro léxico: o ponto e vírgula não é reconhecido.",
        "B) Erro sintático: falta uma expressão após o sinal de igual.",
        "C) Erro semântico: os tipos int e float são incompatíveis.",
        "D) Não há erro nessa entrada.",
        "E) Não sei."
      ]
    },
    {
      "id": "Q04",
      "titulo": "Q04 — Qual é o resultado esperado para o símbolo inválido?",
      "ajuda": "Considere @ int x; na versão atual do software.",
      "opcoes": [
        "A) Há erro sintático e o parser continua normalmente.",
        "B) Há erro léxico e o parser não é executado.",
        "C) Há apenas erro semântico.",
        "D) Não sei."
      ]
    }
  ],
  "likert": [
    {
      "id": "L01",
      "titulo": "L01 — Selecionar um nó da AST ajudou-me a localizar o trecho correspondente no código."
    },
    {
      "id": "L02",
      "titulo": "L02 — A ligação entre AST interativa e trecho do código ajudou-me a explicar por que os parênteses mudam o agrupamento da expressão.",
      "ajuda": "Pergunta específica sobre a contribuição proposta: relacionar a estrutura da AST ao código-fonte. Responda sobre sua percepção nesta atividade."
    },
    {
      "id": "L03",
      "titulo": "L03 — As mensagens separadas por fase ajudaram-me a distinguir erro léxico de erro sintático."
    },
    {
      "id": "L04",
      "titulo": "L04 — Os rótulos e as explicações das construções na AST foram claros."
    },
    {
      "id": "L05",
      "titulo": "L05 — Discutir a interpretação do código com o colega ajudou-me a explicar minha resposta.",
      "ajuda": "Se realizou a atividade individualmente, selecione N/A."
    },
    {
      "id": "L06",
      "titulo": "L06 — Foi fácil usar a interface para realizar as tarefas propostas."
    }
  ],
  "escala": [
    "1 — Discordo totalmente",
    "2 — Discordo",
    "3 — Nem concordo nem discordo",
    "4 — Concordo",
    "5 — Concordo totalmente",
    "N/A — Não utilizei ou não consigo avaliar"
  ],
  "abertas": [
    {
      "id": "A01",
      "titulo": "A01 — Qual foi sua principal dificuldade nesta atividade?",
      "ajuda": "Opcional. Não escreva nomes, e-mails, matrícula ou informações que identifiquem alguém."
    },
    {
      "id": "A02",
      "titulo": "A02 — Que mudança você sugere para melhorar a atividade ou o software?",
      "ajuda": "Opcional. Não escreva dados pessoais."
    }
  ]
};

function criarFormularioMiniCTarefa5() {
  const c = INSTRUMENTO;
  const form = FormApp.create(c.titulo);
  form.setDescription(c.descricao);
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false);
  form.setIsQuiz(false);
  form.setShuffleQuestions(false);
  form.setPublishingSummary(false);
  form.setAllowResponseEdits(false);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage('Obrigado. As respostas serão analisadas em conjunto, sem pontuação ou nota.');
  form.setAcceptingResponses(false);

  const consentimento = form.addMultipleChoiceItem()
    .setTitle(c.consentimento.titulo)
    .setHelpText(c.consentimento.ajuda)
    .setRequired(true);
  const atividade = form.addPageBreakItem().setTitle('Modo de realização e interpretação');
  consentimento.setChoices([
    consentimento.createChoice(c.consentimento.sim, atividade),
    consentimento.createChoice(c.consentimento.nao, FormApp.PageNavigationType.SUBMIT)
  ]);
  [c.modo, c.perfil].forEach(function(q) {
    form.addMultipleChoiceItem().setTitle(q.titulo).setChoiceValues(q.opcoes).setRequired(true);
  });
  c.objetivas.forEach(function(q) {
    form.addMultipleChoiceItem().setTitle(q.titulo).setHelpText(q.ajuda)
      .setChoiceValues(q.opcoes).setRequired(true);
  });
  form.addSectionHeaderItem().setTitle('Sua percepção nesta atividade')
    .setHelpText('Não há resposta certa nos próximos itens. Se não usou o recurso, selecione N/A. No modo individual, L05 é N/A.');
  c.likert.forEach(function(q) {
    const item = form.addMultipleChoiceItem().setTitle(q.titulo)
      .setChoiceValues(c.escala).setRequired(true);
    if (q.ajuda) item.setHelpText(q.ajuda);
  });
  c.abertas.forEach(function(q) {
    form.addParagraphTextItem().setTitle(q.titulo).setHelpText(q.ajuda).setRequired(false);
  });
  Logger.log('FORMULÁRIO FECHADO PARA RESPOSTAS. Revise configurações na URL de edição:');
  Logger.log(form.getEditUrl());
  return form.getEditUrl();
}
