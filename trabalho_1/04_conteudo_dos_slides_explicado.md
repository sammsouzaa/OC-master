# Conteúdo dos slides explicado — focado no que a Equipe 9 precisa

Base: `estudo_prova1/Tópico_1_-_Algoritmos_Genéticos.pdf` (prof. Matheus Raffael Simon). Os números `[slide N]` indicam onde está cada ponto no PDF.

**Equipe 9:** codificação **real** · seleção por **ranking** · cruzamento **BLX-α** · mutação **uniforme** · elitismo **0,5%** · **Função 8** (maximização).

Legenda das seções:
- 🎯 **Núcleo do trabalho:** é o que vocês implementaram. Estudem a fundo.
- 📘 **Contexto:** vale entender, pode cair em pergunta, mas não está no código.
- 💤 **Só para referência:** de outras equipes ou só para binário.

---

## 1. O que é um Algoritmo Genético 📘 [slides 2–15]

### Ideia
Um AG é uma técnica de busca/otimização **inspirada na evolução natural de Darwin**: os indivíduos mais adaptados têm mais chance de sobreviver e se reproduzir, e as variações favoráveis tendem a permanecer na população ao longo das gerações. [slides 2–8]

No computador:
- cada **solução candidata** é um indivíduo (aqui, um par `(x, y)`);
- a **qualidade** da solução é o fitness (aqui, o valor de `Z`);
- as **melhores soluções** têm mais chance de "reproduzir" (seleção + cruzamento);
- pequenas **alterações aleatórias** (mutação) mantêm a variedade;
- repete-se por várias **gerações**, e a população melhora aos poucos.

Origem: proposto por **John Holland (1975)**, popularizado por **Goldberg (1989)**. [slide 10]

### Três elementos de toda tarefa de busca/otimização [slide 11]
1. **Codificação** do problema: como representar uma solução (geralmente a parte mais difícil). *No trabalho: real, `(x, y)` com 3 casas.*
2. **Espaço de busca**: todas as soluções possíveis. *No trabalho: o quadrado `x, y ∈ [−10, 10]`.*
3. **Função de avaliação (fitness)**: mede a qualidade de cada solução. *No trabalho: a Função 8.*

### Como o AG difere dos métodos tradicionais [slides 12–14]
Os AGs diferem em quatro pontos:
1. trabalham com uma **codificação** dos parâmetros, não com os parâmetros diretamente;
2. trabalham com uma **população**, não com um único ponto;
3. usam só o **valor da função** (custo/recompensa), sem derivadas;
4. usam regras de transição **probabilísticas**, não determinísticas.

> No trabalho: não usamos a derivada da Função 8 em lugar nenhum. O ótimo analítico (`x = 2/3`, `y = −5/3`) serve apenas para conferir o resultado.

### Por que população ajuda [slide 15]
Ter muitos pontos ao mesmo tempo reduz a chance de **ficar preso num falso ótimo** (máximo local), que é quando o algoritmo converge para uma solução boa só na vizinhança e ignora o resto do espaço. A Função 8 é côncava e tem um único máximo, então aqui isso não é problema; mas é a justificativa teórica de usar população.

---

## 2. Terminologia 🎯 [slides 22–33]

O slide traz uma tabela com os termos e usa uma população de exemplo (colunas `#Ind`, `X`, `Y`, `Z`, `Fitness`):

| Termo | Definição do slide | No nosso código |
|---|---|---|
| **População** | conjunto de possíveis soluções para o problema | lista `populacao` (N tuplas) |
| **Indivíduo** | cada elemento que compõe uma população | uma tupla `(x, y)` |
| **Cromossomo** | conjunto de características que representa cada indivíduo | a tupla `(x, y)` inteira |
| **Gene** | cada uma das características presentes em cada indivíduo | `x` ou `y` |
| **Alelo** | valor atribuído a cada gene/característica | por exemplo, `x = 0,667` |
| **Genótipo** | estrutura que armazena as informações de cada indivíduo | a tupla `(x, y)` |
| **Fenótipo** | **grau de aptidão** do indivíduo em resolver o problema | o `Z` do indivíduo |
| **Fitness** | valor do fenótipo de um elemento | `fitness(x, y)` / lista `fitnesses` |
| **Geração** | cada um dos ciclos de uma população | cada volta do `for` em `executar_ag` |

Pontos de atenção:
- **Cromossomo × genótipo:** na prática, com representação real simples (como a nossa), os dois coincidem com a tupla `(x, y)`.
- **Fenótipo** no slide é o **grau de aptidão** (não "a decodificação"): é o que resulta de avaliar o genótipo.

---

## 3. Representação 🎯 [slides 34–35]

- **Binária (clássica):** os genes são cadeias de bits. Exige **decodificar** para calcular o fitness, e o cruzamento e a mutação operam sobre os bits. Exemplo do slide: maximizar `f(x) = x²` com `x ∈ [0, 31]` usando 5 bits: `01110` = 14 e fitness 196.
- **Real:** os genes são valores reais (ou inteiros) diretamente. O slide mostra um exemplo com vetor `(x1, x2)` real. **É a nossa.**

**Consequências de usar representação real** (por isso nossos operadores são diferentes dos de binário):
- não há decodificação: o fitness é calculado direto sobre `(x, y)`;
- cruzamento e mutação operam sobre os **valores numéricos**, não sobre bits [slides 56–58 e 62];
- o enunciado exige **3 casas decimais**, então arredondamos depois de cada operador;
- é preciso garantir que o valor fique **dentro do domínio** (`limitar`).

---

## 4. O ciclo do AG 🎯 [slides 36–37]

O slide mostra o **algoritmo básico de Goldberg**:

```
t ← 0
Inicialize(P_t)
Avalie(P_t)
enquanto critério de parada não for alcançado:
    t ← t + 1
    Selecione P_t a partir de P_{t-1}
    Cruze os pais em P_t
    Mute os elementos em P_t
    Avalie(P_t)
```

Em português: **inicializa → avalia → [seleciona → cruza → muta → avalia] até parar**. O nosso `executar_ag` segue exatamente isso, com o **elitismo** acrescentado ao montar a nova geração.

---

## 5. Inicialização 🎯 [slides 38–39]

Cria-se uma população de **N indivíduos**, cada um sendo um ponto do espaço de soluções. Em geral os valores são **aleatórios**; se o projetista conhece o problema, pode **direcionar** (por exemplo, não permitir distâncias negativas em um problema de distância).

> No trabalho: `criar_populacao_inicial` sorteia `x` e `y` uniformemente em `[−10, 10]` e arredonda para 3 casas. Não temos conhecimento prévio a explorar, então usamos o aleatório uniforme.

---

## 6. Cálculo da aptidão (fitness) 🎯 [slides 40–41]

- Calcula-se o fitness de **cada** indivíduo, normalmente com a função objetivo.
- Depois os indivíduos podem ser **ordenados** por aptidão (é o que o ranking e o elitismo usam).
- Em geral exige **decodificar** o indivíduo (só na binária).
- A função é **totalmente dependente do problema**; o valor serve para estimar a competência do indivíduo e é usado depois na **seleção/cruzamento** e no **elitismo**.

> No trabalho: `fitness(x, y) = 5 + 3x − 4y − x² + xy − y²`. É **maximização**: fitness maior = melhor.

---

## 7. Seleção 🎯 [slides 42–51]

### Ideia geral [slides 42–43]
Segundo Schneider (1998), a seleção dá aos **melhores indivíduos preferência na reprodução**, para que passem suas características adiante, como na natureza. Alguns métodos não escolhem só os melhores de forma rígida, mas dão **mais chance** a eles.

### Métodos citados [slides 43–44]
- **Amostragem direta:** critério fixo, "os n melhores".
- **Amostragem aleatória simples (equiprovável):** todos com a mesma chance.
- **Torneio:** sorteia `n` indivíduos (todos com a mesma chance) e fica com o de maior aptidão. 💤
- **Ranking:** 🎯 (o nosso, abaixo).
- **Roleta (amostragem estocástica):** 📘 (abaixo, para comparar).

### 🎯 Seleção por Ranking [slides 45–47]

**Como funciona:**
1. Ordena os indivíduos pelo fitness. O **pior fica com rank 1** e o **melhor com rank N**.
2. Cada indivíduo recebe uma **probabilidade proporcional ao seu rank**:
   `probabilidade = rank / (1 + 2 + … + N)`.
3. Sorteia-se o pai com essas probabilidades. Quem tem rank maior tem mais chance.

**Exemplo do slide** (7 indivíduos):

| Indivíduo | Fitness | Rank | Probabilidade (rank/28) |
|---|---|---|---|
| 1 | 45 | 4 | 0,14 |
| 2 | 89 | 6 | 0,21 |
| 3 | 125 | 7 | 0,25 |
| 4 | 21 | 3 | 0,11 |
| 5 | 52 | 5 | 0,18 |
| 6 | 9 | 1 | 0,04 |
| 7 | 19 | 2 | 0,07 |

(soma dos ranks = 1+2+…+7 = 28)

**Por que usar ranking:** só importa a **posição**, não o **valor** do fitness. Se um indivíduo tem fitness enorme (125) e os outros pequenos, ele **não domina** a seleção (como aconteceria na roleta). E funciona com **fitness negativo**, sem nenhum tratamento especial.

> No código: `selecionar_por_ranking` ordena os índices por fitness crescente, usa `ranks = [1..N]` como pesos e sorteia com `random.choices`.

### 📘 Roleta (Goldberg, 1989) [slides 48–51] — para comparar
Cada indivíduo ocupa uma fatia da roleta **proporcional ao seu fitness absoluto**. No mesmo exemplo de 7 indivíduos (soma dos fitness = 360): o indivíduo 3 (fitness 125) fica com 34,72% da roleta, e o 6 (fitness 9), com 2,5%.

**Diferença-chave para o ranking:** na roleta o **valor** do fitness manda; um indivíduo muito bom pode dominar a seleção. O slide 51 ("Tratamentos") mostra que a roleta precisa de ajustes para:
- **problemas de minimização** (ex.: minimizar `Z = x² + 12y`);
- **fitness negativo** (ex.: minimizar `Z = x² − y`).

A **Função 8 tem fitness negativo** (por exemplo, `fitness(10, 10) = −105`), então com roleta precisaríamos desses tratamentos. Com ranking, não: é uma boa justificativa para a escolha.

---

## 8. Cruzamento 🎯 [slides 52–59]

### Ideia [slide 52]
Depois de escolhidos dois pais, **combina-se o material genético** deles para formar filhos. Na binária, troca-se segmentos de bits. Na **real**, aplicam-se operadores que usam diretamente os valores dos pais. [slide 56]

### 💤 Binária (só para referência) [slides 52–55]
- **Um ponto:** um corte; trocam-se os segmentos depois dele.
- **Dois pontos:** dois cortes; troca-se o trecho entre eles.
- **Pontos aleatórios:** a posição dos cortes é sorteada a cada cruzamento.
- **Uniforme:** uma **máscara** (definida pelo projetista) diz, bit a bit, de qual pai vem cada bit.

### Real: os operadores do slide [slides 56–58]
| Operador | Fórmula | Observação |
|---|---|---|
| Média simples 📘 | `F1 = (P1 + P2) / 2` | um filho no meio dos pais |
| Média geométrica 📘 | `F1 = √(P1 · P2)` | |
| Aritmético 📘 | `F1 = β·P1 + (1−β)·P2`, `F2 = β·P2 + (1−β)·P1`, `β ∈ U[0,1]` | filhos **entre** os pais |
| **BLX-α** 🎯 | `F1 = P1 + β·(P2 − P1)`, `β ∈ U[−α, 1+α]` | filhos **entre e além** dos pais |
| Heurístico 💤 | `F1 = P1 + r·(P1 − P2)` se `f(P1) ≥ f(P2)` (senão com `P2`), `r ∈ U[0,1]` | anda **na direção do pai melhor** |

### 🎯 BLX-α (o nosso)

`U` é a distribuição uniforme. O `α` é "um pequeno valor que **estende os limites** para a definição de F1" [slide 57].

**Entendendo a fórmula:** `P1 + β(P2 − P1)` com `β ∈ [0, 1]` seria um ponto no **segmento entre os pais** (β = 0 dá `P1`, β = 1 dá `P2`). Como `β ∈ [−α, 1 + α]`, o filho pode cair um pouco **antes de P1** (β negativo) ou um pouco **depois de P2** (β > 1). Ou seja, o intervalo dos pais é **estendido em α × distância** para cada lado.

**Forma equivalente (a que usamos, por gene):**
```
d  = |P1 − P2|
filho ∈ uniforme( min(P1,P2) − α·d ,  max(P1,P2) + α·d )
```

**Exemplo numérico:** `P1 = 2`, `P2 = 4`, `α = 0,5`:
- `d = 2`; intervalo = `[2 − 1, 4 + 1] = [1, 5]`.
- Com `α = 0`: intervalo `[2, 4]` (só interpola, a população tende a encolher).
- Com `α = 0,5` (valor clássico): pode **explorar além dos pais**, mantendo diversidade.

**Cuidados no trabalho:**
- aplicamos **separadamente** em `x` e em `y` (BLX **por gene**);
- o intervalo estendido pode sair de `[−10, 10]` → `limitar`;
- o resultado é arredondado em 3 casas;
- se os pais são iguais (`d = 0`), o filho é igual aos pais.

> **Dúvida em aberto:** o slide não diz se o β é sorteado **por gene** ou **um só** para `(x, y)`. Usamos por gene (versão clássica). Se o professor perguntar, explique a diferença: um β único coloca o filho **na reta** que passa pelos pais; por gene o filho pode cair em qualquer ponto do **retângulo** estendido.

### Taxa de cruzamento 🎯 [slide 59]
- Normalmente entre **60% (0,6) e 90% (0,9)**.
- **Como se aplica:** sorteia-se um valor α ∈ [0, 1]. Se **α < taxa**, o cruzamento é feito, gerando um ou dois filhos para a próxima geração. Se **α > taxa**, **não há cruzamento** e um ou os dois pais passam à geração seguinte.

> No código: `if random.random() < taxa_cruzamento:` cruza; senão devolve `(pai1, pai2)`.
> Cuidado com o nome: o "α" do **sorteio** (slide 59) **não é** o α do **BLX**.

---

## 9. Mutação 🎯 [slides 60–64]

### Ideia [slide 60]
A mutação é aplicada aos **cromossomos dos filhos**. Percorrem-se **todos os genes**, e cada um pode ou não mutar, conforme um sorteio contra a **taxa de mutação**. Serve para **introduzir variabilidade**, evitar estagnação (um gene sempre com o mesmo valor) e ajudar a escapar de ótimos locais.

### 💤 Binária [slide 61]
**Inversão de bits:** o bit sorteado troca (0↔1).

### Real: os operadores do slide [slides 62–63]
No caso real, a mutação é "uma variação controlada sobre o valor do gene":

| Operador | O que faz |
|---|---|
| **Uniforme** 🎯 | substitui o gene por **outro valor gerado aleatoriamente, com distribuição uniforme, entre os limites mínimo e máximo** |
| Gaussiana 💤 | substitui o gene por um valor de `N(Fi, σ²)`; `σ²` é definida pelo projetista e pode **diminuir ao longo das gerações** |
| Creep 💤 | **soma ou subtrai** um pequeno valor aleatório de `N(0, σ²)` ao gene |
| Não-uniforme 💤 | substitui o gene segundo uma distribuição não uniforme (exponencial, Bernoulli, qui-quadrado, geométrica), entre os limites |

### 🎯 Mutação uniforme (a nossa)
Para cada gene: se o sorteio for menor que a taxa, o gene vira um número **qualquer do domínio** (`uniforme(−10, 10)`), **independente do valor antigo**. É uma mutação **grande** (um salto para qualquer lugar), ao contrário da creep (pequena alteração).

> **Consequência importante:** como a mutação uniforme joga genes para qualquer ponto, a população **nunca fica totalmente parada**. Por isso o **fitness médio fica abaixo do melhor** nos gráficos, e por isso o critério de convergência do código conta **quantos indivíduos estão perto do melhor** (em vez de usar desvio padrão).

### Taxa de mutação 🎯 [slide 64]
- Normalmente entre **1% (0,01) e 5% (0,05)**.
- **Como se aplica:** para **cada gene**, sorteia-se α ∈ [0, 1]; se **α < taxa**, o gene sofre mutação; senão, não. O processo se repete para **todos os genes dos filhos**.
- **Efeitos:** taxa baixa evita que uma posição fique estagnada; taxa **muito alta** torna a busca **aleatória** e pode destruir boas soluções. [slide 68]

> No código: `_mutar_gene`: `if random.random() < taxa_mutacao:` troca o gene. A taxa vale **por gene**: com 2 genes e taxa 0,05, o esperado é 0,1 gene mutado por indivíduo.

---

## 10. Elitismo 🎯 [slide 65]

Técnica para **melhorar a convergência**: escolhe-se o **melhor (ou os melhores) indivíduo de cada geração** e ele passa à geração seguinte **sem sofrer cruzamento nem mutação**, para **conservar suas boas características**. Isso faz o algoritmo convergir mais cedo, principalmente porque **evita que os mais aptos sejam perdidos ou modificados**.

**No trabalho:** elitismo de **0,5% do tamanho da população**.
- População 200 → 0,5% = 1 indivíduo.
- População 100 → 0,5% = 0,5 (não existe meio indivíduo): adotamos **no mínimo 1** (`max(1, round(0.005·N))`).
- Consequência: o **melhor fitness nunca diminui** de uma geração para a outra.

---

## 11. Parâmetros genéticos 🎯 [slides 66–68]

| Parâmetro | Efeito | Faixa/observação |
|---|---|---|
| **Tamanho da população** [66] | população pequena cobre pouco o espaço de busca; grande cobre melhor e evita convergência prematura, mas gasta mais recursos e tempo | no trabalho, vem da interface |
| **Taxa de cruzamento** [67] | quanto maior, mais rápido surgem estruturas novas; muito alta substitui quase toda a população e pode **perder estruturas boas**; muito baixa deixa o algoritmo **lento** | 60%–90% |
| **Taxa de mutação** [68] | baixa evita estagnação; muito alta vira busca aleatória e pode destruir boas soluções | 1%–5% |

> Esses são exatamente os parâmetros que a interface pede (população, gerações, cruzamento, mutação), mais o α do BLX.

---

## 12. Critérios de parada 🎯 [slide 69]

O slide lista três:
1. **Número máximo de gerações.**
2. **Função objetivo ter alcançado o valor ótimo** (só possível se o ótimo for conhecido).
3. **Convergência da função objetivo:** depois de várias gerações os valores não mudam mais (pode ter chegado à melhor solução **ou** a um máximo local).

> **Atenção, conflito com o enunciado:** o enunciado do trabalho **proíbe** o critério 2 (atingir o valor ótimo). Só valem o **número de gerações** e a **convergência**. O nosso código usa os critérios 1 e 3: o número de gerações (da interface) e a convergência (população concentrada ou melhor sem melhora por 30 gerações).

---

## 13. Quando usar um AG 📘 [slides 19–21]

Os AGs não têm conhecimento específico do problema; só têm como guia a **função objetivo**. São muito usados em **otimização de funções**. Características necessárias:
1. o **espaço de busca** deve estar **delimitado** numa faixa de valores;
2. deve ser possível definir uma **função de aptidão** que meça quão boa é uma resposta;
3. as soluções devem poder ser **codificadas** de forma que facilite a implementação no computador.

> O nosso problema atende aos três: domínio `[−10, 10]²`, fitness `Z`, codificação real `(x, y)`.

---

## 14. Simulação à mão de UMA geração (Função 8) 🎯

População de 4 indivíduos (valores inventados só para o exemplo):

| # | (x, y) | Fitness Z |
|---|---|---|
| A | (0, 0) | 5 |
| B | (2, −2) | 7 |
| C | (5, 5) | −25 |
| D | (−3, 1) | −21 |

Cálculos: `B: 5 + 6 + 8 − 4 − 4 − 4 = 7`; `C: 5 + 15 − 20 − 25 + 25 − 25 = −25`; `D: 5 − 9 − 4 − 9 − 3 − 1 = −21`.

**1. Ranking** (pior = 1): C = 1, D = 2, A = 3, B = 4. Soma = 10, então as probabilidades são **C 0,1 · D 0,2 · A 0,3 · B 0,4**. (O fitness −25 não atrapalha.)

**2. Elitismo:** com `n_elite = 1`, o melhor (**B = (2, −2)**) passa direto para a próxima geração.

**3. Seleção de pais:** suponha que o sorteio escolheu **B** e **A**.

**4. Cruzamento BLX-α** (α = 0,5), supondo que o sorteio `random() < taxa` deu "cruza":
- `x`: pais 2 e 0 → `d = 2` → intervalo `[0 − 1, 2 + 1] = [−1, 3]` → sorteia, por exemplo, **1,4**.
- `y`: pais −2 e 0 → `d = 2` → intervalo `[−2 − 1, 0 + 1] = [−3, 1]` → sorteia, por exemplo, **−0,8**.
- Filho = **(1,4; −0,8)**, com fitness `5 + 4,2 + 3,2 − 1,96 − 1,12 − 0,64 = 8,68`, melhor que A e quase tão bom quanto B.

**5. Mutação uniforme** (taxa 0,05): sorteio do gene `x` = 0,03 < 0,05 → `x` vira `uniforme(−10, 10)`, por exemplo **7,318**; sorteio do gene `y` = 0,61 > 0,05 → `y` fica −0,8. Filho mutado = **(7,318; −0,8)**: um "salto" que provavelmente piora o fitness. É o que a mutação uniforme faz: **explorar**, às vezes custando qualidade.

**6. Nova população:** elite (B) + filhos gerados dessa forma, até completar 4 indivíduos.

---

## 15. Cola rápida: slide → código

| Assunto | Slides | Código |
|---|---|---|
| Representação real | 34–35 | tupla `(x, y)`; `funcao.arredondar` e `funcao.limitar` |
| Ciclo do AG | 36–37 | `ag.executar_ag` |
| Inicialização | 38–39 | `ag.criar_populacao_inicial` |
| Fitness | 40–41 | `funcao.fitness`, `ag.avaliar` |
| Ranking | 45–47 | `ag.selecionar_por_ranking` |
| BLX-α | 56–58 | `ag.cruzar_blx_alpha`, `_blx_filho`, `_blx_gene` |
| Taxa de cruzamento | 59 | `if random.random() < taxa_cruzamento` |
| Mutação uniforme | 62 | `ag.mutar_uniforme`, `_mutar_gene` |
| Taxa de mutação | 64 | `if random.random() < taxa_mutacao` (por gene) |
| Elitismo | 65 | `ag.calcular_tamanho_elite`, `ag.extrair_elite` |
| Parâmetros | 66–68 | `ag.Parametros` e a interface |
| Parada | 69 | `ag.convergiu` e o `for` de `executar_ag` |

## 16. Autoteste (responda sem olhar)

1. Em que ordem acontecem avaliar, selecionar, cruzar, mutar? Onde entra o elitismo?
2. O que são gene, alelo, cromossomo, genótipo e fenótipo na **nossa** representação?
3. Com fitness `45, 89, 125, 21, 52, 9, 19`, quais os ranks e as probabilidades? (4, 6, 7, 3, 5, 1, 2; divididos por 28)
4. Por que ranking e não roleta para a Função 8? (fitness negativo; um indivíduo bom não domina)
5. Se `P1 = 2`, `P2 = 4`, `α = 0,5`, em que intervalo cai o filho do BLX-α? (`[1, 5]`)
6. O que acontece com `α = 0`? E se os pais forem iguais?
7. Como se decide se o cruzamento acontece? E se a mutação acontece em um gene?
8. A mutação uniforme é "pequena" ou "grande"? Qual a diferença para a creep?
9. Por que o fitness médio fica abaixo do melhor no gráfico?
10. O que é elitismo e por que o melhor fitness nunca cai?
11. Quais critérios de parada o slide lista e qual deles o enunciado proíbe?
12. Por que a taxa de mutação não deve ser alta? E a de cruzamento, muito baixa?

---

## 17. Fluxo completo de uma execução 🎯

Juntando tudo, com os números para população 100 (elite de 1 indivíduo, 50 pares por geração).

### Passo a passo

**1. População inicial** (só na geração 1)
- Cada indivíduo recebe `x` e `y` **totalmente aleatórios** em `[−10, 10]` (3 casas).
- Cada um é adicionado a uma lista; essa lista é a **população**.

**2. Para cada geração (1, 2, 3, …):**

**2.1 Avaliar e ranquear**
- Aplica-se a fórmula do fitness a cada indivíduo.
- Ordena-se do pior para o melhor: o pior tem rank 1 e o melhor tem rank N (quanto maior o fitness, maior o rank).
- A probabilidade de escolha de cada um é **proporcional ao rank**: `rank / soma dos ranks`.

**2.2 Registrar**
- Guarda o melhor indivíduo, o melhor fitness e o fitness médio (viram uma linha do `log.csv`).
- Desenha o gráfico da população, com o melhor destacado.

**2.3 Verificar a parada**
- Para se for a **última geração** ou se a **população convergiu**.
- Na última geração **não se reproduz**: a população nova nunca seria avaliada.

**2.4 Elitismo**
- O melhor indivíduo (0,5% da população, no mínimo 1) é copiado **direto** para a próxima geração, sem cruzar e sem mutar.

**2.5 Formar os casais e gerar os filhos** (repete até completar a população; com N = 100 são **50 casais**)
1. **Sorteio dos pais:** `pai1` e `pai2` são sorteados com os pesos do ranking. O sorteio é **com reposição**: o mesmo indivíduo pode ser escolhido várias vezes (e até nos dois lados do mesmo casal).
2. **Sorteio "cruza ou não":** sorteia-se um número entre 0 e 1.
   - Se for **menor que a taxa de cruzamento**: **cruza** (passo 3).
   - Se não: **não cruza**, e os filhos são **cópias dos pais**.
3. **BLX-α** (só quando cruza). Para cada filho, **gene a gene** (primeiro `x`, depois `y`):
   - calcula `d = |gene do pai1 − gene do pai2|`;
   - monta o intervalo `[menor − α·d, maior + α·d]`;
   - sorteia um número aleatório (uniforme) dentro dele.
   Faz isso para o filho 1 e depois para o filho 2, com **sorteios novos** (por isso saem diferentes).
4. **Mutação uniforme** (em **todos** os filhos, inclusive as cópias dos pais). Para cada gene de cada filho:
   - sorteia um número entre 0 e 1;
   - se for **menor que a taxa de mutação**: o gene é **substituído** por um número aleatório em `[−10, 10]`;
   - se não: o gene **continua como estava**.
5. **Ajuste final de cada gene gerado:** corta em `[−10, 10]` (`limitar`) e arredonda em 3 casas (`arredondar`).

**2.6 Nova população**
- Nova população = **elite + filhos**.
- Com N = 100, a elite ocupa 1 vaga e os 50 casais geram 100 filhos; o último é descartado para fechar em 100 (1 + 99).
- A nova população volta ao passo **2.1**.

**3. Fim:** devolve o histórico, que gera o `log.csv`, o gráfico de linha do fitness médio e o resumo na tela (melhor `x`, `y` e fitness).

### Resumo em diagrama

```
1. cria população aleatória
2. repete (geração 1, 2, 3...):
   a. calcula fitness de todos e ranqueia
   b. guarda melhor/médio no log, desenha o gráfico
   c. parou? (última geração ou convergiu) -> encerra
   d. elite: copia o(s) melhor(es)
   e. repete até completar a população:
        - sorteia pai1 e pai2 (pesos do ranking)
        - sorteio: cruza ou não?
              sim -> BLX-α em x e y (2 filhos)
              não -> filhos = cópias dos pais
        - mutação uniforme em cada gene dos 2 filhos
        - limitar + arredondar
   f. nova população = elite + filhos (corta o excesso)
3. grava o log, o gráfico de linha e mostra o resumo
```

### Onde cada etapa está no código (`ag.py`, função `executar_ag`)

| Etapa | Código |
|---|---|
| 1. População inicial | `criar_populacao_inicial` |
| 2.1 Avaliar | `avaliar` (o ranking é feito dentro de `selecionar_por_ranking`) |
| 2.2 Registrar | o histórico em `executar_ag`, o callback `ao_fim_de_geracao` e `log.py` |
| 2.3 Parada | `convergiu` e o `if geracao == num_geracoes` |
| 2.4 Elite | `calcular_tamanho_elite` e `extrair_elite` |
| 2.5.1 Pais | `selecionar_por_ranking` (chamada duas vezes por casal) |
| 2.5.2–3 Cruzamento | `cruzar_blx_alpha`, `_blx_filho` e `_blx_gene` |
| 2.5.4 Mutação | `mutar_uniforme` e `_mutar_gene` |
| 2.5.5 Ajuste | `funcao.limitar` e `funcao.arredondar` (dentro de `_blx_gene` e `_mutar_gene`) |
| 2.6 Nova população | `proxima = elite + filhos` e `populacao = proxima[:n]` |

---

## 18. Minha explicação x o que complementar 🎯

Esta seção usa **as palavras que você mesmo usou** ao explicar o fluxo, e mostra o que já está certo e o que acrescentar para cada ponto do trabalho. Serve para ensaiar a apresentação.

### 18.1 Tabela por ponto do trabalho

| Ponto | Suas palavras | Situação | O que acrescentar |
|---|---|---|---|
| **Representação real** | "a primeira população é gerada a partir de indivíduos cujos valores de x, y são totalmente aleatórios dentre o intervalo [−10, 10]"; "cada indivíduo é adicionado na lista que é a população" | ⚠️ Parcial | Nomear a **representação real**: cada gene é um número real direto (sem bits e sem decodificar). Cada valor gerado é **arredondado em 3 casas** e **limitado a [−10, 10]**. |
| **Ranking** | "ordena os indivíduos baseado no fitness, quanto maior o fitness maior o ranking"; "calculado a probabilidade de escolha, que é proporcional ao ranking"; "sorteio baseado nos pesos" | ✅ Bem | Dizer **por que ranking e não roleta**: só a posição conta, o fitness negativo não atrapalha e um indivíduo muito bom não domina. Probabilidade = `rank / soma dos ranks`. Fitness e rank sobem juntos, mas **a probabilidade é proporcional ao rank, não ao fitness**. |
| **BLX-α** | "para calcular o valor dos filhos, é feito um cálculo do blx-α, baseado no valor do blx determinamos o intervalo de valor de cada gene de cada filho (x, depois y, do filho 1; depois x e y do filho 2) e é escolhido um número aleatório dentre esse intervalo" | ✅ Bem | O que o **α** faz: estende o intervalo em `α·d` para cada lado (`d` = distância entre os pais). **α = 0** só interpola; **α = 0,5** (padrão) permite sair um pouco de entre os pais. É um parâmetro **fixo**, definido na interface. Depois do sorteio, `limitar` e `arredondar`. |
| **Mutação uniforme** | "é sorteado um número aleatório entre 0 e 1, cujo caso seja menor que a taxa de mutação, é sorteado um número aleatório dentre o intervalo [−10, 10] e substitui o valor do filho; caso seja maior, mantém o próprio valor" | ✅ Bem | A taxa vale **por gene**. O novo valor **não depende do antigo** (é um salto grande). Serve para **explorar fora** da região dos pais. Vale para **todos** os filhos, inclusive as cópias de pais que não cruzaram. |
| **Elitismo 0,5%** | "primeiro pegamos o melhor indivíduo, e passamos direto ele para a próxima geração" | ⚠️ Parcial | O **0,5%** da população (com população 100 dá 0,5, então adotamos **no mínimo 1**). A elite **não cruza nem muta**, **ocupa uma vaga** da nova população (1 elite + 99 filhos) e **garante que o melhor fitness nunca piora**. |
| **Função 8** | "depois é aplicado a fórmula do fitness… esse cálculo é informado de acordo com o problema, no nosso caso, o cálculo foi informado" | ❌ Não detalhou | Dizer **qual é**: `Z = 5 + 3x − 4y − x² + xy − y²`, com x e y em [−10, 10]. É **maximização**. Ótimo: `x ≈ 0,667`, `y ≈ −1,667`, `Z ≈ 9,333`. O ótimo serve só para conferir, **nunca como critério de parada**. |

### 18.2 Trechos do fluxo que você explicou e o que falta em cada um

| Etapa do fluxo | Suas palavras | Situação | Complemento |
|---|---|---|---|
| População inicial | "valores de x, y totalmente aleatórios dentro do intervalo, cada indivíduo é adicionado numa lista" | ✅ | Só acontece na geração 1. |
| Fitness e ranking | "aplica a fórmula, ordena, quanto maior o fitness maior o ranking" | ✅ | O ranking é refeito **a cada geração** (é relativo à população atual). |
| Elitismo | "pegamos o melhor e passamos direto para a próxima geração" | ✅ | Acontece **antes** de formar os casais, e o melhor ainda pode ser pai. |
| Casais | "sorteio baseado nos pesos para definirmos os casais; são feitos 50 casais" | ✅ | O sorteio é **com reposição** (um indivíduo pode ser escolhido várias vezes). Os 50 casais valem para população 100 com 1 elite. |
| Cruzar ou não | "cada casal tem a probabilidade de cruzar ou não; se não cruzar, o filho vira a cópia dos pais" | ✅ | A regra é: sorteia um número em [0, 1]; se for **menor que a taxa de cruzamento**, cruza. |
| BLX-α | "cálculo do blx-α… intervalo de cada gene de cada filho… número aleatório dentro" | ✅ | O α é um parâmetro fixo; não confundir com o β sorteado (`P1 + β(P2 − P1)`, `β ∈ [−α, 1 + α]`). |
| Mutação | "sorteado número entre 0 e 1; menor que a taxa, substitui por aleatório em [−10, 10]" | ✅ | Em **todos** os filhos (inclusive as cópias). |
| Nova população | (não mencionou) | ⚠️ Faltou | Nova população = elite + filhos; com 100, os 100 filhos de 50 casais perdem 1 para fechar em 1 + 99. |
| Repetição e parada | (não mencionou) | ⚠️ Faltou | Repete até acabar o **número de gerações** ou convergir. Nunca para por "achou o ótimo". |
| Registro e gráficos | (não mencionou) | ⚠️ Faltou | A cada geração: grava a linha do log e desenha o gráfico, com o melhor destacado. No fim: gráfico de linha do fitness médio. |

### 18.3 Versão completa para falar na apresentação

Mesma ordem da sua explicação, com os trechos que faltavam acrescentados:

1. "A **representação é real**: cada indivíduo é um par `(x, y)` de números reais em [−10, 10], com 3 casas decimais."
2. "A população inicial é uma lista de indivíduos com `x` e `y` totalmente aleatórios nesse intervalo."
3. "Calculo o fitness de cada um com a **Função 8**, `Z = 5 + 3x − 4y − x² + xy − y²`. É maximização, então maior é melhor. O ótimo é `(0,667; −1,667)` com `Z = 9,333`, e só uso isso para conferir."
4. "Ordeno do pior para o melhor e dou o **ranking**: o pior tem rank 1 e o melhor tem rank N. A **probabilidade de escolha é proporcional ao rank**. Uso ranking e não roleta porque o fitness pode ser negativo e um indivíduo muito bom não domina a seleção."
5. "**Elitismo:** copio direto o melhor (**0,5% da população, no mínimo 1**) para a próxima geração, sem cruzar nem mutar. Isso garante que o melhor fitness nunca piore."
6. "Depois sorteio os pais, com os pesos do ranking, e formo os **casais** até completar a população. Com população 100, são 50 casais."
7. "Cada casal sorteia se **cruza ou não**. Se o sorteio for menor que a taxa de cruzamento, cruza. Se não, os filhos são cópias dos pais."
8. "Quando cruza, uso o **BLX-α**: para cada gene de cada filho, calculo um intervalo que vai do menor ao maior valor dos pais, estendido em `α·d` para cada lado, e sorteio um número aleatório dentro dele. O α é um parâmetro, 0,5 por padrão."
9. "Em seguida aplico a **mutação uniforme**: para cada gene de cada filho, sorteio um número entre 0 e 1. Se for menor que a taxa de mutação, o gene vira um valor aleatório em [−10, 10]. Se não, mantém."
10. "Cada gene gerado é cortado em [−10, 10] e arredondado em 3 casas."
11. "A nova população é a **elite mais os filhos**, e o processo se repete até acabar o **número de gerações** ou a população **convergir**."
12. "A cada geração gravo uma linha no log e desenho o gráfico da população com o melhor destacado. No fim, gero o gráfico de linha do fitness médio."
