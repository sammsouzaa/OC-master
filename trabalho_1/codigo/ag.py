# ag.py
# Algoritmo Genético da equipe 9
#
# codificação: real (indivíduo = tupla (x, y))
# seleção: ranking
# cruzamento: BLX-alpha
# mutação: uniforme
# elitismo: 0,5% da população
# função: 8 (maximização), está em funcao.py

import random
from dataclasses import dataclass

import funcao

# 0,5% da população vira elite
PERCENTUAL_ELITE = 0.005


@dataclass
class Parametros:
    # os 4 primeiros (e o alpha) vêm da interface
    tamanho_populacao: int
    num_geracoes: int
    taxa_cruzamento: float  # chance de um casal cruzar
    taxa_mutacao: float     # chance de cada gene mutar
    alpha: float = 0.5      # margem do BLX-alpha

    # critério de parada por convergência
    parar_por_convergencia: bool = True
    limiar_diversidade: float = 0.05  # "perto do melhor" = até 0.05 de distância em x e em y
    fracao_convergencia: float = 0.8  # converge se 80% da população está perto do melhor
    geracoes_sem_melhora: int = 30    # ou se o melhor não melhora em 30 gerações


# ---------- população inicial e avaliação ----------

def criar_populacao_inicial(n):
    # cria n indivíduos com x e y aleatórios dentro do domínio
    populacao = []

    for _ in range(n):
        x = funcao.arredondar(random.uniform(funcao.LIMITE_MIN, funcao.LIMITE_MAX))
        y = funcao.arredondar(random.uniform(funcao.LIMITE_MIN, funcao.LIMITE_MAX))
        populacao.append((x, y))

    return populacao


def avaliar(populacao):
    # calcula o fitness de cada indivíduo
    # a posição i da lista de fitness é do indivíduo i da população
    return [funcao.fitness(x, y) for (x, y) in populacao]


# ---------- seleção por ranking ----------

def selecionar_por_ranking(populacao, fitnesses):
    # sorteia um pai usando ranking
    # o pior fica com rank 1 e o melhor com rank n
    # a chance de cada um é proporcional ao rank (rank / soma dos ranks)
    # o que conta é a posição, não o valor do fitness
    n = len(populacao)

    # índices ordenados do pior para o melhor fitness
    ordem = sorted(range(n), key=lambda i: fitnesses[i])

    # ranks 1, 2, ..., n na mesma ordem de "ordem"
    ranks = list(range(1, n + 1))

    # sorteia um índice usando os ranks como pesos
    indice = random.choices(ordem, weights=ranks, k=1)[0]
    return populacao[indice]


# ---------- cruzamento BLX-alpha ----------

def _blx_gene(gene1, gene2, alpha):
    # BLX-alpha para um gene
    # d é a distância entre os genes dos pais
    # o filho é sorteado entre (menor - alpha*d) e (maior + alpha*d)
    d = abs(gene1 - gene2)
    minimo = min(gene1, gene2) - alpha * d
    maximo = max(gene1, gene2) + alpha * d
    valor = random.uniform(minimo, maximo)

    # o intervalo pode passar do domínio, então limita e arredonda
    return funcao.arredondar(funcao.limitar(valor))


def _blx_filho(pai1, pai2, alpha):
    # um filho: aplica o BLX em x e em y separadamente
    x = _blx_gene(pai1[0], pai2[0], alpha)
    y = _blx_gene(pai1[1], pai2[1], alpha)
    return (x, y)


def cruzar_blx_alpha(pai1, pai2, alpha, taxa_cruzamento):
    # sorteia um número de 0 a 1, se for menor que a taxa o casal cruza
    if random.random() < taxa_cruzamento:
        # cada filho faz sorteios novos, por isso saem diferentes
        filho1 = _blx_filho(pai1, pai2, alpha)
        filho2 = _blx_filho(pai1, pai2, alpha)
        return filho1, filho2

    # não cruzou: os filhos são cópias dos pais
    return pai1, pai2


# ---------- mutação uniforme ----------

def _mutar_gene(gene, taxa_mutacao):
    # se o sorteio for menor que a taxa, troca o gene por um valor qualquer do domínio
    if random.random() < taxa_mutacao:
        novo = random.uniform(funcao.LIMITE_MIN, funcao.LIMITE_MAX)
        return funcao.arredondar(novo)

    return gene


def mutar_uniforme(individuo, taxa_mutacao):
    # a taxa vale para cada gene, então x e y são sorteados separadamente
    x, y = individuo
    return (_mutar_gene(x, taxa_mutacao), _mutar_gene(y, taxa_mutacao))


# ---------- elitismo ----------

def calcular_tamanho_elite(tamanho_populacao):
    # 0,5% da população, mas no mínimo 1
    # com população 100 dá 0,5, e o round() do python arredonda 0.5 para 0,
    # por isso o max(1, ...)
    n_elite = max(1, round(PERCENTUAL_ELITE * tamanho_populacao))

    # a elite não pode ocupar a população inteira
    return min(n_elite, tamanho_populacao - 1)


def extrair_elite(populacao, fitnesses, n_elite):
    # pega os n_elite melhores, eles vão direto pra próxima geração
    ordem = sorted(range(len(populacao)), key=lambda i: fitnesses[i], reverse=True)
    return [populacao[i] for i in ordem[:n_elite]]


# ---------- convergência ----------

def convergiu(populacao, historico_melhor, params):
    # retorna True se a população convergiu (nenhum critério usa o valor do ótimo)
    if not params.parar_por_convergencia:
        return False

    # critério 1: a maior parte da população está perto do melhor
    # (não usei desvio padrão porque a mutação uniforme sempre deixa uns mutantes longe)
    melhor_x, melhor_y = max(populacao, key=lambda ind: funcao.fitness(*ind))
    perto = 0
    for x, y in populacao:
        if (abs(x - melhor_x) <= params.limiar_diversidade
                and abs(y - melhor_y) <= params.limiar_diversidade):
            perto += 1
    if perto / len(populacao) >= params.fracao_convergencia:
        return True

    # critério 2: o melhor fitness parou de melhorar
    k = params.geracoes_sem_melhora
    if len(historico_melhor) > k:
        melhora = historico_melhor[-1] - historico_melhor[-1 - k]
        if melhora < 1e-6:
            return True

    return False


# ---------- loop principal ----------

def executar_ag(params, ao_fim_de_geracao=None):
    # roda o AG e devolve o histórico
    # ao_fim_de_geracao é uma função opcional chamada no fim de cada geração
    # (a interface usa pra desenhar o gráfico, assim o ag.py não depende do tkinter)
    historico = {
        "geracoes": [],
        "fitness_medio": [],
        "melhor_fitness": [],
        "melhor_x": [],
        "melhor_y": [],
    }

    n = params.tamanho_populacao
    n_elite = calcular_tamanho_elite(n)
    populacao = criar_populacao_inicial(n)

    for geracao in range(1, params.num_geracoes + 1):
        # calcula o fitness de todos
        fitnesses = avaliar(populacao)

        # melhor indivíduo e fitness médio da geração
        i_melhor = fitnesses.index(max(fitnesses))
        melhor = populacao[i_melhor]
        melhor_fitness = fitnesses[i_melhor]
        fitness_medio = sum(fitnesses) / n

        # guarda no histórico (vira o log.csv e o gráfico de linha)
        historico["geracoes"].append(geracao)
        historico["fitness_medio"].append(fitness_medio)
        historico["melhor_fitness"].append(melhor_fitness)
        historico["melhor_x"].append(melhor[0])
        historico["melhor_y"].append(melhor[1])

        # avisa a interface (gráfico da população)
        if ao_fim_de_geracao is not None:
            ao_fim_de_geracao(geracao, populacao, fitnesses, melhor, melhor_fitness)

        # para se convergiu ou se é a última geração
        # na última não reproduz, porque a nova população nunca seria avaliada
        if convergiu(populacao, historico["melhor_fitness"], params):
            break
        if geracao == params.num_geracoes:
            break

        # próxima geração: primeiro a elite
        proxima = extrair_elite(populacao, fitnesses, n_elite)

        # depois os filhos, até completar a população
        while len(proxima) < n:
            pai1 = selecionar_por_ranking(populacao, fitnesses)
            pai2 = selecionar_por_ranking(populacao, fitnesses)
            filho1, filho2 = cruzar_blx_alpha(pai1, pai2, params.alpha, params.taxa_cruzamento)
            proxima.append(mutar_uniforme(filho1, params.taxa_mutacao))
            proxima.append(mutar_uniforme(filho2, params.taxa_mutacao))

        # cada casal dá 2 filhos, então pode sobrar 1: corta no tamanho certo
        populacao = proxima[:n]

    # com elitismo o melhor da última geração é o melhor de todas
    historico["melhor_final"] = melhor
    return historico
