from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,re,subprocess,collections
out=Path('/workspace/entregas/etapa5/resultados')
r=json.loads((out/'casos_funcionais.json').read_text())
backend=(out/'backend.txt').read_text();frontend=(out/'frontend.txt').read_text();navegador=(out/'navegador.txt').read_text();integracao=(out/'integracao.txt').read_text()
nb=int(re.search(r'(\d+) passed',backend).group(1)); nf=int(re.search(r'^# pass (\d+)',frontend,re.M).group(1)); ne=int(re.search(r'OK: (\d+) cenários E2E',navegador).group(1))
assert nb==229 and nf==41 and ne==60
assert '# fail 0' in frontend and 'OK: saúde, HTML' in integracao
meta=json.loads((out/'metadados.json').read_text());meta['fim']=datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat();meta['docker_versao_observada']='28.4.0';meta['imagens_verificadas_por_sha256']=True;meta['imagens_reconstruidas_nesta_rodada']=False
meta['observacao_build']='Imagens locais existentes usadas após confronto de SHA-256 de main.py, parser.py, scanner.py e frontend/app.js com o checkout. Smoke executou docker compose up --build, reutilizando camadas; nenhuma alteração de código.'
meta['resultados']={'backend_aprovados':nb,'backend_reprovados':0,'interface_aprovados':nf,'interface_reprovados':0,'e2e_cenarios_aprovados':ne,'e2e_cenarios_reprovados':0,'integracao':'aprovado','casos_planejados_aplicaveis':33,'casos_planejados_executados':33,'casos_planejados_aprovados':33,'casos_semanticos_executados':0,'casos_semanticos_pendentes':3,'participantes_humanos':0,'avaliacao_por_pares':'ainda não aplicada'}
(out/'metadados.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
data=meta['fim'][:10]
texto=f'''# Resultados técnicos observados — Tarefa 5

Revalidação em **26/11/2026**, horário de São Paulo, entre `{meta['inicio']}` e `{meta['fim']}`. Versão examinada: `{r['commit']}`. Todas as saídas abaixo foram obtidas nesta rodada, sem alterar os registros da Etapa 4 ou o código do projeto.

## Resultados das suítes

| Procedimento | Executados/aprovados | Falhas | Evidência |
|---|---:|---:|---|
| pytest: scanner, parser, API e validação | {nb}/{nb} | 0 | `backend.txt` |
| Node/jsdom: lógica e interface | {nf}/{nf} | 0 | `frontend.txt` |
| Smoke nginx → API → scanner → parser | Fluxo aprovado | 0 | `integracao.txt` |
| Chromium real, desktop e viewport móvel | {ne}/{ne} cenários | 0 | `navegador.txt`; `capturas/` |
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
python3 /workspace/entregas/etapa5/resultados/avaliar_casos_funcionais.py
python3 scripts/teste_navegador.py --chromium /usr/bin/chromium --capturas /workspace/entregas/etapa5/resultados/capturas
```

O script dos 33 casos acompanha este pacote. Seu caminho `ROOT` aponta para o checkout desta sessão e pode ser adaptado para o diretório do projeto em outra máquina. Os arquivos do protocolo e os três esperados de AST vêm de `tests/planejamento/`, anteriores à implementação. O script não importa o parser para gerar resultados esperados.

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
'''
for c in r['casos']:
 erros=c['erros_lexicos'] or c['erros_sintaticos']
 if erros:
  e=erros[0];diagnostico=f"{e['tipo']} em {e['linha']}:{e['coluna']}; lexema {e['lexema']!r}".replace('|','\\|')
 elif c['http_observado']==400:diagnostico='Validação de entrada, antes dos analisadores'
 else:diagnostico='Sem erro no conjunto verificado'
 texto+=f"| {c['id']} | {c['http_observado']} | {c['estado_sintatico_observado'] or 'não executada: entrada inválida'} | {diagnostico} | {c['resultado']} |\n"
texto+='\n## Casos semânticos futuros\n\n| ID | Entrada | Controle sintático observado | Avaliação semântica |\n|---|---|---|---|\n'
for c in r['controles_sintaticos_de_casos_semanticos_futuros']:
 texto+=f"| {c['id']} | `{c['codigo']}` | {c['estado_sintatico_observado']} | Pendente; não implementada |\n"
(out/'resumo-resultados.md').write_text(texto,encoding='utf-8')
print('Resumo escrito:',out/'resumo-resultados.md')
