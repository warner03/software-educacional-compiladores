from pathlib import Path
import json,csv
P=Path(__file__).resolve().parent
config={
 'titulo':'Avaliação formativa do Visualizador Educacional Mini-C — Tarefa 5',
 'descricao':'Convite para estudantes adultos avaliarem uma atividade com o software Mini-C. Participação voluntária, sem relação com notas. Duração estimada: 15–20 minutos de atividade e 5–8 minutos de formulário. Não são solicitados nome, e-mail, matrícula ou áudio. Durante a atividade presencial, o facilitador e seu colega veem sua participação; a observação não é anônima para eles. As anotações serão minimizadas e os resultados apresentados somente em conjunto. O formulário não solicita identificadores diretos. Você pode desistir antes de enviar. Sem identificadores, pode não ser possível localizar uma resposta específica após o envio. Os dados serão usados no trabalho acadêmico; eventual uso em publicação depende das orientações institucionais aplicáveis. Não inclua dados pessoais nos campos abertos.',
 'consentimento':{'id':'C01','titulo':'C01 — Consentimento e elegibilidade','ajuda':'Participe somente se tiver 18 anos ou mais e concordar livremente com as condições acima. A opção Não encerra o formulário sem solicitar as tarefas ou outras respostas.','sim':'Sim, tenho 18 anos ou mais e aceito participar voluntariamente.','nao':'Não aceito participar ou tenho menos de 18 anos.'},
 'modo':{'id':'M01','titulo':'M01 — Modo de realização da atividade','opcoes':['Em dupla','Individual']},
 'perfil':{'id':'P01','titulo':'P01 — Perfil amplo','opcoes':['Estudante cursando Compiladores','Estudante que já cursou Compiladores','Docente ou monitor','Outro perfil ou prefiro não informar']},
 'objetivas':[
 {'id':'Q01','titulo':'Q01 — Qual operador está na raiz da expressão inicializadora?','ajuda':'Considere o programa int resultado = 10 + 5 * 2; Responda sobre a expressão após =, não sobre o nó Programa ou Declaracao.','opcoes':['A) Soma (+).','B) Multiplicação (*).','C) Atribuição (=).','D) Não sei.']},
 {'id':'Q02','titulo':'Q02 — Qual operador está na raiz da expressão com parênteses?','ajuda':'Considere o programa int resultado = (10 + 5) * 2; Responda sobre a expressão após =.','opcoes':['A) Soma (+).','B) Multiplicação (*).','C) Atribuição (=).','D) Não sei.']},
 {'id':'Q03','titulo':'Q03 — Como classificar o problema deste programa?','ajuda':'Considere int x = ; e os resultados das análises no software.','opcoes':['A) Erro léxico: o ponto e vírgula não é reconhecido.','B) Erro sintático: falta uma expressão após o sinal de igual.','C) Erro semântico: os tipos int e float são incompatíveis.','D) Não há erro nessa entrada.','E) Não sei.']},
 {'id':'Q04','titulo':'Q04 — Qual é o resultado esperado para o símbolo inválido?','ajuda':'Considere @ int x; na versão atual do software.','opcoes':['A) Há erro sintático e o parser continua normalmente.','B) Há erro léxico e o parser não é executado.','C) Há apenas erro semântico.','D) Não sei.']}
 ],
 'likert':[
 {'id':'L01','titulo':'L01 — Selecionar um nó da AST ajudou-me a localizar o trecho correspondente no código.'},
 {'id':'L02','titulo':'L02 — A ligação entre AST interativa e trecho do código ajudou-me a explicar por que os parênteses mudam o agrupamento da expressão.','ajuda':'Pergunta específica sobre a contribuição proposta: relacionar a estrutura da AST ao código-fonte. Responda sobre sua percepção nesta atividade.'},
 {'id':'L03','titulo':'L03 — As mensagens separadas por fase ajudaram-me a distinguir erro léxico de erro sintático.'},
 {'id':'L04','titulo':'L04 — Os rótulos e as explicações das construções na AST foram claros.'},
 {'id':'L05','titulo':'L05 — Discutir a interpretação do código com o colega ajudou-me a explicar minha resposta.','ajuda':'Se realizou a atividade individualmente, selecione N/A.'},
 {'id':'L06','titulo':'L06 — Foi fácil usar a interface para realizar as tarefas propostas.'}
 ],
 'escala':['1 — Discordo totalmente','2 — Discordo','3 — Nem concordo nem discordo','4 — Concordo','5 — Concordo totalmente','N/A — Não utilizei ou não consigo avaliar'],
 'abertas':[
 {'id':'A01','titulo':'A01 — Qual foi sua principal dificuldade nesta atividade?','ajuda':'Opcional. Não escreva nomes, e-mails, matrícula ou informações que identifiquem alguém.'},
 {'id':'A02','titulo':'A02 — Que mudança você sugere para melhorar a atividade ou o software?','ajuda':'Opcional. Não escreva dados pessoais.'}
 ]
}
(P/'instrumento.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
parts=['# Formulário de avaliação por pares — conteúdo pronto para Google Forms','', '**Estado: instrumento preparado; não aplicado. Nenhum formulário ou link Google Forms foi criado automaticamente nesta entrega.**','', 'Método: avaliação formativa por tarefas, questões objetivas específicas e itens Likert próprios. Este instrumento não é SUS e não possui pontuação global validada. A pergunta L02 trata explicitamente da contribuição proposta.','', '## Configurações antes de disponibilizar','', '- Não coletar e-mails; não solicitar nome ou matrícula; não exigir login, domínio institucional ou limite de uma resposta vinculado à conta. Conferir restrições da conta/organização.','- Desativar modo teste/quiz, divulgação de respostas corretas, resumo público de respostas e edição após envio. Não solicitar upload de arquivos.','- Consentimento C01 em seção própria: Sim → seção de atividade; Não → enviar/encerrar.','- Todos os campos fechados são obrigatórios, com Não sei ou N/A quando cabível. Os dois campos abertos são opcionais.','- O Google pode produzir metadados técnicos ou uma coluna de data/hora. O analisador ignora esses campos; eles não devem ser usados para identificar participantes.','- Respostas serão individuais após a atividade. Não solicitar código da dupla no formulário. As observações de sessão ficam separadas e sem ligação individual.','', '## Título',config['titulo'],'','## Descrição e informação ao participante',config['descricao'],'']
c=config['consentimento']
parts+=['## Seção 1 — participação','',c['titulo'],c['ajuda'],'','- '+c['sim'],'- '+c['nao'],'','**Navegação:** Sim continua; Não encerra. Não aplicar questões a quem não aceitar ou for menor de idade.','', '## Seção 2 — modo, perfil e interpretação','',config['modo']['titulo']]+['- '+x for x in config['modo']['opcoes']]+['',config['perfil']['titulo']]+['- '+x for x in config['perfil']['opcoes']]+['']
for q in config['objetivas']:
 parts+=[q['titulo'],q['ajuda'],'']+['- '+x for x in q['opcoes']]+['']
parts+=['## Percepções sobre a experiência','', 'Use a mesma escala para L01–L06:']+['- '+x for x in config['escala']]+['','No modo individual, L05 é não aplicável.','']
for q in config['likert']:
 parts+=[q['titulo']]
 if q.get('ajuda'):parts+=[q['ajuda']]
 parts+=['']
parts+=['## Comentários opcionais','']
for q in config['abertas']:parts+=[q['titulo'],q['ajuda'],'']
parts+=['## Finalização','', 'Obrigado por participar. Sua resposta será analisada em conjunto. Nenhuma pontuação ou avaliação de nota será apresentada.','', '## Como criar usando o arquivo .gs','', '1. Acesse https://script.google.com/ com sua conta Google e crie um projeto.','2. Cole o conteúdo de criar_formulario.gs, salve e execute criarFormularioMiniCTarefa5.','3. Revise as permissões solicitadas. O script cria um formulário na sua própria conta; esta entrega não executou o script nem acessou sua conta.','4. Consulte o registro de execução para obter a URL de edição. O formulário é criado fechado para respostas.','5. Revise o consentimento, as configurações de privacidade e a navegação com Sim/Não. Faça testes técnicos separados da coleta real e remova somente essas respostas de teste identificadas antes de iniciar a coleta.','6. Depois da revisão e das orientações do professor/instituição, disponibilize/publicue o formulário manualmente e abra a coleta. Nenhum envio a colegas foi realizado por esta entrega.','7. Exporte as respostas como CSV (extraia o ZIP, se o Google fornecer ZIP) e use analisar_respostas.py. Preserve os prefixos dos títulos C01, M01, P01, Q01–Q04, L01–L06, A01–A02.','', '**Não há link de formulário pronto.** O .gs é um gerador a executar pelo usuário, não um formulário já publicado. O conteúdo do gerador foi conferido estaticamente, mas não foi executado no serviço Google Forms.']
(P/'formulario-texto.md').write_text('\n'.join(parts)+'\n',encoding='utf-8')
gs='''/** Gerador não executado nesta entrega. Cria formulário FECHADO para respostas.
 * Revise privacidade e navegação antes de disponibilizar manualmente.
 * Não é quiz; não envia gabarito aos participantes.
 */
const INSTRUMENTO = '''+json.dumps(config,ensure_ascii=False,indent=2)+''';

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
'''
(P/'criar_formulario.gs').write_text(gs,encoding='utf-8')
headers=[c['titulo'],config['modo']['titulo'],config['perfil']['titulo']]+[q['titulo'] for q in config['objetivas']+config['likert']+config['abertas']]
with (P/'respostas-cabecalho.csv').open('w',newline='',encoding='utf-8-sig') as f:csv.writer(f).writerow(headers)
