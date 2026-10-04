# testes do log.py (csv pedido no enunciado)
# usa uma pasta temporária pra não sujar o projeto

import csv
import os
import tempfile
import unittest

import log


def historico_exemplo():
    # histórico pequeno, com 3 gerações
    return {
        "geracoes": [1, 2, 3],
        "fitness_medio": [1.5, 2.5, 3.5],
        "melhor_fitness": [4.0, 5.0, 6.0],
        "melhor_x": [0.1, 0.2, 0.3],
        "melhor_y": [-0.1, -0.2, -0.3],
    }


class TestSalvarLog(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.caminho = os.path.join(self.pasta.name, "log.csv")
        log.salvar_log(historico_exemplo(), self.caminho)
        with open(self.caminho, newline="", encoding="utf-8") as f:
            self.linhas = list(csv.reader(f))

    def tearDown(self):
        self.pasta.cleanup()

    def test_cabecalho(self):
        self.assertEqual(self.linhas[0], log.COLUNAS)

    def test_uma_linha_por_geracao(self):
        self.assertEqual(len(self.linhas) - 1, 3)

    def test_valores_gravados_corretamente(self):
        self.assertEqual(self.linhas[1], ["1", "1.5", "4.0", "0.1", "-0.1"])
        self.assertEqual(self.linhas[3], ["3", "3.5", "6.0", "0.3", "-0.3"])

    def test_cinco_colunas_em_todas_as_linhas(self):
        for linha in self.linhas:
            self.assertEqual(len(linha), 5)


if __name__ == "__main__":
    unittest.main()
