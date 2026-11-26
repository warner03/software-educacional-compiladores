# Gabarito reservado ao facilitador

**Não entregar aos participantes antes da atividade.** O formulário não deve ser configurado como quiz nem exibir correção. Este documento é referência de análise, não resultado de pessoas.

| Item | Resposta correta | Justificativa |
|---|---|---|
| Q01 | A) Soma (+). | Em `10 + 5 * 2`, `+` organiza a expressão, com `10` à esquerda e `5 * 2` à direita. |
| Q02 | B) Multiplicação (*). | Em `(10 + 5) * 2`, `*` organiza a expressão, com a soma agrupada à esquerda e `2` à direita. |
| Q03 | B) Erro sintático: falta uma expressão após o sinal de igual. | `int x = ;` contém tokens reconhecíveis, mas não há operando/inicializador válido. |
| Q04 | B) Há erro léxico e o parser não é executado. | `@` está fora do recorte; a versão bloqueia o parser quando há erro léxico. |

Nas questões Q01–Q02, “raiz” significa raiz da **expressão inicializadora**, não o nó Programa ou Declaracao. “Não sei” é uma resposta válida e não correta. Ausência de resposta e valor não reconhecido ficam identificados separadamente, sem entrar silenciosamente no denominador.

T01 pode ser concluída sem ajuda quando a dupla identifica o agrupamento `10 + (5 * 2)` e usa a interface para relacionar uma construção ao fonte. T02 requer explicar a mudança para `(10 + 5) * 2`. T03 requer distinguir fase léxica sem erro e fase sintática com erro por operando ausente. T04 requer identificar erro léxico e bloqueio da sintática. Registrar ajuda quando fornecida; não atribuir individualmente a conclusão de uma dupla.

L01–L06 não têm gabarito. Apresentar frequências e medianas por item/modalidade/perfil, excluindo N/A. L02 é percepção do apoio da ligação AST–fonte para explicar agrupamento. L05 é não aplicável ao piloto individual. Não calcular uma nota de aprendizagem, SUS ou soma das seis respostas.
