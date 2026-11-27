# Visualizador Educacional de Compiladores — Mini-C

Software web educacional para estudar as fases de um compilador. **Trabalho 5: análise semântica e tabela de símbolos implementadas**, preservando tokens e AST das etapas anteriores. A interface também oferece modos **Sem cores**, com padrões/rótulos, e **Alto contraste**, como apoio ao daltonismo.

## O que funciona

- Editor e 14 exemplos editáveis, incluindo casos válidos e erros intencionais das três fases.
- Scanner e parser preservados: tipos/lexemas/posições, precedência, AST navegável, seleção no fonte e exportação JSON.
- Verificação de declaração antes do uso, redeclaração, escopos, sombreamento, tipos, condições e inicialização definida.
- Tabela de símbolos filtrável por escopo, declaração e referências selecionáveis, com destaque no código e ligação à AST.
- Diagnósticos separados por fase, com localização, regra semântica e sugestão de correção.
- Modos visuais com rótulos, padrões, contornos e foco visível; preferência mantida ao recarregar quando o navegador permite.
- Testes técnicos, integração Docker, navegador real, contraste e inspeções sob simulação de visão de cores.

Os recursos de acessibilidade estão implementados e tecnicamente verificados; ainda não houve avaliação com pessoas daltônicas. A [Tarefa 5 teórica](docs/etapa5/README.md) permanece como registro da preparação anterior à implementação e aguarda revisão do artigo/matriz e simplificação do formulário após esta entrega prática.

## Abrir no seu computador

Requisitos: Docker Engine/Desktop com Compose v2. Na pasta onde está `docker-compose.yml`, abra o terminal (em alguns Linux, **Abrir no Console**) e execute:

```bash
docker compose up --build -d --wait
```

Abra **http://localhost:8501**. A documentação direta da API fica em **http://localhost:8000/docs**. Para encerrar:

```bash
docker compose down
```

Após atualizar arquivos, reconstrua as imagens: o código é copiado no build, sem bind mounts. Se estiver usando uma pasta nova e a versão antiga ainda estiver ativa, encerre os serviços na pasta antiga antes de iniciar a nova.

Se 8000 estiver ocupada, no Bash:

```bash
COMPILADORES_API_PORT=18000 docker compose up --build -d --wait
```

Nesse caso, API em `http://localhost:18000/docs`; interface continua em 8501. O proxy interno permanece em 8000. Ambientes com CA própria: [execução na nuvem](docs/execucao-nuvem.md), com TLS verificado. Não há banco, conta ou segredo obrigatório para o aplicativo.

## Explorar e demonstrar

1. Escolha um exemplo e clique em **Analisar código**. Confira separadamente Léxica, Sintática e Semântica.
2. Compare os tokens com o fonte e use a navegação de tokens.
3. Expanda a AST e selecione **Localizar**. Use **Ver trecho destacado no código** para ir ao resultado.
4. Na tabela de símbolos, filtre escopos e localize declarações/referências. A construção relacionada também recebe contorno na AST.
5. No seletor inicial, escolha **Sem cores** ou **Alto contraste**. A análise e a seleção permanecem; a legenda explica os padrões.
6. Corrija uma entrada com erro e analise novamente. **Destacar token atual** retoma a navegação léxica.

Exemplo 9: `int x=10; total=x+5;` produz erro semântico por `total` não declarado. Tokens e AST continuam disponíveis. Exemplo 10 mostra duas variáveis `x` em escopos diferentes. Exemplo 11 rejeita `float` em variável `int`; o 12 mostra leitura não inicializada; o 13 garante inicialização nos dois ramos; o 14 exige comparação na condição.

[Roteiro do Trabalho 5](docs/demonstracao-etapa5.md) · [Recursos e evidências](docs/trabalho5/README.md)

## Linguagem e política semântica

[Gramática](docs/gramatica.md) · [Scanner](docs/escopo-lexico.md) · [AST](docs/ast.md) · [Semântica e símbolos](docs/semantica.md) · [Acessibilidade](docs/acessibilidade.md)

| Aspecto | Recorte |
|---|---|
| Reservadas e tipos declarados | `int`, `float`, `if`, `else`; tipos `int`/`float` |
| Identificadores/números | ASCII `[A-Za-z_][A-Za-z0-9_]*`; inteiros e reais decimais, lexemas preservados |
| Construções | Uma variável por declaração, inicialização opcional, atribuição, expressões, blocos, `if/else` com chaves |
| Tipos de expressão | Aritmética numérica; promoção `int` → `float`; comparações produzem `bool` interno |
| Condições | `if` exige `bool`, por exemplo `x != 0`; `if(x)` numérico é rejeitado semanticamente |
| Visibilidade | Declaração antes do uso, sem redeclaração no mesmo escopo, sombreamento permitido em bloco interno |
| Inicialização | Exigida na leitura; após condicional, somente o que é garantido em ambos os caminhos |
| Fora do escopo | Funções, laços, arrays, strings, operadores lógicos, casts, execução e geração de código |

`bool` não é novo tipo de variável na gramática. Um `int` não recebe `float` nem `bool` implicitamente. Divisão de dois inteiros tem tipo inteiro; valores não são calculados. Uma declaração sem leitura pode ser válida sem inicialização. O campo da tabela é a garantia ao fim do escopo, não valor em execução.

Comentários `//` e `/* ... */` são ignorados. A vírgula é tokenizada mas não aceita em declaração múltipla. Programa contém ao menos um item: `{}` é válido, comentários sozinhos não. Posições começam em 1, fim de intervalo é exclusivo, CRLF/CR viram LF, tab conta uma coluna e Unicode por ponto de código.

Limites herdados: **10.000 caracteres, 64 níveis estruturais, 2.000 nós construídos e altura 128 da AST**. Excesso de caracteres retorna 400; limite estrutural, diagnóstico sintático controlado. A recuperação sintática pode descartar construções e não garante encontrar todos os erros.

## Comunicação

`POST /api/analisar` no nginx ou `POST /analisar` no FastAPI recebe:

```json
{"codigo":"int numero = 10;"}
```

Campos existentes preservados: `recebido`, `mensagem`, `total_caracteres`, `total_linhas`, `sucesso`, `tokens`, `erros` e `sintatica`. **O `sucesso` superior continua exclusivamente léxico.** O novo objeto `semantica` inclui:

| Campo de `semantica` | Conteúdo |
|---|---|
| `estado`, `sucesso` | Estado da fase e resultado booleano ou `null` |
| `tabelaSimbolos` | Declarações reconhecidas, com tipos, escopos, posições e referências |
| `escopos` | Global e blocos, com pai e intervalo |
| `erros` | Diagnósticos com regra, posição, ligação à AST e sugestão |

Erros semânticos têm estado `erro`, sucesso `false`, diagnósticos e tabela das declarações reconhecidas. A AST sintática permanece disponível. Erro léxico ou sintático bloqueia a semântica: estado `nao_executada`, sucesso `null`, causa explícita e listas vazias.

Análises processadas, inclusive com violações da linguagem, retornam HTTP 200. Entrada inválida retorna 400; falha inesperada, 500 com mensagem genérica. Saúde: `GET /saude`. [Contrato com exemplos reais](docs/contrato-api.md).

## Testar e registrar

```bash
docker compose build backend frontend testes-frontend
docker compose run --rm backend pytest -q
docker compose run --rm testes-frontend
bash scripts/smoke_test.sh
```

O smoke inicia os serviços, verifica o fluxo real e os encerra. Para mantê-los: `KEEP_RUNNING=1 bash scripts/smoke_test.sh`. Para executar os 30 casos semânticos com esperados congelados via API real, com serviços ativos:

```bash
python3 scripts/avaliar_semantica.py --saida /tmp/mini-c-casos-semanticos
```

Navegador é dependência opcional de avaliação:

```bash
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements-e2e.txt
.venv/bin/python -m playwright install chromium
# Em Linux, instalar bibliotecas do navegador quando necessário:
# .venv/bin/python -m playwright install --with-deps chromium
docker compose up -d --wait
.venv/bin/python scripts/teste_navegador.py --capturas /tmp/demonstracao-etapa5
```

Ou informe `--chromium /caminho/do/chromium`. Para executar e registrar tudo:

```bash
.venv/bin/python scripts/registrar_testes.py --integracao --casos --navegador
```

O navegador usa o backend real em desktop e viewport móvel. Verifica símbolos, seleções, diagnósticos, modos, contraste, persistência e teclado. As simulações de visão de cores não são estudo com pessoas ou certificação WCAG. O [registro](docs/registro-de-testes.md) contém resultados efetivos, comandos e limitações. Históricos: [Etapa 2](docs/registro-de-testes-etapa2.md), [Etapa 3](docs/registro-de-testes-etapa3.md), [Etapa 4](docs/registro-de-testes-etapa4.md).

## Depuração e continuidade

`docker compose logs --tail=80 backend frontend` exibe os serviços. O backend registra resumo das fases e contagens; a resposta/console do navegador mostra o contrato. Ao relatar erro, informe entrada mínima, ação, mensagem e versão; evite compartilhar informações pessoais. Nenhuma IA/Ollama é necessária para o aplicativo.

A [Tarefa 4](docs/etapa4/README.md) e a [preparação da Tarefa 5](docs/etapa5/README.md) ficam preservadas como registros anteriores. A documentação atual do [Trabalho 5](docs/trabalho5/README.md) registra decisões, fluxograma, casos e demonstração. A revisão do artigo/matriz e a simplificação do formulário vêm depois desta etapa prática. Não há respostas humanas inventadas ou ganho de aprendizagem comprovado.

A Etapa 6 ampliará a representação semântica e a experiência didática. A navegação atual percorre artefatos prontos; não simula os passos internos dos algoritmos. Acessibilidade é uma contribuição implementada a avaliar, com exclusividade perante a literatura ainda não demonstrada.
