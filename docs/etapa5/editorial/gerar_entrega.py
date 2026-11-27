#!/usr/bin/env python3
"""Exporta documentos da disciplina; anexos de terceiros são opcionais e locais.

Requer pandoc, XeLaTeX, fontes DejaVu e pypdf. Não publica arquivos.
"""
import argparse
from pathlib import Path
import subprocess


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--saida', type=Path, required=True)
    p.add_argument('--artigo-a', type=Path)
    p.add_argument('--artigo-b', type=Path)
    args = p.parse_args()
    if bool(args.artigo_a) != bool(args.artigo_b):
        p.error('Forneça os dois anexos ou nenhum.')
    root = Path(__file__).resolve().parents[1]
    editorial = root / 'editorial'
    out = args.saida.resolve(); out.mkdir(parents=True, exist_ok=True)
    logs = []

    def export(source, name, title=None, docx=False):
        command = ['pandoc', str(source), '--resource-path', str(root), '--lua-filter', str(editorial / 'tabelas.lua')]
        if not docx:
            command += ['--pdf-engine=xelatex', '-H', str(editorial / 'estilo.tex'),
                        '-V', 'mainfont=DejaVu Serif', '-V', 'monofont=DejaVu Sans Mono',
                        '-V', 'geometry:margin=2.2cm', '-V', 'fontsize=11pt']
        if title:
            command += ['-M', 'title=' + title, '-M', 'lang=pt-BR']
        command += ['-o', str(out / name)]
        result = subprocess.run(command, capture_output=True, text=True)
        logs.append(name + '\n' + result.stdout + result.stderr)
        (out / 'exportacao.log').write_text('\n'.join(logs))
        if result.returncode:
            raise RuntimeError('Falha de exportação: ' + name + '. Consulte exportacao.log.')
        print(name, flush=True)

    export(root / 'tarefa5.md', 'tarefa5_warner_atualizada.pdf')
    export(root / 'tarefa5.md', 'tarefa5_warner_editavel.docx', docx=True)
    export(root / 'instrumentos/formulario-para-copiar.md', 'formulario_avaliacao_simples.pdf')
    export(root / 'instrumentos/guia-para-colegas.md', 'guia_para_colegas.pdf', 'Guia de uso — avaliação Mini-C')
    export(root / 'COMECE-AQUI.md', 'COMECE_AQUI.pdf')
    if args.artigo_a:
        from pypdf import PdfReader, PdfWriter
        covers = []
        for letter, title, authors, doi in [
            ('A', 'Avaliação de Ferramentas para Ensino de Programação para Crianças e Adolescentes', 'Pontes et al. (2019)', '10.5753/cbie.wie.2019.744'),
            ('B', 'Desenvolvimento e Avaliação da Usabilidade em Aplicativo Desktop para o Ensino da Programação Orientada a Objetos', 'Veras et al. (2020)', '10.5753/ctrle.2020.11395'),
        ]:
            cover = out / ('anexo_' + letter + '.md')
            cover.write_text(f'# Anexo {letter}\n\n## {title}\n\n{authors}.\n\nDOI: https://doi.org/{doi}\n\nTexto integral obtido no Portal de Publicações da Sociedade Brasileira de Computação. Anexo acadêmico solicitado na Tarefa 5; a paginação original é preservada.\n')
            name = 'capa_anexo_' + letter + '.pdf'
            export(cover, name)
            covers.append(out / name)
        for path, expected in [(args.artigo_a, 9), (args.artigo_b, 10)]:
            assert len(PdfReader(path).pages) == expected, 'Confira o PDF do artigo: ' + str(path)
        writer = PdfWriter()
        writer.append(out / 'tarefa5_warner_atualizada.pdf', outline_item='Tarefa 5 — Mini-C')
        for letter, cover, original in zip(['A', 'B'], covers, [args.artigo_a, args.artigo_b]):
            writer.append(cover, outline_item='Anexo ' + letter)
            writer.append(original, import_outline=False)
        writer.add_metadata({'/Title': 'Mini-C — Tarefa 5 com artigos de avaliação', '/Author': 'Warner Pereira Cardoso Júnior'})
        with (out / 'tarefa5_warner_com_artigos.pdf').open('wb') as f:
            writer.write(f)
        print('tarefa5_warner_com_artigos.pdf', flush=True)


if __name__ == '__main__':
    main()
