# main.py
# ponto de entrada: python3 main.py
#
# problema da equipe 9 (função 8, maximização):
# Z = 5 + 3x - 4y - x^2 + xy - y^2
# intervalo: x em [-10, 10] e y em [-10, 10]
#
# funcao.py     função 8, limites, arredondar e limitar
# ag.py         o algoritmo genético
# graficos.py   gráficos da população e do fitness médio
# log.py        grava o log.csv
# interface.py  janela do tkinter
# saida/        PNGs gerados a cada execução
#
# precisa de matplotlib e numpy (pip install -r requirements.txt)
# o tkinter no linux: sudo apt install python3-tk
#
# testes: python3 -m unittest discover -v

import interface

if __name__ == "__main__":
    interface.iniciar()
