#!/usr/bin/env python3
"""E2E opcional com Playwright; serviços devem estar ativos. Não usa mocks.

Uso: python scripts/teste_navegador.py [--chromium /usr/bin/chromium]
     [--capturas /tmp/capturas]
"""
import argparse
import json
from pathlib import Path
from time import perf_counter

from playwright.sync_api import sync_playwright, expect


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:8501')
    parser.add_argument('--chromium', help='Executável Chromium local; padrão: o instalado pelo Playwright')
    parser.add_argument('--capturas', type=Path, help='Diretório opcional para imagens da demonstração')
    args = parser.parse_args()
    if args.capturas:
        args.capturas.mkdir(parents=True, exist_ok=True)
    total = 0
    with sync_playwright() as p:
        opcoes = {'headless': True}
        if args.chromium:
            opcoes['executable_path'] = args.chromium
        browser = p.chromium.launch(**opcoes)
        for nome, largura, altura in [('desktop', 1366, 900), ('celular', 390, 844)]:
            contexto = browser.new_context(viewport={'width': largura, 'height': altura},
                                          is_mobile=nome == 'celular', has_touch=nome == 'celular')
            page = contexto.new_page()
            falhas = []
            page.on('pageerror', lambda e: falhas.append(str(e)))
            page.goto(args.url)
            expect(page.locator('#codigo')).to_be_visible()

            def analisar(codigo):
                page.locator('#codigo').fill(codigo)
                with page.expect_response(lambda r: r.url.endswith('/api/analisar')) as resposta:
                    page.locator('#btn-analisar').click()
                r = resposta.value
                assert r.status == 200
                dados = r.json()
                expect(page.locator('#tabela-tokens')).to_be_visible()
                expect(page.locator('#tabela-tokens tbody tr')).to_have_count(len(dados['tokens']))
                expect(page.locator('#codigo-analisado')).to_have_text(codigo.replace('\r\n', '\n').replace('\r', '\n'))
                expect(page.locator('#btn-analisar')).to_be_enabled()
                sintatica = dados['sintatica']
                if sintatica['estado'] == 'sucesso':
                    expect(page.locator('#arvore-ast')).to_be_visible()
                    expect(page.locator('#estado-sintatica')).to_contain_text('sem erros')
                    expect(page.locator('#erros-sintaticos')).to_have_count(0)
                else:
                    expect(page.locator('#arvore-ast')).to_have_count(0)
                    if sintatica['estado'] == 'erro':
                        expect(page.locator('#erros-sintaticos > li')).to_have_count(len(sintatica['erros']))
                    else:
                        expect(page.locator('#estado-sintatica')).to_contain_text('não executada')
                return dados

            # Todos os exemplos atravessam de fato nginx e FastAPI.
            ids = page.locator('#exemplos option').evaluate_all('(opcoes) => opcoes.map(o => o.value).filter(Boolean)')
            for id_exemplo in ids:
                page.locator('#exemplos').select_option(id_exemplo)
                codigo = page.locator('#codigo').input_value()
                r = analisar(codigo)
                assert r['sucesso'] is (id_exemplo != 'ex6')
                assert r['sintatica']['estado'] == ('nao_executada' if id_exemplo == 'ex6' else 'erro' if id_exemplo == 'ex8' else 'sucesso')
                total += 1

            r = analisar('int numero = 10;')
            assert r['tokens'][1] == {'tipo': 'IDENTIFICADOR', 'lexema': 'numero', 'linha': 1, 'coluna': 5}
            expect(page.locator('#codigo-analisado mark')).to_have_text('int')
            page.locator('#token-proximo').click()
            expect(page.locator('#codigo-analisado mark')).to_have_text('numero')
            page.locator('#token-anterior').click()
            expect(page.locator('#codigo-analisado mark')).to_have_text('int')
            total += 1

            # Oráculo manual, independente da implementação do parser.
            r = analisar('int resultado = 10 + 5 * 2;\nint agrupado = (10 + 5) * 2;\nint associacao = 20 - 5 - 3;')
            a, b, c = [n['inicializador'] for n in r['sintatica']['ast']['comandos']]
            assert a['operador'] == '+' and a['direita']['operador'] == '*'
            assert b['operador'] == '*' and b['esquerda']['operador'] == '+'
            assert c['operador'] == '-' and c['esquerda']['operador'] == '-'
            total += 1

            # Árvore pronta navegável, sem alegação de construção animada.
            r = analisar('int resultado = 10 + 5 * 2;')
            nos = page.locator('#arvore-ast details')
            expect(nos).to_have_count(7)
            page.locator('#ast-expandir').click()
            assert nos.evaluate_all('(nos) => nos.every(n => n.open)')
            page.locator('#ast-recolher').click()
            assert nos.evaluate_all('(nos) => nos.every(n => !n.open)')
            raiz = page.locator('#arvore-ast > details')
            raiz.locator(':scope > summary').focus()
            page.keyboard.press('Space')
            assert raiz.evaluate('(n) => n.open')
            total += 1
            page.locator('#ast-expandir').click()
            soma = page.locator('#arvore-ast details[data-tipo="Binario"]').first
            soma.locator(':scope > .ast-informacoes > button').click()
            expect(page.locator('#codigo-analisado mark')).to_have_text('10 + 5 * 2')
            expect(page.locator('#posicao-ast')).to_contain_text('fim exclusivo')
            multiplicacao = page.locator('#arvore-ast details[data-tipo="Binario"]').nth(1)
            multiplicacao.locator(':scope > .ast-informacoes > button').click()
            expect(page.locator('#codigo-analisado mark')).to_have_text('5 * 2')
            if args.capturas:
                page.locator('#arvore-ast').evaluate('(n) => { n.scrollTop = 0; n.scrollLeft = 0; }')
                page.screenshot(path=str(args.capturas / f'ast-{nome}.png'), full_page=True)
            page.locator('#token-destacar').click()
            expect(page.locator('#codigo-analisado mark')).to_have_text('int')
            total += 1
            with page.expect_download() as download_info:
                page.locator('#ast-exportar').click()
            download = download_info.value
            assert download.suggested_filename == 'mini-c-ast.json'
            assert json.loads(Path(download.path()).read_text()) == r['sintatica']['ast']
            if args.capturas and nome == 'desktop':
                download.save_as(str(args.capturas / 'mini-c-ast.json'))
            total += 1

            r = analisar('int x=12abc;\n@ float y=7.5;')
            assert not r['sucesso'] and len(r['erros']) == 2
            expect(page.locator('#erros-lexicos')).to_contain_text('Linha 2, coluna 1')
            assert r['tokens'][-2]['lexema'] == '7.5'
            assert r['sintatica']['estado'] == 'nao_executada'
            total += 1
            if args.capturas and nome == 'celular':
                page.screenshot(path=str(args.capturas / 'erros-lexicos-celular.png'), full_page=True)

            r = analisar('/* apenas comentários */')
            assert r['tokens'] == [] and r['sintatica']['estado'] == 'erro'
            r = analisar('int = ;')
            assert r['sucesso'] is True and r['sintatica']['sucesso'] is False
            total += 2

            r = analisar('int x')
            assert r['sintatica']['erros'][0]['coluna'] == 6
            assert r['sintatica']['erros'][0]['esperado'] == [';']
            expect(page.locator('#erros-sintaticos')).to_contain_text('fim do código (EOF)')
            total += 1
            r = analisar('int a = ;\nint b;\nb = ;')
            assert [(e['linha'], e['coluna']) for e in r['sintatica']['erros']] == [(1, 9), (3, 5)]
            expect(page.locator('#estado-lexico')).to_contain_text('sem erros')
            expect(page.locator('#estado-sintatica')).to_contain_text('com erros')
            if args.capturas and nome == 'desktop':
                page.screenshot(path=str(args.capturas / 'erros-sintaticos-desktop.png'), full_page=True)
            total += 1
            for codigo, esperado in [('if (x > 0 { x = 1; }', ')'), ('{ int x;', '}'), ('else {}', 'if')]:
                r = analisar(codigo)
                assert esperado in r['sintatica']['erros'][0]['esperado']
                total += 1
            assert analisar('x = 2.5;')['sintatica']['sucesso'] is True  # só sintaxe, sem tabela de símbolos
            total += 1

            r = analisar('/* 😀 */\n\tint x = (10 + 2) * 3;')
            folhas = page.locator('#arvore-ast details[data-tipo="Literal"]')
            page.locator('#ast-expandir').click()
            folhas.first.locator(':scope > .ast-informacoes > button').click()
            expect(page.locator('#codigo-analisado mark')).to_have_text('10')
            token = next(t for t in r['tokens'] if t['lexema'] == '10')
            no = r['sintatica']['ast']['comandos'][0]['inicializador']['esquerda']['esquerda']
            assert no['inicio'] == {'linha': token['linha'], 'coluna': token['coluna']}
            total += 1

            inicio = perf_counter()
            r = analisar('{}' * 1999)  # exatamente 2.000 nós, incluindo Programa
            expect(page.locator('#arvore-ast details')).to_have_count(2000)
            page.locator('#ast-recolher').click()
            expect(page.locator('#btn-analisar')).to_be_enabled()
            print(f'INFO: {nome}, 2.000 nós e 3.998 tokens: resposta + renderização em {perf_counter() - inicio:.2f}s nesta máquina.')
            total += 1
            for codigo, limite in [('{}' * 2000, 'limite_nos'), ('int x=' + '+'.join(['1'] * 2500) + ';', 'limite_altura'), ('{' * 65 + 'int x;' + '}' * 65, 'limite_profundidade')]:
                r = analisar(codigo)
                assert r['sintatica']['erros'][0]['codigo'] == limite
                total += 1
            r = analisar('{' * 64 + 'int x;' + '}' * 64)
            assert r['sintatica']['sucesso'] is True
            page.locator('#ast-expandir').click()
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Árvore profunda escapou da região rolável'
            total += 1

            page.locator('#codigo').fill('   ')
            page.locator('#btn-analisar').click()
            expect(page.locator('#resultado')).to_contain_text('apenas espaços em branco')
            expect(page.locator('#tabela-tokens')).to_have_count(0)
            total += 1
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Overflow horizontal da página'
            page.locator('#exemplos').focus()
            page.keyboard.press('Tab')
            expect(page.locator('#codigo')).to_be_focused()
            page.keyboard.press('Tab')
            expect(page.locator('#btn-analisar')).to_be_focused()
            assert not falhas, falhas
            total += 1
            print(f'OK: {nome}, {largura}px, exemplos, tokens, AST/precedência, seleção, download, erros/recuperação, limites, validação, teclado e largura.')
            contexto.close()
        browser.close()
    print(f'OK: {total} cenários E2E, sem mocks ou erros JavaScript. Isso não constitui auditoria completa de acessibilidade ou teste em aparelho físico.')


if __name__ == '__main__':
    main()
