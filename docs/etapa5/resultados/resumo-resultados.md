# Resultados atuais — após o Trabalho 5

Código: `2b535d1`; integração prática na main: `1de2b61`. Rodada técnica em **26/11/2026, 21h22–21h23, São Paulo**, anterior aos commits; hashes do código confirmam a correspondência. Esta revisão teórica reutiliza as evidências da rodada aprovada, sem afirmar que executou novamente as suítes.

| Procedimento | Aprovados | Falhas | Registro original |
|---|---:|---:|---|
| Backend | 322 | 0 | [backend.txt](../../trabalho5/evidencias/backend.txt) |
| Interface | 55 | 0 | [frontend.txt](../../trabalho5/evidencias/frontend.txt) |
| Navegador Chromium | 134 cenários | 0 | [navegador.txt](../../trabalho5/evidencias/navegador.txt) |
| Integração nginx/API | Fluxo aprovado | 0 | [integracao.txt](../../trabalho5/evidencias/integracao.txt) |
| API: 30 casos semânticos | 30/30 | 0 | [CSV](../../trabalho5/evidencias/casos-semanticos.csv) — [JSON](../../trabalho5/evidencias/casos-semanticos.json) |
| Docker sem cache | Concluído | 0 | [build](../../trabalho5/evidencias/build-sem-cache.txt) |

O conjunto semântico tem 11 entradas válidas e 19 com violações esperadas. Execução: 30/30 (100% dos casos); aprovação: 30/30 (100% dos executados). Esses casos já pertencem à suíte; a execução HTTP não é somada como novos testes independentes. Cobertura de código não foi medida. M01–M03 são agora verificados semanticamente, com os diagnósticos esperados.

[Metadados originais](../../trabalho5/evidencias/metadados.json) e [commit associado aos hashes](../../trabalho5/evidencias/versao-entregue.json). Scanner/parser e onze arquivos anteriores de testes foram preservados.

## Contraste

[Medidas completas](../../trabalho5/capturas/contraste-medido.json): 24 combinações de texto (3 modos × 4 estados × 2 viewports), além de 6 verificações de foco/seleção. Limiares adotados: texto 4,5:1; foco/seleção 3:1. Valores mínimos observados:

| Modo | Texto | Foco | Seleção |
|---|---:|---:|---:|
| Padrão | 6,749:1 | 6,345:1 | 6,082:1 |
| Sem cores | 8,934:1 | 16,570:1 | 11,589:1 |
| Alto contraste | 16,275:1 | 13,584:1 | 4,217:1 |

São medidas dos elementos examinados, sem certificação WCAG integral ou validação com pessoas daltônicas.

## Avaliação humana

**Ainda não aplicada.** Não há taxas de acerto de pessoas, medianas de opinião, comentários humanos ou resultados de colaboração. [Estado da coleta](estado-coleta.json). O cabeçalho do CSV está vazio de propósito; o analisador conserva estatísticas nulas.

Os resultados da preparação anterior estão preservados em [histórico da versão 2](../historico/versao2/resultados/resumo-resultados.md). As contagens 229/41/60/33 e a semântica pendente pertencem à base anterior; não descrevem o software atual.
