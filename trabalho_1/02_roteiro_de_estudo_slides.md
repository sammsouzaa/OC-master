# Roteiro de estudo — quais slides ler antes de implementar

Arquivo: `estudo_prova1/Tópico_1_-_Algoritmos_Genéticos.pdf` (71 páginas). Os números abaixo são o **número da página/slide** no PDF.

## Ler com atenção (é exatamente o que vocês implementam)

| Slides | Assunto | Liga com |
|---|---|---|
| 9, 11 | O que é um AG; três elementos (codificação, espaço de busca, fitness) | visão geral |
| 15, 17–18 | População evita ótimo local; parâmetros (x, y) e aptidão (z) no gráfico | por que usar população |
| 34 | Representação **real** (a de vocês) | `Individuo = (x, y)` |
| **37** | **Algoritmo básico de Goldberg** (inicializa, avalia, seleciona, cruza, muda, avalia) | `executar_ag` |
| 38 | Inicialização (valores aleatórios, dentro de limites) | `criar_populacao_inicial` |
| 40–41 | Cálculo da aptidão | `fitness`, `avaliar` |
| 42–43 | Ideia da seleção | `selecionar_por_ranking` |
| **45–47** | **Seleção por ranking** (tabela com ranks, e pizza: 4/28=0,14, 6/28=0,21, 7/28=0,25...) | `selecionar_por_ranking` |
| 52 | Cruzamento: troca de segmentos (conceito; é a base) | `cruzar_blx_alpha` |
| **56** | Cruzamento para representação **real**: operadores usam os valores dos pais (média simples, geométrica) | contexto |
| **57** | **BLX-α**: `F1 = P1 + β(P2 − P1)`, `β ∈ U[−α, 1+α]` (e aritmético, que não é o de vocês) | `cruzar_blx_alpha` |
| **59** | Taxa de cruzamento (60%–90%) e regra de sortear α | `taxa_cruzamento` |
| 60 | Mutação aplicada aos filhos, gene a gene | `mutar_uniforme` |
| **62** | **Mutação uniforme** (e gaussiana) para representação real | `mutar_uniforme` |
| **64** | Taxa de mutação (1%–5%) e regra de sortear α por gene | `taxa_mutacao` |
| **65** | **Elitismo** | `calcular_tamanho_elite`, `extrair_elite` |
| 66–68 | Parâmetros genéticos (população, taxa de cruzamento, taxa de mutação) | interface, experimentos |
| **69** | **Critérios de parada** (lembre: o enunciado proíbe parar por atingir o ótimo) | `convergiu` |

### Ordem recomendada de leitura
`34 → 37 → 38 → 40 → 45–47 → 56 → 57 → 59 → 60 → 62 → 64 → 65 → 69`, com `66–68` para escolher os parâmetros.

## Leitura rápida (contexto/teoria geral, útil para a apresentação)

| Slides | Assunto |
|---|---|
| 2–8 | Darwin e seleção natural (analogia biológica) |
| 10 | Holland (1975) e Goldberg (1989) |
| 12–14 | AGs x métodos tradicionais (4 diferenças) |
| 19–21 | Quando usar um AG |
| 22–33 | Terminologia: população, indivíduo, cromossomo, gene, alelo, genótipo, fenótipo, fitness, geração |
| 39 | Exemplo de inicialização dirigida |
| 44 | Amostragem direta e aleatória |

## Pode pular (só para binário ou para outras equipes)

| Slides | Assunto | Por quê |
|---|---|---|
| 48–51 | Roleta | a Equipe 9 usa ranking (mas entendam a diferença, pergunta provável) |
| 53–55 | Cruzamento de 2 pontos, pontos aleatórios, uniforme com máscara | só binário |
| 61 | Mutação por inversão de bits | só binário |
| 63 | Mutação creep e não-uniforme | são de outras equipes |

## O que cada slide deve deixar claro (autoteste)

Antes de programar cada parte, vocês devem conseguir responder sem olhar:

1. **Slide 37:** em que ordem acontecem avaliar, selecionar, cruzar e mutar? *(inicializa → avalia → [seleciona → cruza → muta → avalia] até parar)*
2. **Slides 45–47:** com fitness `45, 89, 125, 21, 52, 9, 19`, quais são os ranks e as probabilidades? *(ranks 4, 6, 7, 3, 5, 1, 2; soma = 28; probabilidades = rank/28)*
3. **Slide 57:** se `P1 = 2`, `P2 = 4`, `α = 0,5`, em que intervalo cai o filho? *([1, 5])*
4. **Slide 59:** como se decide se o cruzamento acontece? *(sorteia α em [0,1]; se α < taxa, cruza; senão os pais passam adiante)*
5. **Slide 62:** o que a mutação uniforme faz com o gene sorteado? *(troca por um valor uniforme entre o mínimo e o máximo)*
6. **Slide 64:** a mutação é decidida por indivíduo ou por gene? *(por gene)*
7. **Slide 65:** o que é elitismo e por que ele garante que o melhor nunca piora?
8. **Slide 69:** quais critérios de parada existem e qual deles o enunciado proíbe?

## Observação sobre o BLX-α do slide

O slide 57 escreve `F1 = P1 + β(P2 − P1)`. O slide não deixa explícito se o `β` é sorteado **por gene** ou **um só** para o par `(x, y)`. A versão mais comum sorteia **por gene**, que é a usada no código (`ag.py`). Vale perguntar ao professor, já que isso muda o resultado.
