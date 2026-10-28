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
    args = parser.parse_args()
    tarefas = [
        ('Backend: scanner, validações e endpoints', ['docker', 'compose', 'run', '--rm', 'backend', 'pytest', '-q'], 'pytest'),
        ('Frontend: lógica e interface jsdom', ['docker', 'compose', 'run', '--rm', 'testes-frontend'], 'tap'),
    ]
    if args.integracao:
        tarefas.append(('Integração nginx/API/scanner', ['bash', 'scripts/smoke_test.sh'], 'smoke'))
    if args.navegador:
        comando = [sys.executable, 'scripts/teste_navegador.py']
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
        linhas.append('| Integração nginx/API/scanner | `bash scripts/smoke_test.sh` | - | - | - | Não executado nesta rodada |')
    if not args.navegador:
        linhas.append('| Navegador real | `python3 scripts/teste_navegador.py` | - | - | - | Não executado nesta rodada |')
    data = datetime.now(ZoneInfo('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M %Z')
    texto = f'''# Registro de testes — Etapa 3

Execução: {data}. Resultados abaixo pertencem a esta rodada; ausência de testes ou erro de execução não é tratado como aprovação.

| Módulo | Comando | Aprovados | Reprovados | Pulados | Resultado |
|---|---|---|---|---|---|
''' + '\n'.join(linhas) + '''

## Ambiente e reprodução

- Docker Compose, backend Python 3.12, frontend de testes Node 20 e jsdom 24.1.0.
- Em rede com proxy TLS, utilizar o bundle confiável da máquina e o override documentado em `docs/execucao-nuvem.md`. Não desativar TLS.
- A execução em navegador usa Playwright; o viewport móvel simula 390px com toque, não um aparelho físico.
- Pré-requisito: reconstruir todas as imagens após alterar código (`docker compose build backend frontend testes-frontend`).
- Histórico da Etapa 2 preservado em [registro-de-testes-etapa2.md](registro-de-testes-etapa2.md).

## Falhas encontradas e correções

- Primeira rodada do scanner: 107 testes passaram e 7 falharam. Um operador simples no fim do arquivo entrava no caminho de operadores de dois caracteres. Correção: exigir comprimento 2 nesse caminho; os casos de borda permanecem na regressão.
- Na preparação inicial do ambiente, arquivos estáticos com permissão 600 não eram legíveis pelo nginx. O Dockerfile agora define leitura 644 dentro da imagem, independentemente da permissão do checkout.
- O healthcheck wget tentava usar o proxy externo para loopback. A consulta local agora usa `-Y off`; o tráfego externo de instalação continua usando o proxy e TLS verificado.
- Os testes de resposta da Etapa 2 foram atualizados para o contrato léxico, mantendo verificações de exemplos, edição, validação e comunicação. A mensagem de recebimento foi substituída pelo resultado da análise.
- Na primeira execução conjunta do registrador, o navegador foi iniciado após o smoke já ter encerrado os serviços e falhou por conexão recusada. O registrador agora reinicia e aguarda os serviços imediatamente antes do E2E; a sequência completa foi reexecutada.

## Limitações

- O pytest informa um aviso de depreciação da integração Starlette/AnyIO; os testes completam sem falha. Não se trata de erro do scanner.
- Não há parser, análise semântica ou AST nesta etapa.
- Não foram realizados estudo com estudantes, medição de aprendizagem ou auditoria completa de acessibilidade.
- A ausência de erro léxico não implica validade sintática ou semântica.
'''
    (ROOT / 'docs/registro-de-testes.md').write_text(texto, encoding='utf-8')
    print('Registro atualizado em docs/registro-de-testes.md')
    return 1 if falha else 0


if __name__ == '__main__':
    raise SystemExit(main())
