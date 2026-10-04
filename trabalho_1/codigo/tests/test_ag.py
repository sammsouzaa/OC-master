# testes dos operadores e do loop do ag.py
# como os operadores são aleatórios, os testes conferem propriedades
# (limites, casas decimais, frequências) e não valores exatos
# a semente é fixada no setUp pro resultado ser sempre o mesmo

import random
import unittest
from collections import Counter

import ag
import funcao


def casas_ok(valor):
    # True se o valor tem no máximo 3 casas decimais
    return round(valor, 3) == valor


def dentro_dos_limites(individuo):
    # True se x e y estão dentro do domínio
    return all(funcao.LIMITE_MIN <= g <= funcao.LIMITE_MAX for g in individuo)


def individuo_valido(individuo):
    return dentro_dos_limites(individuo) and all(casas_ok(g) for g in individuo)


class TestPopulacaoInicial(unittest.TestCase):
    def setUp(self):
        random.seed(42)

    def test_tamanho(self):
        self.assertEqual(len(ag.criar_populacao_inicial(37)), 37)

    def test_dentro_dos_limites(self):
        for ind in ag.criar_populacao_inicial(500):
            self.assertTrue(dentro_dos_limites(ind))

    def test_tres_casas_decimais(self):
        for ind in ag.criar_populacao_inicial(500):
            self.assertTrue(all(casas_ok(g) for g in ind))


class TestAvaliar(unittest.TestCase):
    def test_mesma_ordem_e_tamanho(self):
        populacao = [(0, 0), (1, 1), (10, 10)]
        self.assertEqual(ag.avaliar(populacao), [5, 3, -105])


class TestSelecaoRanking(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        # 4 indivíduos distintos; o fitness é dado à parte, de propósito
        self.populacao = [(0, 0), (1, 1), (2, 2), (3, 3)]

    def frequencias(self, fitnesses, sorteios=5000):
        # sorteia muitas vezes e devolve a frequência de cada indivíduo
        contagem = Counter(ag.selecionar_por_ranking(self.populacao, fitnesses)
                           for _ in range(sorteios))
        return [contagem[ind] / sorteios for ind in self.populacao]

    def test_retorna_individuo_da_populacao(self):
        pai = ag.selecionar_por_ranking(self.populacao, [3, 10, -5, 7])
        self.assertIn(pai, self.populacao)

    def test_probabilidades_seguem_o_ranking(self):
        # fitness [3, 10, -5, 7] -> ranks [2, 4, 1, 3] -> prob. [0.2, 0.4, 0.1, 0.3]
        freq = self.frequencias([3, 10, -5, 7])
        for obtida, esperada in zip(freq, [0.2, 0.4, 0.1, 0.3]):
            self.assertAlmostEqual(obtida, esperada, delta=0.04)

    def test_usa_rank_e_nao_valor_do_fitness(self):
        # mesma ordem, escalas muito diferentes -> mesmas probabilidades
        freq_a = self.frequencias([1, 2, 3, 4])
        freq_b = self.frequencias([1, 2, 3, 1000])
        for a, b in zip(freq_a, freq_b):
            self.assertAlmostEqual(a, b, delta=0.04)

    def test_funciona_com_fitness_negativo(self):
        freq = self.frequencias([-100, -50, -10, -1])
        self.assertAlmostEqual(sum(freq), 1.0)

    def test_direcao_maximizacao(self):
        # o de maior fitness deve ser o mais sorteado
        freq = self.frequencias([1, 2, 3, 4])
        self.assertEqual(freq.index(max(freq)), 3)
        self.assertEqual(freq.index(min(freq)), 0)


class TestCruzamentoBLX(unittest.TestCase):
    def setUp(self):
        random.seed(42)

    def test_retorna_dois_filhos(self):
        filhos = ag.cruzar_blx_alpha((1, 1), (3, 3), 0.5, 1.0)
        self.assertEqual(len(filhos), 2)
        self.assertEqual(len(filhos[0]), 2)

    def test_taxa_zero_filhos_sao_copias_dos_pais(self):
        self.assertEqual(ag.cruzar_blx_alpha((1, 2), (3, 4), 0.5, 0.0), ((1, 2), (3, 4)))

    def test_taxa_um_filhos_dentro_do_intervalo_blx(self):
        # x: pais 2 e 4, alpha 0.5 -> [1, 5];  y: pais -1 e 3, d = 4 -> [-3, 5]
        for _ in range(1000):
            for x, y in ag.cruzar_blx_alpha((2, -1), (4, 3), 0.5, 1.0):
                self.assertTrue(1 <= x <= 5)
                self.assertTrue(-3 <= y <= 5)

    def test_alpha_zero_filho_entre_os_pais(self):
        for _ in range(1000):
            for x, y in ag.cruzar_blx_alpha((2, -1), (4, 3), 0.0, 1.0):
                self.assertTrue(2 <= x <= 4)
                self.assertTrue(-1 <= y <= 3)

    def test_pais_iguais_geram_filhos_iguais(self):
        filhos = ag.cruzar_blx_alpha((2.5, -1.5), (2.5, -1.5), 0.5, 1.0)
        self.assertEqual(filhos, ((2.5, -1.5), (2.5, -1.5)))

    def test_filhos_sao_diferentes_entre_si(self):
        # cada filho faz sorteios próprios
        filho1, filho2 = ag.cruzar_blx_alpha((-5, -5), (5, 5), 0.5, 1.0)
        self.assertNotEqual(filho1, filho2)

    def test_respeita_limites_e_casas(self):
        for _ in range(1000):
            for filho in ag.cruzar_blx_alpha((9.9, -9.9), (10, -10), 1.0, 1.0):
                self.assertTrue(individuo_valido(filho))


class TestMutacaoUniforme(unittest.TestCase):
    def setUp(self):
        random.seed(42)

    def test_taxa_zero_nao_muda(self):
        self.assertEqual(ag.mutar_uniforme((1.5, -2.5), 0.0), (1.5, -2.5))

    def test_taxa_um_muda_todos_os_genes(self):
        mudou = sum(ag.mutar_uniforme((1.5, -2.5), 1.0) != (1.5, -2.5) for _ in range(200))
        self.assertGreater(mudou, 195)

    def test_taxa_aproximada_por_gene(self):
        total, mutados = 5000, 0
        for _ in range(total):
            x, y = ag.mutar_uniforme((1.5, -2.5), 0.2)
            mutados += (x != 1.5) + (y != -2.5)
        self.assertAlmostEqual(mutados / (2 * total), 0.2, delta=0.03)

    def test_respeita_limites_e_casas(self):
        for _ in range(1000):
            self.assertTrue(individuo_valido(ag.mutar_uniforme((0, 0), 1.0)))


class TestElitismo(unittest.TestCase):
    def test_tamanho_elite_populacao_200(self):
        self.assertEqual(ag.calcular_tamanho_elite(200), 1)

    def test_tamanho_elite_minimo_um(self):
        for n in (2, 10, 50, 100):
            self.assertEqual(ag.calcular_tamanho_elite(n), 1)

    def test_tamanho_elite_populacao_grande(self):
        self.assertEqual(ag.calcular_tamanho_elite(1000), 5)
        self.assertEqual(ag.calcular_tamanho_elite(2000), 10)

    def test_extrair_elite_pega_os_melhores(self):
        populacao = [(0, 0), (1, 1), (2, 2), (3, 3)]
        self.assertEqual(ag.extrair_elite(populacao, [3, 10, -5, 7], 2), [(1, 1), (3, 3)])

    def test_extrair_elite_nao_altera_populacao_original(self):
        populacao = [(0, 0), (1, 1), (2, 2)]
        fitnesses = [5, 9, 1]
        ag.extrair_elite(populacao, fitnesses, 1)
        self.assertEqual(populacao, [(0, 0), (1, 1), (2, 2)])
        self.assertEqual(fitnesses, [5, 9, 1])


class TestConvergencia(unittest.TestCase):
    def setUp(self):
        self.params = ag.Parametros(100, 100, 0.8, 0.05)

    def test_populacao_identica_convergiu(self):
        self.assertTrue(ag.convergiu([(1.0, 1.0)] * 50, [1.0], self.params))

    def test_populacao_diversa_nao_convergiu(self):
        random.seed(42)
        populacao = ag.criar_populacao_inicial(100)
        self.assertFalse(ag.convergiu(populacao, [1.0], self.params))

    def test_estagnacao(self):
        populacao = [(float(i), float(i)) for i in range(-5, 5)]  # diversa
        self.assertTrue(ag.convergiu(populacao, [5.0] * 40, self.params))
        self.assertFalse(ag.convergiu(populacao, list(range(40)), self.params))

    def test_desligado_nunca_converge(self):
        self.params.parar_por_convergencia = False
        self.assertFalse(ag.convergiu([(1.0, 1.0)] * 50, [5.0] * 100, self.params))


class TestExecutarAG(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        # convergência desligada: roda todas as gerações pedidas
        self.params = ag.Parametros(
            tamanho_populacao=50, num_geracoes=30,
            taxa_cruzamento=0.8, taxa_mutacao=0.05, alpha=0.5,
            parar_por_convergencia=False)

    def test_historico_tem_as_chaves_esperadas(self):
        h = ag.executar_ag(self.params)
        for chave in ("geracoes", "fitness_medio", "melhor_fitness",
                      "melhor_x", "melhor_y", "melhor_final"):
            self.assertIn(chave, h)

    def test_listas_do_historico_tem_mesmo_tamanho(self):
        h = ag.executar_ag(self.params)
        for chave in ("geracoes", "fitness_medio", "melhor_fitness", "melhor_x", "melhor_y"):
            self.assertEqual(len(h[chave]), 30)

    def test_melhor_fitness_nunca_cai(self):
        mf = ag.executar_ag(self.params)["melhor_fitness"]
        for anterior, atual in zip(mf, mf[1:]):
            self.assertGreaterEqual(atual, anterior)

    def test_tamanho_da_populacao_constante_mesmo_impar(self):
        for n in (50, 51):
            self.params.tamanho_populacao = n
            tamanhos = []
            ag.executar_ag(self.params, lambda g, pop, f, m, mf: tamanhos.append(len(pop)))
            self.assertEqual(set(tamanhos), {n})

    def test_callback_chamado_uma_vez_por_geracao(self):
        geracoes = []
        ag.executar_ag(self.params, lambda g, pop, f, m, mf: geracoes.append(g))
        self.assertEqual(geracoes, list(range(1, 31)))

    def test_aproxima_do_otimo(self):
        self.params.tamanho_populacao = 100
        self.params.num_geracoes = 100
        h = ag.executar_ag(self.params)
        x, y = h["melhor_final"]
        self.assertAlmostEqual(x, 2 / 3, delta=0.1)
        self.assertAlmostEqual(y, -5 / 3, delta=0.1)
        self.assertAlmostEqual(h["melhor_fitness"][-1], 28 / 3, delta=0.01)

    def test_reprodutivel_com_mesma_semente(self):
        random.seed(7)
        h1 = ag.executar_ag(self.params)
        random.seed(7)
        h2 = ag.executar_ag(self.params)
        self.assertEqual(h1, h2)

    def test_nao_para_so_por_atingir_o_otimo(self):
        # sem convergência, roda todas as gerações mesmo que o ótimo já tenha sido achado
        self.params.num_geracoes = 60
        self.params.tamanho_populacao = 100
        h = ag.executar_ag(self.params)
        self.assertEqual(len(h["geracoes"]), 60)

    def test_todos_os_individuos_validos_em_todas_as_geracoes(self):
        def confere(g, populacao, f, m, mf):
            for ind in populacao:
                self.assertTrue(individuo_valido(ind))
        ag.executar_ag(self.params, confere)

    def test_melhor_final_e_o_ultimo_melhor_registrado(self):
        h = ag.executar_ag(self.params)
        self.assertEqual(h["melhor_final"], (h["melhor_x"][-1], h["melhor_y"][-1]))


if __name__ == "__main__":
    unittest.main()
