#!/usr/bin/env python3
"""E2E opcional com Playwright; serviços devem estar ativos. Não usa mocks.

Uso: python scripts/teste_navegador.py [--chromium /usr/bin/chromium]
     [--capturas /tmp/capturas]
"""
import argparse
import json
import re
from pathlib import Path
from time import perf_counter

from playwright.sync_api import sync_playwright, expect


def contraste(cor_a, cor_b):
    def luminancia(cor):
        canais = [v / 255 for v in cor[:3]]
        canais = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in canais]
        return sum(v * peso for v, peso in zip(canais, (0.2126, 0.7152, 0.0722)))
    a, b = sorted((luminancia(cor_a), luminancia(cor_b)))
    return (b + 0.05) / (a + 0.05)


def medir_contraste(page):
    """Texto efetivamente renderizado; gradientes são conferidos em cada cor."""
    cores = page.evaluate('''() => {
      function rgb(texto) { return (texto.match(/[\\d.]+/g) || []).map(Number); }
      function fundos(elemento) {
        for (let n = elemento; n; n = n.parentElement) {
          const s = getComputedStyle(n);
          if (s.backgroundImage !== 'none') {
            const cores = s.backgroundImage.match(/rgba?\\([^)]+\\)/g);
            if (cores) return cores.map(rgb);
          }
          const cor = rgb(s.backgroundColor);
          if (cor.length >= 3 && (cor.length < 4 || cor[3] === 1)) return [cor];
        }
        throw Error('Fundo opaco não encontrado');
      }
      return [...document.querySelectorAll('body, header p, h1, h2, h3, a, label, legend, .nota, .msg, .estado-analise, .token, caption, th, td, summary, button:not(:disabled), select, textarea')]
        .filter(n => n.getBoundingClientRect().width && n.getBoundingClientRect().height && !n.closest('button:disabled'))
        .map(n => ({elemento: n.id || n.className || n.tagName, frente: rgb(getComputedStyle(n).color), fundos: fundos(n)}));
    }''')
    medicoes = [(contraste(item['frente'], fundo), item) for item in cores for fundo in item['fundos']]
    assert medicoes, 'Nenhum elemento de contraste foi medido'
    menor, item = min(medicoes, key=lambda v: v[0])
    assert menor >= 4.5, f'Contraste de texto insuficiente: {menor:.2f}:1 em {item}'
    return {'elementos_medidos': len(cores), 'menor_razao_texto': round(menor, 3), 'elemento_menor_razao': item['elemento']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:8501')
    parser.add_argument('--chromium', help='Executável Chromium local; padrão: o instalado pelo Playwright')
    parser.add_argument('--capturas', type=Path, help='Diretório opcional para imagens da demonstração')
    args = parser.parse_args()
    if args.capturas:
        args.capturas.mkdir(parents=True, exist_ok=True)
    total = 0
    contraste_medido = []
    assert contraste((0, 0, 0), (255, 255, 255)) == 21
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
                semantica = dados['semantica']
                if sintatica['estado'] != 'sucesso':
                    assert semantica['estado'] == 'nao_executada'
                    expect(page.locator('#estado-semantica')).to_contain_text('não executada')
                    expect(page.locator('#tabela-simbolos')).to_have_count(0)
                else:
                    expect(page.locator('#tabela-simbolos tbody tr')).to_have_count(len(semantica['tabelaSimbolos']))
                    if semantica['sucesso']:
                        expect(page.locator('#estado-semantica')).to_contain_text('sem erros')
                    else:
                        expect(page.locator('#erros-semanticos > li')).to_have_count(len(semantica['erros']))
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
            r = analisar('x = 2.5;')
            assert r['sintatica']['sucesso'] is True and r['semantica']['sucesso'] is False
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

            # Símbolos, escopos, sombreamento e ligação ao mesmo fonte/AST.
            codigo_escopos = 'int x = 10;\n{\n    float y = 2.5;\n    int x = 20;\n    x = x + 1;\n}\nx = x + 1;'
            r = analisar(codigo_escopos)
            assert r['semantica']['sucesso'] is True
            assert [(s['nome'], s['tipo'], s['escopo']) for s in r['semantica']['tabelaSimbolos']] == [('x', 'int', 'E0'), ('y', 'float', 'E1'), ('x', 'int', 'E1')]
            page.locator('#filtro-escopo').select_option('E1')
            expect(page.locator('#tabela-simbolos tbody tr')).to_have_count(2)
            local = page.locator('#tabela-simbolos tr[data-simbolo-id="S3"]')
            local.locator('.localizar-simbolo').click()
            expect(page.locator('#codigo-analisado mark')).to_have_text('x')
            assert page.locator('.ast-relacionado').get_attribute('data-no-ast') == '/comandos/1/comandos/1'
            expect(page.locator('#selecao-semantica')).to_contain_text('coluna 9')
            local.locator('summary').click()
            local.locator('.localizar-referencia').first.click()
            assert page.locator('.ast-relacionado').get_attribute('data-no-ast') == '/comandos/1/comandos/2/alvo'
            page.locator('#token-destacar').click()
            expect(page.locator('#codigo-analisado mark')).to_have_text('int')
            total += 1

            erros_semanticos = [
                ('int x=10;\ntotal=x+5;', 'IDENTIFICADOR_NAO_DECLARADO'),
                ('int x=2.5;', 'TIPOS_INCOMPATIVEIS'),
                ('int x; int x;', 'REDECLARACAO_NO_ESCOPO'),
                ('int x; int y=x;', 'VARIAVEL_NAO_INICIALIZADA'),
                ('int x=1; if(x){}', 'CONDICAO_NAO_BOOLEANA'),
                ('int x=(1<2)+3;', 'OPERANDOS_NAO_NUMERICOS'),
                ('if(1<2<3){}', 'TIPOS_NAO_COMPARAVEIS'),
            ]
            for codigo, regra in erros_semanticos:
                r = analisar(codigo)
                assert r['sucesso'] is True and r['sintatica']['sucesso'] is True
                assert r['semantica']['erros'][0]['regra'] == regra
                page.locator('#erros-semanticos button').first.click()
                expect(page.locator('#codigo-analisado mark')).to_be_visible()
                assert page.locator('.ast-relacionado').count() == 1
                if args.capturas and nome == 'desktop' and regra == 'IDENTIFICADOR_NAO_DECLARADO':
                    page.screenshot(path=str(args.capturas / 'erro-semantico-desktop.png'), full_page=True)
                total += 1
            r = analisar('int x; if(1<2){x=1;}else{x=2;} int y=x;')
            assert r['semantica']['sucesso'] and all(s['inicializado'] for s in r['semantica']['tabelaSimbolos'])
            total += 1
            r = analisar('int x; if(1<2){x=1;} int y=x;')
            assert r['semantica']['erros'][0]['regra'] == 'VARIAVEL_NAO_INICIALIZADA'
            total += 1

            # Cada modo deve preservar o fonte, as três fases e os rótulos.
            estados = [('sucesso', 'int x=10; x=x+1;'), ('lexico', '@ int x;'),
                       ('sintatico', 'int x=;'), ('semantico', 'int x; int y=x;')]
            for modo in ['padrao', 'sem-cores', 'contraste']:
                page.locator('#modo-visual').select_option(modo)
                for fase, codigo in estados:
                    r = analisar(codigo)
                    medicao = medir_contraste(page)
                    contraste_medido.append({'viewport': nome, 'modo': modo, 'estado': fase, **medicao})
                    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
                    assert page.locator('#estado-lexico').inner_text()
                    assert page.locator('#estado-sintatica').inner_text()
                    assert page.locator('#estado-semantica').inner_text()
                    total += 1
                r = analisar(codigo_escopos)
                page.locator('#tabela-simbolos .localizar-simbolo').first.click()
                expect(page.locator('#codigo-analisado mark')).to_have_text('x')
                assert page.locator('#modo-visual').input_value() == modo
                selecao = page.locator('#codigo-analisado mark').evaluate('(n) => ({borda:getComputedStyle(n).outlineColor,fundo:getComputedStyle(n.parentElement).backgroundColor})')
                rgb = lambda texto: [float(v) for v in re.findall(r'[\d.]+', texto)]
                razao_selecao = contraste(rgb(selecao['borda']), rgb(selecao['fundo']))
                assert razao_selecao >= 3, ('Seleção sem contorno contrastante', selecao)
                page.locator('#modo-visual').focus()
                page.keyboard.press('Tab')
                page.keyboard.press('Shift+Tab')
                foco = page.locator('#modo-visual').evaluate('(n) => ({cor:getComputedStyle(n).outlineColor,fundo:getComputedStyle(n).backgroundColor,estilo:getComputedStyle(n).outlineStyle})')
                razao_foco = contraste(rgb(foco['cor']), rgb(foco['fundo']))
                assert foco['estilo'] != 'none' and razao_foco >= 3
                contraste_medido.append({'viewport': nome, 'modo': modo, 'estado': 'foco_e_selecao',
                                        'razao_foco': round(razao_foco, 3), 'razao_selecao': round(razao_selecao, 3)})
                if modo != 'padrao':
                    decoracoes = page.locator('.legenda-tokens .token').evaluate_all('(nos) => nos.map(n => getComputedStyle(n).textDecorationStyle)')
                    assert decoracoes[:5] == ['double', 'solid', 'dotted', 'dashed', 'wavy']
                    page.locator('#legenda-visual').evaluate('(n) => { n.open = true; }')
                if args.capturas:
                    page.locator('.tabela-responsiva').evaluate_all('(regioes) => regioes.forEach(n => { n.scrollLeft = 0; })')
                    page.locator('#arvore-ast').evaluate('(n) => { n.scrollTop = 0; n.scrollLeft = 0; }')
                    page.screenshot(path=str(args.capturas / f'semantica-{modo}-{nome}.png'), full_page=True)
                    if modo == 'sem-cores':
                        page.locator('#token-destacar').click()
                        page.screenshot(path=str(args.capturas / f'tokens-sem-cores-{nome}.png'), full_page=True)
                total += 1

            # Preferência persiste de fato após recarregar, sem persistir o código.
            page.locator('#modo-visual').select_option('sem-cores')
            page.reload()
            expect(page.locator('#modo-visual')).to_have_value('sem-cores')
            analisar('int x=1;')
            total += 1
            # Inspeção sob simulação técnica; não equivale a estudo com pessoas.
            sessao = contexto.new_cdp_session(page)
            for deficiencia in ['protanopia', 'deuteranopia', 'tritanopia', 'achromatopsia']:
                sessao.send('Emulation.setEmulatedVisionDeficiency', {'type': deficiencia})
                page.locator('#tabela-simbolos .localizar-simbolo').click()
                expect(page.locator('#codigo-analisado mark')).to_have_text('x')
                expect(page.locator('#estado-semantica')).to_contain_text('sem erros')
                assert page.locator('.ast-relacionado').count() == 1
                if args.capturas and nome == 'desktop':
                    page.screenshot(path=str(args.capturas / f'simulacao-{deficiencia}.png'), full_page=True)
                total += 1
            sessao.send('Emulation.setEmulatedVisionDeficiency', {'type': 'none'})
            sessao.detach()
            page.locator('#modo-visual').focus()
            page.keyboard.press('Home')
            page.keyboard.press('ArrowDown')
            page.keyboard.press('Tab')
            expect(page.locator('#modo-visual')).to_have_value('sem-cores')
            page.locator('#modo-visual').focus()
            foco = page.locator('#modo-visual').evaluate('(n) => { const s=getComputedStyle(n); return {cor:s.outlineColor, fundo:s.backgroundColor, estilo:s.outlineStyle}; }')
            assert foco['estilo'] != 'none'
            assert contraste([float(v) for v in re.findall(r'[\d.]+', foco['cor'])], [float(v) for v in re.findall(r'[\d.]+', foco['fundo'])]) >= 3
            total += 1
            page.locator('#modo-visual').select_option('padrao')

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
            print(f'OK: {nome}, {largura}px, tokens/AST, semântica, escopos, inicialização, seleções, modos visuais, contraste, simulações, teclado e regressão.')
            contexto.close()
        browser.close()
    if args.capturas:
        (args.capturas / 'contraste-medido.json').write_text(json.dumps({
            'criterio_texto_regular': 4.5, 'criterio_foco': 3,
            'metodo': 'Luminância relativa sRGB; cores computadas dos elementos e fundos/gradientes renderizados. Controles desabilitados excluídos.',
            'medicoes': contraste_medido,
            'limites': 'Inspeção técnica, sem participantes com daltonismo, sem certificação WCAG integral; simulação móvel não é aparelho físico.'
        }, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'OK: {total} cenários E2E, sem mocks ou erros JavaScript. Não constitui auditoria completa WCAG nem estudo com pessoas daltônicas ou aparelho físico.')


if __name__ == '__main__':
    main()
