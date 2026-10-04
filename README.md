# OC-master

Material da disciplina de **Otimização Combinatória** (OC): trabalhos práticos e resumos de estudo para a prova.

## Estrutura do repositório

```
OC-master/
├── trabalho_1/       Trabalho 1: Algoritmo Genético (Equipe 9)
│   ├── codigo/           código-fonte em Python, com README próprio
│   ├── 01_explicacao_da_atividade.md
│   ├── 02_roteiro_de_estudo_slides.md
│   ├── 03_explicacao_do_codigo.md
│   ├── 04_conteudo_dos_slides_explicado.md
│   └── PDFs do enunciado e das funções
└── estudo_prova1/    Material de estudo da 1ª prova
    ├── Resumo_1_Algoritmos_Geneticos.md
    ├── Resumo_2_Busca_Tabu.md
    ├── Resumo_3_Colonia_de_Formigas.md
    ├── Respostas_Lista_1_OC.md
    └── slides e lista de exercícios (PDF, PPTX, DOCX)
```

## Trabalho 1: Algoritmo Genético

Implementação de um Algoritmo Genético, sem bibliotecas de AG, para maximizar uma função de duas variáveis.

**Equipe 9:** Samuel Moreira de Souza e Giovanni Nadalin Sansana.

| Item | Escolha |
|---|---|
| Codificação | Real, com 3 casas decimais |
| Seleção | Ranking |
| Cruzamento | BLX-alpha |
| Mutação | Uniforme |
| Elitismo | 0,5% da população (no mínimo 1 indivíduo) |
| Função | Função 8: `Z = 5 + 3x - 4y - x² + xy - y²`, com x e y em [-10, 10] (maximização) |

O programa tem uma interface em tkinter onde se informam população, gerações, taxa de cruzamento, taxa de mutação e o alpha do BLX. A cada execução ele gera:

- o gráfico da população em cada geração, com o melhor indivíduo destacado;
- o gráfico de linha do fitness médio;
- o `log.csv` com geração, fitness médio, melhor fitness, melhor x e melhor y.

### Como executar

Precisa de Python 3 com `tkinter`, `matplotlib` e `numpy`.

```bash
cd trabalho_1/codigo

# no Linux o tkinter vem de um pacote à parte
sudo apt install python3-tk
pip install -r requirements.txt

python3 main.py
```

Mais detalhes (parâmetros, arquivos gerados, fluxo do código) em [`trabalho_1/codigo/README.md`](trabalho_1/codigo/README.md).

### Documentação do trabalho

| Arquivo | Conteúdo |
|---|---|
| [`01_explicacao_da_atividade.md`](trabalho_1/01_explicacao_da_atividade.md) | o que o enunciado pede, regras e especificação da equipe |
| [`02_roteiro_de_estudo_slides.md`](trabalho_1/02_roteiro_de_estudo_slides.md) | quais slides ler para implementar cada parte |
| [`03_explicacao_do_codigo.md`](trabalho_1/03_explicacao_do_codigo.md) | explicação de cada arquivo e função do código |
| [`04_conteudo_dos_slides_explicado.md`](trabalho_1/04_conteudo_dos_slides_explicado.md) | o conteúdo dos slides de AG explicado, com o fluxo completo do algoritmo |

## Estudo para a prova 1

Resumos dos três tópicos da disciplina e respostas da lista de exercícios:

| Arquivo | Tópico |
|---|---|
| [`Resumo_1_Algoritmos_Geneticos.md`](estudo_prova1/Resumo_1_Algoritmos_Geneticos.md) | Algoritmos Genéticos |
| [`Resumo_2_Busca_Tabu.md`](estudo_prova1/Resumo_2_Busca_Tabu.md) | Busca Tabu |
| [`Resumo_3_Colonia_de_Formigas.md`](estudo_prova1/Resumo_3_Colonia_de_Formigas.md) | Colônia de Formigas (ACO) |
| [`Respostas_Lista_1_OC.md`](estudo_prova1/Respostas_Lista_1_OC.md) | respostas da Lista 1 |
