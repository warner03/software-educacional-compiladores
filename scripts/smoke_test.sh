#!/usr/bin/env bash
# Teste de implantação: sobe o Compose, verifica serviços, HTML da interface e a comunicação.
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { echo "FALHOU: $1"; docker compose down; exit 1; }

docker compose up --build -d --wait

curl -fsS http://localhost:8000/saude | grep -q '"ok"'                        || fail "backend /saude"

# a interface precisa estar no HTML puro (sem depender de JavaScript)
pagina=$(curl -fsS http://localhost:8501/)
for el in "<textarea" "<select" "<button" 'id="resultado"' "Mini-C"; do
  echo "$pagina" | grep -q "$el"                                              || fail "elemento ausente no HTML: $el"
done
[ "$(echo "$pagina" | grep -o '<option value="ex' | wc -l)" -ge 3 ]          || fail "menos de 3 exemplos"

# comunicação frontend -> backend (pelo proxy do nginx, como o navegador faz)
code=$(curl -s -o /tmp/r.json -w '%{http_code}' -X POST http://localhost:8501/api/analisar \
  -H 'Content-Type: application/json' -d '{"codigo":"int numero = 10;"}')
[ "$code" = 200 ] && grep -q '"recebido":true' /tmp/r.json                    || fail "POST válido via proxy"

code=$(curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:8501/api/analisar \
  -H 'Content-Type: application/json' -d '{"codigo":"   "}')
[ "$code" = 400 ]                                                             || fail "POST só espaços deveria ser 400"

echo "OK: todas as verificações de implantação passaram"
docker compose down
