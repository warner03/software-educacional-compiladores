# Contrato da API (Etapa 2)

## GET /saude
`200` → `{"status": "ok"}`

## POST /analisar
Requisição: `{"codigo": "int numero = 10;"}`

| Situação | HTTP | Corpo |
|---|---|---|
| Código recebido | 200 | `{"recebido": true, "mensagem": "Código recebido com sucesso.", "total_caracteres": N, "total_linhas": M}` |
| `codigo` vazio / só espaços / tipo errado / acima de 10.000 caracteres | 400 | `{"recebido": false, "erro": "entrada_invalida", "mensagem": "..."}` |
| JSON inválido, corpo não-objeto ou campo `codigo` ausente | 400 | `{"recebido": false, "erro": "requisicao_invalida", "mensagem": "..."}` |
| Erro inesperado | 500 | `{"recebido": false, "erro": "erro_interno", "mensagem": "Ocorreu um erro inesperado no servidor. Tente novamente."}` |

O backend **não** executa análise léxica, sintática ou semântica nesta etapa.
