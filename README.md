# Visualizador Educacional de Compiladores

Software educacional interativo para o ensino de Compiladores, voltado a demonstrar visualmente as etapas de análise léxica e sintática.

## 1. Escopo

**Linguagem analisada: Mini-C**, um subconjunto da linguagem C.

- **Tipos:** `int`, `float`
- **Operadores:** `+`, `-`, `*`, `/` e atribuição `=`
- **Controle:** `if` / `else`

**Justificativa:** C é amplamente conhecida no meio acadêmico e tem tipagem estática forte; limitar o escopo a um subconjunto mantém o foco na transição entre a teoria de autômatos/gramáticas e a prática.

## 2. Estado atual (Etapa 2)

Já implementado: interface web, entrada/edição de código, exemplos, comunicação real frontend↔backend, validações e testes automatizados.

**Ainda não implementado:** análise léxica, sintática e semântica. O backend apenas recebe e valida o código.

## 3. Tecnologias e estrutura

- `backend/` — API em Python (FastAPI): `app/main.py` (rotas), `app/validation.py` (validações), `tests/` (pytest).
- `frontend/` — página HTML + CSS + JavaScript puro, servida pelo nginx:
  - `index.html` (tela e exemplos), `style.css`, `app.js` (validação, comunicação e comportamento da tela);
  - `nginx.conf` (serve a página e repassa `/api/` ao backend);
  - `tests/` (Node.js + jsdom).
- `docker-compose.yml` — orquestração, com healthchecks.
- `scripts/` — `smoke_test.sh` (teste de implantação) e `registrar_testes.py` (gera o registro de testes).
- `docs/` — contrato da API e registro de testes.

## 4. Como executar

```bash
docker compose up --build -d    # iniciar
docker compose down             # encerrar
```

Acesse a interface em **http://localhost:8501**. A documentação interativa da API fica em http://localhost:8000/docs.

O navegador carrega a página do nginx e envia o código para `/api/analisar` (mesma origem). O nginx repassa a chamada ao backend por `http://backend:8000` na rede interna do Compose.

## 5. Como usar

1. Escolha um exemplo na lista (o código aparece na área de entrada) ou escreva/cole seu próprio programa.
2. Edite à vontade — o sistema não presume que o código seja válido.
3. Clique em **Analisar código** e veja a resposta em **Resultados**.

### Exemplos disponíveis

| Exemplo | Construção demonstrada |
|---|---|
| 1 - Declaração e inicialização | `int` com atribuição |
| 2 - Operação aritmética | expressão com `+` |
| 3 - Estrutura condicional | `if` com bloco |
| 4 - Condicional com else e float | `float`, comparação e `if/else` |

## 6. Comunicação frontend ↔ backend

`POST /api/analisar` (proxy) → `POST /analisar` (backend) com `{"codigo": "..."}`. Respostas, códigos HTTP e erros estão em [`docs/contrato-api.md`](docs/contrato-api.md).

### Validações e mensagens

| Situação | Onde é tratada |
|---|---|
| Entrada vazia | frontend e backend |
| Entrada só com espaços | frontend e backend |
| Requisição inválida (JSON ruim, campo ausente, tipo errado) | backend (HTTP 400) |
| Falha de comunicação (servidor fora do ar, timeout, 502/503/504) | frontend |
| Erro inesperado | backend (HTTP 500, mensagem genérica) e frontend |

## 7. Testes

```bash
docker compose run --rm backend pytest -v        # validações e endpoints (pytest)
docker compose run --rm testes-frontend          # lógica, exemplos e interface (Node + jsdom)
./scripts/smoke_test.sh                          # implantação, HTML da interface e comunicação via proxy
python3 scripts/registrar_testes.py              # roda os testes e atualiza docs/registro-de-testes.md
```

Os resultados executados ficam em [`docs/registro-de-testes.md`](docs/registro-de-testes.md).

## 8. Limitações conhecidas

- Sem análises léxica/sintática/semântica (próximas etapas).
- Editor simples (sem realce de sintaxe nem numeração de linhas).
- Limite de 10.000 caracteres por código.
- Sem testes de ponta a ponta com navegador real.
