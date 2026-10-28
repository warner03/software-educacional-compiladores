#!/usr/bin/env bash
# Integração real: nginx -> FastAPI -> scanner; sem depender de mocks.
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
from html.parser import HTMLParser
from urllib.error import HTTPError
from urllib.request import Request, build_opener, ProxyHandler

# Apenas as requisições loopback deste teste são feitas diretamente.
http = build_opener(ProxyHandler({}))

def requisitar(caminho, codigo=None):
    base = 'http://127.0.0.1:8000' if caminho == '/saude' else 'http://127.0.0.1:8501'
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
assert requisitar('/api/analisar', '   ')[0] == 400
status, corpo = requisitar('/api/analisar', 'int = ;')
assert status == 200 and json.loads(corpo)['sucesso'] is True, 'Scanner não substitui parser'
status, corpo = requisitar('/api/analisar', '/* apenas comentário */')
assert status == 200 and json.loads(corpo)['tokens'] == []
print('OK: saúde, HTML, exemplos, tokens/posições, erros/recuperação, entrada vazia, escopo léxico e comentários passaram.')
PY
