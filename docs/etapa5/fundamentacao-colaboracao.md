# Fonte adicional verificada para atividade em duplas

Consulta: 26/11/2026. Esta fonte fundamenta colaboração; não substitui os dois novos artigos de avaliação e não precisa ser terceiro anexo obrigatório.

## Referência completa

GEROSA, Marco Aurélio; RAPOSO, Alberto Barbosa; FUKS, Hugo; LUCENA, Carlos José Pereira de. **Component-Based Groupware Development Based on the 3C Collaboration Model**. In: SIMPÓSIO BRASILEIRO DE ENGENHARIA DE SOFTWARE (SBES), 20., 2006, Florianópolis. *Anais [...]*. Porto Alegre: Sociedade Brasileira de Computação, 2006. p. 129–144. DOI: **10.5753/sbes.2006.21209**.

Registro oficial e texto aberto:

- https://sol.sbc.org.br/index.php/sbes/article/view/21209
- https://sol.sbc.org.br/index.php/sbes/article/download/21209/21034

PDF integral baixado HTTP 200 com TLS: `gerosa2006_3c.pdf` (16 páginas). Texto extraído: `gerosa2006_3c.txt`. Registro oficial e Crossref conferem título, quatro autores, ano e DOI; páginas 129–144 confirmadas no registro oficial e no PDF. `gerosa2006_3c_metadata.json` preserva os metadados Crossref. Não confundir com Fuks et al. (2005), que é outra referência citada pelo próprio estudo.

## Trecho e localização conferidos

Seção **3. THE 3C COLLABORATION MODEL**, páginas impressas **132–133**, páginas **4–5 do PDF**:

> “The 3C collaboration model is based on the idea that to collaborate, members of a group communicate, coordinate and cooperate.” (p. 132)

> “Communication involves the exchange of messages and the negotiation of commitments. Coordination enables people, activities and resources to be managed so as to resolve conflicts and facilitate communication and cooperation. Cooperation is the joint production of members of a group within a shared space, generating and manipulating cooperation objects in order to complete tasks [...].” (p. 132)

Na continuação, p. 133: “communication, coordination and cooperation should not be seen in an isolated fashion; there is a constant interplay between them.” A figura 1 ilustra as três dimensões. Os autores esclarecem a origem em Ellis et al. e a diferença de terminologia entre colaboração e cooperação; a fonte usada aqui é Gerosa et al. (2006), sem atribuir-lhe invenção absoluta do modelo.

O artigo propõe componentes de groupware organizados segundo 3C e investiga a abordagem no redesenvolvimento do AulaNet. É uma fonte conceitual de análise/projeto da colaboração, **não uma validação de aprendizagem em duplas com Mini-C**, nem uma escala pronta para medir esse efeito.

## Adaptação proposta ao piloto Mini-C

| Dimensão | Procedimento proposto | Evidência a coletar |
|---|---|---|
| Comunicação | Cada integrante explica ao colega o agrupamento da expressão usando a AST e o trecho destacado; ambos discutem divergências. | Justificativa escrita curta da dupla e nota estruturada de observação sobre discussão/explicação. |
| Coordenação | Um integrante opera a interface e outro interpreta/confere a estrutura; papéis são alternados no segundo caso. | Registro de que houve dois turnos e troca de papéis, sem nomes. |
| Cooperação | Ambos produzem uma resposta comum: expressão agrupada, nó correspondente e explicação acordada, ou código corrigido. | Resposta conjunta com rubrica de correção e indicação de divergência não resolvida, se houver. |

Código, AST e justificativa são os objetos de referência comuns. A atividade pode ocorrer em dupla no mesmo computador; comunicação oral e organização por roteiro são externas ao software. A implementação atual não oferece chat, edição concorrente ou contas. A interface atua como suporte à referência visual durante a explicação e revisão entre pares; não se deve atribuir ao software controle automático de turnos, coordenação ou histórico de discussão.

Possível pergunta específica de percepção, sem pretensão de escala validada: **“Relacionar um nó da AST ao trecho do código ajudou a dupla a explicar e conferir o agrupamento da expressão?”** Respostas 1–5 e “Não utilizei esse recurso”. Complementar com tarefa de interpretação e rubrica; opinião favorável não prova aprendizagem nem efeito causal da colaboração.

A adaptação 3C explicita os aspectos do uso colaborativo a observar. Ela permanece proposta até coleta real. Sem comparação, pré/pós-teste e amostra adequada, relatar conclusão de tarefas, dificuldades e percepções do piloto, sem afirmar superioridade ou ganho de aprendizagem. Conformidade institucional/consentimento deve ser acertada com o professor antes de aplicar o estudo; observação identificável não deve ser descrita como coleta totalmente anônima só porque o formulário não pede nome.
