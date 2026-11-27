#!/usr/bin/env python3
"""Reexecuta por HTTP os casos semânticos fixados antes da implementação."""
import argparse
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, build_opener, ProxyHandler
from zoneinfo import ZoneInfo


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raiz', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--saida', type=Path)
    parser.add_argument('--url', default='http://127.0.0.1:8501/api/analisar')
    args = parser.parse_args()
    raiz = args.raiz.resolve()
    saida = args.saida or raiz / 'docs/trabalho5/evidencias'
    saida.mkdir(parents=True, exist_ok=True)
    arquivo = raiz / 'backend/tests/fixtures/etapa5-semantica.json'
    protocolo = json.loads(arquivo.read_text())
    git = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=raiz, capture_output=True, text=True)
    estado_git = subprocess.run(['git', 'status', '--porcelain'], cwd=raiz, capture_output=True, text=True)
    http = build_opener(ProxyHandler({})) if urlparse(args.url).hostname in ('127.0.0.1', 'localhost', '::1') else build_opener()
    rows = []
    for caso in protocolo['casos']:
        dados = None
        status = None
        falha = ''
        try:
            req = Request(args.url, data=json.dumps({'codigo': caso['codigo']}).encode(), headers={'Content-Type': 'application/json'})
            try:
                with http.open(req, timeout=20) as resp:
                    status, dados = resp.status, json.loads(resp.read())
            except HTTPError as e:
                status, dados = e.code, json.loads(e.read())
            assert status == 200, f'HTTP esperado 200, observado {status}'
            assert dados['sucesso'] is True and dados['sintatica']['sucesso'] is True, 'Os casos são lexical/sintaticamente válidos'
            sem = dados['semantica']
            assert sem['sucesso'] is caso['sucesso_esperado'], 'Resultado semântico diferente da política'
            assert [e['regra'] for e in sem['erros']] == caso['regras_esperadas'], 'Regras diferentes do esperado'
            assert sem['estado'] == ('sucesso' if caso['sucesso_esperado'] else 'erro')
            assert dados['sintatica']['ast'] is not None, 'AST deve continuar disponível'
        except (AssertionError, URLError, OSError, ValueError, KeyError, TypeError) as e:
            falha = f'{type(e).__name__}: {e}'
        sem = (dados or {}).get('semantica', {})
        rows.append({
            'id': caso['id'], 'codigo': caso['codigo'], 'regras_esperadas': caso['regras_esperadas'],
            'sucesso_esperado': caso['sucesso_esperado'], 'http_observado': status,
            'estado_observado': sem.get('estado'), 'regras_observadas': [e['regra'] for e in sem.get('erros', [])],
            'simbolos_observados': sem.get('tabelaSimbolos', []), 'diagnosticos_observados': sem.get('erros', []),
            'resultado': 'reprovado' if falha else 'aprovado', 'falha': falha,
        })
        print(caso['id'], rows[-1]['resultado'], sem.get('estado'), falha)
    executados = sum(r['http_observado'] is not None for r in rows)
    aprovados = sum(r['resultado'] == 'aprovado' for r in rows)
    relatorio = {
        'data': datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat(),
        'commit_checkout': git.stdout.strip() if git.returncode == 0 else 'sem metadados Git',
        'alteracoes_locais_presentes': bool(estado_git.stdout.strip()),
        'arquivos_sha256': {nome: hashlib.sha256((raiz / nome).read_bytes()).hexdigest() for nome in
                           ['backend/app/main.py', 'backend/app/scanner.py', 'backend/app/parser.py', 'backend/app/semantica.py']},
        'url': args.url, 'fixture_sha256': hashlib.sha256(arquivo.read_bytes()).hexdigest(),
        'planejados': len(rows), 'executados': executados, 'aprovados': aprovados,
        'cobertura_casos_pct': 100 * executados / len(rows),
        'aprovacao_pct': 100 * aprovados / executados if executados else None,
        'prontidao_pct': 100 * aprovados / len(rows),
        'limites': 'Mesmo conjunto usado na suíte; não somar como casos independentes. Não mede cobertura de código, aprendizagem ou acessibilidade com pessoas.',
        'casos': rows,
    }
    (saida / 'casos-semanticos.json').write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with (saida / 'casos-semanticos.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        for row in rows:
            w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, list) else v for k, v in row.items()})
    print(f'OK: {aprovados}/{len(rows)} casos semânticos aprovados; {executados} executados.')
    return int(aprovados != len(rows))


if __name__ == '__main__':
    raise SystemExit(main())
