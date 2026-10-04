# Resumo — Colônia de Formigas (ACO — Ant Colony Optimization)

> Resumo focado nos pontos cobrados na Lista de Exercícios 1 (questões 23 a 31), com base no conteúdo do slide "Tópico 3 - Colônia de Formigas".

## 1. Origem e ideia central

- Proposta no início dos anos 90 por **Marco Dorigo** (pesquisa de doutorado, com foco no **TSP** — Problema do Caixeiro Viajante), depois difundida em parceria com **Gambardella**.
- Inspirada no comportamento de colônias de insetos: individualmente cada formiga é simples, mas a organização coletiva resolve problemas complexos.
- Aplicada a diversos problemas combinatórios e não lineares (TSP, roteamento, etc.).

## 2. AG x ACO — estratégias de busca (Q23)

- **Algoritmos Genéticos:** baseados em **competição** entre indivíduos (seleção dos mais aptos, cruzamento, mutação, elitismo).
- **ACO:** baseado em **cooperação** indireta entre os agentes (formigas), que compartilham informação através do feromônio depositado no ambiente — não há "competição" direta entre soluções, mas sim reforço coletivo dos melhores caminhos ao longo das iterações.

## 3. Feromônio (Q24)

- É a substância química que as formigas depositam ao longo do trajeto percorrido.
- **Papel no algoritmo:** funciona como um mecanismo de **memória coletiva** — caminhos com mais feromônio têm maior chance de serem escolhidos por outras formigas. Caminhos curtos são percorridos mais rapidamente e mais vezes, acumulando mais feromônio; caminhos longos acumulam menos e, como o feromônio evapora com o tempo, tendem a ser "esquecidos".
- No início da busca, o processo é praticamente "cego" (sem informação de feromônio acumulada), e a solução vai se refinando a cada iteração.

## 4. Estigmergia (Q25)

- É a **comunicação indireta** entre os agentes de um sistema auto-organizado — nesse caso, as formigas "se comunicam" não diretamente, mas por meio das alterações que fazem no ambiente (a quantidade de feromônio em cada caminho).
- Está associada a duas outras características dos sistemas baseados em insetos sociais vistas no slide: **controle descentralizado** (cada agente só conhece o problema localmente) e **heterarquia densa** (não existe um controle centralizado vertical).

## 5. Heurística de visibilidade — ηᵢⱼ (Q26)

- Representa o quão "atrativo" é, do ponto de vista da distância, seguir de um nó i para um nó j.
- Calculada como o **inverso da distância**: **ηᵢⱼ = 1 / dᵢⱼ**.
- Quanto **menor a distância**, **maior** o valor de ηᵢⱼ, ou seja, caminhos mais curtos têm maior visibilidade/atratividade.
  - Exemplo do slide: para distância 1 → η = 1/1 = 1; para distância 9 → η = 1/9 ≈ 0,11 (caminho bem menos atrativo).

## 6. Etapas de um ACO e a atualização da matriz de feromônios (Q27)

**Etapas gerais de um ACO:**
1. Inicialização dos parâmetros;
2. Geração da matriz de feromônio inicial (valores iguais e pequenos para todas as arestas, ex.: τᵢⱼ = 0,1);
3. Construção de uma heurística construtiva para o problema;
4. Geração de uma população de formigas de forma construtiva (cada formiga monta uma rota/solução);
5. **Atualização da matriz de feromônios** — repetida a cada iteração até o critério de parada.

**Cálculo da probabilidade de escolha de um caminho:**
- Combina-se o feromônio (τᵢⱼ) com a heurística de visibilidade (ηᵢⱼ): **τᵢⱼ · ηᵢⱼ**, que define a atratividade daquele caminho.
- A probabilidade final **p(i,j)** de uma formiga escolher aquele caminho é obtida dividindo essa atratividade pela soma das atratividades de todos os caminhos possíveis a partir do nó atual (normalização).
- A escolha da rota é **estocástica** (feita por sorteio, tipo "roleta"), o que evita que as formigas sempre sigam o mesmo caminho, favorecendo a exploração do espaço de soluções.

**Objetivo da atualização da matriz de feromônios (Q27):**
- Reforçar os caminhos percorridos pelas formigas (mais reforço para rotas mais curtas/melhores) e, ao mesmo tempo, permitir que caminhos pouco usados percam relevância (evaporação) — fazendo o algoritmo **aprender progressivamente** quais são os melhores caminhos ao longo das iterações.
- Depósito de feromônio: cada formiga deposita uma quantidade **Δτ**, calculada com base em **Q** (constante que define a intensidade base de feromônio) e **dₖ** (custo total da rota da formiga): rotas mais curtas (dₖ menor) resultam em mais feromônio depositado (recompensa); rotas mais longas resultam em menos feromônio.

## 7. Parâmetro σ (sigma) (Q28)

- **σ (sigma)** representa a **taxa de evaporação do feromônio** (também chamada de ρ).
- **Função:** define qual fração do feromônio é perdida a cada iteração (exemplo do slide: σ = 0,1, ou seja, 10% do feromônio evapora a cada rodada).
- Junto com σ, o slide também apresenta:
  - **α (alfa):** peso da influência do feromônio — quanto maior, mais as formigas seguem trilhas já bastante utilizadas.
  - **β (beta):** peso da influência da visibilidade/distância — quanto maior, mais as formigas preferem caminhos curtos.

## 8. Importância da evaporação do feromônio (Q29)

- Sem evaporação, o feromônio se acumularia indefinidamente e os primeiros caminhos encontrados dominariam a busca, mesmo que não fossem os melhores possíveis.
- A evaporação garante que **trilhas antigas não dominem o processo indefinidamente**, permitindo que o algoritmo continue explorando novas rotas e evitando estagnação/convergência prematura para soluções ruins.
- Complementa o mecanismo de exploração x explotação: **exploração** (tentar novos caminhos, mesmo parecendo piores, para não ficar preso em soluções locais) e **explotação** (seguir os caminhos já conhecidos como bons, com mais feromônio e menor distância).

## 9. Aplicações do ACO (Q30)

- Muito aplicado a problemas de **otimização combinatória**, com destaque para:
  - **Problema do Caixeiro Viajante (TSP)** — aplicação original do método;
  - **Problemas de roteamento** (ex.: redes, distribuição);
  - Problemas de **restauração/otimização de redes** (ex.: redes elétricas de distribuição, citado na bibliografia do slide);
  - De forma geral, problemas não lineares e combinatórios em que soluções podem ser construídas incrementalmente (passo a passo) por agentes que compartilham informação através de um mecanismo de reforço (feromônio).

## 10. Exemplo resolvido — ACO aplicado ao TSP (referência para a Q31)

O slide traz um exemplo passo a passo com 4 cidades (Campinas, Salvador, Fortaleza e Manaus), útil como modelo para aplicar o ACO com iterações:

1. **Inicialização:** matriz de feromônio com valores iguais para todas as arestas (ex.: τᵢⱼ = 0,1); cada formiga parte de uma cidade diferente.
2. **Cálculo da atratividade de cada aresta:** combina-se a heurística de visibilidade (ηᵢⱼ = 1/dᵢⱼ) com o feromônio atual (τᵢⱼ · ηᵢⱼ).
3. **Cálculo da probabilidade de escolha (p(i,j)):** normaliza-se a atratividade de cada aresta pela soma das atratividades disponíveis a partir do nó atual (excluindo cidades já visitadas).
4. **Construção da rota de cada formiga:** por sorteio (roleta) ponderado pelas probabilidades calculadas, cada formiga vai escolhendo a próxima cidade até visitar todas e retornar ao ponto de partida.
5. **Cálculo do custo total (dₖ)** de cada rota construída.
6. **Depósito de feromônio (Δτ):** cada formiga deposita feromônio nas arestas que percorreu, proporcional a Q/dₖ — rotas mais curtas depositam mais feromônio.
7. **Evaporação:** aplica-se a taxa σ sobre toda a matriz de feromônios, reduzindo o valor de todas as arestas antes de somar o novo feromônio depositado.
8. **Nova matriz de feromônio** = feromônio remanescente (após evaporação) + feromônio novo depositado pelas formigas.
9. Repetem-se os passos 2 a 8 por várias iterações — a cada rodada, as rotas mais curtas tendem a acumular mais feromônio e se tornar mais prováveis, enquanto arestas pouco usadas perdem relevância.
10. **Critérios de parada:** número de iterações pré-definido atingido; estagnação do método (rotas ou resultados param de mudar/melhorar); ou já ter atingido o melhor resultado conhecido.

---
*Bibliografia citada no slide: Dorigo, Di Caro & Gambardella (1999); Dorigo & Gambardella (1997); Goliatt, Angelo & Barbosa (2013); Marsh & Onof (2008); Silva (2016).*
