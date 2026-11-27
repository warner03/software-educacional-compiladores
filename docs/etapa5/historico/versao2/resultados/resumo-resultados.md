# Resultados técnicos observados — Tarefa 5

Revalidação em **26/11/2026**, horário de São Paulo, entre `2026-11-26T20:13:54.268602-03:00` e `2026-11-26T20:18:08.417994-03:00`. Versão examinada: `7fcb5ca26e314e4374f2a48a04e7f28dbaffa946`. Todas as saídas abaixo foram obtidas nesta rodada, sem alterar os registros da Etapa 4 ou o código do projeto.

## Resultados das suítes

| Procedimento | Executados/aprovados | Falhas | Evidência |
|---|---:|---:|---|
| pytest: scanner, parser, API e validação | 229/229 | 0 | `backend.txt` |
| Node/jsdom: lógica e interface | 41/41 | 0 | `frontend.txt` |
| Smoke nginx → API → scanner → parser | Fluxo aprovado | 0 | `integracao.txt` |
| Chromium real, desktop e viewport móvel | 60/60 cenários | 0 | `navegador.txt`; `capturas/` |
| Protocolo congelado de casos via API real | 33/33 | 0 | `casos_funcionais.csv`, `.json` e `.log` |

Os 33 casos já são parte dos testes do backend; a execução externa via nginx é uma verificação adicional do mesmo conjunto, não 33 novos cenários independentes para inflar um total. As contagens de suíte (229/41), cenários de navegador (60) e casos de protocolo (33) são relatadas separadamente.

## Cobertura do protocolo

- Planejados aplicáveis à versão: 33 (12 válidos, 3 léxicos inválidos, 10 sintáticos inválidos e 8 de borda).
- Executados: 33/33 = **100% de cobertura de execução dos casos aplicáveis**.
- Aprovados: 33/33 executados = **100% de aprovação no conjunto verificado**.
- Prontidão funcional: 33/33 planejados aplicáveis = **100%**.
- Falhas: 0. Não executados no conjunto aplicável: 0.
- Oráculos V04–V06 definidos em 18/11/2026 foram comparados à AST real sem posições; folhas e posições foram examinadas separadamente.
- As três entradas M01–M03 foram aceitas **apenas como controles de sintaxe**. A avaliação semântica permanece **0/3 executados e 3 pendentes**, pois declaração/redeclaração/política de tipos ainda não foram implementadas na versão examinada.
- Cobertura de linhas/ramos de código **não foi medida** nesta rodada. Cobertura de casos não equivale à cobertura de código nem prova correção para todos os programas Mini-C.

A distribuição observada dos 33 casos foi: 14 análises sintáticas bem-sucedidas, 12 resultados de erro sintático, 4 análises sintáticas não executadas por erro léxico e 3 entradas rejeitadas com HTTP 400. Rejeições esperadas contam como aprovação do teste, e não como falha de implementação.

## Reprodução

Na raiz do repositório, neste ambiente:

```bash
export CLOUD_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
export COMPOSE_FILE=docker-compose.yml:compose.cloud.yaml
export COMPILADORES_API_PORT=18000

docker compose run --rm --no-deps backend pytest -q
docker compose run --rm --no-deps testes-frontend
KEEP_RUNNING=1 bash scripts/smoke_test.sh
python3 scripts/avaliar_plano_funcional.py --saida /tmp/mini-c-tarefa5-nova-rodada
python3 scripts/teste_navegador.py --chromium /usr/bin/chromium --capturas /workspace/entregas/etapa5/resultados/capturas
```

O script dos 33 casos acompanha este pacote. A versão em `scripts/avaliar_plano_funcional.py` deriva a raiz do próprio checkout e aceita `--raiz`, `--saida` e `--url`. A implementação de verificação preserva os mesmos esperados; a adaptação de caminhos foi feita após a rodada e não constitui uma execução nova. Os arquivos do protocolo e os três esperados de AST vêm de `tests/planejamento/`, anteriores à implementação. O script não importa o parser para gerar resultados esperados.

Docker 28.4.0, imagens Python3.12/Node20 já existentes e conferidas por SHA-256, frontend nginx e Chromium instalado no ambiente. O smoke reutilizou o build existente. Não foi necessário reconstruir imagens sem cache nesta rodada. O ambiente anterior possui registro de build sem cache na Etapa4; esse registro não é apresentado como uma reconstrução feita hoje.

## Fatos, percepções e interpretações

**Fatos observados:** os testes e cenários acima passaram, os resultados por caso estão salvos, nenhum participante humano foi avaliado. Os limites de 2.000 nós/altura128/aninhamento64 foram exercitados nas suítes; semântica é futura. O pytest produziu um aviso de depreciação Starlette/AnyIO, sem falha.

**Percepções relatadas:** nenhuma resposta de colega foi coletada nesta rodada. Não existem medianas Likert, opiniões, taxas de sucesso de pessoas ou conclusões de usabilidade a reportar.

**Interpretação permitida:** há evidência funcional de que a versão atende aos casos técnicos previamente especificados e se mantém operacional no ambiente testado. Isso não demonstra ganho de aprendizagem, facilidade de uso com estudantes ou exclusividade em relação à literatura.

## Limitações e ameaças à validade

- Os casos são de um recorte finito da gramática; aprovação total não cobre toda entrada possível nem C completo.
- A revalidação foi executada em um ambiente Linux/Docker. O viewport390px simula tela móvel, não aparelho físico ou avaliação de toque com pessoas.
- Não há estudo de acessibilidade completo, avaliação por pares, pré/pós-teste ou grupo de comparação nesta execução.
- Os tempos de renderização impressos pelo navegador (1,12s desktop;1,46s viewport móvel para2.000nós nesta rodada) são observações locais; não formam um benchmark controlado e não indicam melhora educacional.
- Semântica e código executável permanecem fora da versão atual. Seus casos não são classificados como aprovados por mera aceitação sintática.

## Casos individuais

| ID | HTTP observado | Estado sintático observado | Diagnóstico inicial observado | Resultado |
|---|---:|---|---|---|
| V01 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| V02 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| V03 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| V04 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| V05 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| V06 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| V07 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| V08 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| V09 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| V10 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| V11 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| V12 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| L01 | 200 | nao_executada | ERRO_LEXICO em 1:1; lexema '@' | aprovado |
| L02 | 200 | nao_executada | ERRO_LEXICO em 1:7; lexema '1.2.3' | aprovado |
| L03 | 200 | nao_executada | ERRO_LEXICO em 1:8; lexema '/* aberto' | aprovado |
| S01 | 200 | erro | ERRO_SINTATICO em 1:6; lexema '' | aprovado |
| S02 | 200 | erro | ERRO_SINTATICO em 1:11; lexema '{' | aprovado |
| S03 | 200 | erro | ERRO_SINTATICO em 1:9; lexema '' | aprovado |
| S04 | 200 | erro | ERRO_SINTATICO em 1:9; lexema ';' | aprovado |
| S05 | 200 | erro | ERRO_SINTATICO em 1:1; lexema 'else' | aprovado |
| S06 | 200 | erro | ERRO_SINTATICO em 1:13; lexema '*' | aprovado |
| S07 | 200 | erro | ERRO_SINTATICO em 1:5; lexema 'if' | aprovado |
| S08 | 200 | erro | ERRO_SINTATICO em 1:8; lexema '' | aprovado |
| S09 | 200 | erro | ERRO_SINTATICO em 1:6; lexema ',' | aprovado |
| S10 | 200 | erro | ERRO_SINTATICO em 1:7; lexema '(' | aprovado |
| B01 | 400 | não executada: entrada inválida | Validação de entrada, antes dos analisadores | aprovado |
| B02 | 400 | não executada: entrada inválida | Validação de entrada, antes dos analisadores | aprovado |
| B03 | 200 | erro | ERRO_SINTATICO em 1:24; lexema '' | aprovado |
| B04 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| B05 | 400 | não executada: entrada inválida | Validação de entrada, antes dos analisadores | aprovado |
| B06 | 200 | sucesso | Sem erro no conjunto verificado | aprovado |
| B07 | 200 | erro | ERRO_SINTATICO em 1:65; lexema '{' | aprovado |
| B08 | 200 | nao_executada | ERRO_LEXICO em 1:1; lexema '@' | aprovado |

## Casos semânticos futuros

| ID | Entrada | Controle sintático observado | Avaliação semântica |
|---|---|---|---|
| M01 | `x = 1;` | sucesso | Pendente; não implementada |
| M02 | `int x; int x;` | sucesso | Pendente; não implementada |
| M03 | `int x; x = 2.5;` | sucesso | Pendente; não implementada |
