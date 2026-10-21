#!/usr/bin/env bash
# Teste de implantação: sobe o Compose, verifica serviços e a comunicação ponta a ponta.
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { echo "FALHOU: $1"; docker compose down; exit 1; }

docker compose up --build -d --wait
curl -fsS http://localhost:8000/saude | grep -q '"ok"'            || fail "backend /saude"
curl -fsS http://localhost:8501/_stcore/health | grep -q ok        || fail "frontend health"

code=$(curl -s -o /tmp/r.json -w '%{http_code}' -X POST http://localhost:8000/analisar \
  -H 'Content-Type: application/json' -d '{"codigo":"int numero = 10;"}')
[ "$code" = 200 ] && grep -q '"recebido":true' /tmp/r.json         || fail "POST válido"

code=$(curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:8000/analisar \
  -H 'Content-Type: application/json' -d '{"codigo":"   "}')
[ "$code" = 400 ]                                                  || fail "POST só espaços deveria ser 400"

# comunicação entre contêineres (frontend -> backend pela rede do Compose)
docker compose exec -T frontend python -c "import api_client as a; r=a.enviar_codigo('int x;'); assert r['tipo']=='sucesso', r" \
                                                                   || fail "frontend -> backend"
echo "OK: todas as verificações de implantação passaram"
docker compose down
