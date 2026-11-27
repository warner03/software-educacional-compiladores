# Protocolo de avaliação — versão 3.0

Definido em 26/11/2026 após o Trabalho 5 e antes da coleta humana. Código `2b535d1`; seis perguntas de avaliação. A versão 2 está preservada em `historico/versao2/`.


## 5.1. Participação e procedimento

O protocolo versão 3.0 foi definido após o Trabalho 5 e antes de qualquer coleta humana informada. A versão anterior foi preservada no histórico; seus itens e gabaritos não serão misturados aos atuais. A amostra será de conveniência, entre colegas adultos cursando ou que já cursaram Compiladores. Pretende-se convidar de 4 a 6 duplas, se viável; será informado o número efetivo, sem tratar a meta como resultado.

Cada sessão utilizará a mesma versão do software, entradas e instruções, com cerca de 10–15 minutos de atividade e aproximadamente três minutos para o formulário. Em dupla, as pessoas alternam entre operar a interface e explicar o resultado. Um piloto individual poderá verificar o roteiro e será analisado separadamente.

Antes das tarefas, o facilitador explica o objetivo, a participação voluntária e as condições de uso dos dados, conforme orientações do professor e da instituição. O formulário solicita aceite, modo de uso e as seis perguntas, sem nome, e-mail, matrícula ou condição de saúde. Não haverá áudio/vídeo. A observação presencial é conhecida pelos envolvidos; as anotações serão por sessão, sem ligação individual ao formulário.

| Atividade | Ação e registro |
|---|---|
| A1 — símbolos e fonte | Analisar `int x = 1; float y = x + 2.5;`. Localizar a declaração e a referência de `x`, observando fonte e AST. Registrar conclusão e ajuda. |
| A2 — significado | Analisar `int x = 1; total = x + 2;`. Identificar fase, regra e trecho do erro; alternar quem opera e quem explica. |
| A3 — informação sem cor | Escolher Sem cores e analisar `int x = ;`; identificar a fase pelos rótulos. Depois testar `@ int x;`, comparar os estados e experimentar Alto contraste. |

O facilitador usa um exemplo neutro para explicar os controles, sem revelar respostas. O gabarito fica separado do guia dos colegas. Para cada atividade, anota conclusão sem ajuda, com ajuda ou não conclusão. O formulário é respondido individualmente, com a interface disponível e sem acesso ao gabarito.

## 5.2. Seis perguntas e questão do diferencial

As duas questões objetivas oferecem alternativas léxico, sintático, semântico e “não sei”, ajustadas ao enunciado. Para as afirmações, a escala é 1 discordo totalmente, 2 discordo, 3 nem concordo nem discordo, 4 concordo e 5 concordo totalmente, com **N/A — não usei ou não consigo avaliar** fora da escala.

| Código | Pergunta exata | Tipo |
|---|---|---|
| Q01 | Em `int x = 1; total = x + 2;`, qual erro o software indicou? | Múltipla escolha |
| Q02 | No modo Sem cores, em `int x = ;`, qual fase indicou o erro? | Múltipla escolha |
| L01 | Foi fácil usar o software. | Concordância 1–5 ou N/A |
| L02 | No modo Sem cores, consegui identificar os resultados sem depender das cores. | Concordância 1–5 ou N/A |
| L03 | A tabela de símbolos ajudou a entender onde as variáveis foram declaradas. | Concordância 1–5 ou N/A |
| A01 | O que você melhoraria no software? | Aberta, opcional |

**L02 é a pergunta diretamente relacionada ao diferencial.** Ela mede percepção de identificação sem dependência de cores. Q02 e a observação de A3 verificam uma tarefa realizada nesse modo; L03 e A1 examinam o apoio dos símbolos. A combinação permite comparar relatos com ações, sem concluir que um acerto demonstra aprendizagem ou que respondentes em geral representam pessoas daltônicas.

O conteúdo completo está pronto para copiar no Google Forms. Há também um gerador opcional de rascunho, fechado para respostas até revisão. Ele não foi executado em conta Google nesta entrega: nenhum link de formulário foi criado, publicado ou enviado a colegas.

## 5.3. Análise e contexto colaborativo

Serão apresentados, por modo individual/dupla, os números de respostas elegíveis, perdas e não respostas. Para Q01/Q02, serão informados acertos e denominadores; “não sei” é resposta válida não correta. Para cada afirmação, serão apresentadas frequências em 1–5, mediana e quantidade de N/A, excluída somente do denominador daquele item. Não haverá soma em uma nota global de aprendizagem ou escore SUS.

As sugestões serão agrupadas por tema após leitura e retirada de identificadores. A análise automática não reproduz os textos livres. Sem respostas, as estatísticas permanecem nulas. Dados sintéticos usados para testar o analisador são rotulados e não entram nos resultados acadêmicos.

Para aproximar o projeto do contexto do SBSC, a atividade em dupla prevê comunicação por explicação/negociação, coordenação por alternância de papéis e cooperação na interpretação do mesmo código. Essa organização é inspirada no Modelo 3C (Gerosa et al., 2006, p. 132–133). O facilitador registra se os comportamentos ocorreram, sem inferir colaboração apenas pela presença de duas pessoas. Comunicação e turnos ocorrem presencialmente; o software não implementa chat ou edição multiusuário. As respostas de membros da mesma dupla podem ser dependentes e não serão tratadas como observações independentes em inferências estatísticas.
