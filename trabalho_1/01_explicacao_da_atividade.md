# Trabalho 1 de OC — Algoritmo Genético (2026)

**Equipe 9:** Samuel Moreira de Souza e Giovanni Nadalin Sansana
**Entrega:** **05/10/2026**, pela tarefa no Teams, mais apresentação do código.

Fontes: `1º_Trabalho_de_OC_2026.pdf` (regras e equipes) e `1º_Trabalho_de_OC_2025_funções.pdf` (catálogo das 13 funções; apesar do "2025" no nome, é o catálogo usado).

---

## 1. O que é a atividade

Implementar **do zero** um Algoritmo Genético (AG) que otimiza uma função de duas variáveis `Z = f(x, y)`. Cada equipe recebe uma combinação fixa de componentes (codificação, seleção, cruzamento, mutação, elitismo) e uma função. Você não escolhe nada disso: o enunciado diz que fugir da especificação conta como errado.

O AG evolui uma população de pares `(x, y)` ao longo de várias gerações. Em cada geração ele avalia o fitness, seleciona pais, cruza, muda e passa para a próxima geração. Espera-se que a população se concentre perto do ótimo da função.

## 2. Especificação da Equipe 9

| Item | Definição |
|---|---|
| Codificação | **Real** |
| Seleção | **Ranking** |
| Cruzamento | **BLX-α** |
| Mutação | **Uniforme** |
| Elitismo | **0,5% do tamanho da população** |
| Função | **Função 8** |

### Função 8

```
Z = 5 + 3x − 4y − x² + xy − y²
x ∈ [−10, 10]
y ∈ [−10, 10]
```

- Valor de referência (ótimo): **x = 0,6667, y = −1,6667, z = 9,3333**.
- É uma função **côncava com um único máximo**, então o problema é de **maximização** (as regiões claras dos gráficos do PDF são o melhor fitness).
- Verificação: ∂Z/∂x = 3 − 2x + y = 0 e ∂Z/∂y = −4 + x − 2y = 0 dão x = 2/3 e y = −5/3. Substituindo, Z = 9,3333.
- É uma função fácil, sem mínimos locais. Por isso a nota deve vir de implementar bem as peças e os gráficos pedidos, não de a função ser difícil.

## 3. Regras obrigatórias (resumo)

1. Seguir **exatamente** a especificação da equipe.
2. **Proibido** usar código pronto de AG (GitHub, Bitbucket, sites, bibliotecas de AG). Resultado: **nota zero**.
3. O enunciado diz **"Idem LLMs"**: usar LLM para gerar o código levava a nota zero. Você informou que o professor removeu essa regra em outro momento; **peça confirmação por escrito** (mensagem no Teams ou e-mail) e guarde. A regra sobre códigos prontos de repositórios (GitHub etc.) continua valendo.
4. Funções auxiliares da linguagem são permitidas (ordenar, exibir, salvar arquivo, números aleatórios).
5. Linguagens aceitas: **C, C++, Python, Java**.
6. Os parâmetros devem ser definidos **na interface do sistema**: taxa de cruzamento, taxa de mutação, tamanho da população e número de gerações.
7. Representação real deve permitir **3 casas decimais**.
8. (Regra da codificação binária, com bit de sinal sem complemento de dois: **não se aplica a vocês**, que usam real.)
9. **Ao final de cada geração**, gerar um gráfico da população no espaço de busca, **com o melhor indivíduo destacado**. Pode aparecer em tela ou ser gravado em disco e mostrado depois.
10. Gerar um **gráfico de linha do fitness médio por geração**.
11. Gravar em **CSV/TXT** o log com: geração, fitness médio, melhor fitness, melhor x, melhor y.
12. **Não** usar "atingir o valor ótimo" como critério de parada. Usar **número de gerações** ou **convergência prematura da população**.

## 4. Glossário rápido

- **Indivíduo:** um candidato `(x, y)`. Na codificação real, são dois números reais.
- **Fitness:** a qualidade do indivíduo. Aqui é o próprio `Z`, e maior é melhor.
- **Seleção por ranking:** ordena a população pelo fitness e sorteia pais com probabilidade que depende da posição (rank), não do valor. Evita que um indivíduo muito bom domine tudo.
- **Cruzamento BLX-α:** o filho é sorteado uniformemente num intervalo que estende o intervalo entre os dois pais em α dos dois lados. Para cada gene, com `d = |p1 − p2|`, sorteia-se em `[min(p1,p2) − α·d, max(p1,p2) + α·d]`. O valor típico é α = 0,5.
- **Mutação uniforme:** com probabilidade igual à taxa de mutação, um gene é substituído por um valor sorteado uniformemente em todo o intervalo permitido da variável.
- **Elitismo de 0,5%:** os melhores `0,5% × tamanho da população` indivíduos passam direto para a próxima geração, sem cruzar nem mudar.
- **Gene, alelo, genótipo, fenótipo:** pela tabela do slide 22: gene é cada característica do indivíduo (aqui, x ou y), alelo é o valor atribuído a um gene, cromossomo é o conjunto de características que representa o indivíduo, genótipo é a estrutura que armazena as informações do indivíduo, fenótipo é o **grau de aptidão** dele em resolver o problema e fitness é o valor do fenótipo. Com codificação **real** não há etapa de decodificação como na binária. Explicação completa em `04_conteudo_dos_slides_explicado.md`.
- **Convergência prematura:** a população fica quase toda igual (pouca diversidade) cedo demais. Pode servir de critério de parada.

## 5. O que deve ser entregue

- Código-fonte do AG em uma das linguagens permitidas.
- Interface onde se informam taxa de cruzamento, taxa de mutação, tamanho da população e nº de gerações.
- Gráficos por geração (população no espaço de busca, com o melhor destacado).
- Gráfico de linha do fitness médio por geração.
- Arquivo CSV/TXT com o log por geração.
- **Apresentação do código** ao professor (vão perguntar como cada parte funciona).

## 6. Pontos de atenção

- **O prazo é 05/10/2026.**
- A apresentação do código é parte da avaliação: os dois precisam saber explicar cada função.
- O PDF não define valores de α, taxas, população ou gerações. A escolha é de vocês, e é bom justificá-la.
- Pergunte ao professor, se não estiver claro, o que conta como "interface" (janela gráfica ou terminal) e como arredondar 0,5% de uma população pequena (no código adotamos no mínimo 1 indivíduo; ver `03_explicacao_do_codigo.md`).
