# Protocolo de avaliação — versão 2.0

26/11/2026. Definido após conhecer os resultados da Etapa 4, antes de coletar respostas de colegas. Base funcional 7fcb5ca.


## 5.1. Versão, participantes e aplicação

O protocolo desta tarefa é definido em 26/11/2026, após a implementação da Etapa 4 e antes da coleta com colegas. Não é apresentado como pré-registro independente do desenvolvimento. Os casos funcionais e três oráculos estruturais foram fixados em 18/11/2026 e conservados sem alteração dos esperados. O histórico do projeto e os arquivos desta entrega permitem distinguir esse planejamento da reexecução atual.

A amostragem será por conveniência, com meta de viabilidade de 4 a 6 duplas (8 a 12 estudantes adultos cursando ou que já cursaram Compiladores). A meta não é cálculo de poder nem requisito que autorize fabricar participantes. A quantidade efetiva e as perdas deverão ser informadas. Professores e outros perfis serão mantidos em estratos separados. Um piloto individual poderá identificar problemas do roteiro, mas seus dados não serão agregados como evidência de colaboração.

Antes da aplicação, o autor combinará com o professor as regras institucionais de participação e uso/publicação dos dados. A chamada do SBSC não constitui dispensa geral de procedimentos institucionais. A participação será autorizada antes de iniciar as tarefas; o campo C01 registra novamente a decisão no formulário. A coleta será voluntária, com informação sobre objetivo, duração aproximada (20–30 minutos no total), ausência de avaliação acadêmica individual e possibilidade de sair antes do envio. O formulário não solicitará nome, e-mail ou matrícula; o registro do facilitador será por sessão, sem identificação direta, áudio ou vídeo. Comentários serão revisados para remover identificadores antes de qualquer divulgação.

A versão do software e do instrumento será congelada para a rodada. Corrigir um problema relevante exige registrar data, motivo e quais sessões foram afetadas; resultados de versões diferentes não serão silenciosamente combinados. O facilitador fará uma introdução igual para todos, explicando controles com um exemplo neutro, sem revelar os gabaritos das tarefas.

## 5.2. Atividade e componente colaborativo proposto

O modo principal prevê duas pessoas no mesmo computador, alternando os papéis de quem opera a interface e de quem explica a estrutura. Na primeira expressão, uma pessoa seleciona nós e a outra explica o agrupamento; na expressão com parênteses, os papéis se invertem. O objetivo comum é produzir uma explicação coerente e localizar o trecho correspondente. A discussão ocorre presencialmente, não por funcionalidades de chat, edição compartilhada ou coordenação automática do software.

Gerosa et al. (2006, seção 3, p. 132–133) descrevem o Modelo 3C: comunicação, coordenação e cooperação como dimensões interdependentes da colaboração. Aqui, a adaptação operacional será observar explicações/negociação sobre o agrupamento (comunicação), alternância dos papéis por roteiro (coordenação) e construção de uma justificativa ou correção comum sobre o código/AST (cooperação). A fonte fundamenta essa decomposição, não uma escala educacional validada nem um efeito de aprendizagem. O objeto visual é fornecido pelo Mini-C; comunicação e gestão dos turnos serão externas à aplicação. A observação presencial não se torna anônima para o facilitador apenas porque o Forms não solicita nomes; seu registro será minimizado e apresentado somente de forma agregada.

O facilitador observará se houve alternância, referência conjunta a nós/trechos, pedido de justificativa e correção ou negociação de uma explicação. Registrará comportamento ocorrido, ajuda fornecida e dificuldades; não inferirá colaboração apenas porque duas pessoas estavam presentes. O formulário será respondido individualmente após a atividade, com a interface disponível e sem consulta ao gabarito. As respostas podem ser dependentes pela discussão em dupla; não serão tratadas como observações independentes em testes inferenciais.

| Tarefa | Ação solicitada | Evidência a observar |
|---|---|---|
| A1 | Analisar `int resultado = 10 + 5 * 2;`, identificar agrupamento e localizar o operando direito da expressão | Operador que organiza a expressão, explicação e correspondência nó–fonte; necessidade de ajuda |
| A2 | Alterar para `int resultado = (10 + 5) * 2;`, inverter papéis e explicar a mudança | Uso dos parênteses na justificativa e mudança da estrutura; referência conjunta à representação |
| A3 | Analisar `int x = ;` e explicar fase, localização e conteúdo esperado | Distinção entre token reconhecido e expressão incompleta; leitura do diagnóstico |
| A4 | Analisar `@ int x;` e comparar os estados das fases com A3 | Identificação do erro léxico e explicação do parser não executado |

As respostas de referência e a rubrica do facilitador são fornecidas em arquivo separado. Uma resposta correta sem justificativa não será automaticamente interpretada como compreensão conceitual aprofundada. Quando houver ajuda, ela será registrada, permitindo distinguir realização autônoma, realização com ajuda e tarefa não concluída.

## 5.3. Instrumento e pergunta específica da contribuição

O formulário contém consentimento, perfil amplo, modo de aplicação, quatro questões objetivas (Q01–Q04), seis itens de percepção (L01–L06) e campos abertos para dificuldade e sugestão. A escala será: 1 discordo totalmente; 2 discordo; 3 nem concordo nem discordo; 4 concordo; 5 concordo totalmente; e **Não utilizei/não consigo avaliar**, fora da escala.

A pergunta diretamente associada à contribuição proposta é **L02: “A ligação entre AST interativa e trecho do código ajudou-me a explicar por que os parênteses mudam o agrupamento da expressão.”** A resposta verifica apoio percebido; Q01 e Q02, e a observação de A1/A2, verificam respostas e ações relacionadas. Essa triangulação evita usar somente uma opinião para afirmar que a interação cumpriu seu papel.

| Item | Aspecto investigado |
|---|---|
| L01 | Localizar no fonte a construção selecionada na AST |
| L02 | Apoio percebido para explicar o efeito dos parênteses no agrupamento |
| L03 | Distinção das fases de erro léxico e sintático |
| L04 | Clareza de rótulos/regras associados às construções |
| L05 | Apoio percebido da discussão com o colega à explicação; não aplicável no piloto individual |
| L06 | Facilidade geral de realização das tarefas |

O pacote inclui o texto exato para Google Forms e um Apps Script para criar um formulário **fechado para respostas até revisão** na conta do autor. O script não foi executado em uma conta Google nesta sessão; não existe link de formulário publicado nesta entrega. A criação/revisão e a aplicação são etapas do autor. O roteiro orienta conferir ausência de coleta de e-mails, restrição institucional e identificação nas perguntas antes de disponibilizar o link aos colegas.

## 5.4. Plano de análise

**Fatos observados:** número de casos funcionais executados/aprovados, respostas de Q01–Q04 conforme gabarito, tarefas concluídas e registros de ajuda/comportamento. **Percepções relatadas:** frequências e medianas dos itens Likert e comentários. **Interpretações:** relação cautelosa entre esses dados e os objetivos do projeto, sem generalização causal.

Para cada questão objetiva, relatar-se-ão número de respostas válidas e taxa de acerto, por modo e perfil. O total de formulários não será automaticamente chamado de número de participantes únicos: o anonimato impede verificar plenamente duplicações. Respostas sem consentimento serão excluídas; casos incompletos terão denominadores informados. No Forms, perguntas obrigatórias e alternativas explícitas reduzem ambiguidades, sem substituir a descrição de perdas.

Para cada item Likert, apresentar-se-ão frequências em 1–5, mediana, número de respostas válidas e não aplicáveis. Não aplicáveis serão informados e excluídos somente do denominador daquele item. Não haverá soma arbitrária de itens em um escore de aprendizagem ou de usabilidade validada. O item de dupla será analisado apenas nas sessões em dupla.

Campos abertos serão lidos e agrupados por tema, distinguindo relato de problema, sugestão e opinião. Não se fabricarão citações ilustrativas. A ferramenta de análise entregue ignora o conteúdo textual na saída agregada, reduzindo exposição acidental; o exame qualitativo e a remoção de identificadores exigem leitura humana. Os achados da observação por sessão serão apresentados separadamente dos formulários individuais, pois não há identificação pessoal para ligar as bases.

O analisador de CSV recebe a exportação do Forms, valida os campos e produz contagens por item, modo e perfil. Uma planilha vazia gera estado **sem respostas elegíveis**, sem médias, medianas ou porcentagens fictícias. Os testes do analisador usam apenas entradas sintéticas explicitamente identificadas como testes de código; elas não integram os resultados do estudo.
