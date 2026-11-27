#!/usr/bin/env python3
"""Executa as suítes e registra contagens reais, sem aceitar uma execução vazia.

Use --integracao para executar o smoke e --navegador para E2E com Playwright.
COMPOSE_FILE e demais configurações Docker são herdados do ambiente.
"""
import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def rodar(comando, formato):
    r = subprocess.run(comando, cwd=ROOT, capture_output=True, text=True)
    saida = r.stdout + r.stderr
    print(saida, end='')
    pasta = ROOT / 'docs/trabalho5/evidencias'
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = {'pytest': 'backend.txt', 'tap': 'frontend.txt', 'e2e': 'navegador.txt', 'smoke': 'integracao.txt', 'casos': 'casos-semanticos.txt'}[formato]
    (pasta / arquivo).write_text(saida, encoding='utf-8')
    if formato == 'pytest':
        encontrar = lambda termo: re.search(rf'(\d+) {termo}', saida)
        contagem = lambda termo: int(encontrar(termo).group(1)) if encontrar(termo) else 0
        passou, falhou, pulou = contagem('passed'), contagem('failed'), contagem('skipped')
        valido = r.returncode == 0 and passou > 0 and falhou == 0
    elif formato == 'tap':
        def contar(termo):
            m = re.search(rf'^# {termo} (\d+)\s*$', saida, re.MULTILINE)
            return int(m.group(1)) if m else 0
        passou, falhou, pulou = contar('pass'), contar('fail'), contar('skipped')
        valido = r.returncode == 0 and passou > 0 and falhou == 0 and contar('cancelled') == 0
    elif formato == 'e2e':
        m = re.search(r'OK: (\d+) cenários E2E', saida)
        passou, falhou, pulou = int(m.group(1)) if m else 0, 0, 0
        valido = r.returncode == 0 and passou > 0
    elif formato == 'casos':
        m = re.search(r'OK: (\d+)/(\d+) casos semânticos aprovados; (\d+) executados', saida)
        passou, total, executados = (map(int, m.groups()) if m else (0, 0, 0))
        falhou, pulou = total - passou, total - executados
        valido = r.returncode == 0 and total > 0 and passou == executados == total
    else:
        passou, falhou, pulou = '-', '-', '-'
        valido = r.returncode == 0 and 'OK: saúde, HTML' in saida
    return passou, falhou, pulou, valido, r.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integracao', action='store_true')
    parser.add_argument('--navegador', action='store_true')
    parser.add_argument('--casos', action='store_true', help='Executar os 30 casos semânticos pela API real')
    parser.add_argument('--chromium')
    parser.add_argument('--capturas', default='docs/trabalho5/capturas', help='Imagens E2E e exemplo JSON da AST')
    args = parser.parse_args()
    pasta = ROOT / 'docs/trabalho5/evidencias'
    pasta.mkdir(parents=True, exist_ok=True)
    versao = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True)
    estado_git = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True)
    arquivos = ['backend/app/main.py', 'backend/app/scanner.py', 'backend/app/parser.py', 'backend/app/semantica.py',
                'frontend/app.js', 'frontend/index.html', 'frontend/style.css']
    metadados = {
        'inicio': datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat(),
        'commit_base_checkout': versao.stdout.strip() if versao.returncode == 0 else 'sem metadados Git',
        'alteracoes_locais_presentes': bool(estado_git.stdout.strip()),
        'arquivos_sha256': {nome: hashlib.sha256((ROOT / nome).read_bytes()).hexdigest() for nome in arquivos},
        'observacao': 'A versão efetivamente testada é identificada pelos hashes. Commit-base pode preceder mudanças ainda não commitadas.',
        'avaliacao_humana_executada': False,
    }
    tarefas = [
        ('Backend: scanner, parser, semântica e endpoints', ['docker', 'compose', 'run', '--rm', 'backend', 'pytest', '-q'], 'pytest'),
        ('Frontend: lógica e interface jsdom', ['docker', 'compose', 'run', '--rm', 'testes-frontend'], 'tap'),
    ]
    if args.integracao:
        tarefas.append(('Integração nginx/API/scanner/parser/semântica', ['bash', 'scripts/smoke_test.sh'], 'smoke'))
    if args.casos:
        tarefas.append(('Casos semânticos por API real', [sys.executable, 'scripts/avaliar_semantica.py'], 'casos'))
    if args.navegador:
        comando = [sys.executable, 'scripts/teste_navegador.py', '--capturas', args.capturas]
        if args.chromium:
            comando.extend(['--chromium', args.chromium])
        tarefas.append(('Navegador real: desktop e viewport móvel', comando, 'e2e'))
    linhas, falha = [], False
    for nome, comando, formato in tarefas:
        if formato in ('e2e', 'casos'):
            # Executar depois do smoke, que encerra os serviços por padrão.
            inicio = subprocess.run(['docker', 'compose', 'up', '-d', '--wait'], cwd=ROOT)
            if inicio.returncode:
                falha = True
                linhas.append(f'| {nome} | Inicialização dos serviços | - | - | - | Não executado: falha de inicialização (exit {inicio.returncode}) |')
                continue
        ap, reprovados, pulados, valido, retorno = rodar(comando, formato)
        falha |= not valido
        estado = 'Aprovado' if valido else f'Falha ou execução sem testes válidos (exit {retorno}); consultar saída'
        linhas.append(f"| {nome} | `{' '.join(comando)}` | {ap} | {reprovados} | {pulados} | {estado} |")
    if not args.integracao:
        linhas.append('| Integração nginx/API/scanner/parser/semântica | `bash scripts/smoke_test.sh` | - | - | - | Não executado nesta rodada |')
    if not args.navegador:
        linhas.append('| Navegador real | `python3 scripts/teste_navegador.py` | - | - | - | Não executado nesta rodada |')
    if not args.casos:
        linhas.append('| Casos semânticos por API real | `python3 scripts/avaliar_semantica.py` | - | - | - | Não executado nesta rodada |')
    metadados['fim'] = datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat()
    metadados['rodada_sem_falhas'] = not falha
    (pasta / 'metadados.json').write_text(json.dumps(metadados, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    data = datetime.now(ZoneInfo('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M %Z')
    texto = f'''# Registro de testes — Etapa 5

Execução: {data}. Resultados abaixo pertencem a esta rodada; ausência de testes ou erro de execução não é tratado como aprovação.

| Módulo | Comando | Aprovados | Reprovados | Pulados | Resultado |
|---|---|---|---|---|---|
''' + '\n'.join(linhas) + f'''

## Ambiente e reprodução

- Docker Compose, Python 3.12, Node 20/jsdom 24.1.0 e Chromium headless via Playwright.
- Pré-requisito: reconstruir imagens após mudanças (`docker compose build backend frontend testes-frontend`). Build sem cache desta entrega preservado em `trabalho5/evidencias/build-sem-cache.txt`.
- Na nuvem: `COMPILADORES_API_PORT=18000`, `COMPOSE_FILE=docker-compose.yml:compose.cloud.yaml`, `CLOUD_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt`. Ver [execução](execucao-nuvem.md); TLS continua verificado.
- Saídas desta rodada: [trabalho5/evidencias/](trabalho5/evidencias/). Capturas/medidas: `{args.capturas}`.
- Históricos preservados: [Etapa 2](registro-de-testes-etapa2.md), [Etapa 3](registro-de-testes-etapa3.md) e [Etapa 4](registro-de-testes-etapa4.md). A Tarefa 5 teórica original permanece como fotografia da base anterior.

## Escopo e esperados

- Política semântica e acessibilidade definidas antes do analisador em [decisoes.md](trabalho5/decisoes.md). Trinta casos próprios em `backend/tests/fixtures/etapa5-semantica.json` fixam resultados e regras esperadas, sem gerar os esperados com a implementação avaliada.
- Declaração antes do uso, redeclaração no escopo, sombreamento, tipos/promoção, comparação, condição bool e inicialização definida, incluindo interseção dos caminhos do if/else e leituras no próprio inicializador.
- M01–M03, antes previstos como casos futuros, agora exigem os diagnósticos semânticos definidos. Aceitação sintática permanece preservada; não basta para aprovar os casos semânticos.
- AST/tokens e seus testes anteriores preservados. Dados de contrato nos testes do frontend são entradas, com esperados DOM escritos separadamente; não substituem os oráculos semânticos.
- Os 30 casos externos também pertencem à suíte; a execução por nginx verifica integração, sem somá-los como casos independentes. Cobertura de casos não é cobertura de código; linhas/ramos não foram medidos.
- O navegador verifica três fases, tabela/referências/escopos, ligações à AST e fonte, erros, limites, modos visuais, persistência, teclado e responsividade em 1366px e 390px.
- Contraste textual mínimo exigido de 4,5:1 para os elementos medidos em três modos e quatro estados. Foco/contorno de seleção exigem 3:1. As cores/fundos computados e gradientes são examinados; controles desabilitados ficam excluídos.

## Rodadas e correções

- Primeira rodada: 322 testes de backend, 55 de interface e 134 cenários de navegador aprovados, sem reprovações. O registro acima corresponde à última rodada, com as alterações finais reconstruídas.
- Conferência visual: reduzida a largura de texto nas legendas e reposicionada a captura das tabelas na sua borda esquerda, pois a seleção automática do navegador rolava a região até o botão à direita.
- Acrescentado acesso direto do resultado ao trecho destacado e conferência de foco/contorno em cada modo, mantendo a posição e os resultados ao alterar a preferência.
- O smoke encerra os serviços por padrão; o registrador inicia/aguarda os serviços antes dos casos HTTP e do E2E.
- As correções históricas das etapas anteriores continuam registradas nos documentos correspondentes. Não se alteraram regras ou esperados para transformar falha em aprovação.

## Limitações

- Nenhum estudo com pessoas daltônicas ou avaliação por pares foi executado. As simulações de protanopia/deuteranopia/tritanopia/acromatopsia são inspeções técnicas no Chromium, não resultados humanos.
- Os critérios medidos não constituem auditoria WCAG integral ou certificação. Viewport móvel não é aparelho físico; tempos impressos não são benchmark controlado.
- Sem execução do programa, valores constantes, funções, laços, conversões explícitas, otimização ou geração de código. A representação semântica ampliada fica para a Etapa 6.
- O pytest pode emitir aviso de depreciação Starlette/AnyIO; isso não é falha funcional. Estatísticas humanas e ganho de aprendizagem continuam sem dados.
'''
    (ROOT / 'docs/registro-de-testes.md').write_text(texto, encoding='utf-8')
    print('Registro atualizado em docs/registro-de-testes.md')
    return 1 if falha else 0


if __name__ == '__main__':
    raise SystemExit(main())
