# Visualizador Educacional de Compiladores — Mini-C

Software web educacional para estudar as fases de um compilador. **Etapa 3: análise léxica funcional**, integrada à interface e à API. A base da Etapa 2 foi ampliada, mantendo exemplos, edição, validações e comunicação via nginx.

## O que já funciona

- Edição de código e seis exemplos selecionáveis, incluindo comentários e erros propositais.
- Scanner manual em Python: tokens com tipo, lexema, linha e coluna; erros acumulados e recuperação da leitura.
- Tabela de tokens, contagem por categoria, código colorido e navegação por tokens reconhecidos.
- Erros didáticos com localização, sem stack traces na interface.
- Guia inicial na própria página, disposição em uma coluna em telas pequenas e controles por teclado.
- Testes unitários, de API, interface, integração e navegador real.

**Ainda não implementado:** parser/análise sintática (Etapa 4), AST e análise semântica (etapas seguintes). Um texto sem erros léxicos pode continuar sintaticamente errado: `int = ;` é tokenizado normalmente. A navegação visual percorre o resultado do scanner, não anima cada estado interno do algoritmo.

## Executar com Docker

Requisitos: Docker Engine/Desktop com Compose v2. Não há banco de dados, segredos, variáveis obrigatórias da aplicação ou novas portas nesta etapa.

```bash
docker compose up --build -d --wait
# Encerrar:
docker compose down
```

No seu computador, abra a interface na porta **8501** e a documentação da API na porta **8000**, caminho `/docs`. O nginx recebe `/api/analisar` e encaminha para `/analisar` no FastAPI. O endpoint `GET /saude` informa a saúde do backend.

Se a máquina usa proxy HTTPS com certificado próprio, siga [execução na nuvem](docs/execucao-nuvem.md), que preserva a verificação TLS. Esse ajuste é de infraestrutura, não uma exigência para quem usa Docker em rede comum.

As imagens copiam o código no build. **Depois de editar arquivos, reconstrua as imagens**, inclusive a imagem de testes: os contêineres não usam bind mounts do checkout.

## Usar e demonstrar

1. Selecione um exemplo ou escreva Mini-C no editor.
2. Clique em **Analisar código**.
3. Compare cada lexema com seu tipo e posição na tabela. Linha e coluna começam em 1.
4. Use **Token anterior** e **Próximo token** para localizar o token no código colorido.
5. Se houver erro, confira a localização e o trecho, corrija e analise novamente. Tokens válidos depois do erro continuam sendo mostrados quando a recuperação é possível.

Exemplo: `int numero = 10;` produz cinco tokens: `int`, `numero`, `=`, `10`, `;`.

Exemplo com erros: `int x=12abc;` seguido de `@ float y=7.5;` em outra linha informa dois problemas, preservando o token real `7.5` e os demais tokens válidos.

Veja o [roteiro de demonstração](docs/demonstracao-etapa3.md).

## Subconjunto léxico

| Categoria | Regra e exemplos |
|---|---|
| Palavras reservadas | `int`, `float`, `if`, `else` (sensíveis a maiúsculas) |
| Identificadores | `[A-Za-z_][A-Za-z0-9_]*`: `numero`, `_x1`, `media2` |
| Literais inteiros | `[0-9]+`: `0`, `10`, `001` (sem interpretação octal nesta etapa) |
| Literais reais | `[0-9]+\.[0-9]+`: `7.5`, `0.0`; ponto obrigatório e dígitos dos dois lados |
| Operadores aritméticos | `+`, `-`, `*`, `/` |
| Atribuição | `=` |
| Operadores relacionais | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| Delimitadores | `(`, `)`, `{`, `}`, `;`, `,` |
| Comentários | `//` até o fim da linha e `/* ... */`, sem aninhamento |
| Espaços | Espaço ASCII, tab, LF, CR/CRLF, tab vertical e form feed; não produzem tokens |
| Fora do recorte | Strings, literais de caractere, expoentes, hexadecimal, operadores lógicos, incremento, atribuições compostas, colchetes, diretivas e símbolos não listados |
| Erros | `ERRO_LEXICO`, com trecho, mensagem, linha e coluna; a leitura continua quando possível |

Veja [especificação e recuperação do scanner](docs/escopo-lexico.md), com decisões sobre números malformados, posições e funcionalidades fora do escopo. Outros nomes, como `while` e `return`, são identificadores nesta etapa; o scanner não valida construções sintáticas. O projeto permanece em Mini-C: não se afirma que uma linguagem inspirada em C seja inédita na literatura.

## Implementação e comunicação

O scanner em [backend/app/scanner.py](backend/app/scanner.py) percorre o texto manualmente e agrupa lexemas. Não adiciona dependências de produção. A implementação em Python aproveita o backend existente e mantém explícitas as decisões didáticas de leitura, posição e recuperação; expressões regulares apenas validam o formato final dos números.

`POST /api/analisar` pelo nginx (ou `POST /analisar` diretamente na API):

```json
{"codigo": "int numero = 10;"}
```

Resposta HTTP 200:

```json
{
  "recebido": true,
  "mensagem": "Análise léxica concluída sem erros.",
  "total_caracteres": 16,
  "total_linhas": 1,
  "sucesso": true,
  "tokens": [
    {"tipo": "PALAVRA_RESERVADA", "lexema": "int", "linha": 1, "coluna": 1},
    {"tipo": "IDENTIFICADOR", "lexema": "numero", "linha": 1, "coluna": 5},
    {"tipo": "OPERADOR", "lexema": "=", "linha": 1, "coluna": 12},
    {"tipo": "LITERAL_INTEIRO", "lexema": "10", "linha": 1, "coluna": 14},
    {"tipo": "DELIMITADOR", "lexema": ";", "linha": 1, "coluna": 16}
  ],
  "erros": []
}
```

Com erros léxicos, a API retorna HTTP 200 com `recebido: true`, `sucesso: false`, tokens recuperados e `erros`. Isso indica que a solicitação foi processada, embora o código tenha erros. Requisições ou entradas inválidas continuam com HTTP 400; falhas internas, HTTP 500 com mensagem genérica. Consulte o [contrato completo](docs/contrato-api.md).

## Testes

```bash
# Sempre reconstruir após alterações; o perfil de testes pode ser construído explicitamente:
docker compose build backend frontend testes-frontend

docker compose run --rm backend pytest -v
docker compose run --rm testes-frontend
bash scripts/smoke_test.sh
```

O smoke inicia os serviços, verifica HTML e comunicação real via proxy, tokens/posições, erros/recuperação, comentários e rejeição de entrada vazia, e encerra os serviços ao terminar. Use `KEEP_RUNNING=1 bash scripts/smoke_test.sh` para mantê-los ativos.

Para gerar o registro com resultados das suítes e da integração:

```bash
python3 scripts/registrar_testes.py --integracao
```

Navegador real é um teste adicional opcional, separado das dependências da aplicação:

```bash
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements-e2e.txt
.venv/bin/python -m playwright install chromium
# Em Linux, as bibliotecas do navegador também devem estar instaladas;
# Playwright documenta `playwright install --with-deps chromium` quando necessário.
docker compose up -d --wait
.venv/bin/python scripts/teste_navegador.py
# Alternativa: --chromium /caminho/do/chromium já instalado.
```

Esse teste usa o backend real, percorre os seis exemplos e verifica navegação por tokens, erros, comentários, edição, validações, teclado e largura em desktop e viewport móvel de 390px. Não substitui teste em dispositivo físico ou auditoria completa de acessibilidade.

Registro completo, incluindo navegador instalado no ambiente:

```bash
.venv/bin/python scripts/registrar_testes.py --integracao --navegador
```

Resultados executados e limitações ficam em [docs/registro-de-testes.md](docs/registro-de-testes.md); o [histórico da Etapa 2](docs/registro-de-testes-etapa2.md) foi preservado.

## Estrutura

- `backend/app/main.py`: API ativa; `scanner.py`: análise léxica; `validation.py`: validação da entrada.
- `backend/tests/`: scanner, endpoints e regressão.
- `frontend/`: HTML/CSS/JavaScript e nginx; `tests/`: lógica e interface jsdom.
- `docker-compose.yml`: serviços e healthchecks; `compose.cloud.yaml`: override opcional de CA para builds.
- `scripts/`: smoke, registro de testes e navegador real opcional.
- `docs/`: escopo léxico, contrato, demonstração e registros.

## Limitações e próximas etapas

Máximo de 10.000 caracteres por entrada. Identificadores usam ASCII; acentos são permitidos dentro de comentários, não em nomes. Strings e caracteres entre aspas são reportados como fora do subconjunto. Números malformados são agrupados em um erro; comentário de bloco sem fechamento consome o restante da entrada, pois não há ponto seguro de recuperação. Não há leitura de arquivos, execução do programa, geração de código, tabela de símbolos ou AST.

O guia, os diagnósticos e a navegação visual apoiam o objetivo educacional, mas ainda não foram avaliados com estudantes. Não se declara ganho de aprendizagem nem superioridade sobre ferramentas relacionadas. A Etapa 4 deverá definir a gramática e implementar o parser sobre os tokens desta etapa.
