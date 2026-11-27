# Instrumento curto — versão 3.0

Seis perguntas: Q01/Q02 objetivas, L01–L03 de percepção e A01 aberta opcional. C01 registra aceite e M01 indica uso em dupla/individual. A versão 2 anterior ao Trabalho 5 está em `../historico/versao2/instrumentos/`; os dois instrumentos não devem ser misturados.

Use [formulario-texto.md](formulario-texto.md) para criar manualmente um Google Forms. O [gerador opcional](criar_formulario.gs) pode ser executado pelo autor na própria conta em https://script.google.com: cole o código, execute `criarFormularioMiniCTarefa5` e confira o endereço de edição no registro. Ele cria rascunho fechado, sem liberar respostas. Esse código foi verificado localmente; não foi executado no serviço Google.

Depois de revisar privacidade, campos e navegação do aceite, disponibilize o link de responder aos colegas. Nenhum formulário foi criado ou publicado por esta entrega. Não se solicita nome, e-mail, matrícula ou condição de saúde; não habilite login obrigatório, quiz ou resumo público.

- Para colegas: [guia sem gabarito](guia-para-colegas.md).
- Para o autor: [roteiro](roteiro-aplicacao.md) e [gabarito](gabarito-facilitador.md).
- Registro: `observacoes-cabecalho.csv`, sem sessões preenchidas.
- Respostas: `respostas-cabecalho.csv`, somente cabeçalho e zero registros.

Após a aplicação:

```bash
python3 analisar_respostas.py respostas-reais.csv --saida analise-respostas.json
```

O programa separa modos, calcula acertos por questão, frequências e mediana por item e conta comentários sem expô-los. N/A não entra no denominador do item. Sem respostas, não produz estatísticas. O CSV da versão antiga é rejeitado; use o analisador correspondente no histórico.

Quatro testes locais usam apenas dados sintéticos para verificar denominadores, mediana, exclusões, ausência de dados, privacidade e rejeição de versão incorreta. Esses dados não são resultados de participantes:

```bash
python3 -m unittest -v test_analise_instrumento.py
```

Não há escore SUS, nota global ou prova de ganho de aprendizagem. Os comentários exigem leitura humana para agrupar temas e remover identificadores.
