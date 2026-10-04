# funcao.py
# Função 8 da equipe 9: Z = 5 + 3x - 4y - x^2 + xy - y^2, com x e y em [-10, 10]
# é maximização (quanto maior o Z, melhor)
# ótimo conhecido: x = 0.6667, y = -1.6667, Z = 9.3333 (só pra conferir o resultado)

# limites do espaço de busca, valem para x e para y
LIMITE_MIN = -10.0
LIMITE_MAX = 10.0

# o enunciado pede 3 casas decimais
CASAS_DECIMAIS = 3


def fitness(x, y):
    # valor da função 8, que é o fitness do indivíduo
    # também funciona com arrays do numpy (usado no gráfico)
    return 5 + 3 * x - 4 * y - x ** 2 + x * y - y ** 2


def arredondar(valor):
    # arredonda o gene em 3 casas
    return round(valor, CASAS_DECIMAIS)


def limitar(valor):
    # não deixa o gene sair de [LIMITE_MIN, LIMITE_MAX]
    # o BLX-alpha pode gerar valores fora do domínio
    if valor > LIMITE_MAX:
        return LIMITE_MAX
    if valor < LIMITE_MIN:
        return LIMITE_MIN
    return valor
