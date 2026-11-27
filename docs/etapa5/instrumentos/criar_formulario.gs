/** Instrumento v3: cria rascunho fechado na conta de quem executar.
 * Conferir configurações e navegação antes de liberar aos colegas.
 */
const INSTRUMENTO = {
  "versao": "3.0",
  "titulo": "Avaliação do software educacional Mini-C",
  "descricao": "Depois de experimentar o Mini-C, responda a seis perguntas rápidas (cerca de 3 minutos). A participação é voluntária e não afeta notas. Não informe nome, e-mail ou matrícula. Os resultados serão apresentados em conjunto no trabalho acadêmico. Você pode parar antes de enviar. A atividade presencial é vista pelo colega e pelo facilitador; as anotações não terão nomes. Como o formulário não identifica você, pode não ser possível localizar sua resposta depois do envio.",
  "consentimento": {
    "id": "C01",
    "titulo": "C01 — Você tem 18 anos ou mais e aceita participar?",
    "sim": "Sim, tenho 18 anos ou mais e aceito participar.",
    "nao": "Não. Encerrar o formulário."
  },
  "modo": {
    "id": "M01",
    "titulo": "M01 — Como você experimentou o software?",
    "opcoes": [
      "Em dupla",
      "Individual"
    ]
  },
  "objetivas": [
    {
      "id": "Q01",
      "titulo": "Q01 — Em int x = 1; total = x + 2;, qual erro o software indicou?",
      "opcoes": [
        "A) Léxico.",
        "B) Sintático.",
        "C) Semântico.",
        "D) Não sei."
      ]
    },
    {
      "id": "Q02",
      "titulo": "Q02 — No modo Sem cores, em int x = ;, qual fase indicou o erro?",
      "opcoes": [
        "A) Léxica.",
        "B) Sintática.",
        "C) Semântica.",
        "D) Não sei."
      ]
    }
  ],
  "likert": [
    {
      "id": "L01",
      "titulo": "L01 — Foi fácil usar o software."
    },
    {
      "id": "L02",
      "titulo": "L02 — No modo Sem cores, consegui identificar os resultados sem depender das cores."
    },
    {
      "id": "L03",
      "titulo": "L03 — A tabela de símbolos ajudou a entender onde as variáveis foram declaradas."
    }
  ],
  "escala": [
    "1 — Discordo totalmente",
    "2 — Discordo",
    "3 — Nem concordo nem discordo",
    "4 — Concordo",
    "5 — Concordo totalmente",
    "N/A — Não usei ou não consigo avaliar"
  ],
  "abertas": [
    {
      "id": "A01",
      "titulo": "A01 — O que você melhoraria no software? (opcional)",
      "ajuda": "Pode citar uma dificuldade. Não inclua nomes ou outros dados pessoais."
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
  form.setConfirmationMessage('Obrigado! As respostas serão analisadas em conjunto.');
  form.setAcceptingResponses(false);
  const consentimento = form.addMultipleChoiceItem()
    .setTitle(c.consentimento.titulo).setRequired(true);
  const perguntas = form.addPageBreakItem().setTitle('Sua experiência com o Mini-C');
  consentimento.setChoices([
    consentimento.createChoice(c.consentimento.sim, perguntas),
    consentimento.createChoice(c.consentimento.nao, FormApp.PageNavigationType.SUBMIT)
  ]);
  form.addMultipleChoiceItem().setTitle(c.modo.titulo)
    .setChoiceValues(c.modo.opcoes).setRequired(true);
  c.objetivas.forEach(function(q) {
    form.addMultipleChoiceItem().setTitle(q.titulo).setChoiceValues(q.opcoes).setRequired(true);
  });
  c.likert.forEach(function(q) {
    form.addMultipleChoiceItem().setTitle(q.titulo).setChoiceValues(c.escala).setRequired(true);
  });
  c.abertas.forEach(function(q) {
    form.addParagraphTextItem().setTitle(q.titulo).setHelpText(q.ajuda).setRequired(false);
  });
  Logger.log('Rascunho fechado. Abra o endereço de edição, confira as configurações e libere manualmente:');
  Logger.log(form.getEditUrl());
  return form.getEditUrl();
}
