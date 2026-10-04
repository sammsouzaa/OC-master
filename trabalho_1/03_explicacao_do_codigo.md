# Explicação completa do código — Equipe 9

Este documento explica **o que cada arquivo e cada função faz e por quê**, e o fluxo de uma execução do início ao fim. Use junto com o roteiro de slides (`02_roteiro_de_estudo_slides.md`) para estudar e se preparar para a apresentação.

Pasta: `codigo/`

```
codigo/
├── main.py         ponto de entrada
├── interface.py    janela tkinter (parâmetros, botão, abas com os gráficos)
├── ag.py           o Algoritmo Genético (coração do trabalho)
├── funcao.py       Função 8 + funções auxiliares sobre os genes
├── graficos.py     gráficos (matplotlib) gravados em PNG
├── log.py          grava o log.csv
├── saida/          PNGs gerados a cada execução (geracao_001.png, ..., fitness_medio.png)
├── log.csv         gerado a cada execução
└── tests/          56 testes automatizados (unittest)
```

---

## 1. Visão geral do problema e das escolhas

**Problema:** maximizar `Z = 5 + 3x − 4y − x² + xy − y²`, com `x, y ∈ [−10, 10]`. Ótimo conhecido: `x = 2/3 ≈ 0,667`, `y = −5/3 ≈ −1,667`, `Z = 28/3 ≈ 9,333`.

**Especificação da Equipe 9 (e onde está no código):**

| Item | Escolha | Onde |
|---|---|---|
| Codificação | Real: indivíduo = tupla `(x, y)` com 3 casas decimais | `funcao.arredondar`, `ag.criar_populacao_inicial` |
| Seleção | Ranking | `ag.selecionar_por_ranking` |
| Cruzamento | BLX-α | `ag.cruzar_blx_alpha` (+ `_blx_filho`, `_blx_gene`) |
| Mutação | Uniforme | `ag.mutar_uniforme` (+ `_mutar_gene`) |
| Elitismo | 0,5% da população (mínimo 1) | `ag.calcular_tamanho_elite`, `ag.extrair_elite` |
| Parada | Nº de gerações **ou** convergência (nunca o ótimo) | `ag.executar_ag`, `ag.convergiu` |

**Conceitos usados no código:**
- **Indivíduo** = tupla `(x, y)`. Tuplas são imutáveis, então nenhum operador altera um pai por acidente.
- **Fitness** = o próprio `Z`. Maior é melhor.
- **População** = lista de tuplas. O **fitness** fica numa lista **paralela** (`fitnesses[i]` pertence a `populacao[i]`).

---

## 2. Fluxo de uma execução (visão de cima)

```
main.py
  └─ interface.iniciar()  abre a janela
        │  usuário preenche parâmetros e clica "Executar"
        ▼
  Aplicacao.executar()
     1. _ler_parametros()     lê e valida -> ag.Parametros
     2. limpa PNGs antigos de saida/
     3. ag.executar_ag(params, ao_fim_de_geracao)
           │
           │   para cada geração:
           │     avaliar -> estatísticas -> histórico -> callback -> parada? -> próxima geração
           │                                              │
           │                                              └─ callback = ao_fim_de_geracao (da interface):
           │                                                   graficos.grafico_populacao(...) -> PNG
           │                                                   mostra o PNG na aba "População"
           ▼
     4. log.salvar_log(historico)               -> log.csv
     5. graficos.grafico_fitness_medio(...)     -> saida/fitness_medio.png (aba "Fitness médio")
     6. mostra o resumo (melhor x, y, fitness)
```

**Por que existe o callback `ao_fim_de_geracao`?** Para o `ag.py` não depender de tkinter nem de matplotlib. O AG apenas "avisa" quem quiser ouvir ao fim de cada geração; a interface decide o que fazer (desenhar gráfico, atualizar texto). Isso também deixa o AG testável sozinho, sem janela.

### Fluxo detalhado de uma geração dentro de `executar_ag`

```
população g  ──avaliar──▶ fitnesses
     │
     ├─ acha melhor indivíduo e fitness médio
     ├─ guarda no histórico (vira o log e o gráfico de linha)
     ├─ chama o callback (gráfico da população)
     ├─ convergiu?  ──sim──▶ para
     ├─ é a última geração? ──sim──▶ para
     │
     ▼ constrói a população g+1:
   elite  = os n_elite melhores (copiados sem alteração)
   enquanto faltar gente:
        pai1, pai2 = selecionar_por_ranking (2 vezes)
        f1, f2     = cruzar_blx_alpha(pai1, pai2)
        f1, f2     = mutar_uniforme(f1), mutar_uniforme(f2)
        adiciona f1 e f2
   corta o excesso (se sobrou 1)  ──▶ população g+1
```

Esse é o mesmo ciclo do slide 37 (Goldberg): inicializa, avalia, seleciona, cruza, muta, avalia.

---

## 3. `funcao.py`

### Constantes
- `LIMITE_MIN = -10.0`, `LIMITE_MAX = 10.0`: domínio de x e y.
- `CASAS_DECIMAIS = 3`: exigência do enunciado.

### `fitness(x, y)`
Retorna `5 + 3x − 4y − x² + xy − y²`. É só a fórmula do PDF. Como usa apenas operações aritméticas, funciona também com arrays do numpy, e o `graficos.py` aproveita isso para calcular a grade das curvas de nível de uma vez.

### `arredondar(valor)`
`round(valor, 3)`. É chamada depois de **todo** operador genético para garantir 3 casas.

### `limitar(valor)`
"Clamp": se `valor > 10` devolve `10`; se `valor < −10` devolve `−10`; senão devolve o valor. Necessária porque o BLX-α pode sortear fora do domínio.

---

## 4. `ag.py` (o arquivo mais importante)

### `PERCENTUAL_ELITE = 0.005`
Os 0,5% do enunciado, em forma decimal.

### `Parametros` (dataclass)
Agrupa os parâmetros em um objeto só, para não passar uma lista longa de argumentos.

| Campo | Significado | Vem de |
|---|---|---|
| `tamanho_populacao` | N indivíduos | interface |
| `num_geracoes` | máximo de gerações | interface |
| `taxa_cruzamento` | prob. de um par realmente cruzar | interface |
| `taxa_mutacao` | prob. de **cada gene** mutar | interface |
| `alpha` | extensão do BLX (padrão 0,5) | interface |
| `parar_por_convergencia` | liga/desliga a parada por convergência | caixinha da interface |
| `limiar_diversidade` | "perto do melhor" = distância ≤ 0,05 em x e em y | valor padrão |
| `fracao_convergencia` | converge se ≥ 80% da população está perto do melhor | valor padrão |
| `geracoes_sem_melhora` | converge se o melhor não melhorou em 30 gerações | valor padrão |

### `criar_populacao_inicial(n)`
Cria `n` indivíduos. Para cada um, sorteia `x` e `y` com `random.uniform(−10, 10)` e arredonda para 3 casas. Retorna a lista de tuplas. Cobre todo o espaço de busca de forma uniforme (slide 38).

### `avaliar(populacao)`
Devolve `[fitness(x, y) para cada (x, y)]`. **A posição `i` da saída corresponde ao indivíduo `i`**; todo o resto do código depende desse alinhamento.

### `selecionar_por_ranking(populacao, fitnesses)`  (slides 45–47)
Sorteia **um** pai.
1. `ordem = sorted(range(n), key=lambda i: fitnesses[i])`: índices do **pior para o melhor**.
2. `ranks = [1, 2, ..., n]`: o pior tem rank 1, o melhor rank `n`.
3. `random.choices(ordem, weights=ranks, k=1)[0]`: sorteia um índice com peso = rank. A chance de cada um é `rank / (1+2+…+n)`.
4. Devolve `populacao[indice]`.

**Ponto-chave:** só a posição no ranking conta, não o valor do fitness. Um indivíduo com fitness 1000 e outro com 4 têm as mesmas chances se ocupam os mesmos ranks. Isso evita a "dominância" que ocorre na roleta e funciona com fitness negativo (nesta função há fitness muito negativos, como −100).

Exemplo: fitness `[3, 10, −5, 7]` dá ranks `[2, 4, 1, 3]` e probabilidades `[0,2; 0,4; 0,1; 0,3]`.

### `_blx_gene(gene1, gene2, alpha)` (auxiliar)
BLX-α para **um gene**:
- `d = |gene1 − gene2|`
- intervalo = `[min − α·d, max + α·d]`
- `valor = random.uniform(intervalo)`
- `arredondar(limitar(valor))`

Com `α = 0,5` o intervalo é 50% maior que o dos pais em cada ponta. Isso permite explorar um pouco **além** dos pais. Se os pais são iguais, `d = 0` e o filho é igual a eles. Equivale à fórmula do slide 57, `F1 = P1 + β(P2 − P1)` com `β ∈ [−α, 1+α]`.

### `_blx_filho(pai1, pai2, alpha)` (auxiliar)
Aplica `_blx_gene` ao `x` e depois ao `y` (separadamente) e monta a tupla do filho.

### `cruzar_blx_alpha(pai1, pai2, alpha, taxa_cruzamento)`  (slides 57 e 59)
- Sorteia `random.random()`. Se for **menor que a taxa**, cruza: gera `filho1` e `filho2` chamando `_blx_filho` **duas vezes** (cada chamada faz sorteios novos, por isso saem diferentes).
- Senão, devolve `(pai1, pai2)` sem alteração (os pais passam adiante).
- Taxa 0 nunca cruza; taxa 1 sempre cruza (porque `random()` está em `[0, 1)`).

### `_mutar_gene(gene, taxa_mutacao)` (auxiliar)
Sorteia `random.random()`. Se for menor que a taxa, **troca o gene** por `random.uniform(−10, 10)` (arredondado). Senão, devolve o gene como estava.

### `mutar_uniforme(individuo, taxa_mutacao)`  (slides 62 e 64)
Chama `_mutar_gene` em `x` e em `y` **independentemente** e devolve a tupla nova. A taxa vale **por gene**: com taxa 0,05, cada gene tem 5% de chance, e o número esperado de genes mutados por indivíduo é 0,1. Mutação uniforme é "agressiva": o gene vai para qualquer ponto do domínio, daí a taxa ser baixa.

### `calcular_tamanho_elite(tamanho_populacao)`
`max(1, round(0.005 × N))`, limitado a `N − 1`.
- Para N = 100, 0,5% dá 0,5, e `round(0.5)` em Python devolve `0` (arredonda para o par), por isso o `max(1, …)`: garante **pelo menos 1** elite.
- N = 200 dá 1; N = 1000 dá 5.
- O `min(…, N − 1)` é só segurança para populações minúsculas.

### `extrair_elite(populacao, fitnesses, n_elite)`  (slide 65)
Ordena os **índices** do melhor para o pior (`reverse=True`) e devolve os `n_elite` primeiros indivíduos. Não altera a lista original. Esses indivíduos vão para a próxima geração **sem cruzar e sem mutar**, garantindo que o melhor fitness nunca piore.

### `convergiu(populacao, historico_melhor, params)`  (slide 69)
Decide se pára antes de completar `num_geracoes`. Retorna `False` se `parar_por_convergencia` estiver desligado. Dois critérios, e **nenhum olha o valor 9,333** (o enunciado proíbe parar por atingir o ótimo):

1. **População concentrada:** acha o melhor indivíduo, conta quantos estão a no máximo `limiar_diversidade` (0,05) dele em `x` **e** em `y`. Se essa fração for ≥ `fracao_convergencia` (80%), converge.
   - *Por que não usar desvio padrão?* A mutação uniforme sempre joga alguns genes para pontos aleatórios, então o desvio padrão da população nunca fica pequeno. Contar quem está perto do melhor é imune a esses poucos mutantes.
2. **Estagnação:** se `melhor_fitness` não melhorou (ganho < 1e-6) nas últimas `geracoes_sem_melhora` (30) gerações. Compara `historico_melhor[-1]` com `historico_melhor[-1-30]`.

### `executar_ag(params, ao_fim_de_geracao=None)`
O loop principal. Passo a passo:
1. Cria o `historico` (dicionário com listas vazias para cada coluna do log).
2. Calcula `n` e `n_elite` uma vez e cria a população inicial.
3. Para cada geração `g = 1 … num_geracoes`:
   1. `fitnesses = avaliar(populacao)`.
   2. Acha `i_melhor` (índice do maior fitness), `melhor`, `melhor_fitness` e `fitness_medio = soma / n`.
   3. Acrescenta g, média, melhor fitness, melhor x e melhor y no histórico.
   4. Chama o callback (se existir).
   5. Se `convergiu(...)`, sai do loop. Se `g` é a última, também sai.
      *(Na última geração não reproduz: a população nova nunca seria avaliada nem registrada.)*
   6. Monta a próxima população: começa com a **elite**; enquanto tiver menos que `n`, seleciona 2 pais, cruza, muta os 2 filhos e adiciona. Como cada rodada adiciona 2, pode sobrar 1: `proxima[:n]` corta.
4. Ao fim, `historico["melhor_final"] = melhor` (o melhor da última geração avaliada; com elitismo é também o melhor de todas).
5. Devolve o histórico.

**Estrutura do `historico`:**
```
{ "geracoes": [1, 2, ...], "fitness_medio": [...], "melhor_fitness": [...],
  "melhor_x": [...], "melhor_y": [...], "melhor_final": (x, y) }
```
Esse formato é o "contrato" com `log.py` e `interface.py`.

---

## 5. `graficos.py`

- `TAMANHO = (5, 4)` e `DPI = 100`: imagem de 500×400 pixels (cabe na janela).
- `_grade`: variável de módulo que guarda a grade de Z, para calcular só uma vez.

### `_obter_grade()`
Na primeira chamada, cria 100 valores entre −10 e 10 (`numpy.linspace`), monta a grade 100×100 (`meshgrid`) e calcula `fitness(X, Y)` nos 10 mil pontos de uma vez. Nas chamadas seguintes reaproveita. Sem esse cache, cada geração recalcularia tudo.

### `grafico_populacao(geracao, populacao, melhor, caminho_png)`
1. Cria a figura. 2. Desenha o **fundo** com `contourf` (curvas de nível: regiões claras = fitness maior). 3. `scatter` de toda a população (pontos brancos com borda preta). 4. `scatter` do melhor como **estrela vermelha grande** (o destaque pedido pelo enunciado). 5. Fixa os eixos em [−10, 10] (a imagem não "pula"), título "Geração N", legenda. 6. Salva o PNG. 7. **`plt.close(fig)`**: libera a memória.

### `grafico_fitness_medio(geracoes, fitness_medio, melhor_fitness, caminho_png)`
Gráfico de linha: fitness médio por geração e (opcional) melhor fitness. Eixos, grade, legenda, salva e fecha. Esperado: o melhor fica colado em ~9,33 e a média sobe e se estabiliza **abaixo** dele (os mutantes uniformes puxam a média para baixo).

---

## 6. `log.py`

### `COLUNAS`
`geracao, fitness_medio, melhor_fitness, melhor_x, melhor_y`: as colunas exigidas pelo enunciado.

### `salvar_log(historico, caminho)`
Abre o arquivo com `newline=""` (evita linhas em branco no Windows) e `utf-8`, escreve o cabeçalho e uma linha por geração. Usa `zip` para percorrer as 5 listas do histórico ao mesmo tempo, formando `(geração, média, melhor, x, y)` por linha. Os dois fitness são arredondados em 6 casas só para o arquivo ficar legível; `x` e `y` já vêm com 3 casas do AG.

---

## 7. `interface.py`

### Setup
- `matplotlib.use("Agg")` **antes** de importar `graficos`: os gráficos viram só PNG (sem abrir janelas do matplotlib); quem mostra é o tkinter.
- `PASTA`, `PASTA_SAIDA`, `CAMINHO_LOG`, `CAMINHO_FITNESS`: caminhos baseados na pasta do arquivo (funcionam de qualquer diretório).
- `CAMPOS`: lista `(chave, rótulo, valor padrão)` dos 5 campos. Os campos vêm de uma lista para o código montar a tela com um laço.

### Classe `Aplicacao`
- `__init__`: título, janela de tamanho fixo, dicionários `entradas` (os campos) e `imagens`, a flag `fechada` e o tratamento do botão X (`_fechar`): se o usuário fechar a janela no meio da execução, o callback levanta `InterruptedError`, que `executar` captura para encerrar sem mostrar erro. **`imagens` guarda referências** das `PhotoImage`; sem isso o tkinter descarta a imagem e a tela fica em branco.
- `_montar_widgets`: cria os campos de texto (com os valores padrão), a caixinha "Parar por convergência", o botão Executar, o texto de status, o texto de resultado e um `Notebook` (abas) com "População" e "Fitness médio".
- `_ler_parametros`: lê os campos, troca vírgula por ponto (usuário pt-BR digita "0,8"), converte com `int`/`float`, valida (população ≥ 2, gerações ≥ 1, taxas em [0, 1], α ≥ 0). Em erro mostra `messagebox` e devolve `None`; senão devolve um `ag.Parametros`.
- `_mostrar_imagem(aba, caminho)`: carrega o PNG com `tk.PhotoImage` e coloca no rótulo da aba.
- `executar` (handler do botão):
  1. Lê parâmetros (aborta se inválidos).
  2. Cria `saida/` e apaga os `geracao_*.png` antigos.
  3. Define o callback `ao_fim_de_geracao`: salva o PNG da geração, mostra na aba, atualiza o status e chama `raiz.update()` (mantém a janela respondendo durante o loop).
  4. Desabilita o botão, roda `ag.executar_ag`, salva o log, gera o gráfico de linha, mostra o resumo. O `finally` reabilita o botão mesmo se der erro.
- `_mostrar_resumo`: escreve "Concluído em N gerações" e o melhor x, y e fitness.

### `iniciar()`
Cria a janela `Tk`, instancia `Aplicacao` e entra no `mainloop`.

---

## 8. `main.py`
Só importa `interface` e chama `interface.iniciar()`. Rodar: `python3 main.py` dentro de `codigo/`.

---

## 9. `tests/` (56 testes)

Rodar: `python3 -m unittest discover -v` dentro de `codigo/`.

| Arquivo | O que verifica |
|---|---|
| `test_funcao.py` | valores calculados à mão (0,0 → 5; 1,1 → 3; 10,10 → −105), ótimo 9,333, vizinhos piores, arredondar e limitar |
| `test_ag.py` | população (tamanho, limites, 3 casas), ranking (probabilidades 0,2/0,4/0,1/0,3, independência da escala, direção), BLX (taxa 0 e 1, intervalo, α = 0, pais iguais, limites), mutação (taxa 0, 1 e aproximada), elitismo, convergência e `executar_ag` (chaves, tamanhos, melhor nunca cai, pop. ímpar, callback, aproxima o ótimo, reprodutível, roda todas as gerações sem convergência) |
| `test_log.py` | cabeçalho, uma linha por geração, valores, 5 colunas |
| `test_graficos.py` | PNG criado e não vazio, nenhuma figura fica aberta |

Os operadores são aleatórios, então os testes conferem **propriedades** (limites, frequências com tolerância) e fixam a semente (`random.seed`) para serem reprodutíveis.

---

## 10. Decisões de projeto que vale saber justificar

1. **Tupla `(x, y)` como indivíduo:** simples, imutável, fácil de comparar e imprimir.
2. **Lista de fitness paralela à população:** evita recalcular fitness e mantém a lógica simples (os operadores recebem os dois).
3. **BLX-α por gene:** a forma clássica; cada variável sorteia seu próprio valor no intervalo estendido.
4. **Clamp + arredondamento em todo operador:** garante domínio e 3 casas sempre.
5. **Mínimo de 1 elite:** com 0,5% de populações pequenas o número daria 0; assim o melhor nunca se perde.
6. **Convergência por "fração perto do melhor":** mais robusta que o desvio padrão com mutação uniforme.
7. **Não reproduz na última geração:** evita gerar uma população que ninguém avalia.
8. **Callback em vez de gráfico dentro do AG:** separação de responsabilidades.
9. **Gráficos em PNG + `Agg`:** não abre dezenas de janelas, e o enunciado aceita gravar em disco.
10. **Mesma exigência do enunciado atendida em tela:** gráfico por geração (aba População), linha do fitness (aba Fitness médio), log em CSV, parâmetros na interface.

## 11. Perguntas que o professor pode fazer (resposta curta)

- **Ranking x roleta?** Peso é a posição, não o valor; imune a escala e a fitness negativo.
- **O que o BLX-α faz e para que serve o α?** Sorteia no intervalo dos pais estendido em α·d de cada lado. α = 0 só interpola; α > 0 explora além dos pais.
- **Por que o clamp?** O intervalo estendido pode sair de [−10, 10].
- **Taxa de mutação é por quê?** Por gene. Esperado: 2 × taxa genes mutados por indivíduo.
- **Como o elitismo foi calculado?** 0,5% × N, no mínimo 1.
- **Por que o fitness médio fica abaixo do melhor?** A mutação uniforme injeta indivíduos aleatórios.
- **Por que parou antes de 100 gerações?** Convergência (80% da população perto do melhor, ou 30 gerações sem melhora). Pode desligar na caixinha.
- **Por que não pára ao achar 9,333?** O enunciado proíbe.
- **Como garantem 3 casas?** `arredondar` em todo operador (população inicial, BLX e mutação).
