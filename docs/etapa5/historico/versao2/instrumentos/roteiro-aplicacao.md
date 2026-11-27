# Protocolo prático de aplicação — avaliação formativa

**Estado:** pronto para revisão e aplicação; nenhuma sessão, convite ou coleta com colegas foi executada por esta entrega. As metas abaixo são planejamento, não amostra realizada.

## Objetivo e unidade de observação

Examinar se a sequência de exploração de tokens, AST simplificada, fonte destacado e diagnósticos por fase permite realizar tarefas de interpretação e como os participantes percebem esse apoio. O estudo é descritivo e formativo. Os quatro itens objetivos não constituem pré/pós-teste nem medida validada de ganho de aprendizagem. Os seis itens Likert são próprios, sem pontuação global SUS ou equivalência a uma escala validada.

**Privacidade:** a observação presencial não é anônima para quem acompanha a sessão. O facilitador vê quem participa; o compromisso é não registrar identidades, minimizar anotações e divulgar somente resultados agregados. O formulário é sem identificadores diretos, sem promessa de anonimato absoluto perante a plataforma Google.

A aplicação principal é **em duplas co-localizadas**, com um computador e alternância dos papéis “quem opera” e “quem explica”. A observação tem a sessão/dupla como unidade; o formulário posterior tem a resposta individual como unidade. Não tratar respostas de membros de uma dupla como observações independentes em testes inferenciais. As respostas individuais não serão ligadas a códigos de sessão.

**Meta de conveniência:** 4–6 duplas (8–12 estudantes), adultos. É uma meta viável para piloto, não número mínimo obrigatório, cálculo de poder ou garantia de saturação. Se houver menos participantes, registrar a amostra real e as limitações. Um piloto individual pode ser feito para verificar o roteiro e deve ser identificado e analisado separadamente, não misturado às duplas para aparentar uma amostra maior.

## Preparação pelo facilitador

1. Registrar a versão exata do software, navegador, data em nível de dia e modalidade. Verificar funcionamento antes da sessão.
2. Criar o formulário usando `formulario-texto.md` ou o gerador `criar_formulario.gs`. O gerador não foi executado e nenhum link Google Forms foi criado automaticamente. Ele cria o formulário fechado; revisar privacidade e navegação e só então disponibilizar manualmente.
3. Não coletar nome, e-mail, matrícula, áudio, vídeo, identificação da turma, IP por ferramenta própria ou código de participante. Desativar coleta de e-mail, restrição por conta e resumo público. O Google pode processar metadados técnicos próprios; o estudo não os utilizará para identificar pessoas.
4. Informar uso acadêmico das respostas, acesso restrito ao responsável e modo de publicação agregada. Definir com o professor os requisitos institucionais, prazo de guarda e eventual uso em publicação antes da coleta; não presumir aprovação ética ou dispensa sem orientação aplicável.
5. Explicar que participação é voluntária, para maiores de 18 anos, sem relação com notas ou obrigação de agradar ao responsável. Se o colega não aceitar, encerrar sem aplicar tarefas. O formulário também contém saída C01 = Não.
6. Escolher S001, S002 etc. apenas para identificar **sessões de observação**. Não associar esses códigos aos formulários, nomes, assentos ou lista de presença. Não publicar horários precisos.
7. Guardar o gabarito separadamente. Não enviar `gabarito-facilitador.md` ou o código do analisador aos participantes antes da atividade. Não configurar Google Forms como quiz.

## Abertura padronizada, aproximadamente 2 minutos

Ler: “Esta é uma avaliação do software e da atividade, não de sua nota. Você pode desistir. Não vamos registrar nomes nem áudio. Vocês poderão explorar os recursos para interpretar o código. Em cada tarefa, uma pessoa opera a interface e outra explica sua interpretação; depois trocam. Ao final, cada pessoa responderá ao formulário individualmente. Dificuldades são informações úteis para melhorar o projeto.”

Apresentar somente editor, botão Analisar código, tabela de tokens, caixa da AST, Expandir/recolher e Localizar. Explicar onde estão os controles sem resolver os exemplos das tarefas. Não dizer as respostas corretas ou sugerir que a funcionalidade deverá ser avaliada positivamente.

## Tarefas, aproximadamente 12–18 minutos

### T01 — interpretação sem parênteses

Programa: `int resultado = 10 + 5 * 2;`

Uma pessoa opera e a outra explica. Solicitar: “Identifiquem qual operador organiza a expressão após o igual, quais são seus dois operandos e como a árvore representa o agrupamento. Usem Localizar para relacionar uma construção ao trecho no código.” Permitir exploração da interface. Registrar conclusão, ajuda e dificuldade de navegação, sem transcrever falas identificáveis.

### T02 — mudança de agrupamento

Trocar os papéis. Programa: `int resultado = (10 + 5) * 2;`

Solicitar: “Comparem o agrupamento desta expressão com o da tarefa anterior. Expliquem o que muda na estrutura e localizem o trecho que representa a soma.” Não informar o operador esperado. Registrar se a troca de papéis ocorreu, conclusão e ajuda.

### T03 — erro de estrutura

Trocar novamente os papéis. Programa: `int x = ;`

Solicitar: “Analisem a entrada, indiquem em qual fase aparece o problema e expliquem o que seria necessário corrigir. Observem se há tokens e se há AST.” Não corrigir a entrada pelo participante durante a resposta inicial. Registrar os mesmos critérios de observação.

### T04 — unidade inválida

Trocar os papéis. Programa: `@ int x;`

Solicitar: “Analisem esta entrada e comparem os estados das duas fases com a tarefa anterior. Expliquem o que acontece com a análise sintática.” Registrar conclusão e ajuda, mantendo as observações separadas das respostas individuais.

## Regra de ajuda

Aguardar que a dupla conclua ou peça ajuda; não definir sucesso pelo tempo arbitrário. Se houver dificuldade com o controle da interface, o facilitador pode repetir a instrução ou indicar onde está um botão e deve marcar “concluiu com ajuda”. Se oferecer uma dica conceitual, também registrar ajuda. Não mudar o critério depois de ver o resultado. Podem encerrar ou deixar tarefa sem conclusão. Tempos são opcionais e aproximados, usados apenas descritivamente.

## Formulário individual, aproximadamente 5–8 minutos

Cada participante responde por conta própria, sem discutir respostas durante o preenchimento. A consulta ao aplicativo é permitida para todos; por isso, os acertos representam interpretação apoiada pelo ambiente, não retenção sem apoio. Em computador compartilhado, preencher um por vez, sem o colega observar a resposta. Solicitar uma resposta por pessoa sem recorrer a login ou identificação para impor isso. Duplicatas continuam como ameaça à validade; não excluir automaticamente respostas só porque são iguais.

C01 registra consentimento/elegibilidade. M01 distingue Em dupla de Individual; P01 registra perfil amplo. Q01–Q04 são itens objetivos. L01–L06 são percepções, incluindo L02 sobre a contribuição específica. L05 é N/A para atividade individual. Se o modo estiver ausente ou inválido, o analisador preserva o estrato Modo não informado e não calcula L05: registra aplicabilidade indeterminada e exclusão do denominador. A01–A02 são abertos e opcionais, com instrução para não inserir dados pessoais.

## Piloto individual

Usar as mesmas quatro tarefas e regra de ajuda, com a própria pessoa operando e explicando. Registrar modalidade Individual e troca de papéis N/A. No formulário, M01 = Individual e L05 = N/A. Descrever os resultados como piloto individual. Não interpretar essa alternativa como atividade colaborativa ou como grupo de controle experimental.

## Registro e análise

- Usar `observacoes-cabecalho.csv` para sessões; o arquivo contém apenas cabeçalho, sem sessões inventadas. Critérios de conclusão: sem ajuda, com ajuda, não concluiu, não tentou. Quantidade de pessoas é contagem, não identificação.
- Exportar CSV do formulário e usar `analisar_respostas.py`; preservar os prefixos dos títulos. O arquivo `respostas-cabecalho.csv` contém somente o cabeçalho e não é base de resultados.
- Excluir C01 = Não ou ausente dos resultados; excluir N/A do denominador de cada item Likert; analisar modalidades e perfis separadamente. Não gerar escore global nem converter Likert em prova de aprendizagem.
- O analisador não expõe comentários, nomes, e-mails ou horários; campos abertos têm somente contagem de preenchimento. A leitura temática dos comentários deve ser feita privadamente, removendo identificadores incidentais antes de qualquer citação, sem inventar categorias como se já tivessem sido observadas.
- Distinguir fatos (acerto, tarefa concluída, ajuda), percepções (Likert e relatos) e interpretação do pesquisador. Sem respostas elegíveis, a saída é “sem respostas” e não há estatísticas.
- Para publicação, revisar risco de identificação em estratos muito pequenos e apresentar agregados adequados; não expor planilhas brutas ou comentários individuais por padrão.
