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

- `backend/` — API em Python (FastAPI): `app/main.py` (rotas), `app/validation.py` (validações), `tests/`.
- `frontend/` — interface em Python (Streamlit): `app.py` (tela), `api_client.py` (comunicação), `examples.py` (exemplos), `tests/`.
- `docker-compose.yml` — orquestração, com healthchecks.
- `scripts/smoke_test.sh` — teste de implantação.
- `docs/` — contrato da API e registro de testes.

## 4. Como executar

```bash
docker compose up --build -d    # iniciar
docker compose down             # encerrar
```

Acesse a interface em **http://localhost:8501**. A documentação interativa da API fica em http://localhost:8000/docs.

O navegador acessa apenas o frontend. O Streamlit (dentro do contêiner) chama o backend por `http://backend:8000`, definido na variável `BACKEND_URL` do Compose.

## 5. Como usar

1. Escolha um exemplo e clique em **Carregar exemplo** (ou escreva/cole seu próprio código).
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

`POST /analisar` com `{"codigo": "..."}`. Respostas, códigos HTTP e erros estão em [`docs/contrato-api.md`](docs/contrato-api.md).

## 7. Testes

```bash
docker compose run --rm backend pytest -v     # validações e endpoints
docker compose run --rm frontend pytest -v    # cliente HTTP, exemplos e interface (Streamlit AppTest)
./scripts/smoke_test.sh                       # implantação + comunicação entre contêineres
```

Os resultados executados ficam em [`docs/registro-de-testes.md`](docs/registro-de-testes.md).

## 8. Limitações conhecidas

- Sem análises léxica/sintática/semântica (próximas etapas).
- Editor simples (sem realce de sintaxe nem numeração de linhas).
- Limite de 10.000 caracteres por código.
- Sem testes de ponta a ponta com navegador real.
