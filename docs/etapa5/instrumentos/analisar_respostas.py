#!/usr/bin/env python3
"""Analisa CSV Google Forms por prefixos; sem escore global e sem expor texto livre.

Uso: python3 analisar_respostas.py respostas.csv --saida analise.json
Aceita UTF-8/BOM e separadores vírgula, ponto e vírgula ou tabulação.
"""
import argparse
import csv
import json
from pathlib import Path
import re
from statistics import median
import unicodedata

IDS_Q = ('Q01', 'Q02')
IDS_L = ('L01', 'L02', 'L03')
IDS_A = ('A01',)
OBRIGATORIOS = ('C01', 'M01') + IDS_Q + IDS_L
GABARITO = {'Q01': 'C', 'Q02': 'B'}
OPCOES = {'Q01': 'ABCD', 'Q02': 'ABCD'}
MODOS = ('Em dupla', 'Individual', 'Modo não informado')


def normalizar(valor):
    texto = unicodedata.normalize('NFKD', str(valor or ''))
    return ' '.join(''.join(c for c in texto if not unicodedata.combining(c)).lower().split())


def identificar_coluna(titulo):
    if not isinstance(titulo, str):
        return None
    m = re.match(r'^\s*(C01|M01|P01|Q0[1-4]|L0[1-6]|A0[1-2])\b', titulo, re.I)
    return m.group(1).upper() if m else None


def ler_csv(caminho):
    with Path(caminho).open(encoding='utf-8-sig', newline='') as arquivo:
        amostra = arquivo.read(8192)
        arquivo.seek(0)
        try:
            dialeto = csv.Sniffer().sniff(amostra, delimiters=',;\t')
        except csv.Error:
            dialeto = csv.excel
        leitor = csv.DictReader(arquivo, dialect=dialeto)
        if not leitor.fieldnames:
            return []
        colunas = {}
        for nome in leitor.fieldnames:
            id = identificar_coluna(nome)
            if id:
                if id in colunas.values():
                    raise ValueError(f'Prefixo duplicado no cabeçalho: {id}.')
                colunas[nome] = id
        faltam = [id for id in OBRIGATORIOS if id not in colunas.values()]
        if set(colunas.values()) - set(OBRIGATORIOS) - set(IDS_A):
            raise ValueError('O CSV pertence a outra versão do instrumento. Use o analisador da versão correspondente; não misture as coletas.')
        if faltam:
            raise ValueError('Cabeçalhos obrigatórios ausentes: ' + ', '.join(faltam))
        linhas = []
        for linha in leitor:
            if None in linha:
                raise ValueError('Há linha com mais campos que o cabeçalho. Confira separador e aspas do CSV.')
            if not any(str(v or '').strip() for v in linha.values()):
                continue
            # Timestamp/e-mail/qualquer coluna sem prefixo são descartados aqui.
            linhas.append({id: (linha.get(nome) or '').strip() for nome, id in colunas.items()})
        return linhas


def consentiu(linha):
    return bool(re.match(r'^sim\b', normalizar(linha.get('C01'))))


def modo(linha):
    valor = normalizar(linha.get('M01'))
    if valor == 'em dupla':
        return 'Em dupla'
    if valor == 'individual':
        return 'Individual'
    return 'Modo não informado'


def resposta_objetiva(valor, item):
    valor = str(valor or '').strip()
    if not valor:
        return 'ausente', None
    if normalizar(valor).startswith('nao sei'):
        return 'valida', OPCOES[item][-1]
    m = re.match(r'^([A-E])(?:\)|\.|\s|$)', valor, re.I)
    if m and m.group(1).upper() in OPCOES[item]:
        return 'valida', m.group(1).upper()
    return 'invalida', None


def resposta_likert(valor):
    valor = str(valor or '').strip()
    if not valor:
        return 'ausente', None
    n = normalizar(valor)
    if n.startswith('n/a') or n in ('na', 'nao se aplica', 'nao aplicavel'):
        return 'na', None
    m = re.fullmatch(r'([1-5])(?:\s*[—–-].*)?', valor)
    if m:
        return 'valida', int(m.group(1))
    return 'invalida', None


def resumir(linhas, modalidade):
    objetivas = {}
    for item in IDS_Q:
        freq = {opcao: 0 for opcao in OPCOES[item]}
        ausentes = invalidas = 0
        for linha in linhas:
            estado, opcao = resposta_objetiva(linha.get(item), item)
            if estado == 'valida':
                freq[opcao] += 1
            elif estado == 'ausente':
                ausentes += 1
            else:
                invalidas += 1
        n = sum(freq.values())
        acertos = freq[GABARITO[item]]
        objetivas[item] = {
            'n_respostas_validas': n, 'n_acertos': acertos,
            'n_nao_corretas_incluindo_nao_sei': n - acertos,
            'taxa_acerto_pct': round(100 * acertos / n, 2) if n else None,
            'frequencias_opcoes': freq, 'n_sem_resposta': ausentes, 'n_invalidas': invalidas,
        }
    likert = {}
    for item in IDS_L:
        valores = []
        freq = {str(n): 0 for n in range(1, 6)}
        na = ausentes = invalidas = 0
        for linha in linhas:
            estado, valor = resposta_likert(linha.get(item))
            if estado == 'valida':
                valores.append(valor)
                freq[str(valor)] += 1
            elif estado == 'na':
                na += 1
            elif estado == 'ausente':
                ausentes += 1
            else:
                invalidas += 1
        likert[item] = {
            'n_respostas_numericas': len(valores), 'frequencias': freq,
            'mediana': median(valores) if valores else None,
            'n_na': na, 'n_sem_resposta': ausentes, 'n_invalidas': invalidas,
        }
    return {
        'n_respostas_individuais': len(linhas), 'objetivas': objetivas, 'likert': likert,
        'campos_abertos_apenas_contagem': {
            id: sum(bool(str(linha.get(id) or '').strip()) for linha in linhas) for id in IDS_A
        },
    }


def analisar_linhas(linhas, origem='Respostas fornecidas; origem humana não verificada pelo programa'):
    elegiveis = [linha for linha in linhas if consentiu(linha)]
    resultado = {
        'versao_instrumento': '3.0',
        'origem': origem,
        'estado': 'com_respostas_elegiveis' if elegiveis else 'sem_respostas_elegiveis' if linhas else 'sem_respostas',
        'n_linhas_lidas': len(linhas), 'n_respostas_elegiveis': len(elegiveis),
        'n_excluidas_consentimento_ou_elegibilidade': len(linhas) - len(elegiveis),
        'estatisticas_por_modo': None,
        'avisos': [
            'Análise descritiva: não estima ganho de aprendizagem ou efeito causal.',
            'Não há escore global, SUS ou soma dos itens Likert.',
            'Modalidade individual é separada da atividade em duplas.',
            'Seis perguntas: duas objetivas, três itens de percepção e uma aberta opcional.',
            'L02 mede identificação sem depender de cores percebida pelos respondentes, sem comprovar eficácia com pessoas daltônicas.',
            'A unidade do formulário é a resposta individual; não é número de duplas nem de observações independentes.',
            'N/A, ausências e valores inválidos ficam fora dos denominadores indicados.',
            'Texto livre, identificadores e data/hora não são expostos nesta saída.',
            'Revisar risco de identificação antes de publicar estratos pequenos.',
        ],
    }
    if not elegiveis:
        return resultado
    modos = {}
    for m in MODOS:
        grupo = [linha for linha in elegiveis if modo(linha) == m]
        if not grupo:
            continue
        resumo = resumir(grupo, m)
        modos[m] = resumo
    resultado['estatisticas_por_modo'] = modos
    return resultado


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=Path)
    parser.add_argument('--saida', type=Path)
    parser.add_argument('--dados-sinteticos-teste', action='store_true', help='Rotula explicitamente dados artificiais de validação do código.')
    args = parser.parse_args()
    try:
        linhas = ler_csv(args.csv)
        origem = 'APENAS DADOS SINTÉTICOS DE TESTE — não são respostas de participantes' if args.dados_sinteticos_teste else 'Respostas fornecidas; origem humana não verificada pelo programa'
        resultado = analisar_linhas(linhas, origem=origem)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        # Evitar ecoar caminho/linha/célula que possa conter informação pessoal.
        print(json.dumps({'estado': 'erro_de_leitura', 'estatisticas_por_modo': None,
                          'mensagem': str(exc) if isinstance(exc, ValueError) else 'Não foi possível ler o CSV UTF-8 informado.'}, ensure_ascii=False, indent=2))
        return 1
    texto = json.dumps(resultado, ensure_ascii=False, indent=2) + '\n'
    if args.saida:
        args.saida.parent.mkdir(parents=True, exist_ok=True)
        args.saida.write_text(texto, encoding='utf-8')
    print(texto, end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
