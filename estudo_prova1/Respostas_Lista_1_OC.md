# Respostas — Lista de Exercícios 1 (Otimização Combinatória)

## 1) Cite três áreas que podem se beneficiar de técnicas de otimização.

Engenharia (projeto e dimensionamento de estruturas), logística/roteirização de veículos e distribuição, e machine learning (calibração de hiperparâmetros de modelos, como visto no exemplo do KNN com Busca Tabu). Outras áreas comuns: telecomunicações (roteamento de redes) e planejamento de produção.

## 2) Diferencie heurísticas e metaheurísticas.

**Heurísticas** são regras práticas voltadas a um problema específico, construídas com conhecimento do domínio, sem garantia de encontrar o ótimo, mas geralmente eficientes e rápidas para aquele problema em particular.

**Metaheurísticas** são estratégias de busca mais genéricas e de alto nível — como os Algoritmos Genéticos, a Busca Tabu e o ACO — que não dependem do conhecimento específico do problema (guiam-se apenas pela função objetivo) e podem orientar heurísticas de busca local a explorar o espaço de soluções de forma mais ampla, sendo aplicáveis a diversas classes de problemas.

## 3) Qual é o objetivo comum entre os métodos de otimização estudados?

Encontrar a melhor solução (ou um conjunto de boas soluções) dentro do espaço de busca de um problema, evitando ficar preso em ótimos locais — seja através de evolução de uma população (AG), de memória e movimentos guiados (Busca Tabu), ou de cooperação indireta via feromônio (ACO).

## 4) O que caracteriza uma solução "ótima global"?

É a melhor solução possível dentro de **todo** o espaço de busca do problema, e não apenas a melhor solução dentro de uma vizinhança restrita. Isso a diferencia do **ótimo (máximo) local**, que ocorre quando o algoritmo converge para uma solução localmente boa e para de explorar, ignorando o restante do espaço — podendo existir soluções melhores em outras regiões não exploradas.

---

## 5) Quais são os três elementos básicos de um AG?

1. **Codificação do problema** — representação das variáveis do problema (geralmente a etapa mais complexa do processo).
2. **Espaço de busca** — conjunto de todas as soluções possíveis para o problema.
3. **Função de avaliação (fitness)** — mede a qualidade de cada solução do espaço de busca; varia de acordo com o problema.

## 6) Diferencie o conceito de gene, cromossomo e população.

- **Gene:** menor unidade de informação; representa uma característica/variável codificada (ex.: um bit).
- **Cromossomo:** conjunto de genes que representa uma solução completa (um indivíduo) para o problema.
- **População:** conjunto de vários cromossomos (indivíduos) existentes simultaneamente em uma geração.

## 7) Explique a importância da função fitness em um AG.

A função fitness avalia a **aptidão** de cada indivíduo da população, normalmente derivada da função objetivo do problema (muitas vezes exigindo antes uma decodificação do indivíduo). É essencial porque é ela quem orienta todas as etapas seguintes do algoritmo — **seleção**, **cruzamento** e **elitismo** — permitindo distinguir soluções boas de ruins. Sem ela, o AG não teria como guiar a evolução da população em direção a soluções melhores.

## 8) Qual a diferença entre cruzamento de um ponto e de dois pontos?

- **Cruzamento de um ponto:** define-se um único ponto de corte no cromossomo; os segmentos após esse ponto são trocados entre os pais.
- **Cruzamento de dois pontos:** definem-se dois pontos de corte; apenas o segmento **entre** eles é trocado entre os pais.

O cruzamento de dois pontos promove maior mistura de genes, gera soluções mais diversas e evita que apenas as extremidades dos cromossomos sejam preservadas (problema que pode ocorrer no cruzamento de um ponto).

## 9) O que é elitismo e qual sua importância no processo evolutivo?

Elitismo é a técnica de escolher o(s) melhor(es) indivíduo(s) de cada geração e passá-lo(s) diretamente para a geração seguinte, **sem sofrer cruzamento ou mutação**. Sua importância está em acelerar a convergência do algoritmo, evitando que os elementos mais aptos sejam perdidos ou degradados pelos operadores genéticos.

## 10) Qual é a função do operador de mutação?

Introduzir variabilidade genética na população, alterando aleatoriamente genes dos filhos (cada gene sujeito a uma taxa de mutação). Isso evita a estagnação de uma posição do cromossomo em um único valor e ajuda o algoritmo a escapar de ótimos locais, aumentando a diversidade do espaço explorado.

## 11) Cite os principais parâmetros genéticos de um AG e suas faixas típicas de valores.

- **Tamanho da população:** afeta o desempenho — população pequena cobre pouco o espaço de busca; população grande cobre melhor, mas exige mais recursos computacionais e tempo (não há uma faixa numérica fixa; depende do problema).
- **Taxa de cruzamento:** tipicamente entre **60% e 90%** (0,6 a 0,9).
- **Taxa de mutação:** tipicamente entre **1% e 5%** (0,01 a 0,05).

## 12) Em que casos o uso de AGs é indicado?

- Quando o espaço de busca é grande, mas pode ser delimitado dentro de uma faixa de valores;
- Quando é possível definir uma função fitness que meça a qualidade das soluções;
- Quando as soluções podem ser codificadas de forma relativamente simples para implementação computacional.

São particularmente eficientes em problemas de **otimização de funções**, mesmo sem conhecimento específico do domínio (guiam-se apenas pela função objetivo).

## 13) Representação binária para "maximizar x²" com x ∈ [0,7]

Como x varia de 0 a 7, bastam **3 bits** (2³ = 8 combinações).

- **Gene/cromossomo (exemplo):** `1 0 1`
- **Decodificação:** `101` em binário = 1·2² + 0·2¹ + 1·2⁰ = 4 + 0 + 1 = **5**
- **Valor da função fitness:** f(x) = x² → f(5) = 5² = **25**

| Cromossomo | x (decodificado) | Fitness f(x)=x² |
|---|---|---|
| 000 | 0 | 0 |
| 001 | 1 | 1 |
| 010 | 2 | 4 |
| 011 | 3 | 9 |
| 100 | 4 | 16 |
| **101** | **5** | **25** |
| 110 | 6 | 36 |
| 111 | 7 | 49 |

(O ótimo global desse problema é o cromossomo `111`, x = 7, fitness = 49.)

---

## 14) Explique, em linhas gerais, como a BT evita ficar presa em ótimos locais.

A Busca Tabu aceita se mover para o melhor vizinho disponível **mesmo que ele seja pior** que a solução atual, desde que o movimento não esteja proibido (tabu). Isso permite escapar temporariamente de vales/ótimos locais em busca de regiões melhores do espaço de soluções. A lista tabu evita que o algoritmo desfaça imediatamente o movimento recém-feito, o que causaria um ciclo e prenderia a busca sempre no mesmo ótimo local.

## 15) O que é a lista tabu e qual sua função?

É uma estrutura de memória que armazena os **movimentos recentes proibidos** (não soluções proibidas, mas os movimentos que desfariam ou repetiriam passos recentes). Cada movimento proibido recebe um **tenure** (número de iterações restantes de proibição), decrescido a cada iteração. Sua função é evitar ciclos e forçar a busca a explorar regiões novas do espaço de soluções.

## 16) Diferencie memória de curto prazo e memória de longo prazo.

- **Memória de curto prazo (recency):** guarda os movimentos feitos recentemente, indicando quais estão temporariamente proibidos — evita ciclos imediatos.
- **Memória de longo prazo (frequency):** conta quantas vezes cada movimento foi realizado ao longo de toda a execução; usada para **diversificação**, penalizando movimentos muito frequentes e incentivando a exploração de movimentos raros/regiões pouco visitadas.

## 17) O que é o critério de aspiração e em que situação ele é usado?

É uma regra de exceção à lista tabu: um movimento marcado como tabu pode ser executado se ele levar a uma solução **melhor do que a melhor solução encontrada até o momento (best-so-far)**. É usado quando o único caminho para melhorar significativamente a solução global passa por um movimento tabu, valendo a pena quebrar a proibição pelo ganho obtido.

## 18) No problema das 8 rainhas, qual é o objetivo da busca?

Posicionar as 8 rainhas no tabuleiro de forma que **nenhuma ataque outra** (mesma linha, coluna ou diagonal), minimizando o número de pares de rainhas em conflito até chegar a **zero ataques**.

## 19) Como são definidos os vizinhos de uma solução?

Um vizinho é obtido a partir de **um único movimento**: no problema das 8 rainhas, mover uma única rainha para uma linha diferente dentro de sua própria coluna. O conjunto de vizinhos de uma solução é formado por todos os movimentos possíveis de uma única rainha por vez (o total de vizinhos é a soma das posições alternativas disponíveis para cada rainha).

## 20) Explique o conceito de penalização em problemas com restrições.

Quando um movimento pode gerar uma solução **infactível** (que viola alguma restrição, como capacidade de um agente/recurso), uma estratégia é permitir essa solução, mas **penalizá-la** na função objetivo. A penalização é calculada multiplicando a quantidade excedida pela restrição por um **parâmetro positivo P**, somando esse valor ao custo da solução. Valores muito altos de P fazem a busca priorizar soluções factíveis; valores muito baixos permitem mais soluções infactíveis.

## 21) Em que tipo de problema a BT é mais indicada?

Em problemas de **otimização combinatória** com espaço de soluções **discreto**, mas que cresce **exponencialmente** com o tamanho da entrada — como o problema das 8 rainhas, a mochila binária, o caixeiro viajante (TSP), a designação generalizada (PDG), problemas de roteamento e até a calibração de hiperparâmetros em Machine Learning.

## 22) Duas iterações manuais da BT para o problema das 8 rainhas (solução inicial com duas rainhas na mesma linha)

Considerando um tabuleiro reduzido de 4 colunas (R1 a R4), com uma solução inicial contendo duas rainhas na mesma linha:

**Solução inicial:** 4 ataques.

**Iteração 1:**
- Avaliam-se os vizinhos gerados ao mover cada rainha (R1, R2, R3, R4) para as linhas disponíveis em sua coluna, recalculando o número de ataques para cada candidato.
- O melhor vizinho encontrado é obtido movendo **R1**, resultando em **2 ataques** (melhora em relação aos 4 iniciais).
- Como esse valor é menor que o melhor conhecido, atualiza-se **Melhor = 2**; a rainha movida (R1) entra na lista tabu, não podendo ser movida na próxima iteração.

**Iteração 2:**
- Partindo da solução com 2 ataques (sem poder mover R1, que está tabu), avaliam-se os vizinhos possíveis movendo R2, R3 ou R4.
- O melhor vizinho encontrado reduz o resultado para **1 ataque**.
- Atualiza-se **Melhor = 1**; a rainha movida na iteração anterior (R1) sai da lista tabu, e a rainha usada nesta iteração (R2) entra em seu lugar.

**Melhora obtida:** 4 ataques (inicial) → 2 ataques (iteração 1) → 1 ataque (iteração 2), evidenciando a convergência progressiva da BT rumo à solução ótima (0 ataques).

---

## 23) Diferencie a abordagem dos AGs e dos ACOs quanto à estratégia de busca.

**AGs** baseiam-se em **competição** entre indivíduos de uma população (seleção dos mais aptos, cruzamento, mutação, elitismo). **ACO** baseia-se em **cooperação** indireta entre agentes (formigas), que compartilham informação através do feromônio depositado no ambiente, reforçando coletivamente os melhores caminhos ao longo das iterações.

## 24) O que é o feromônio e qual seu papel no algoritmo?

É a substância que as formigas depositam ao longo do trajeto percorrido. Funciona como uma **memória coletiva**: caminhos com mais feromônio têm maior chance de serem escolhidos por outras formigas. Caminhos curtos são percorridos mais rapidamente e mais vezes (acumulando mais feromônio); caminhos longos acumulam menos e, como o feromônio evapora com o tempo, tendem a ser esquecidos.

## 25) Explique o conceito de estigmergia.

É a comunicação **indireta** entre os agentes de um sistema auto-organizado. No ACO, as formigas não se comunicam diretamente, mas sim através das alterações que fazem no ambiente (a quantidade de feromônio em cada caminho). Está associada ao controle descentralizado (cada agente conhece o problema apenas localmente) e à heterarquia densa (ausência de controle centralizado vertical) desses sistemas.

## 26) O que é a heurística de visibilidade (ηᵢⱼ) e como é calculada?

Representa o quão atrativo é, em termos de distância, seguir do nó i para o nó j. É calculada como o **inverso da distância**: **ηᵢⱼ = 1/dᵢⱼ**. Quanto menor a distância, maior o valor de ηᵢⱼ — ou seja, caminhos mais curtos têm maior visibilidade/atratividade.

## 27) Qual é o objetivo principal da atualização da matriz de feromônios?

Reforçar os caminhos percorridos pelas formigas (mais reforço para rotas mais curtas/melhores) e, simultaneamente, permitir que caminhos pouco usados percam relevância pela evaporação — fazendo o algoritmo aprender progressivamente quais são os melhores caminhos ao longo das iterações, até convergir para uma solução de boa qualidade.

## 28) O que representa o parâmetro σ (sigma) e qual sua função?

σ (sigma) representa a **taxa de evaporação do feromônio** (também chamada de ρ). Define qual fração do feromônio é perdida a cada iteração (por exemplo, σ = 0,1 significa que 10% do feromônio evapora a cada rodada), evitando que trilhas antigas dominem indefinidamente o processo.

## 29) Explique a importância do processo de evaporação do feromônio.

Sem evaporação, o feromônio se acumularia indefinidamente e os primeiros caminhos encontrados dominariam a busca, mesmo que não fossem os melhores. A evaporação garante que trilhas antigas não dominem o processo, permitindo que o algoritmo continue explorando novas rotas e evitando a convergência prematura para soluções ruins — equilibrando **exploração** (testar novos caminhos) e **explotação** (seguir os caminhos já conhecidos como bons).

## 30) Em quais tipos de problemas o ACO é mais aplicado?

Problemas de **otimização combinatória**, com destaque para o **Problema do Caixeiro Viajante (TSP)** — sua aplicação original —, problemas de **roteamento** (redes, distribuição) e problemas não lineares em que soluções podem ser construídas incrementalmente por agentes que compartilham informação via feromônio (ex.: restauração de redes elétricas de distribuição).

## 31) Aplicação do ACO com iterações (grafo do exercício)

**Grafo dado** (cidades e distâncias):

- 1 = Campinas, 2 = Manaus, 3 = Fortaleza, 4 = Salvador
- d(1,2) = 15 · d(1,3) = 13 · d(1,4) = 14 · d(2,3) = 10 · d(2,4) = 20 · d(3,4) = 12

**Parâmetros adotados** (mesmos usados nos exemplos do slide): τ inicial = 0,1 em todas as arestas; α = 1; β = 1; Q = 10; σ (taxa de evaporação) = 0,1; uma formiga parte de cada cidade (F1 de 1, F2 de 2, F3 de 3, F4 de 4).

**Heurística de visibilidade (ηᵢⱼ = 1/dᵢⱼ):**

| Aresta | Distância | η = 1/d |
|---|---|---|
| 1-2 | 15 | 0,0667 |
| 1-3 | 13 | 0,0769 |
| 1-4 | 14 | 0,0714 |
| 2-3 | 10 | 0,1000 |
| 2-4 | 20 | 0,0500 |
| 3-4 | 12 | 0,0833 |

### Iteração 1

Como τ inicial é igual (0,1) em todas as arestas, a atratividade (τ·η) é proporcional apenas a η nesta primeira iteração. Calculando as probabilidades p(i,j) em cada nó (normalizando pela soma das atratividades disponíveis) e seguindo, em cada passo, a aresta de maior probabilidade:

- **F1** (parte de 1): 1 → 3 (maior atratividade) → 2 → 4 → volta a 1. Rota: **1-3-2-4-1**, custo = 13+10+20+14 = **57**
- **F2** (parte de 2): 2 → 3 → 4 → 1 → volta a 2. Rota: **2-3-4-1-2**, custo = 10+12+14+15 = **51**
- **F3** (parte de 3): 3 → 2 → 1 → 4 → volta a 3. Rota: **3-2-1-4-3**, custo = 10+15+14+12 = **51**
- **F4** (parte de 4): 4 → 3 → 2 → 1 → volta a 4. Rota: **4-3-2-1-4**, custo = 12+10+15+14 = **51**

Note que existem apenas 3 ciclos hamiltonianos possíveis nesse grafo de 4 cidades: {1-2-3-4-1} (custo 51 — o ótimo), {1-3-2-4-1} (custo 57) e {1-2-4-3-1} (custo 60). Três das quatro formigas (F2, F3, F4) já encontram o ciclo ótimo (custo 51); apenas F1 encontra o segundo melhor (57).

**Depósito de feromônio (Δτ = Q/dₖ):**
- F1 (57): Δτ = 10/57 ≈ 0,1754
- F2, F3, F4 (51 cada): Δτ = 10/51 ≈ 0,1961

**Atualização da matriz (τ_novo = (1-σ)·τ_antigo + Σ Δτ recebido em cada aresta):**

| Aresta | Depósito recebido | τ novo = 0,9×0,1 + depósito |
|---|---|---|
| 1-2 | 0,1961×3 = 0,5883 (F2,F3,F4) | 0,6783 |
| 2-3 | 0,1754+0,1961×3 = 0,7637 (todas as 4 formigas) | 0,8537 |
| 3-4 | 0,1961×3 = 0,5883 (F2,F3,F4) | 0,6783 |
| 1-4 | 0,1754+0,1961×3 = 0,7637 (todas as 4 formigas) | 0,8537 |
| 1-3 | 0,1754 (só F1) | 0,2654 |
| 2-4 | 0,1754 (só F1) | 0,2654 |

As arestas do ciclo ótimo (1-2, 2-3, 3-4, 1-4) já saem bem mais reforçadas que a diagonal 1-3/2-4.

### Iteração 2

Recalculando a atratividade τ·η com a matriz atualizada:

| Aresta | τ | η | τ·η |
|---|---|---|---|
| 1-2 | 0,6783 | 0,0667 | 0,0452 |
| 1-3 | 0,2654 | 0,0769 | 0,0204 |
| 1-4 | 0,8537 | 0,0714 | 0,0610 |
| 2-3 | 0,8537 | 0,1000 | 0,0854 |
| 2-4 | 0,2654 | 0,0500 | 0,0133 |
| 3-4 | 0,6783 | 0,0833 | 0,0565 |

Repetindo a construção das rotas (escolhendo, a cada passo, a aresta de maior atratividade disponível), as quatro formigas agora convergem para o **mesmo ciclo ótimo**:

- F1: 1-4-3-2-1, custo = 14+12+10+15 = **51**
- F2: 2-3-4-1-2, custo = 10+12+14+15 = **51**
- F3: 3-2-1-4-3, custo = 10+15+14+12 = **51**
- F4: 4-1-2-3-4, custo = 14+15+10+12 = **51**

Todas as formigas percorrem as mesmas 4 arestas do ciclo ótimo (1-2, 2-3, 3-4, 1-4), cada uma com Δτ = 10/51 ≈ 0,1961, totalizando um depósito de 4×0,1961 ≈ 0,7844 em cada uma dessas arestas; as arestas 1-3 e 2-4 não recebem depósito nesta iteração.

**Nova matriz de feromônio (τ_novo = 0,9×τ_antigo + depósito):**

| Aresta | τ novo |
|---|---|
| 1-2 | 0,9×0,6783 + 0,7844 ≈ **1,3949** |
| 2-3 | 0,9×0,8537 + 0,7844 ≈ **1,5527** |
| 3-4 | 0,9×0,6783 + 0,7844 ≈ **1,3949** |
| 1-4 | 0,9×0,8537 + 0,7844 ≈ **1,5527** |
| 1-3 | 0,9×0,2654 ≈ **0,2389** |
| 2-4 | 0,9×0,2654 ≈ **0,2389** |

### Conclusão

Após apenas duas iterações, o ACO já concentra fortemente o feromônio no ciclo **1 → 2 → 3 → 4 → 1** (custo total = **51**, o ótimo global do grafo dado), enquanto as arestas da diagonal (1-3 e 2-4) ficam com feromônio bem menor. Isso ilustra bem o mecanismo do algoritmo: reforço dos caminhos mais curtos a cada iteração, combinado com a evaporação, levando a colônia a convergir para a melhor rota encontrada.
