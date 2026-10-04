# Resumo — Busca Tabu (BT)

> Resumo focado nos pontos cobrados na Lista de Exercícios 1 (questões 14 a 22), com base no conteúdo do slide "Tópico 2 - Busca Tabu".

## 1. Origem e ideia central

- Proposta por **Fred Glover em 1986**.
- Surgiu para **guiar uma heurística de busca local** na exploração do espaço de soluções **além da otimalidade local**, usando estruturas de memória (tabelas) para evitar retrabalho e ciclos.
- Indicada para problemas de otimização em que o conjunto de soluções é **discreto**, mas cresce **exponencialmente**.
- Funcionamento geral: parte de uma solução inicial e se move, a cada iteração, para uma solução **vizinha** (obtida por um "movimento", como *swap* — troca de posições — ou *insertion* — inserção de um elemento em outra posição).

## 2. Como a BT evita ficar presa em ótimos locais (Q14)

- Diferente de uma busca local pura (que para ao não encontrar mais vizinhos melhores), a BT **aceita mover-se para o melhor vizinho disponível mesmo que ele seja pior que a solução atual**, desde que esse movimento não esteja proibido (tabu).
- Isso permite "escapar" de vales/ótimos locais explorando temporariamente soluções piores, na esperança de encontrar, adiante, uma solução melhor que a global até então.
- O mecanismo da **lista tabu** evita que o algoritmo desfaça imediatamente o movimento que acabou de fazer (o que causaria um ciclo, voltando sempre ao mesmo ótimo local).

## 3. Lista tabu (Q15)

- É uma estrutura de memória que armazena **movimentos recentes proibidos** (não soluções proibidas, mas sim os movimentos que levariam de volta a soluções já visitadas).
- Cada movimento proibido recebe um **tenure** (número de iterações restantes em que ele fica proibido); a cada iteração esse contador decresce até liberar o movimento novamente.
- **Função:** evitar ciclos e o recálculo/retorno a soluções já exploradas, forçando a busca a se mover para regiões novas do espaço de soluções.

## 4. Memória de curto prazo x memória de longo prazo (Q16)

- **Memória de curto prazo (recency):** guarda os movimentos feitos **recentemente**, indicando quais estão temporariamente proibidos (tabu) — evita ciclos imediatos.
- **Memória de longo prazo (frequency):** conta **quantas vezes** cada movimento foi realizado ao longo de toda a execução.
  - Usada para **diversificação:** movimentos muito frequentes podem ser penalizados (para não repetir sempre os mesmos caminhos), enquanto movimentos raros podem receber um bônus, incentivando a exploração de regiões ainda pouco visitadas do espaço de busca.

## 5. Critério de aspiração (Q17)

- É uma **regra de exceção** à lista tabu: mesmo que um movimento esteja marcado como tabu, ele pode ser executado se levar a uma solução **melhor do que a melhor solução encontrada até o momento (best-so-far)**.
- Situação de uso: quando o único caminho para melhorar significativamente a solução global passa por um movimento tabu — nesse caso, "vale a pena" quebrar a proibição, pois o ganho supera o risco de ciclo.

## 6. Problema das 8 Rainhas (Q18, Q19, Q22)

- **Objetivo da busca (Q18):** posicionar as 8 rainhas no tabuleiro de forma que **nenhuma ataque outra** (mesma linha, coluna ou diagonal) — ou seja, minimizar o número de pares de rainhas em conflito até chegar a **zero ataques**.
- Representação: cada rainha fica fixa em uma coluna e só pode mudar de **linha**.
- **Função-objetivo:** número de pares de rainhas se atacando (quanto menor, melhor; o ideal é 0).
- **Definição de vizinhos (Q19):** um vizinho é obtido movendo **uma única rainha** para uma linha diferente dentro da sua coluna (um único movimento a partir da solução atual). Se cada rainha pode ir para outras posições possíveis, o total de vizinhos de uma solução é a soma dessas possibilidades (ex.: em um exemplo simplificado com 4 rainhas e 3 posições livres cada, há 12 vizinhos possíveis).
- O movimento realizado (mover determinada rainha) entra na lista tabu por algumas iterações, para não desfazer imediatamente o que acabou de ser feito.

### Exemplo resolvido (simplificado, base para Q22 — duas iterações)

Considerando um tabuleiro reduzido (4 colunas) com uma solução inicial contendo **duas rainhas na mesma linha** (gerando ataques):

**Solução inicial:** 4 ataques.

**Iteração 1:**
- Avaliam-se os vizinhos gerados ao mover cada rainha (R1, R2, R3, R4) para as linhas disponíveis em sua coluna, recalculando o número de ataques para cada candidato.
- No exemplo do slide, o melhor vizinho encontrado foi **R1 → nova linha**, resultando em **2 ataques** (melhora em relação aos 4 iniciais).
- Como esse valor é menor que o melhor conhecido, atualiza-se **Melhor = 2**, e a rainha movida (R1) entra na lista tabu — não pode ser movida novamente na próxima iteração.

**Iteração 2:**
- Partindo da nova solução (2 ataques), avaliam-se os vizinhos possíveis (agora sem poder mover R1, que está tabu), movendo R2, R3 ou R4.
- O melhor vizinho encontrado reduz o resultado para **1 ataque**.
- Atualiza-se **Melhor = 1**; a rainha movida anteriormente (R1) sai da lista tabu e a rainha usada nesta iteração (R2) entra em seu lugar.

**Melhora obtida:** de 4 ataques (solução inicial) → 2 ataques (iteração 1) → 1 ataque (iteração 2), evidenciando a convergência progressiva da BT em direção à solução ótima (0 ataques).

## 7. Penalização em problemas com restrições (Q20)

- Quando um movimento pode gerar uma solução **infactível** (que viola alguma restrição, como capacidade de um agente/recurso), uma estratégia é **permitir** essa solução, mas **penalizá-la** na função objetivo.
- A penalização é calculada multiplicando a **quantidade excedida** (o quanto a restrição foi violada) por um **parâmetro positivo P**, e esse valor é somado ao custo da solução.
- Efeito do parâmetro P:
  - **P muito alto** → a busca prioriza fortemente soluções factíveis (evita infactibilidade a qualquer custo).
  - **P muito baixo** → pode permitir um número grande de soluções infactíveis.
- Exemplo do slide (Problema da Designação Generalizada — PDG): custo total inicial de uma alocação = 258; após aplicar a BT com movimentos de inserção (permitindo temporariamente violações de capacidade penalizadas com P=2), o algoritmo consegue reduzir o custo total ajustado e, ao final das iterações, encontrar uma solução **viável e mais barata** (por exemplo, evoluindo de 258 para 230, e depois para 166 em iterações seguintes), mostrando como a BT escapa de ótimos locais mesmo aceitando violações temporárias de restrições.

## 8. Em que tipo de problema a BT é mais indicada (Q21)

- Problemas de **otimização combinatória** com espaço de soluções **discreto**, mas muito grande (cresce exponencialmente com o tamanho da entrada) — exemplos vistos no slide: Problema das 8 Rainhas, Problema da Mochila Binária, Problema do Caixeiro Viajante (TSP), Problema da Designação Generalizada (PDG), problemas de roteamento, e também a calibração de hiperparâmetros em Machine Learning (ex.: K e "weights" do classificador KNN).
- É especialmente útil quando métodos de busca local tradicionais ficariam presos em ótimos locais e é necessário um mecanismo de memória para guiar a exploração de forma mais inteligente.

---
*Bibliografia citada no slide: Glover (1986); Glover & Laguna (1997) — "Tabu Search Background"; RapidMiner (2024).*
