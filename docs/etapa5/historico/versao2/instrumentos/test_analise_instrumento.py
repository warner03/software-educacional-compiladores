"""APENAS DADOS SINTÉTICOS DE TESTE. Não contém sessões/respostas reais.

Não publicar os dados artificiais como resultados do estudo.
"""
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest

from analisar_respostas import analisar_linhas, ler_csv, OBRIGATORIOS, IDS_A

SINTETICO = 'APENAS DADOS SINTÉTICOS DE TESTE — não são respostas de participantes'


def linha(**alteracoes):
    r = {'C01': 'Sim, tenho 18 anos ou mais e aceito participar voluntariamente.',
         'M01': 'Em dupla', 'P01': 'Estudante cursando Compiladores',
         'Q01': 'A) Soma (+).', 'Q02': 'B) Multiplicação (*).',
         'Q03': 'B) Erro sintático.', 'Q04': 'B) Há erro léxico e o parser não é executado.'}
    r.update({f'L{n:02d}': '4 — Concordo' for n in range(1, 7)})
    r.update({'A01': '', 'A02': ''})
    r.update(alteracoes)
    return r


class TesteSomenteDadosSinteticos(unittest.TestCase):
    def test_01_consentimento_estratos_mediana_e_privacidade(self):
        """APENAS DADOS SINTÉTICOS: Não excluído; estratos preservados; PII não ecoada."""
        dados = [
            linha(L02='1 — Discordo totalmente', A01='DADO SINTÉTICO: nome Ana e ana@example.test'),
            linha(L02='5 — Concordo totalmente'),
            linha(L02='N/A — Não utilizei ou não consigo avaliar'),
            linha(C01='Não aceito participar ou tenho menos de 18 anos.', L02='5 — Concordo totalmente'),
            linha(M01='Individual', P01='Docente ou monitor', L02='2 — Discordo'),
        ]
        # Cabeçalhos longos reais do Forms + BOM/separador ; + colunas incidentais.
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'APENAS_DADOS_SINTETICOS.csv'
            ids = list(OBRIGATORIOS) + list(IDS_A)
            headers = [id + ' — Título sintético de validação' for id in ids]
            with p.open('w', encoding='utf-8-sig', newline='') as f:
                w = csv.writer(f, delimiter=';')
                w.writerow(['Carimbo de data/hora', 'E-mail'] + headers)
                for r in dados:
                    w.writerow(['DATA SINTÉTICA', 'identidade@example.test'] + [r.get(id, '') for id in ids])
            lidas = ler_csv(p)
        r = analisar_linhas(lidas, origem=SINTETICO)
        self.assertEqual(r['n_respostas_elegiveis'], 4)
        self.assertEqual(r['n_excluidas_consentimento_ou_elegibilidade'], 1)
        duplas = r['estatisticas_por_modo']['Em dupla']
        self.assertEqual(duplas['n_respostas_individuais'], 3)
        self.assertEqual(duplas['likert']['L02']['n_respostas_numericas'], 2)
        self.assertEqual(duplas['likert']['L02']['n_na'], 1)
        self.assertEqual(duplas['likert']['L02']['mediana'], 3)
        self.assertEqual(duplas['likert']['L02']['frequencias'], {'1': 1, '2': 0, '3': 0, '4': 0, '5': 1})
        self.assertIn('Docente ou monitor', r['estatisticas_por_modo']['Individual']['por_perfil'])
        saida = json.dumps(r, ensure_ascii=False)
        for segredo in ['ana@example.test', 'identidade@example.test', 'nome Ana', 'DATA SINTÉTICA']:
            self.assertNotIn(segredo, saida)

    def test_02_na_ausencias_invalidos_e_item_individual(self):
        """APENAS DADOS SINTÉTICOS: denominadores e incerteza não viram nota."""
        dados = [linha(M01='Individual', Q01='D) Não sei.', Q02='', Q03='VALOR INVÁLIDO',
                       L01='N/A', L02='', L03='6', L04='5 — Concordo totalmente', L05='4 — Concordo')]
        r = analisar_linhas(dados, origem=SINTETICO)['estatisticas_por_modo']['Individual']
        self.assertEqual(r['objetivas']['Q01']['n_respostas_validas'], 1)
        self.assertEqual(r['objetivas']['Q01']['n_acertos'], 0)
        self.assertEqual(r['objetivas']['Q01']['taxa_acerto_pct'], 0)
        self.assertIsNone(r['objetivas']['Q02']['taxa_acerto_pct'])
        self.assertEqual(r['objetivas']['Q03']['n_invalidas'], 1)
        for item in ['L01', 'L02', 'L03', 'L05']:
            self.assertEqual(r['likert'][item]['n_respostas_numericas'], 0)
            self.assertIsNone(r['likert'][item]['mediana'])
        self.assertEqual(r['likert']['L05']['n_na'], 1)
        self.assertEqual(r['likert']['L05']['n_inconsistencias_modo'], 1)
        self.assertEqual(r['likert']['L04']['mediana'], 5)
        self.assertNotIn('escore_global', r)

    def test_03_cabecalho_vazio_e_todos_sem_consentimento_nao_geram_estatisticas(self):
        """APENAS DADOS SINTÉTICOS: nenhuma base elegível => nenhuma estatística."""
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'SOMENTE_CABECALHO.csv'
            with p.open('w', encoding='utf-8', newline='') as f:
                csv.writer(f).writerow([id + ' — Título' for id in OBRIGATORIOS])
            r = analisar_linhas(ler_csv(p), origem=SINTETICO)
        self.assertEqual(r['estado'], 'sem_respostas')
        self.assertIsNone(r['estatisticas_por_modo'])
        r = analisar_linhas([linha(C01='Não aceito'), linha(C01='')], origem=SINTETICO)
        self.assertEqual(r['estado'], 'sem_respostas_elegiveis')
        self.assertEqual(r['n_respostas_elegiveis'], 0)
        self.assertIsNone(r['estatisticas_por_modo'])


    def test_04_l05_nao_e_calculado_quando_modo_e_ausente_ou_invalido(self):
        """APENAS DADOS SINTÉTICOS: aplicabilidade exige modo Em dupla confirmado."""
        dados = [linha(M01='', L05='5 — Concordo totalmente'),
                 linha(M01='MODO SINTÉTICO INVÁLIDO', L05='5 — Concordo totalmente')]
        r = analisar_linhas(dados, origem=SINTETICO)
        self.assertNotIn('Em dupla', r['estatisticas_por_modo'])
        grupo = r['estatisticas_por_modo']['Modo não informado']
        self.assertEqual(grupo['n_respostas_individuais'], 2)
        item = grupo['likert']['L05']
        self.assertEqual(item['n_respostas_numericas'], 0)
        self.assertIsNone(item['mediana'])
        self.assertEqual(sum(item['frequencias'].values()), 0)
        self.assertEqual(item['n_excluidas_aplicabilidade_modo'], 2)
        self.assertEqual(item['n_aplicabilidade_indeterminada_modo'], 2)
        self.assertEqual(item['n_inconsistencias_modo'], 2)
        self.assertEqual(item['n_na'], 0)
        self.assertEqual(grupo['likert']['L02']['mediana'], 4)
        self.assertNotIn('MODO SINTÉTICO INVÁLIDO', json.dumps(r, ensure_ascii=False))


if __name__ == '__main__':
    unittest.main(verbosity=2)
