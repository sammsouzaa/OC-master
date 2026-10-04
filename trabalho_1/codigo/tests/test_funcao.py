# testes do funcao.py
# rodar tudo (dentro de codigo/): python3 -m unittest discover -v
# rodar só este arquivo: python3 -m unittest tests.test_funcao -v

import unittest

import funcao


class TestFitness(unittest.TestCase):
    def test_otimo_conhecido(self):
        # o ótimo do PDF é (0.6667, -1.6667) com z = 9.3333
        self.assertAlmostEqual(funcao.fitness(2 / 3, -5 / 3), 28 / 3, places=6)
        self.assertAlmostEqual(funcao.fitness(0.667, -1.667), 9.3333, places=3)

    def test_valores_calculados_a_mao(self):
        self.assertEqual(funcao.fitness(0, 0), 5)
        self.assertEqual(funcao.fitness(1, 1), 3)         # 5 + 3 - 4 - 1 + 1 - 1
        self.assertEqual(funcao.fitness(10, 10), -105)    # 5 + 30 - 40 - 100 + 100 - 100

    def test_vizinhos_do_otimo_sao_piores(self):
        # é maximização: qualquer deslocamento a partir do ótimo diminui o fitness
        otimo = funcao.fitness(2 / 3, -5 / 3)
        for dx, dy in [(0.1, 0), (-0.1, 0), (0, 0.1), (0, -0.1), (0.1, 0.1)]:
            self.assertLess(funcao.fitness(2 / 3 + dx, -5 / 3 + dy), otimo)


class TestArredondar(unittest.TestCase):
    def test_tres_casas(self):
        self.assertEqual(funcao.arredondar(1.23456), 1.235)

    def test_ja_arredondado_nao_muda(self):
        self.assertEqual(funcao.arredondar(2.5), 2.5)


class TestLimitar(unittest.TestCase):
    def test_dentro_do_intervalo_nao_muda(self):
        self.assertEqual(funcao.limitar(3.0), 3.0)

    def test_acima_do_maximo(self):
        self.assertEqual(funcao.limitar(15), funcao.LIMITE_MAX)

    def test_abaixo_do_minimo(self):
        self.assertEqual(funcao.limitar(-15), funcao.LIMITE_MIN)

    def test_bordas_exatas(self):
        self.assertEqual(funcao.limitar(funcao.LIMITE_MIN), funcao.LIMITE_MIN)
        self.assertEqual(funcao.limitar(funcao.LIMITE_MAX), funcao.LIMITE_MAX)


if __name__ == "__main__":
    unittest.main()
