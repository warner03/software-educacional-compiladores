#!/usr/bin/env bash
# Integração real: nginx -> FastAPI -> scanner -> parser; sem mocks.
set -euo pipefail
cd "$(dirname "$0")/.."
cleanup() {
  resultado=$?
  trap - EXIT
  if [ "$resultado" -ne 0 ]; then docker compose logs --tail=40 || true; fi
  if [ "${KEEP_RUNNING:-0}" != 1 ]; then docker compose down; fi
  exit "$resultado"
}
trap cleanup EXIT

docker compose up --build -d --wait
python3 - <<'PY'
import json
import os
from html.parser import HTMLParser
from urllib.error import HTTPError
from urllib.request import Request, build_opener, ProxyHandler

# Apenas as requisições loopback deste teste são feitas diretamente.
http = build_opener(ProxyHandler({}))

def requisitar(caminho, codigo=None):
    porta = os.environ.get('COMPILADORES_API_PORT', '8000')
    base = f'http://127.0.0.1:{porta}' if caminho == '/saude' else 'http://127.0.0.1:8501'
    dados = None if codigo is None else json.dumps({'codigo': codigo}).encode()
    req = Request(base + caminho, data=dados, headers={'Content-Type': 'application/json'})
    try:
        with http.open(req, timeout=10) as r:
            return r.status, r.read().decode()
    except HTTPError as e:
        return e.code, e.read().decode()

assert requisitar('/saude') == (200, '{"status":"ok"}'), 'Saúde do backend'
status, pagina = requisitar('/')
assert status == 200 and 'Mini-C' in pagina
class Interface(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags, self.exemplos = set(), 0
    def handle_starttag(self, tag, attrs):
        self.tags.add(tag)
        if tag == 'option' and dict(attrs).get('value', '').startswith('ex'):
            self.exemplos += 1
html = Interface()
html.feed(pagina)
assert {'textarea', 'select', 'button'} <= html.tags and html.exemplos >= 6
status, corpo = requisitar('/api/analisar', 'int numero = 10;')
r = json.loads(corpo)
assert status == 200 and r['sucesso'] is True and r['erros'] == []
assert r['sintatica']['sucesso'] is True
assert r['sintatica']['ast']['comandos'][0]['nome'] == 'numero'
assert r['tokens'] == [
    {'tipo': 'PALAVRA_RESERVADA', 'lexema': 'int', 'linha': 1, 'coluna': 1},
    {'tipo': 'IDENTIFICADOR', 'lexema': 'numero', 'linha': 1, 'coluna': 5},
    {'tipo': 'OPERADOR', 'lexema': '=', 'linha': 1, 'coluna': 12},
    {'tipo': 'LITERAL_INTEIRO', 'lexema': '10', 'linha': 1, 'coluna': 14},
    {'tipo': 'DELIMITADOR', 'lexema': ';', 'linha': 1, 'coluna': 16},
]
status, corpo = requisitar('/api/analisar', 'int x=12abc;\n@ float y=7.5;')
r = json.loads(corpo)
assert status == 200 and r['sucesso'] is False
assert [(e['lexema'], e['linha'], e['coluna']) for e in r['erros']] == [('12abc', 1, 7), ('@', 2, 1)]
assert any(t['lexema'] == '7.5' for t in r['tokens']), 'Recuperação após erro'
assert r['sintatica'] == {'estado': 'nao_executada', 'sucesso': None, 'motivo': 'erros_lexicos', 'ast': None, 'erros': []}
assert requisitar('/api/analisar', '   ')[0] == 400
status, corpo = requisitar('/api/analisar', 'int = ;')
r = json.loads(corpo)
assert status == 200 and r['sucesso'] is True, 'Scanner preservado'
assert r['sintatica']['estado'] == 'erro' and r['sintatica']['ast'] is None
assert r['sintatica']['erros'][0]['esperado'] == ['IDENTIFICADOR']
status, corpo = requisitar('/api/analisar', '/* apenas comentário */')
r = json.loads(corpo)
assert status == 200 and r['tokens'] == [] and r['sintatica']['estado'] == 'erro'
status, corpo = requisitar('/api/analisar', 'int x = 10 + 5 * 2;')
expr = json.loads(corpo)['sintatica']['ast']['comandos'][0]['inicializador']
assert expr['operador'] == '+' and expr['direita']['operador'] == '*'
status, corpo = requisitar('/api/analisar', 'int a = ;\nint b;\nb = ;')
erros = json.loads(corpo)['sintatica']['erros']
assert [(e['linha'], e['coluna']) for e in erros] == [(1, 9), (3, 5)]
print('OK: saúde, HTML, exemplos, tokens/posições, scanner preservado, AST/precedência, erros léxicos/sintáticos, recuperação e validação passaram.')
PY
