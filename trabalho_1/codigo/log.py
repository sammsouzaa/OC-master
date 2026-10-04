# log.py
# grava o log do AG em csv, uma linha por geração
# colunas: geracao, fitness_medio, melhor_fitness, melhor_x, melhor_y

import csv

COLUNAS = ["geracao", "fitness_medio", "melhor_fitness", "melhor_x", "melhor_y"]


def salvar_log(historico, caminho="log.csv"):
    # newline="" evita linhas em branco no windows
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(COLUNAS)

        # o zip percorre as 5 listas do histórico juntas, uma geração por vez
        for geracao, medio, melhor, x, y in zip(historico["geracoes"],
                                                historico["fitness_medio"],
                                                historico["melhor_fitness"],
                                                historico["melhor_x"],
                                                historico["melhor_y"]):
            # arredonda o fitness só pra deixar o arquivo legível
            escritor.writerow([geracao, round(medio, 6), round(melhor, 6), x, y])
