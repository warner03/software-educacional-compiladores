#!/usr/bin/env python3
"""Executa as suítes e registra contagens reais, sem aceitar uma execução vazia.

Use --integracao para executar o smoke e --navegador para E2E com Playwright.
COMPOSE_FILE e demais configurações Docker são herdados do ambiente.
"""
import argparse
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
    pasta = ROOT / 'docs/trabalho4/evidencias'
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = {'pytest': 'backend.txt', 'tap': 'frontend.txt', 'e2e': 'navegador.txt', 'smoke': 'integracao.txt'}[formato]
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
    else:
        passou, falhou, pulou = '-', '-', '-'
        valido = r.returncode == 0 and 'OK: saúde, HTML' in saida
    return passou, falhou, pulou, valido, r.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integracao', action='store_true')
    parser.add_argument('--navegador', action='store_true')
    parser.add_argument('--chromium')
    parser.add_argument('--capturas', default='docs/trabalho4/capturas', help='Imagens E2E e exemplo JSON da AST')
    args = parser.parse_args()
    tarefas = [
        ('Backend: scanner, parser, validações e endpoints', ['docker', 'compose', 'run', '--rm', 'backend', 'pytest', '-q'], 'pytest'),
        ('Frontend: lógica e interface jsdom', ['docker', 'compose', 'run', '--rm', 'testes-frontend'], 'tap'),
    ]
    if args.integracao:
        tarefas.append(('Integração nginx/API/scanner/parser', ['bash', 'scripts/smoke_test.sh'], 'smoke'))
    if args.navegador:
        comando = [sys.executable, 'scripts/teste_navegador.py', '--capturas', args.capturas]
        if args.chromium:
            comando.extend(['--chromium', args.chromium])
        tarefas.append(('Navegador real: desktop e viewport móvel', comando, 'e2e'))
    linhas, falha = [], False
    for nome, comando, formato in tarefas:
        if formato == 'e2e':
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
        linhas.append('| Integração nginx/API/scanner/parser | `bash scripts/smoke_test.sh` | - | - | - | Não executado nesta rodada |')
    if not args.navegador:
        linhas.append('| Navegador real | `python3 scripts/teste_navegador.py` | - | - | - | Não executado nesta rodada |')
    data = datetime.now(ZoneInfo('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M %Z')
    texto = f'''# Registro de testes — Etapa 4

Execução: {data}. Resultados abaixo pertencem a esta rodada; ausência de testes ou erro de execução não é tratado como aprovação.

| Módulo | Comando | Aprovados | Reprovados | Pulados | Resultado |
|---|---|---|---|---|---|
''' + '\n'.join(linhas) + f'''

## Ambiente e reprodução

- Docker Compose, backend Python 3.12, frontend de testes Node 20 e jsdom 24.1.0.
- Em rede com proxy TLS, utilizar o bundle confiável da máquina e o override documentado em `docs/execucao-nuvem.md`. Não desativar TLS.
- A execução em navegador usa Playwright; o viewport móvel simula 390px com toque, não um aparelho físico.
- Pré-requisito: reconstruir todas as imagens após alterar código (`docker compose build backend frontend testes-frontend`).
- Histórico da Etapa 2 preservado em [registro-de-testes-etapa2.md](registro-de-testes-etapa2.md).
- Histórico da Etapa 3 preservado em [registro-de-testes-etapa3.md](registro-de-testes-etapa3.md).
- Saídas completas desta rodada em [trabalho4/evidencias/](trabalho4/evidencias/); capturas em `{args.capturas}`.
- Neste ambiente: `COMPILADORES_API_PORT=18000`, `COMPOSE_FILE=docker-compose.yml:compose.cloud.yaml` e `CLOUD_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt`. Porta padrão local permanece 8000.

## Casos e referências anteriores à implementação

- Os 33 casos aplicáveis fixados na Tarefa 4 são parametrizados em `test_api_sintatica.py`, com os mesmos códigos e resultados esperados. Os três oráculos V04–V06 são comparados estruturalmente em `test_parser.py`; posições são verificadas separadamente.
- Fixtures Docker são cópias binárias dos originais do planejamento. O scanner não foi alterado; sua suíte original e sua saída completa continuam verificadas.
- M01–M03 confirmam somente aceitação sintática; a avaliação semântica desses casos permanece pendente para a Etapa 5.
- Testes adicionais cobrem todas as construções, precedência, associação, recuperação, EOF, posições Unicode/CRLF/tab, limites em 64/65 níveis, altura e quantidade de nós, API, seleção/exportação e respostas incoerentes.
- Critérios, limites e decisões foram registrados antes da primeira execução em [trabalho4/decisoes.md](trabalho4/decisoes.md). O teste da UI usa referência manual; não gera o esperado com o parser.

## Falhas encontradas e correções

- Primeira rodada do backend: 228 aprovados, sem falhas. A suíte léxica e os testes anteriores da API/validação foram mantidos sem alteração.
- Primeira rodada da interface: 40 aprovados e um reprovado. O seletor do novo teste de hierarquia alcançava o resumo da própria adição em vez da multiplicação filha. Correção apenas no seletor, usando `:scope > .ast-filhos`; esperado matemático preservado.
- A apresentação do destaque foi ajustada para informar quando a AST está selecionada, evitando confundir o trecho da árvore com o token corrente da navegação.
- Correções históricas do scanner/infraestrutura permanecem descritas no registro da Etapa 3. Nenhum limite de recursos foi criado depois de observar resultados para fazer um caso planejado passar.

## Limitações

- O pytest pode informar aviso de depreciação da integração Starlette/AnyIO; verificar contagens/estado da rodada acima.
- Semântica, tabela de símbolos, execução e geração de código ainda não foram implementadas.
- Não foram realizados estudo com estudantes, medição de aprendizagem ou auditoria completa de acessibilidade.
- A ausência de erro sintático não implica validade semântica. A recuperação pode descartar comandos e não garante enumerar todos os erros.
- Tempos de resposta/renderização impressos pelo E2E são observações desta máquina, não comparação de desempenho ou benchmark controlado.
'''
    (ROOT / 'docs/registro-de-testes.md').write_text(texto, encoding='utf-8')
    print('Registro atualizado em docs/registro-de-testes.md')
    return 1 if falha else 0


if __name__ == '__main__':
    raise SystemExit(main())
