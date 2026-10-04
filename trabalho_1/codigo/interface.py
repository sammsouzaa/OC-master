# interface.py
# janela do tkinter. Os parâmetros do AG são digitados aqui (exigência do enunciado)
# a interface só lê os campos, monta o Parametros e chama o ag.executar_ag
#
# ao clicar em Executar:
# 1. lê e valida os parâmetros
# 2. roda o AG, e a cada geração salva o gráfico em saida/geracao_XXX.png e mostra na aba População
# 3. salva o log.csv
# 4. salva o gráfico de linha em saida/fitness_medio.png e mostra na aba Fitness médio

import glob
import os
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib

# os gráficos só viram PNG, quem mostra é o tkinter
matplotlib.use("Agg")

import ag  # noqa: E402
import graficos  # noqa: E402
import log  # noqa: E402

PASTA = os.path.dirname(os.path.abspath(__file__))
PASTA_SAIDA = os.path.join(PASTA, "saida")
CAMINHO_LOG = os.path.join(PASTA, "log.csv")
CAMINHO_FITNESS = os.path.join(PASTA_SAIDA, "fitness_medio.png")

# (chave, texto do campo, valor padrão)
CAMPOS = [
    ("tamanho_populacao", "Tamanho da população", "100"),
    ("num_geracoes", "Número de gerações", "100"),
    ("taxa_cruzamento", "Taxa de cruzamento (0 a 1)", "0.8"),
    ("taxa_mutacao", "Taxa de mutação (0 a 1)", "0.05"),
    ("alpha", "Alpha do BLX", "0.5"),
]


class Aplicacao:
    def __init__(self, raiz):
        self.raiz = raiz
        raiz.title("AG - Equipe 9 (Função 8)")
        raiz.resizable(False, False)

        self.entradas = {}
        # guarda as imagens, senão o tkinter apaga e a tela fica em branco
        self.imagens = {}
        # vira True se fecharem a janela no meio da execução
        self.fechada = False
        raiz.protocol("WM_DELETE_WINDOW", self._fechar)

        self._montar_widgets()

    def _fechar(self):
        # clicou no X da janela
        self.fechada = True
        self.raiz.destroy()

    # ---------- tela ----------

    def _montar_widgets(self):
        quadro = ttk.Frame(self.raiz, padding=12)
        quadro.grid()

        # campos dos parâmetros
        for linha, (chave, texto, padrao) in enumerate(CAMPOS):
            ttk.Label(quadro, text=texto).grid(row=linha, column=0, sticky="w", pady=2)
            entrada = ttk.Entry(quadro, width=10, justify="right")
            entrada.insert(0, padrao)
            entrada.grid(row=linha, column=1, padx=(12, 0), pady=2)
            self.entradas[chave] = entrada

        # se marcada, o AG também para quando a população converge
        self.parar_conv = tk.BooleanVar(value=True)
        ttk.Checkbutton(quadro, text="Parar por convergência",
                        variable=self.parar_conv).grid(
            row=len(CAMPOS), column=0, columnspan=2, sticky="w", pady=(6, 0))

        self.botao = ttk.Button(quadro, text="Executar", command=self.executar)
        self.botao.grid(row=len(CAMPOS) + 1, column=0, columnspan=2, pady=(10, 4), sticky="ew")

        self.status = tk.StringVar(value="Pronto.")
        ttk.Label(quadro, textvariable=self.status).grid(
            row=len(CAMPOS) + 2, column=0, columnspan=2, sticky="w")

        self.resultado = tk.StringVar(value="")
        ttk.Label(quadro, textvariable=self.resultado, justify="left").grid(
            row=len(CAMPOS) + 3, column=0, columnspan=2, sticky="w", pady=(6, 0))

        # abas dos gráficos
        abas = ttk.Notebook(quadro)
        abas.grid(row=0, column=2, rowspan=len(CAMPOS) + 4, padx=(16, 0))
        self.rotulos_img = {}
        for nome in ("População", "Fitness médio"):
            aba = ttk.Frame(abas)
            rotulo = ttk.Label(aba, text="(sem gráfico ainda)", width=60, anchor="center")
            rotulo.pack(ipady=80)
            abas.add(aba, text=nome)
            self.rotulos_img[nome] = rotulo

    # ---------- leitura dos campos ----------

    def _ler_parametros(self):
        # devolve o Parametros, ou None se tiver algum valor inválido
        try:
            def ler(chave):
                # troca vírgula por ponto, pra aceitar "0,8"
                return self.entradas[chave].get().strip().replace(",", ".")

            params = ag.Parametros(
                tamanho_populacao=int(ler("tamanho_populacao")),
                num_geracoes=int(ler("num_geracoes")),
                taxa_cruzamento=float(ler("taxa_cruzamento")),
                taxa_mutacao=float(ler("taxa_mutacao")),
                alpha=float(ler("alpha")),
                parar_por_convergencia=self.parar_conv.get(),
            )
        except ValueError:
            messagebox.showerror("Valor inválido", "Preencha todos os campos com números.")
            return None

        erro = None
        if params.tamanho_populacao < 2:
            erro = "A população precisa ter pelo menos 2 indivíduos."
        elif params.num_geracoes < 1:
            erro = "O número de gerações precisa ser pelo menos 1."
        elif not 0 <= params.taxa_cruzamento <= 1:
            erro = "A taxa de cruzamento deve estar entre 0 e 1."
        elif not 0 <= params.taxa_mutacao <= 1:
            erro = "A taxa de mutação deve estar entre 0 e 1."
        elif params.alpha < 0:
            erro = "O alpha do BLX não pode ser negativo."

        if erro:
            messagebox.showerror("Valor inválido", erro)
            return None
        return params

    # ---------- imagens ----------

    def _mostrar_imagem(self, aba, caminho):
        # o tkinter lê PNG direto
        imagem = tk.PhotoImage(file=caminho)
        self.imagens[aba] = imagem
        self.rotulos_img[aba].configure(image=imagem, text="")

    # ---------- execução ----------

    def executar(self):
        params = self._ler_parametros()
        if params is None:
            return

        # apaga os PNGs da execução anterior
        os.makedirs(PASTA_SAIDA, exist_ok=True)
        for antigo in glob.glob(os.path.join(PASTA_SAIDA, "geracao_*.png")):
            os.remove(antigo)

        def ao_fim_de_geracao(geracao, populacao, fitnesses, melhor, melhor_fitness):
            # se fecharam a janela, interrompe o AG
            if self.fechada:
                raise InterruptedError

            caminho = os.path.join(PASTA_SAIDA, f"geracao_{geracao:03d}.png")
            graficos.grafico_populacao(geracao, populacao, melhor, caminho)
            self._mostrar_imagem("População", caminho)
            self.status.set(f"Geração {geracao}/{params.num_geracoes}  |  "
                            f"melhor fitness: {melhor_fitness:.4f}")

            # atualiza a tela, senão a janela trava até o fim
            self.raiz.update()

        self.botao.configure(state="disabled")
        self.resultado.set("")
        self.status.set("Executando...")
        self.raiz.update()

        try:
            historico = ag.executar_ag(params, ao_fim_de_geracao)
            log.salvar_log(historico, CAMINHO_LOG)
            graficos.grafico_fitness_medio(
                historico["geracoes"], historico["fitness_medio"],
                historico["melhor_fitness"], CAMINHO_FITNESS)
            self._mostrar_imagem("Fitness médio", CAMINHO_FITNESS)
            self._mostrar_resumo(historico)
        except InterruptedError:
            # fecharam a janela durante a execução
            return
        finally:
            # libera o botão de novo, a não ser que a janela tenha sido fechada
            if not self.fechada:
                self.botao.configure(state="normal")

    def _mostrar_resumo(self, historico):
        x, y = historico["melhor_final"]
        self.status.set(f"Concluído em {len(historico['geracoes'])} gerações.")
        self.resultado.set(f"Melhor x: {x:.3f}\n"
                           f"Melhor y: {y:.3f}\n"
                           f"Fitness: {historico['melhor_fitness'][-1]:.4f}\n"
                           f"Log: {os.path.basename(CAMINHO_LOG)}")


def iniciar():
    raiz = tk.Tk()
    Aplicacao(raiz)
    raiz.mainloop()
