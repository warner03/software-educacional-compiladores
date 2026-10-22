#!/usr/bin/env python3
"""Roda os testes e escreve docs/registro-de-testes.md com os números reais."""
import datetime
import re
import subprocess
from pathlib import Path


def rodar(comando):
    r = subprocess.run(comando, capture_output=True, text=True)
    saida = r.stdout + r.stderr
    ap = re.search(r"(?:passed|pass)\s*[:#]?\s*(\d+)|(\d+) passed", saida)
    ap_n = next((int(g) for g in ap.groups() if g), 0) if ap else 0
    rp = re.search(r"(\d+) failed|fail\s*(\d+)", saida)
    rp_n = next((int(g) for g in rp.groups() if g), 0) if rp else 0
    if r.returncode != 0 and rp_n == 0:
        rp_n = 1  # falhou por outro motivo (ex.: erro de execução)
    return ap_n, rp_n


hoje = datetime.date.today().strftime("%d/%m/%Y")
b_ok, b_fail = rodar(["docker", "compose", "run", "--rm", "backend", "pytest", "-q"])
f_ok, f_fail = rodar(["docker", "compose", "run", "--rm", "testes-frontend"])
obs = lambda f: "Todos aprovados" if f == 0 else "Há falhas, investigar"

texto = f"""# Registro de testes

| Data | Módulo | Tipo | Comando | Aprovados | Reprovados | Observações |
|---|---|---|---|---|---|---|
| {hoje} | Backend: validações e endpoints | Unitário + endpoint | `docker compose run --rm backend pytest -v` | {b_ok} | {b_fail} | {obs(b_fail)} |
| {hoje} | Frontend: lógica, exemplos e interface (jsdom) | Unitário + interface | `docker compose run --rm testes-frontend` | {f_ok} | {f_fail} | {obs(f_fail)} |
| - | Implantação e integração frontend↔backend | Implantação / integração | `./scripts/smoke_test.sh` | - | - | Não executado |

## Falhas encontradas e correções
- Correção após avaliação do professor: o frontend em Streamlit só montava a tela via JavaScript, e o HTML
  inicial não continha campo de texto, botão nem exemplos. Foi substituído por uma página HTML/JS servida
  pelo nginx, com os elementos presentes no HTML puro e comunicação via proxy `/api`.

## Limitações / testes pendentes
- Sem testes de ponta a ponta com navegador real (ex.: Playwright).
- Análises léxica, sintática e semântica ainda não implementadas (etapas seguintes).
"""
Path("docs").mkdir(exist_ok=True)
Path("docs/registro-de-testes.md").write_text(texto, encoding="utf-8")
print(f"Backend:  {b_ok} aprovados, {b_fail} reprovados")
print(f"Frontend: {f_ok} aprovados, {f_fail} reprovados")
print("Arquivo docs/registro-de-testes.md atualizado.")
