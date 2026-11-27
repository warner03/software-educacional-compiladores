"""Somente dados sintéticos de teste de código; não são resultados de participantes."""
import csv
import json
from pathlib import Path
import tempfile
import unittest

from analisar_respostas import analisar_linhas, ler_csv, OBRIGATORIOS, IDS_A

ORIGEM = 'APENAS DADOS SINTÉTICOS DE TESTE — não são respostas de participantes'


def linha(**campos):
    dados = {'C01': 'Sim, tenho 18 anos ou mais e aceito participar.', 'M01': 'Em dupla',
             'Q01': 'C) Semântico.', 'Q02': 'B) Sintática.',
             'L01': '4 — Concordo', 'L02': '4 — Concordo', 'L03': '4 — Concordo', 'A01': ''}
    dados.update(campos)
    return dados


class AnaliseV3(unittest.TestCase):
    def test_denominadores_mediana_e_estratos(self):
        dados = [linha(L02='1'), linha(L02='5', Q01='D) Não sei.'), linha(L02='N/A'),
                 linha(C01='Não. Encerrar o formulário.', L02='5'), linha(M01='Individual', L02='2')]
        resultado = analisar_linhas(dados, ORIGEM)
        self.assertEqual(resultado['n_respostas_elegiveis'], 4)
        self.assertEqual(resultado['n_excluidas_consentimento_ou_elegibilidade'], 1)
        duplas = resultado['estatisticas_por_modo']['Em dupla']
        self.assertEqual(duplas['objetivas']['Q01']['n_respostas_validas'], 3)
        self.assertEqual(duplas['objetivas']['Q01']['n_acertos'], 2)
        self.assertEqual(duplas['objetivas']['Q01']['taxa_acerto_pct'], 66.67)
        self.assertEqual(duplas['likert']['L02']['n_respostas_numericas'], 2)
        self.assertEqual(duplas['likert']['L02']['n_na'], 1)
        self.assertEqual(duplas['likert']['L02']['mediana'], 3)
        self.assertEqual(duplas['likert']['L02']['frequencias'], {'1': 1, '2': 0, '3': 0, '4': 0, '5': 1})
        self.assertEqual(resultado['estatisticas_por_modo']['Individual']['likert']['L02']['mediana'], 2)

    def test_ausencias_invalidos_e_modo_desconhecido(self):
        dados = [linha(M01='MODO SINTÉTICO', Q01='', Q02='INVÁLIDO', L01='6', L02='', L03='N/A')]
        r = analisar_linhas(dados, ORIGEM)['estatisticas_por_modo']['Modo não informado']
        self.assertIsNone(r['objetivas']['Q01']['taxa_acerto_pct'])
        self.assertEqual(r['objetivas']['Q02']['n_invalidas'], 1)
        for item in ['L01', 'L02', 'L03']:
            self.assertIsNone(r['likert'][item]['mediana'])
            self.assertEqual(r['likert'][item]['n_respostas_numericas'], 0)
        self.assertNotIn('escore_global', r)

    def test_sem_respostas_ou_sem_aceite_nao_produz_estatisticas(self):
        for dados in [[], [linha(C01='Não. Encerrar o formulário.')]]:
            r = analisar_linhas(dados, ORIGEM)
            self.assertEqual(r['n_respostas_elegiveis'], 0)
            self.assertIsNone(r['estatisticas_por_modo'])

    def test_csv_privacidade_e_rejeicao_de_versao_anterior(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'DADOS_SINTETICOS.csv'
            ids = list(OBRIGATORIOS) + list(IDS_A)
            with path.open('w', encoding='utf-8-sig', newline='') as f:
                w = csv.writer(f, delimiter=';')
                w.writerow(['Data', 'E-mail'] + [id + ' — Pergunta' for id in ids])
                dado = linha(A01='DADO SINTÉTICO: ana@example.test')
                w.writerow(['DATA SINTÉTICA', 'identidade@example.test'] + [dado[id] for id in ids])
            output = json.dumps(analisar_linhas(ler_csv(path), ORIGEM))
            for valor in ['ana@example.test', 'identidade@example.test', 'DATA SINTÉTICA']:
                self.assertNotIn(valor, output)
            with path.open('w', encoding='utf-8', newline='') as f:
                csv.writer(f).writerow(list(OBRIGATORIOS) + ['P01 — Perfil antigo'])
            with self.assertRaisesRegex(ValueError, 'outra versão'):
                ler_csv(path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
