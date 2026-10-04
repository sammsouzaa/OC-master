# Resumo — Algoritmos Genéticos (AG)

> Resumo focado nos pontos cobrados na Lista de Exercícios 1 (questões 1 a 13), com base no conteúdo do slide "Tópico 1 - Algoritmos Genéticos".

## 1. Conceitos gerais de otimização

- **Áreas que se beneficiam de otimização:** engenharia (projeto de estruturas, roteirização), machine learning (ajuste de hiperparâmetros), logística/distribuição, telecomunicações, entre outras — qualquer problema em que se busca a melhor solução dentro de um espaço de possibilidades.
- **Heurísticas x metaheurísticas:** heurísticas são regras práticas voltadas a um problema específico, sem garantia de otimalidade, mas eficientes na prática; metaheurísticas são estratégias mais genéricas e de alto nível (como os AGs, a Busca Tabu e o ACO) que orientam heurísticas de busca para explorar o espaço de soluções de forma mais ampla, sendo aplicáveis a diversas classes de problemas.
- **Objetivo comum dos métodos de otimização estudados** (AG, Busca Tabu, ACO): encontrar a melhor solução (ou um conjunto de boas soluções) para um problema, evitando ficar preso em ótimos locais e evoluindo/gerando a busca a cada iteração.
- **Ótimo global:** é a melhor solução possível dentro de todo o espaço de busca, e não apenas a melhor dentro de uma vizinhança restrita (como ocorre no ótimo/máximo local, quando o algoritmo converge para uma solução localmente boa mas ignora o restante do espaço).

## 2. Origem e ideia central

- Os AGs são inspirados na **teoria da evolução de Darwin** (seleção natural): indivíduos mais adaptados sobrevivem e se reproduzem mais, passando suas características adiante; variações favoráveis tendem a permanecer na população.
- Propostos por **John Holland (1975)**, em *"Adaptation in Natural and Artificial Systems"*, e popularizados por **Goldberg (1989)**, em *"Genetic Algorithms in Search, Optimization and Machine Learning"*.
- São técnicas de busca que representam as variáveis do problema como **genes em um cromossomo**, combinando seleção natural, cruzamento e mutação para encontrar a(s) melhor(es) solução(ões).
- Diferem dos métodos tradicionais porque: (1) trabalham com uma **codificação** dos parâmetros, não com os parâmetros diretamente; (2) trabalham com uma **população**, não com um único ponto; (3) usam informações de custo/recompensa, sem precisar de derivadas; (4) usam regras de transição **probabilísticas**, não determinísticas.
- Vantagem de trabalhar com população: reduz o risco de ficar preso em um máximo/ótimo local, pois vários pontos do espaço de busca são explorados ao mesmo tempo.

## 3. Os três elementos básicos de uma tarefa de busca/otimização (Q5)

1. **Codificação do problema** — representar o problema de forma que o algoritmo consiga manipulá-lo (geralmente a etapa mais complexa).
2. **Espaço de busca** — conjunto de todas as soluções possíveis para o problema.
3. **Função de avaliação (fitness)** — mede quão boa é cada solução; varia conforme o problema.

## 4. Terminologia: gene, cromossomo, população (Q6)

- **Gene:** menor unidade de informação, representa uma característica/variável codificada (ex.: um bit ou um valor).
- **Cromossomo:** conjunto de genes que representa uma solução completa (um indivíduo) para o problema.
- **População:** conjunto de vários cromossomos (indivíduos) que existem simultaneamente em uma geração.
- Outros termos relacionados vistos no slide: **alelo** (valor que um gene pode assumir), **genótipo** (composição genética do indivíduo), **fenótipo** (como essa composição se expressa/é avaliada) e **geração** (cada "rodada" da população ao longo da evolução).

## 5. Representação dos indivíduos

- **Binária (clássica):** genes representados por cadeias de bits; usada na função fitness, no cruzamento e na mutação.
- **Real:** indivíduos representados diretamente por valores inteiros ou reais.

## 6. Função fitness (Q7)

- É a função que **avalia a aptidão** de cada indivíduo da população, geralmente derivada da função objetivo do problema.
- Muitas vezes exige **decodificar** o indivíduo (ex.: binário → valor real) antes de calcular seu valor.
- É totalmente dependente do problema, e seu resultado orienta a **seleção**, o **cruzamento** e o **elitismo** — sem ela, o algoritmo não teria como distinguir soluções boas de ruins.

## 7. Ciclo básico de um AG

1. **Inicialização:** cria-se uma população de N indivíduos, geralmente com valores aleatórios (podendo ser direcionados se houver conhecimento prévio do problema).
2. **Cálculo da aptidão (fitness):** avalia-se cada indivíduo e ordena-se a população pela aptidão.
3. **Seleção:** escolhem-se indivíduos mais aptos para gerar a próxima geração. Métodos vistos:
   - **Amostragem direta** ("os n melhores").
   - **Amostragem aleatória simples** (todos com a mesma chance).
   - **Seleção por torneio** (sorteiam-se n indivíduos e escolhe-se o melhor entre eles).
   - **Seleção por ranking** (probabilidade proporcional à posição no ranking, não ao fitness absoluto).
   - **Roleta (amostragem estocástica)** — proposta por Goldberg (1989): cada indivíduo ocupa uma fatia da "roleta" proporcional ao seu fitness absoluto (indivíduos muito bons podem dominar, diferente do ranking).
4. **Cruzamento (crossover):** combina o material genético de dois pais.
5. **Mutação:** altera aleatoriamente genes dos filhos.
6. **Elitismo (opcional):** preserva os melhores indivíduos sem alterá-los.
7. **Critério de parada** e repetição do ciclo.

## 8. Cruzamento — um ponto x dois pontos (Q8)

- **Cruzamento de um ponto:** define-se **um único ponto de corte** no cromossomo; os segmentos após esse ponto são trocados entre os pais.
- **Cruzamento de dois pontos:** definem-se **dois pontos de corte**; troca-se apenas o segmento entre eles. Isso promove maior mistura genética, gera soluções mais diversas e evita que apenas as extremidades dos cromossomos sejam preservadas (o que acontece no cruzamento de um ponto).
- Também existem o **cruzamento de pontos aleatórios** (posição de corte varia a cada operação) e o **cruzamento uniforme** (usa uma "máscara" fixa definida previamente, que não muda ao longo do processo).
- **Taxa de cruzamento:** normalmente entre 60% e 90%. Sorteia-se α ∈ [0,1]; se α for menor que a taxa, o cruzamento ocorre; caso contrário, os pais seguem inalterados para a próxima geração.

## 9. Mutação (Q10)

- Aplicada aos cromossomos dos **filhos**, gene a gene, cada um sujeito a uma **taxa de mutação** (probabilidade de sofrer alteração).
- **Função:** introduzir variabilidade genética na população, evitando estagnação (um gene sempre com o mesmo valor) e ajudando a escapar de ótimos locais.
- **Taxa de mutação:** normalmente entre 1% e 5%. Sorteia-se α ∈ [0,1] para cada gene; se α for menor que a taxa, o gene muta.
- Taxa muito alta → busca praticamente aleatória, com risco de destruir boas soluções. Taxa muito baixa → risco de estagnação.

## 10. Elitismo (Q9)

- Técnica que **preserva o(s) melhor(es) indivíduo(s)** de cada geração, passando-o(s) diretamente para a próxima geração **sem sofrer cruzamento ou mutação**.
- Importância: acelera a convergência do algoritmo e evita que os elementos mais aptos sejam perdidos ou degradados pelos operadores genéticos.

## 11. Parâmetros genéticos e faixas típicas (Q11)

- **Tamanho da população:** afeta diretamente o desempenho — população pequena cobre pouco o espaço de busca; população grande cobre melhor, mas exige mais recursos computacionais e tempo.
- **Taxa de cruzamento:** tipicamente **60% a 90%** (0,6 a 0,9). Taxa alta introduz estruturas novas rapidamente, mas pode destruir boas soluções; taxa baixa deixa o algoritmo lento para convergir.
- **Taxa de mutação:** tipicamente **1% a 5%** (0,01 a 0,05). Evita estagnação, mas se muito alta torna a busca aleatória demais.
- **Critérios de parada:** número máximo de gerações; valor ótimo já alcançado (se conhecido); convergência da função objetivo (valores não mudam mais após várias gerações — pode indicar ótimo global **ou** um máximo local).

## 12. Quando usar um AG (Q12)

AGs são indicados quando:
- O espaço de busca é grande, mas pode ser delimitado dentro de uma faixa de valores;
- É possível definir uma função fitness que meça a qualidade das soluções;
- As soluções podem ser codificadas de forma relativamente simples para implementação computacional.

São muito usados em problemas de **otimização de funções**, sendo eficientes mesmo sem conhecimento específico do domínio do problema (guiam-se apenas pela função objetivo).

## 13. Exemplo prático — representação binária para maximizar x² (Q13)

Para o problema **"maximizar x² com x ∈ [0,7]"**:

- Como x vai de 0 a 7, bastam **3 bits** para representar todos os valores possíveis (2³ = 8 combinações, de 0 a 7).
- **Gene/cromossomo (exemplo):** `1 0 1` (3 genes binários formando um cromossomo).
- **Decodificação:** o cromossomo binário é convertido para decimal. `101` em binário = 1·2² + 0·2¹ + 1·2⁰ = 4 + 0 + 1 = **5**.
- **Valor da função fitness:** f(x) = x² → f(5) = 5² = **25**.

| Cromossomo (binário) | x (decodificado) | Fitness f(x) = x² |
|---|---|---|
| 000 | 0 | 0 |
| 001 | 1 | 1 |
| 010 | 2 | 4 |
| 011 | 3 | 9 |
| 100 | 4 | 16 |
| **101** | **5** | **25** |
| 110 | 6 | 36 |
| 111 | 7 | 49 |

O AG buscaria, através de seleção, cruzamento e mutação sobre cromossomos como esse, convergir para o cromossomo `111` (x = 7, fitness = 49), que é o ótimo global desse problema simples.

---
*Bibliografia citada no slide: Holland (1975), Goldberg (1989), Schneider (1998), entre outras referências sobre seleção natural e biologia evolutiva usadas como analogia.*
