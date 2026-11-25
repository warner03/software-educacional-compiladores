# Visualizador Educacional de Compiladores — Mini-C

Software web educacional para estudar as fases de um compilador. **Trabalho 4: análise sintática e AST implementadas**, integradas ao scanner, à API e à interface das etapas anteriores.

## O que funciona

- Editor e oito exemplos, incluindo precedência e erros propositais.
- Scanner da Etapa 3 preservado: tokens, posições, contagens, mensagens e recuperação.
- Parser manual por descida recursiva: declarações `int`/`float`, atribuições, expressões aritméticas/relacionais, sinais unários, blocos e `if/else` com chaves obrigatórias.
- AST hierárquica com nós expansíveis, regras explicadas, localização do nó no código e download em JSON.
- Diagnósticos sintáticos com encontrado, esperado, linha/coluna e recuperação em `;` ou `}`.
- Estados léxico e sintático separados; parser não é executado diante de erro léxico.
- Testes de parser, API, interface, regressão, integração Docker e navegador real.

A análise semântica ficará para a **Etapa 5**. `x = 1;` ainda é sintaticamente válido, sem verificar declaração ou tipos. A aplicação não executa programas. A navegação explora tokens e a AST prontos; não simula passo a passo a construção da árvore.

## Executar no seu computador

Requisitos: Docker Engine/Desktop com Compose v2. Sem banco de dados, contas ou segredos obrigatórios.

```bash
docker compose up --build -d --wait
```

Abra **http://localhost:8501**. Documentação da API: **http://localhost:8000/docs**. Para encerrar:

```bash
docker compose down
```

Se 8000 já estiver ocupada, configure a porta externa da API, por exemplo no Bash:

```bash
COMPILADORES_API_PORT=18000 docker compose up --build -d --wait
```

Nesse caso, a documentação direta da API fica em `http://localhost:18000/docs`; a interface continua em 8501. O nginx encaminha `/api/analisar` ao backend interno na porta 8000. Em rede com proxy TLS próprio, veja [execução na nuvem](docs/execucao-nuvem.md), sem desativar TLS.

As imagens copiam o código durante o build. **Após editar arquivos, reconstrua as imagens**, inclusive a de testes. Os serviços não usam bind mounts do checkout.

## Usar e demonstrar

1. Escolha um exemplo ou escreva Mini-C e clique em **Analisar código**.
2. Confira separadamente os resultados léxico e sintático.
3. Use **Token anterior** e **Próximo token** para localizar lexemas e compare a tabela de tokens.
4. Na AST, abra os nós; **Expandir tudo** e **Recolher tudo** controlam a árvore. Enter/Espaço também abre um resumo focado.
5. Use **Localizar** em um nó para destacar sua construção no código. **Destacar token atual** retoma o destaque individual.
6. Use **Baixar AST em JSON** para guardar a estrutura. Corrija os erros e analise novamente quando necessário.

Em `int resultado = 10 + 5 * 2;`, a AST contém a adição com a multiplicação no ramo direito. Em `20 - 5 - 3`, organiza `(20 - 5) - 3`. Parênteses alteram a estrutura: `(10 + 5) * 2` tem multiplicação na raiz da expressão.

Em `int x = ;`, os tokens continuam disponíveis, mas há erro sintático e AST nula. Em `@ int x;`, há erro léxico e o parser não é executado. Veja o [roteiro de demonstração](docs/demonstracao-etapa4.md).

## Linguagem, parser e AST

[Gramática formal e estratégia](docs/gramatica.md) · [Esquema da AST](docs/ast.md) · [Especificação léxica](docs/escopo-lexico.md)

| Aspecto | Recorte efetivo |
|---|---|
| Reservadas | `int`, `float`, `if`, `else`, sensíveis a maiúsculas |
| Identificadores | `[A-Za-z_][A-Za-z0-9_]*` |
| Números | Inteiros `[0-9]+` e reais `[0-9]+\.[0-9]+`; lexemas preservados |
| Operadores | `+ - * / = == != < > <= >=`; `=` somente em declaração/atribuição |
| Declarações | Uma variável por instrução, inicialização opcional, `;` obrigatório |
| Controle | Blocos, `if` e `else` opcional, sempre com chaves |
| Comentários | `//` e `/* ... */`, sem aninhamento; ignorados na AST |
| Fora do escopo | Funções, laços, vetores, strings, operadores lógicos, incremento, atribuição composta, declarações múltiplas |

A vírgula é reconhecida pelo scanner, mas rejeitada pelo parser. Programa precisa de ao menos um item; comentários sozinhos geram diagnóstico de programa vazio; `{}` é válido. Tokens e nós usam linha/coluna a partir de 1; tab conta uma coluna, CRLF/CR são normalizados para LF e Unicode conta por ponto de código. O fim de um nó é exclusivo.

O [parser Python](backend/app/parser.py) recebe os tokens originais do [scanner](backend/app/scanner.py), sem reimplementá-lo e sem nova dependência. Funções reconhecem construções; níveis de expressão controlam precedência e associação. A AST simplifica as construções e omite pontuação e regras intermediárias. Uma árvore de derivação conteria esses detalhes e não é exibida.

Limites: **10.000 caracteres, 64 níveis estruturais simultâneos, 2.000 nós construídos e altura 128 da AST**. Excesso de caracteres gera HTTP 400; excesso estrutural gera diagnóstico controlado, com tokens preservados e AST nula. A recuperação pode descartar comandos e não garante encontrar todos os erros.

## Comunicação

`POST /api/analisar` pelo nginx, ou `POST /analisar` diretamente na API:

```json
{"codigo": "int numero = 10;"}
```

A resposta preserva **todos os campos da Etapa 3**: `recebido`, `mensagem`, `total_caracteres`, `total_linhas`, `sucesso`, `tokens` e `erros`. Acrescenta `sintatica`:

| `sintatica.estado` | `sintatica.sucesso` | AST e diagnósticos |
|---|---|---|
| `sucesso` | `true` | AST completa e `erros: []` |
| `erro` | `false` | `ast: null` e erros sintáticos |
| `nao_executada` | `null` | `motivo: "erros_lexicos"`, AST nula, lista sintática vazia |

**O campo superior `sucesso` continua indicando somente o resultado léxico**, por compatibilidade. Confira `sintatica.sucesso` para a sintaxe. Erros no programa retornam HTTP 200 porque a análise foi processada; entrada inválida retorna 400; falha interna, 500 com mensagem genérica. Saúde: `GET /saude`. Veja o [contrato completo com exemplos](docs/contrato-api.md).

## Testes reproduzíveis

```bash
docker compose build backend frontend testes-frontend
docker compose run --rm backend pytest -q
docker compose run --rm testes-frontend
bash scripts/smoke_test.sh
```

O smoke sobe os serviços, valida HTML e o caminho real nginx → API → scanner → parser e encerra os serviços. Para mantê-los: `KEEP_RUNNING=1 bash scripts/smoke_test.sh`.

Registro automático das suítes e integração:

```bash
python3 scripts/registrar_testes.py --integracao
```

Navegador real é uma dependência opcional de avaliação, separada da aplicação:

```bash
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements-e2e.txt
.venv/bin/python -m playwright install chromium
# Em Linux, instalar também as bibliotecas do navegador quando necessário:
# .venv/bin/python -m playwright install --with-deps chromium
docker compose up -d --wait
.venv/bin/python scripts/teste_navegador.py --capturas /tmp/demonstracao-etapa4
# Ou navegador existente: --chromium /caminho/do/chromium
```

Para executar e registrar tudo:

```bash
.venv/bin/python scripts/registrar_testes.py --integracao --navegador
```

O navegador testa os oito exemplos, edição, tokens, precedência, seleção de nós, expansão/recolhimento, download, erros, recuperação, limites, teclado e largura em desktop e viewport móvel de 390px. Usa backend real, sem mocks. Não substitui um aparelho físico ou auditoria de acessibilidade.

Os [resultados e comandos executados](docs/registro-de-testes.md) distinguem aprovações, falhas e pendências. Históricos: [Etapa 2](docs/registro-de-testes-etapa2.md) e [Etapa 3](docs/registro-de-testes-etapa3.md).

## Relação com o artigo

A [Tarefa 4 teórica](docs/etapa4/README.md) é um **registro histórico do plano de 18/11/2026**: mantém sua matriz de literatura e resultados então pendentes. A implementação atual está descrita em [Trabalho 4](docs/trabalho4/README.md), com [decisões e mudanças](docs/trabalho4/decisoes.md), [fluxograma atualizado](docs/trabalho4/fluxograma.png) e [rastreabilidade dos requisitos](docs/trabalho4/entrega.md).

Os 33 casos aplicáveis e os três oráculos definidos antes do parser foram reutilizados sem reescrever os esperados. Os três casos semânticos só confirmam aceitação sintática nesta etapa. Não houve estudo com participantes ou medição de aprendizagem; os recursos implementados não demonstram por si só superioridade ou novidade na literatura.

## Estrutura

- `backend/app/`: API, validação, scanner e parser.
- `backend/tests/`: testes e cópias congeladas dos oráculos para execução no Docker.
- `frontend/`: HTML/CSS/JavaScript, nginx e testes Node/jsdom.
- `tests/planejamento/`: plano acadêmico original, sem resultados reescritos.
- `scripts/`: smoke, registro de testes e E2E Playwright opcional.
- `docs/`: gramática, AST, contrato, demonstração e registros.

Semântica, tabela de símbolos, checagem de tipos, execução do programa e geração de código permanecem como etapas futuras.
