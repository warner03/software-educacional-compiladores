# Roteiro de demonstração — Etapa 3 prática

## Preparar

Execute `docker compose up --build -d --wait`. No ambiente com proxy, aplique antes as configurações de `execucao-nuvem.md`. Abra a interface na porta 8501 do seu computador. Não são necessários login nem banco de dados.

## 1. Categorias e posição

Selecione o exemplo 1, “Declaração e inicialização”, e clique em **Analisar código**. Para `int numero = 10;`, mostre:

- Os cinco tokens e as categorias palavra reservada, identificador, operador, literal inteiro e delimitador.
- O lexema `numero` na linha 1, coluna 5.
- A diferença entre categoria (tipo de unidade) e lexema (texto reconhecido).
- Contagem por categoria, cores e os comandos de token anterior/próximo. O destaque representa a sequência já reconhecida, não a execução caractere a caractere do scanner.

## 2. Condicional, real e operadores compostos

Selecione o exemplo 4. Mostre `float`, `if`, `else`, `7.5`, chaves e o operador `>=` como uma unidade. Explique que a análise não decide se a condição ou a estrutura estão corretas.

## 3. Comentários

Selecione o exemplo 5. Os comentários de linha e bloco não geram tokens, mas suas posições continuam contando. O identificador `_contador` é válido. Confira a coluna do próximo token após o comentário.

## 4. Erros e recuperação

Selecione o exemplo 6. O sistema informa `12abc` (linha 1, coluna 14) e `@` (linha 2, coluna 1), sem interromper a página. Mostre que `7.5` e a atribuição da última linha continuam na tabela. Corrija `12abc` para `12` e remova `@`; analise novamente e confira o sucesso.

Outro caso: `int x; /* comentário aberto`. Há um erro com a posição de início do comentário; o restante é consumido porque não existe fechamento seguro.

## 5. Separação entre scanner e parser

Digite `int = ;`: o scanner retorna sucesso e três tokens porque todos os lexemas pertencem ao recorte. Isso **não** significa que a declaração esteja correta. O parser da Etapa 4 será responsável pela estrutura; a semântica virá depois.

## 6. Regressão e telas menores

Limpe o editor e analise: a mensagem de entrada vazia continua funcionando. Troque de exemplo e edite o texto. Os resultados antigos são limpos para não serem associados ao código novo. Mostre o guia “Primeiros passos e subconjunto Mini-C”.

Em tela estreita, os painéis ficam em coluna única; código e tabela podem ser rolados na própria região. Navegue por teclado entre exemplos, editor e botão. O teste automatizado também usa viewport de 390px com toque simulado; isso não é validação em celular físico nem auditoria completa de acessibilidade.

## Evidências automatizadas

- `docker compose run --rm backend pytest -v`
- `docker compose run --rm testes-frontend`
- `bash scripts/smoke_test.sh` (encerra os serviços; reinicie para demonstrar)
- `python3 scripts/teste_navegador.py` (Playwright opcional, instruções no README)

Os números e a data pertencem ao registro em `registro-de-testes.md`. Não apresentar testes técnicos como estudo de aprendizagem com estudantes.
