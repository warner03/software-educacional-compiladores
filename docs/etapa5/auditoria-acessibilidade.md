# Auditoria dos critérios de acessibilidade visual

Conferência em 26/11/2026. Os critérios **Sem cores** e **Alto contraste** foram introduzidos após o pedido de apoio ao daltonismo, antes da aplicação com colegas. As definições foram aplicadas igualmente às dez linhas; não alteram os quinze critérios anteriores dos estudos.

Sem cores exige um modo selecionável que use padrões/rótulos para diferenciar resultados. Alto contraste exige um modo visual alternativo explicitamente documentado. Rótulos isolados, figuras impressas em preto e branco ou o uso de realce colorido não confirmam esses modos. A escolha se apoia nas orientações W3C de uso da cor e contraste, sem converter um recurso específico em requisito universal de uma ferramenta de compiladores.

| Referência | Documento integral delimitado | Resultado dos dois critérios |
|---|---|---|
| Graciano Junior et al. (2022) | p. 224–233; funcionalidades e telas descritas no artigo | NI |
| Borela et al. (2025) | PDF p. 1–11; especialmente arquitetura/linguagem/interface, seções 3.1–3.2 | NI |
| Santini et al. (2022) | Mapeamento de jogos, não ferramenta única | N/A |
| Mernik e Žumer (2003) | Manuscrito de 22 páginas fornecido pelo autor; visualizações do LISA | NI |
| Resler e Deaver (1998) | p. 199–202; interface e funcionalidades do VCOCO | NI |
| Rodger et al. (2009) | p. 403–407; uso do JFLAP e avaliação educacional | NI |
| Moreno et al. (2004) | p. 373–376; visualização/interface do Jeliot 3 | NI |
| Schneider et al. (2005) | PDF p. 1–10; descrição do VERTO | NI |
| Jabri (2013) | p. 134–150; especificação e saída gráfica/tabular do GCT | NI |
| Este trabalho — Mini-C | Código `2b535d1`, seletor visual, CSS, controles, capturas e testes | ✓ |

Os textos já haviam sido consultados integralmente na Tarefa 4. Nesta revisão, foram rechecados os registros e as descrições de interface/funcionalidades e feita busca auxiliar nos textos por termos relacionados a daltonismo, acessibilidade, modos sem cor e alto contraste, em português e inglês. A busca textual não foi usada como prova de ausência. Os documentos não confirmaram os dois modos selecionáveis, o que sustenta **NI**, e não ✗. Não se auditou cada software em execução ou suas versões mais recentes.

A classe N/A em Santini evita reunir recursos de nove jogos como se pertencessem a um só software. Um modo não documentado no artigo pode existir na implementação: confirmar exclusividade exigiria inspecionar versões equivalentes e outras fontes primárias.

## Evidência própria e limites

O seletor está em `frontend/index.html`, a preferência em `frontend/app.js` e os modos/padrões em `frontend/style.css`. As capturas e as medidas de contraste estão em `docs/trabalho5/capturas/`; os testes e metadados, em `docs/trabalho5/evidencias/`. A tabela de símbolos interativa é documentada separadamente em `docs/semantica.md`.

As medidas confirmam os limiares nos elementos examinados. Não houve participação de pessoas daltônicas, avaliação clínica, auditoria WCAG integral ou demonstração de superioridade. A contribuição defendida é a implementação integrada e seu protocolo de avaliação, não a afirmação de ser a única ferramenta acessível.

## Fontes normativas conferidas

- W3C, uso da cor: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
- W3C, contraste mínimo: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- W3C, contraste não textual: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html

Páginas oficiais conferidas por HTTPS, HTTP 200, com verificação TLS em 26/11/2026. As referências completas dos estudos constam no artigo e as evidências anteriores em `docs/etapa4/matriz-evidencias.csv`.
