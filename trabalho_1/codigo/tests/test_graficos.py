# testes do graficos.py
# só confere se o PNG é criado e se nenhuma figura fica aberta
# o resto dá pra ver abrindo a imagem

import os
import tempfile
import unittest

import matplotlib

# sem abrir janelas
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

import graficos  # noqa: E402


class TestGraficoPopulacao(unittest.TestCase):
    def test_gera_png(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "g.png")
            graficos.grafico_populacao(1, [(0, 0), (1, 1), (-2, 3)], (1, 1), caminho)
            self.assertTrue(os.path.getsize(caminho) > 0)

    def test_nao_deixa_figuras_abertas(self):
        for g in range(5):
            graficos.grafico_populacao(g, [(0, 0), (1, 1)], (1, 1))
        self.assertEqual(plt.get_fignums(), [])


class TestGraficoFitnessMedio(unittest.TestCase):
    def test_gera_png(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "f.png")
            graficos.grafico_fitness_medio([1, 2, 3], [1.0, 2.0, 3.0], [2.0, 3.0, 4.0], caminho)
            self.assertTrue(os.path.getsize(caminho) > 0)

    def test_aceita_sem_melhor_fitness(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "f.png")
            graficos.grafico_fitness_medio([1, 2, 3], [1.0, 2.0, 3.0], None, caminho)
            self.assertTrue(os.path.exists(caminho))
        self.assertEqual(plt.get_fignums(), [])


if __name__ == "__main__":
    unittest.main()
