#!/usr/bin/env python3
"""Gera o instrumento curto v3; não acessa nem publica no Google Forms."""
import csv
import json
from pathlib import Path

P = Path(__file__).resolve().parent
CONFIG = {
    'versao': '3.0',
    'titulo': 'Avaliação do software educacional Mini-C',
    'descricao': 'Depois de experimentar o Mini-C, responda a seis perguntas rápidas (cerca de 3 minutos). A participação é voluntária e não afeta notas. Não informe nome, e-mail ou matrícula. Os resultados serão apresentados em conjunto no trabalho acadêmico. Você pode parar antes de enviar. A atividade presencial é vista pelo colega e pelo facilitador; as anotações não terão nomes. Como o formulário não identifica você, pode não ser possível localizar sua resposta depois do envio.',
    'consentimento': {
        'id': 'C01', 'titulo': 'C01 — Você tem 18 anos ou mais e aceita participar?',
        'sim': 'Sim, tenho 18 anos ou mais e aceito participar.',
        'nao': 'Não. Encerrar o formulário.',
    },
    'modo': {'id': 'M01', 'titulo': 'M01 — Como você experimentou o software?', 'opcoes': ['Em dupla', 'Individual']},
    'objetivas': [
        {'id': 'Q01', 'titulo': 'Q01 — Em int x = 1; total = x + 2;, qual erro o software indicou?',
         'opcoes': ['A) Léxico.', 'B) Sintático.', 'C) Semântico.', 'D) Não sei.']},
        {'id': 'Q02', 'titulo': 'Q02 — No modo Sem cores, em int x = ;, qual fase indicou o erro?',
         'opcoes': ['A) Léxica.', 'B) Sintática.', 'C) Semântica.', 'D) Não sei.']},
    ],
    'likert': [
        {'id': 'L01', 'titulo': 'L01 — Foi fácil usar o software.'},
        {'id': 'L02', 'titulo': 'L02 — No modo Sem cores, consegui identificar os resultados sem depender das cores.'},
        {'id': 'L03', 'titulo': 'L03 — A tabela de símbolos ajudou a entender onde as variáveis foram declaradas.'},
    ],
    'escala': ['1 — Discordo totalmente', '2 — Discordo', '3 — Nem concordo nem discordo',
               '4 — Concordo', '5 — Concordo totalmente', 'N/A — Não usei ou não consigo avaliar'],
    'abertas': [{'id': 'A01', 'titulo': 'A01 — O que você melhoraria no software? (opcional)',
                 'ajuda': 'Pode citar uma dificuldade. Não inclua nomes ou outros dados pessoais.'}],
}


def gerar():
    c = CONFIG
    (P / 'instrumento.json').write_text(json.dumps(c, ensure_ascii=False, indent=2) + '\n')
    parts = ['# Formulário curto — Mini-C', '',
             '**Versão 3.0. Seis perguntas de avaliação, uma informação de modo e o aceite de participação. Ainda não aplicado.**', '',
             '## Título', '', c['titulo'], '', '## Descrição', '', c['descricao'], '',
             '## Aceite — primeira seção', '', c['consentimento']['titulo'], '',
             '- ' + c['consentimento']['sim'], '- ' + c['consentimento']['nao'], '',
             'No Google Forms, use “Ir para a seção com base na resposta”: Sim continua para a próxima seção; Não envia/encerra.', '',
             '## Uso do software — segunda seção', '', c['modo']['titulo'], '']
    parts += ['- ' + option for option in c['modo']['opcoes']] + ['']
    for q in c['objetivas']:
        parts += [q['titulo'], ''] + ['- ' + option for option in q['opcoes']] + ['']
    parts += ['Para as três afirmações abaixo, use a mesma escala:', '']
    parts += ['- ' + option for option in c['escala']] + ['']
    parts += [q['titulo'] + '\n' for q in c['likert']]
    parts += [c['abertas'][0]['titulo'], '', c['abertas'][0]['ajuda'], '',
              '## Configuração na sua conta', '',
              'Use múltipla escolha nas perguntas fechadas; deixe somente A01 opcional. Não ative coleta de e-mail, login obrigatório, limite por conta, modo teste ou resumo público. Não solicite nome, matrícula ou condição de saúde. Confira as regras de uso dos dados com o professor.', '',
              'Copie o conteúdo para um formulário em branco em https://forms.google.com. O arquivo criar_formulario.gs é uma alternativa opcional para gerar o formulário na sua conta pelo Apps Script; não foi executado no serviço Google. Nenhum link de formulário foi criado ou publicado nesta entrega.', '',
              'Preserve os códigos das perguntas ao exportar o CSV. Não misture respostas deste formulário com as da versão 2; os itens mudaram.', '']
    (P / 'formulario-texto.md').write_text('\n'.join(parts))
    short = ['---', 'title: "Avaliação do software Mini-C"', 'lang: pt-BR', '---', '',
             c['descricao'], '', '**Participação**', '', c['consentimento']['titulo'], '',
             '- ' + c['consentimento']['sim'], '- ' + c['consentimento']['nao'], '',
             c['modo']['titulo'] + ' **Em dupla / Individual**', '', '**Seis perguntas de avaliação**', '']
    for q in c['objetivas']:
        short += [q['titulo'], '', '  '.join(q['opcoes']), '']
    short += ['**Para L01–L03:** 1 discordo totalmente; 2 discordo; 3 nem concordo nem discordo; 4 concordo; 5 concordo totalmente; **N/A — não usei ou não consigo avaliar**.', '']
    short += [q['titulo'] + '\n' for q in c['likert']]
    short += [c['abertas'][0]['titulo'], '', 'Pode citar uma dificuldade. Não inclua dados pessoais.', '',
              '**Para criar no Forms:** perguntas fechadas obrigatórias; sugestão opcional. Sem coleta de e-mail, login obrigatório ou modo teste. Aceite em seção separada: Sim continua; Não encerra. Instrumento v3.0, ainda não aplicado; nenhum link foi criado nesta entrega.', '']
    (P / 'formulario-para-copiar.md').write_text('\n'.join(short))
    code = '''/** Instrumento v3: cria rascunho fechado na conta de quem executar.
 * Conferir configurações e navegação antes de liberar aos colegas.
 */
const INSTRUMENTO = ''' + json.dumps(c, ensure_ascii=False, indent=2) + ''';

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
'''
    (P / 'criar_formulario.gs').write_text(code)
    questions = [c['consentimento'], c['modo']] + c['objetivas'] + c['likert'] + c['abertas']
    with (P / 'respostas-cabecalho.csv').open('w', encoding='utf-8-sig', newline='') as f:
        csv.writer(f, lineterminator='\n').writerow(q['titulo'] for q in questions)
    print('Instrumento v3 gerado: seis perguntas, sem respostas de participantes.')


if __name__ == '__main__':
    gerar()
