# graficos.py
# gráfico da população em cada geração (com o melhor destacado)
# e gráfico de linha do fitness médio
# os dois são salvos em PNG e a interface mostra na janela

import matplotlib.pyplot as plt
import numpy as np

import funcao

# imagem de 500x400 pixels
TAMANHO = (5, 4)
DPI = 100

# grade das curvas de nível, calculada só uma vez
_grade = None


def _obter_grade():
    # calcula o Z de uma grade 100x100 só na primeira chamada
    global _grade

    if _grade is None:
        eixo = np.linspace(funcao.LIMITE_MIN, funcao.LIMITE_MAX, 100)
        X, Y = np.meshgrid(eixo, eixo)
        _grade = (X, Y, funcao.fitness(X, Y))

    return _grade


def grafico_populacao(geracao, populacao, melhor, caminho_png=None):
    fig, ax = plt.subplots(figsize=TAMANHO, dpi=DPI)

    # fundo com as curvas de nível (mais claro = fitness maior)
    X, Y, Z = _obter_grade()
    ax.contourf(X, Y, Z, levels=20, cmap="viridis")

    # população
    xs = [x for x, y in populacao]
    ys = [y for x, y in populacao]
    ax.scatter(xs, ys, s=12, c="white", edgecolors="black", linewidths=0.5,
               label="População")

    # melhor indivíduo destacado
    ax.scatter([melhor[0]], [melhor[1]], s=180, c="red", marker="*",
               edgecolors="black", label="Melhor", zorder=5)

    # eixos fixos pra imagem não pular de uma geração pra outra
    ax.set_xlim(funcao.LIMITE_MIN, funcao.LIMITE_MAX)
    ax.set_ylim(funcao.LIMITE_MIN, funcao.LIMITE_MAX)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Geração {geracao}")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()

    if caminho_png:
        fig.savefig(caminho_png)

    # fecha a figura pra não acumular na memória
    plt.close(fig)


def grafico_fitness_medio(geracoes, fitness_medio, melhor_fitness=None, caminho_png=None):
    fig, ax = plt.subplots(figsize=TAMANHO, dpi=DPI)

    ax.plot(geracoes, fitness_medio, label="Fitness médio")
    if melhor_fitness is not None:
        ax.plot(geracoes, melhor_fitness, label="Melhor fitness")

    ax.set_xlabel("Geração")
    ax.set_ylabel("Fitness")
    ax.set_title("Evolução do fitness")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()

    if caminho_png:
        fig.savefig(caminho_png)

    plt.close(fig)
