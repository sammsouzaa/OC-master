# Algoritmo Genético - Equipe 9

Trabalho 1 de Otimização Combinatória (2026). Equipe: Samuel Moreira de Souza e Giovanni Nadalin Sansana.

## O problema

Maximizar a **Função 8**, com x e y no intervalo [-10, 10]:

```
Z = 5 + 3x - 4y - x^2 + xy - y^2
```

Ótimo conhecido (só para conferir o resultado): x = 0,667, y = -1,667, Z = 9,333.

## Especificação da equipe

| Item | Escolha |
|---|---|
| Codificação | Real (indivíduo = par `(x, y)`, 3 casas decimais) |
| Seleção | Ranking |
| Cruzamento | BLX-alpha |
| Mutação | Uniforme |
| Elitismo | 0,5% da população (no mínimo 1 indivíduo) |
| Função | 8 |

## Como executar

Precisa de Python 3 com `tkinter`, `matplotlib` e `numpy`.

```bash
# dependências (no Linux o tkinter vem de um pacote à parte)
sudo apt install python3-tk
pip install -r requirements.txt

# rodar o programa (dentro da pasta codigo/)
python3 main.py
```

Para rodar os testes (opcional):

```bash
python3 -m unittest discover -v
```

## Como usar a janela

| Campo | Significado | Padrão |
|---|---|---|
| Tamanho da população | quantos indivíduos por geração | 100 |
| Número de gerações | máximo de gerações | 100 |
| Taxa de cruzamento | chance de um casal cruzar (0 a 1) | 0.8 |
| Taxa de mutação | chance de cada gene mutar (0 a 1) | 0.05 |
| Alpha do BLX | margem do intervalo do BLX-alpha | 0.5 |
| Parar por convergência | para antes se a população convergir | marcado |

Clique em **Executar**. A aba **População** mostra o gráfico de cada geração (com o melhor indivíduo em destaque) e a aba **Fitness médio** mostra o gráfico de linha ao final. Aceita vírgula ou ponto nos números (`0,8` ou `0.8`).

## O que é gerado

| Arquivo | Conteúdo |
|---|---|
| `log.csv` | uma linha por geração: `geracao, fitness_medio, melhor_fitness, melhor_x, melhor_y` |
| `saida/geracao_XXX.png` | gráfico da população em cada geração |
| `saida/fitness_medio.png` | gráfico de linha do fitness médio (e do melhor) |

Esses arquivos são sobrescritos a cada execução.

## Estrutura dos arquivos

| Arquivo | Papel |
|---|---|
| `main.py` | ponto de entrada, só chama a interface |
| `interface.py` | janela tkinter: lê os parâmetros, chama o AG, mostra gráficos e resultado |
| `ag.py` | o algoritmo genético (população, ranking, BLX-alpha, mutação, elitismo, parada) |
| `funcao.py` | Função 8, `arredondar` (3 casas) e `limitar` (mantém no intervalo) |
| `graficos.py` | gera os PNGs com matplotlib |
| `log.py` | grava o `log.csv` |
| `tests/` | testes automatizados (não são exigidos pelo enunciado) |
| `requirements.txt` | dependências |

## Fluxo do código

### 1. Abrir a janela

```
main.py (if __name__ == "__main__")
  -> interface.iniciar()
       -> Aplicacao.__init__
       -> _montar_widgets()
       -> mainloop()          espera o clique em "Executar"
```

### 2. Clicar em Executar

```
interface.executar()
  -> _ler_parametros()        lê e valida os campos, cria ag.Parametros
  -> define o callback ao_fim_de_geracao
  -> ag.executar_ag(params, ao_fim_de_geracao)
```

### 3. Dentro de `ag.executar_ag`

Uma vez, no início:

```
calcular_tamanho_elite()         quantos indivíduos viram elite
criar_populacao_inicial()        lista de (x, y) aleatórios
```

Em cada geração:

```
avaliar()                        fitness de todos (funcao.fitness)
guarda melhor e fitness médio no histórico
ao_fim_de_geracao(...)           callback da interface:
    graficos.grafico_populacao() gera o PNG
    interface._mostrar_imagem()  mostra na aba
convergiu()?                     se sim, para
é a última geração?              se sim, para (não reproduz)
extrair_elite()                  copia os melhores direto pra próxima geração
enquanto faltar gente na população:
    selecionar_por_ranking()     pai1
    selecionar_por_ranking()     pai2
    cruzar_blx_alpha()           sorteia se cruza; se cruzar, _blx_filho -> _blx_gene
    mutar_uniforme()             nos dois filhos, _mutar_gene em x e y
população nova = elite + filhos (corta o excesso)
```

### 4. Depois que o AG termina

```
log.salvar_log()                   grava o log.csv
graficos.grafico_fitness_medio()   gera o gráfico de linha
interface._mostrar_resumo()        mostra melhor x, y e fitness
```

O `ag.py` não conhece a interface. Ele só chama o callback `ao_fim_de_geracao` que recebe como parâmetro, por isso funciona sozinho (é como os testes o usam).

## Resumo do algoritmo

1. A população inicial é uma lista de indivíduos com x e y aleatórios em [-10, 10].
2. O fitness de cada indivíduo é o valor da função 8. O ranking vai do pior (rank 1) ao melhor (rank N).
3. O melhor indivíduo (elite) passa direto para a próxima geração.
4. Os casais são sorteados com chance proporcional ao rank (com reposição), até completar a população.
5. Cada casal cruza com probabilidade igual à taxa de cruzamento. Se não cruzar, os filhos são cópias dos pais.
6. No cruzamento BLX-alpha, cada gene do filho é sorteado entre o menor e o maior valor dos pais, estendido em `alpha * distância` para cada lado.
7. Cada gene dos filhos tem chance igual à taxa de mutação de ser trocado por um valor aleatório em [-10, 10].
8. Todo valor gerado é limitado ao intervalo e arredondado em 3 casas.
9. Repete até acabar o número de gerações ou a população convergir (nunca por atingir o ótimo).

## Critério de convergência

O AG para antes do número de gerações se:

- 80% da população está a menos de 0,05 do melhor indivíduo (em x e em y), ou
- o melhor fitness não melhora há 30 gerações.

Desmarcando "Parar por convergência" na janela, ele roda todas as gerações pedidas.
