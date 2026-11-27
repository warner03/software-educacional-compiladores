# Exportação da entrega acadêmica

Requer Pandoc, XeLaTeX com os pacotes do estilo, fontes DejaVu e Python com pypdf. Na raiz do projeto:

```bash
python3 docs/etapa5/editorial/gerar_entrega.py --saida /tmp/mini-c-tarefa5
```

Para acrescentar os textos integrais dos dois artigos obtidos em suas fontes oficiais, informe também `--artigo-a /caminho/pontes2019.pdf --artigo-b /caminho/veras2020.pdf`. O programa verifica a quantidade de páginas, cria capas e combina os anexos, preservando a paginação original. Os PDFs de terceiros não ficam no repositório público.

Saídas: artigo PDF/DOCX, formulário de uma página, guia dos colegas e Comece Aqui. O log registra falhas/avisos de exportação. As tabelas usam abreviações de cabeçalhos e alinhamento de valores para evitar sobreposição; a matriz fonte conserva os nomes completos. Esta é a versão ampliada da disciplina, não o modelo final de uma trilha do SBSC.

O artigo reutiliza as evidências técnicas do Trabalho 5 e não inventa coleta humana. Antes de uma entrega integral da Tarefa 5, incorporar respostas/observações reais conforme o protocolo.
