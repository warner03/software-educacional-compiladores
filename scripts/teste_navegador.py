#!/usr/bin/env python3
"""E2E opcional com Playwright; serviços devem estar ativos. Não usa mocks.

Uso: python scripts/teste_navegador.py [--chromium /usr/bin/chromium]
     [--capturas /tmp/capturas]
"""
import argparse
from pathlib import Path

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
                expect(page.locator('#codigo-analisado')).to_have_text(codigo)
                expect(page.locator('#btn-analisar')).to_be_enabled()
                return dados

            # Todos os exemplos atravessam de fato nginx e FastAPI.
            ids = page.locator('#exemplos option').evaluate_all('(opcoes) => opcoes.map(o => o.value).filter(Boolean)')
            for id_exemplo in ids:
                page.locator('#exemplos').select_option(id_exemplo)
                codigo = page.locator('#codigo').input_value()
                r = analisar(codigo)
                assert r['sucesso'] is (id_exemplo != 'ex6')
                total += 1

            r = analisar('int numero = 10;')
            assert r['tokens'][1] == {'tipo': 'IDENTIFICADOR', 'lexema': 'numero', 'linha': 1, 'coluna': 5}
            expect(page.locator('#codigo-analisado mark')).to_have_text('int')
            page.locator('#token-proximo').click()
            expect(page.locator('#codigo-analisado mark')).to_have_text('numero')
            page.locator('#token-anterior').click()
            expect(page.locator('#codigo-analisado mark')).to_have_text('int')
            total += 1
            if args.capturas and nome == 'desktop':
                page.screenshot(path=str(args.capturas / 'analise-lexica-desktop.png'), full_page=True)

            r = analisar('int x=12abc;\n@ float y=7.5;')
            assert not r['sucesso'] and len(r['erros']) == 2
            expect(page.locator('#erros-lexicos')).to_contain_text('Linha 2, coluna 1')
            assert r['tokens'][-2]['lexema'] == '7.5'
            total += 1
            if args.capturas and nome == 'celular':
                page.screenshot(path=str(args.capturas / 'erros-lexicos-celular.png'), full_page=True)

            assert analisar('/* apenas comentários */')['tokens'] == []
            assert analisar('int = ;')['sucesso'] is True
            total += 2
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
            print(f'OK: {nome}, {largura}px, exemplos, edição/envio, navegação, erros, comentários, validação, teclado e largura.')
            contexto.close()
        browser.close()
    print(f'OK: {total} cenários E2E, sem mocks ou erros JavaScript. Isso não constitui auditoria completa de acessibilidade ou teste em aparelho físico.')


if __name__ == '__main__':
    main()
