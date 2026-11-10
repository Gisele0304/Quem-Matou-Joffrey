
import customtkinter as ctk
import json
import webbrowser
import networkx as nx

from mapa import criar_mapa
from ordenacao import (
    bubble_sort,
    insertion_sort,
    selection_sort,
    quick_sort,
    comparar_algoritmos
)

from estruturas import (
    ListaSequencial,
    ListaEncadeada,
    Pilha,
    Fila,
    Deque
)

from tkinter import messagebox
from pathlib import Path
from dados import suspeitos, vitima, evidencias
from tabela_hash import TabelaHash
from grafos import criar_grafo, desenhar_grafo
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


arquivo_evidencias = Path(__file__).with_name("evidencias.json")


def carregar_evidencias():

    if arquivo_evidencias.exists():

        try:
            with open(arquivo_evidencias, "r", encoding="utf-8") as arquivo:
                dados_salvos = json.load(arquivo)

            if isinstance(dados_salvos, list) and dados_salvos:
                evidencias.clear()
                evidencias.extend(dados_salvos)

        except (json.JSONDecodeError, OSError):
            print("Não foi possível carregar as evidências.")


def salvar_evidencias():

    try:
        with open(arquivo_evidencias, "w", encoding="utf-8") as arquivo:
            json.dump(
                evidencias,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

        return True

    except OSError:
        messagebox.showerror(
            "Erro",
            "Não foi possível salvar as evidências."
        )
        return False


class Envenamento(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Investigação de Envenenamento")
        self.geometry("1100x850")
        self.minsize(780, 650)

        carregar_evidencias()

        self.tabela_hash = TabelaHash()

        for evidencia in evidencias:
            self.tabela_hash.inserir(evidencia)

        self.lista_estruturas = ListaSequencial()
        self.lista_encadeada = ListaEncadeada()
        self.pilha_acoes = Pilha()
        self.fila_analise = Fila()
        self.deque_investigacao = Deque()

        for evidencia in evidencias:
            self.lista_estruturas.inserir(evidencia["codigo"])
            self.lista_encadeada.inserir(evidencia["codigo"])

        self.area_conteudo = ctk.CTkFrame(self)
        self.area_conteudo.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.mostrar_inicio()

    def limpar_tela(self):

        for item in self.area_conteudo.winfo_children():
            item.destroy()

    def criar_titulo(self, titulo, subtitulo):

        ctk.CTkLabel(
            self.area_conteudo,
            text=titulo,
            font=("Arial", 28, "bold")
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self.area_conteudo,
            text=subtitulo,
            font=("Arial", 15)
        ).pack(pady=(0, 20))

    def mostrar_inicio(self):

        self.limpar_tela()

        self.criar_titulo(
            "Investigação de Envenenamento",
            "Quem matou o Rei Joffrey Baratheon?"
        )

        frame_cards = ctk.CTkFrame(self.area_conteudo)
        frame_cards.pack(fill="x", padx=20, pady=10)

        self.criar_card(
            frame_cards,
            "Suspeitos",
            len(suspeitos)
        )

        self.criar_card(
            frame_cards,
            "Vítima",
            vitima["nome"]
        )

        self.criar_card(
            frame_cards,
            "Evidências",
            len(evidencias)
        )

        
        botoes = ctk.CTkFrame(
            self.area_conteudo,
            fg_color="transparent"
        )

        botoes.pack(fill="x", padx=20, pady=10)

        botoes.grid_columnconfigure(0, weight=1)
        botoes.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            botoes,
            text="Ler depoimentos",
            height=45,
            font=("Arial", 15, "bold"),
            command=self.mostrar_depoimentos
        ).grid(row=0, column=0, padx=8, pady=6, sticky="ew")

        ctk.CTkButton(
            botoes,
            text="Cadastrar evidência",
            height=45,
            font=("Arial", 15, "bold"),
            command=self.mostrar_cadastro
        ).grid(row=0, column=1, padx=8, pady=6, sticky="ew")

        ctk.CTkButton(
            botoes,
            text="Visualizar conexões",
            height=45,
            font=("Arial", 15, "bold"),
            command=self.mostrar_grafo
        ).grid(row=1, column=0, padx=8, pady=6, sticky="ew")

        ctk.CTkButton(
            botoes,
            text="Mapa da investigação",
            height=45,
            font=("Arial", 15, "bold"),
            command=self.mostrar_mapa
        ).grid(row=1, column=1, padx=8, pady=6, sticky="ew")

        ctk.CTkButton(
            botoes,
            text="Análise de ordenação",
            height=45,
            font=("Arial", 15, "bold"),
            command=self.mostrar_ordenacao
        ).grid(row=2, column=0, columnspan=2, padx=8, pady=6, sticky="ew")

        ctk.CTkButton(
            botoes,
            text="Estruturas de dados",
            height=45,
            font=("Arial", 15, "bold"),
            command=self.mostrar_estruturas
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            padx=8,
            pady=6,
            sticky="ew"
        )

        ctk.CTkLabel(
            self.area_conteudo,
            text="Pesquisar evidência pelo código",
            font=("Arial", 18, "bold")
        ).pack(pady=(10, 5))

        self.campo_busca = ctk.CTkEntry(
            self.area_conteudo,
            placeholder_text="Exemplo: E1",
            width=300
        )
        self.campo_busca.pack(pady=5)

        ctk.CTkButton(
            self.area_conteudo,
            text="Buscar evidência",
            width=200,
            command=self.buscar_evidencia
        ).pack(pady=5)

        self.resultado_busca = ctk.CTkLabel(
            self.area_conteudo,
            text="",
            font=("Arial", 13),
            wraplength=750,
            justify="left"
        )
        self.resultado_busca.pack(pady=5)

        ctk.CTkLabel(
            self.area_conteudo,
            text="Evidências registradas",
            font=("Arial", 20, "bold")
        ).pack(pady=(10, 5))

        self.lista_principal = ctk.CTkScrollableFrame(
            self.area_conteudo,
            height=180
        )
        self.lista_principal.pack(
            padx=20,
            pady=10,
            fill="x",
            expand=False
        )

        self.atualizar_lista_principal()

    def criar_card(self, frame, titulo, valor):

        card = ctk.CTkFrame(
            frame,
            height=110
        )
        card.pack(
            side="left",
            padx=10,
            pady=10,
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            card,
            text=titulo,
            font=("Arial", 16)
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            card,
            text=str(valor),
            font=("Arial", 20, "bold"),
            wraplength=180
        ).pack(pady=5)

    def atualizar_lista_principal(self):

        for item in self.lista_principal.winfo_children():
            item.destroy()

        for evidencia in evidencias:

            ctk.CTkLabel(
                self.lista_principal,
                text=f"{evidencia['codigo']} - {evidencia['nome']}",
                font=("Arial", 14)
            ).pack(anchor="w", padx=10, pady=5)

    def buscar_evidencia(self):

        codigo = self.campo_busca.get().strip().upper()

        if not codigo:
            self.resultado_busca.configure(
                text="Digite o código da evidência."
            )
            return

        evidencia = self.tabela_hash.buscar(codigo)

        if evidencia is None:

            self.resultado_busca.configure(
                text="Nenhuma evidência encontrada."
            )

        else:

            self.resultado_busca.configure(
                text=(
                    f"Código: {evidencia['codigo']}\n"
                    f"Nome: {evidencia['nome']}\n"
                    f"Tipo: {evidencia['tipo']}\n"
                    f"Descrição: {evidencia['descricao']}\n"
                    f"Local: {evidencia['local']}\n"
                    f"Importância: {evidencia['importancia']}"
                )
            )

    def mostrar_depoimentos(self):

        self.limpar_tela()

        self.criar_titulo(
            "Depoimentos dos Personagens",
            "Leia atentamente os relatos e investigue os acontecimentos."
        )

        lista = ctk.CTkScrollableFrame(
            self.area_conteudo,
            width=850,
            height=480
        )
        lista.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        depoimentos = [
            {
                "personagem": "Sansa Stark",
                "relato": (
                    "Antes do casamento, recebi de Dontos um "
                    "presente que deveria me acompanhar durante "
                    "a cerimônia. Em determinado momento da "
                    "celebração, a senhora Olenna se aproximou "
                    "e ajeitou algo em meu cabelo. Eu estava "
                    "nervosa demais para prestar atenção aos "
                    "detalhes. Depois de tudo o que aconteceu, "
                    "percebi que algumas coisas daquela noite "
                    "não pareciam estar como antes."
                )
            },
            {
                "personagem": "Margaery Tyrell",
                "relato": (
                    "O casamento deveria ser um dos dias mais "
                    "importantes da minha vida. Durante o banquete, "
                    "Joffrey estava bastante animado e fez questão "
                    "de chamar a atenção de todos. Ele bebeu em "
                    "sua taça e, pouco depois, começou a tossir "
                    "violentamente. Em questão de instantes, "
                    "a comemoração se transformou em desespero. "
                    "Ninguém parecia entender o que estava acontecendo."
                )
            },
            {
                "personagem": "Dontos Hollard",
                "relato": (
                    "Eu tinha uma dívida de gratidão com Sansa "
                    "e prometi ajudá-la. Conversamos sobre uma "
                    "maneira de sair da Fortaleza Vermelha sem "
                    "chamar a atenção. O plano precisava acontecer "
                    "depois da cerimônia, quando todos estivessem "
                    "ocupados com a comemoração. Algumas pessoas "
                    "não imaginam o quanto uma fuga exige "
                    "planejamento e discrição."
                )
            }
        ]

        for depoimento in depoimentos:

            card = ctk.CTkFrame(lista)
            card.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(
                card,
                text=depoimento["personagem"],
                font=("Arial", 18, "bold")
            ).pack(anchor="w", padx=15, pady=10)

            ctk.CTkLabel(
                card,
                text=depoimento["relato"],
                font=("Arial", 14),
                wraplength=760,
                justify="left"
            ).pack(anchor="w", padx=15, pady=(5, 15))

        ctk.CTkButton(
            self.area_conteudo,
            text="Voltar à página inicial",
            width=220,
            height=40,
            command=self.mostrar_inicio
        ).pack(pady=15)

    
    
    def mostrar_grafo(self):
        self.limpar_tela()

        self.criar_titulo(
            "Quadro de Investigação",
            "Organize os suspeitos e evidências e investigue as conexões"
        )

        grafo = criar_grafo()
        posicoes = nx.spring_layout(
            grafo,
            seed=42,
            k=2.5,
            iterations=200
        )

        selecionados = []
        estado = {
            "modo": "mover",
            "arrastando": None
        }

        instrucoes = ctk.CTkLabel(
            self.area_conteudo,
            text="Modo: Mover vértices | Clique e arraste os elementos.",
            font=("Arial", 13)
        )
        instrucoes.pack(pady=5)

        controles = ctk.CTkFrame(
            self.area_conteudo,
            fg_color="transparent"
        )
        controles.pack(fill="x", padx=10, pady=5)

        figura = Figure(
            figsize=(10, 5),
            dpi=100,
            facecolor="#F4F6F8"
        )

        ax = figura.add_subplot(111)

        desenhar_grafo(grafo, ax, posicoes, selecionados)

        canvas = FigureCanvasTkAgg(
            figura,
            master=self.area_conteudo
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        ctk.CTkButton(
            self.area_conteudo,
            text="Voltar à página inicial",
            width=220,
            height=40,
            command=self.mostrar_inicio
        ).pack(pady=10)

        def redesenhar():
            desenhar_grafo(
                grafo,
                ax,
                posicoes,
                selecionados
            )
            canvas.draw_idle()

        def definir_modo(modo):
            estado["modo"] = modo
            estado["arrastando"] = None
            selecionados.clear()

            if modo == "mover":
                instrucoes.configure(
                    text="Modo: Mover vértices | Clique e arraste os elementos."
                )

            elif modo == "criar":
                instrucoes.configure(
                    text="Modo: Criar ligação | Selecione dois vértices."
                )

            elif modo == "remover":
                instrucoes.configure(
                    text="Modo: Remover ligação | Selecione dois vértices conectados."
                )

            redesenhar()

        def localizar_vertice(event):
            if event.inaxes != ax:
                return None

            menor_distancia = 45
            vertice_encontrado = None

            for vertice, posicao in posicoes.items():
                x, y = ax.transData.transform(posicao)

                distancia = (
                    (event.x - x) ** 2 +
                    (event.y - y) ** 2
                ) ** 0.5

                if distancia < menor_distancia:
                    menor_distancia = distancia
                    vertice_encontrado = vertice

            return vertice_encontrado

        def ao_clicar(event):
            if event.button != 1:
                return

            vertice = localizar_vertice(event)

            if vertice is None:
                return

            if estado["modo"] == "mover":
                estado["arrastando"] = vertice

            else:
                if vertice in selecionados:
                    return

                selecionados.append(vertice)

                if len(selecionados) == 2:
                    primeiro = selecionados[0]
                    segundo = selecionados[1]

                    if estado["modo"] == "criar":
                        if grafo.has_edge(primeiro, segundo):
                            messagebox.showinfo(
                                "Ligação existente",
                                "Esses vértices já estão conectados."
                            )
                        else:
                            grafo.add_edge(primeiro, segundo)
                            messagebox.showinfo(
                                "Investigação",
                                "Ligação criada com sucesso!"
                            )

                    elif estado["modo"] == "remover":
                        if grafo.has_edge(primeiro, segundo):
                            grafo.remove_edge(primeiro, segundo)
                            messagebox.showinfo(
                                "Investigação",
                                "Ligação removida com sucesso!"
                            )
                        else:
                            messagebox.showinfo(
                                "Investigação",
                                "Não existe ligação entre esses vértices."
                            )

                    selecionados.clear()

            redesenhar()

        def ao_mover(event):
            vertice = estado["arrastando"]

            if vertice is None:
                return

            if event.inaxes != ax:
                return

            if event.xdata is None or event.ydata is None:
                return

            posicoes[vertice] = (event.xdata, event.ydata)
            redesenhar()

        def ao_soltar(event):
            estado["arrastando"] = None

        canvas.mpl_connect(
            "button_press_event",
            ao_clicar
        )

        canvas.mpl_connect(
            "motion_notify_event",
            ao_mover
        )

        canvas.mpl_connect(
            "button_release_event",
            ao_soltar
        )

        ctk.CTkButton(
            controles,
            text="Mover vértices",
            command=lambda: definir_modo("mover")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controles,
            text="Criar ligação",
            command=lambda: definir_modo("criar")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controles,
            text="Remover ligação",
            command=lambda: definir_modo("remover")
        ).pack(side="left", padx=5)

        def restaurar_grafo():
            grafo_original = criar_grafo()

            grafo.clear()
            grafo.add_nodes_from(grafo_original.nodes(data=True))
            grafo.add_edges_from(grafo_original.edges(data=True))

            posicoes.clear()
            posicoes.update(
                nx.spring_layout(
                    grafo,
                    seed=42,
                    k=2.5,
                    iterations=200
                )
            )

            selecionados.clear()
            estado["modo"] = "mover"
            estado["arrastando"] = None

            instrucoes.configure(
                text="Modo: Mover vértices | Clique e arraste os elementos."
            )

            redesenhar()

        ctk.CTkButton(
            controles,
            text="Restaurar grafo",
            command=restaurar_grafo
        ).pack(side="left", padx=5)

    
    def mostrar_ordenacao(self):
        self.limpar_tela()

        self.criar_titulo(
            "Análise de Desempenho",
            "Compare os algoritmos de ordenação das evidências."
        )

        ctk.CTkButton(
             self.area_conteudo,
            text="Voltar à página inicial",
            width=220,
            height=40,
            command=self.mostrar_inicio
        ).pack(pady=10)

        algoritmos = {
            "Bubble Sort": bubble_sort,
            "Insertion Sort": insertion_sort,
            "Selection Sort": selection_sort,
            "QuickSort": quick_sort
        }

        resultados_tempo = comparar_algoritmos(evidencias)

        ctk.CTkLabel(
            self.area_conteudo,
            text="Escolha um algoritmo:",
            font=("Arial", 15, "bold")
        ).pack(pady=5)

        lista_resultados = ctk.CTkScrollableFrame(
            self.area_conteudo,
            height=180
        )
        lista_resultados.pack(
            fill="x",
            padx=20,
            pady=10
        )

        def mostrar_resultado(nome):
            for item in lista_resultados.winfo_children():
                item.destroy()

            resultado = algoritmos[nome](evidencias)

            for evidencia in resultado:
                ctk.CTkLabel(
                    lista_resultados,
                    text=(
                        f"{evidencia['codigo']} - "
                        f"{evidencia['nome']} | "
                        f"Importância: {evidencia['importancia']}"
                    ),
                    font=("Arial", 13)
                ).pack(anchor="w", padx=10, pady=5)

        escolha = ctk.CTkOptionMenu(
            self.area_conteudo,
            values=list(algoritmos.keys()),
            width=250,
            command=mostrar_resultado
        )
        escolha.pack(pady=5)

        mostrar_resultado("Bubble Sort")

        figura = Figure(
            figsize=(9, 4),
            dpi=100,
            facecolor="#F4F6F8"
        )

        ax = figura.add_subplot(111)

        nomes = list(resultados_tempo.keys())
        tempos = list(resultados_tempo.values())

        ax.bar(
            nomes,
            tempos,
            color=["#C0392B", "#2980B9", "#239B56", "#8E44AD"]
        )

        ax.set_title(
            "Comparação dos tempos de execução",
            fontsize=14,
            fontweight="bold"
        )

        ax.set_ylabel("Tempo médio (ms)")
        ax.set_xlabel("Algoritmos")
        ax.tick_params(axis="x", rotation=10)

        figura.tight_layout()

        canvas = FigureCanvasTkAgg(
            figura,
            master=self.area_conteudo
        )
        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=20,
            pady=5
        )

    
    
    def mostrar_estruturas(self):
        self.limpar_tela()

        self.criar_titulo(
            "Estruturas de Dados",
            "Escolha uma estrutura para realizar operações."
        )

        codigos = [e["codigo"] for e in evidencias]

        lista = ListaSequencial()
        encadeada = ListaEncadeada()
        pilha = Pilha()
        fila = Fila()
        deque = Deque()

        for codigo in codigos:
            lista.inserir(codigo)
            encadeada.inserir(codigo)
            pilha.empilhar(codigo)
            fila.enfileirar(codigo)
            deque.inserir_fim(codigo)

        estruturas = {
            "Lista sequencial": lista,
            "Lista encadeada": encadeada,
            "Pilha": pilha,
            "Fila": fila,
            "Deque": deque
        }

        area_opcoes = ctk.CTkFrame(
            self.area_conteudo,
            fg_color="transparent"
        )
        area_opcoes.pack(fill="x", padx=20, pady=20)

        area_opcoes.grid_columnconfigure(0, weight=1)
        area_opcoes.grid_columnconfigure(1, weight=1)

        def abrir_estrutura(nome):
            self.limpar_tela()

            estrutura = estruturas[nome]

            self.criar_titulo(
                nome,
                "Escolha uma operação para executar."
            )

            resultado = ctk.CTkLabel(
                self.area_conteudo,
                text="Elementos: " + str(estrutura.listar()),
                font=("Arial", 14),
                wraplength=750
            )
            resultado.pack(pady=20)

            entrada = ctk.CTkEntry(
                self.area_conteudo,
                placeholder_text="Digite o código da evidência (ex.: E8)",
                width=280
            )
            entrada.pack(pady=10)

            def atualizar():
                resultado.configure(
                    text="Elementos: " + str(estrutura.listar())
                )

            def adicionar_inicio():
                codigo = entrada.get().strip().upper()

                if not codigo:
                    messagebox.showwarning(
                        "Atenção",
                        "Digite um código."
                    )
                    return

                if nome == "Deque":
                    estrutura.inserir_inicio(codigo)
                else:
                    messagebox.showinfo(
                        "Operação inválida",
                        "Essa estrutura não permite inserir no início."
                    )
                    return

                entrada.delete(0, "end")
                atualizar()

            def adicionar_fim():
                codigo = entrada.get().strip().upper()

                if not codigo:
                    messagebox.showwarning(
                        "Atenção",
                        "Digite um código."
                    )
                    return

                if nome in ["Lista sequencial", "Lista encadeada"]:
                    estrutura.inserir(codigo)
                elif nome == "Pilha":
                    estrutura.empilhar(codigo)
                elif nome == "Fila":
                    estrutura.enfileirar(codigo)
                elif nome == "Deque":
                    estrutura.inserir_fim(codigo)

                entrada.delete(0, "end")
                atualizar()

            def remover_inicio():
                if nome == "Lista sequencial":
                    elementos = estrutura.listar()
                    if elementos:
                        estrutura.remover(elementos[0])
                        atualizar()
                    else:
                        messagebox.showinfo("Aviso", "A lista está vazia.")

                elif nome == "Lista encadeada":
                    elementos = estrutura.listar()
                    if elementos:
                        estrutura.remover(elementos[0])
                        atualizar()
                    else:
                        messagebox.showinfo("Aviso", "A lista está vazia.")

                elif nome == "Fila":
                    removido = estrutura.desenfileirar()
                    messagebox.showinfo(
                        "Fila",
                        f"Elemento retirado: {removido}"
                    )
                    atualizar()

                elif nome == "Deque":
                    removido = estrutura.remover_inicio()
                    messagebox.showinfo(
                        "Deque",
                        f"Elemento retirado: {removido}"
                    )
                    atualizar()

                else:
                    messagebox.showinfo(
                        "Operação inválida",
                        "Essa estrutura não permite retirar pelo início."
                    )

            def remover_fim():
                if nome == "Pilha":
                    removido = estrutura.desempilhar()
                elif nome == "Deque":
                    removido = estrutura.remover_fim()
                else:
                    messagebox.showinfo(
                        "Operação inválida",
                        "Essa operação não está disponível nesta estrutura."
                    )
                    return

                messagebox.showinfo(
                    "Resultado",
                    f"Elemento retirado: {removido}"
                )
                atualizar()

            def remover_elemento():
                codigo = entrada.get().strip().upper()

                if not codigo:
                    messagebox.showwarning(
                        "Atenção",
                        "Digite o código que deseja remover."
                    )
                    return

                if nome in ["Lista sequencial", "Lista encadeada"]:
                    sucesso = estrutura.remover(codigo)

                    if sucesso:
                        messagebox.showinfo(
                            "Resultado",
                            "Elemento removido."
                        )
                    else:
                        messagebox.showinfo(
                            "Resultado",
                            "Elemento não encontrado."
                        )

                    entrada.delete(0, "end")
                    atualizar()
                else:
                    messagebox.showinfo(
                        "Operação inválida",
                        "Use as operações próprias dessa estrutura."
                    )

            def consultar():
                if nome == "Pilha":
                    valor = estrutura.topo()
                elif nome == "Fila":
                    valor = estrutura.frente()
                else:
                    codigo = entrada.get().strip().upper()

                    if nome == "Lista sequencial":
                        valor = estrutura.buscar(codigo)
                    elif nome == "Lista encadeada":
                        valor = estrutura.buscar(codigo)
                    else:
                        elementos = estrutura.listar()
                        valor = codigo if codigo in elementos else None

                messagebox.showinfo(
                    "Consulta",
                    f"Resultado: {valor}"
                )

            botoes = ctk.CTkFrame(
                self.area_conteudo,
                fg_color="transparent"
            )
            botoes.pack(fill="x", padx=20, pady=10)

            botoes.grid_columnconfigure(0, weight=1)
            botoes.grid_columnconfigure(1, weight=1)

            operacoes = []

            if nome in ["Lista sequencial", "Lista encadeada"]:
                operacoes = [
                    ("Inserir elemento", adicionar_fim),
                    ("Remover elemento", remover_elemento),
                    ("Buscar elemento", consultar)
                ]

            elif nome == "Pilha":
                operacoes = [
                    ("Empilhar", adicionar_fim),
                    ("Desempilhar", remover_fim),
                    ("Consultar topo", consultar)
                ]

            elif nome == "Fila":
                operacoes = [
                    ("Enfileirar", adicionar_fim),
                    ("Desenfileirar", remover_inicio),
                    ("Consultar frente", consultar)
                ]

            elif nome == "Deque":
                operacoes = [
                    ("Inserir no início", adicionar_inicio),
                    ("Inserir no fim", adicionar_fim),
                    ("Retirar do início", remover_inicio),
                    ("Retirar do fim", remover_fim)
                ]

            for i, (texto, comando) in enumerate(operacoes):
                ctk.CTkButton(
                    botoes,
                    text=texto,
                    height=40,
                    command=comando
                ).grid(
                    row=i // 2,
                    column=i % 2,
                    padx=6,
                    pady=6,
                    sticky="ew"
                )

            ctk.CTkButton(
                self.area_conteudo,
                text="Voltar às estruturas",
                command=self.mostrar_estruturas
            ).pack(pady=10)

            ctk.CTkButton(
                self.area_conteudo,
                text="Voltar à página inicial",
                command=self.mostrar_inicio
            ).pack(pady=5)

        opcoes = [
            "Lista sequencial",
            "Lista encadeada",
            "Pilha",
            "Fila",
            "Deque"
        ]

        for i, nome in enumerate(opcoes):
            ctk.CTkButton(
                area_opcoes,
                text=nome,
                height=65,
                font=("Arial", 16, "bold"),
                command=lambda n=nome: abrir_estrutura(n)
            ).grid(
                row=i // 2,
                column=i % 2,
                padx=10,
                pady=10,
                sticky="ew"
            )

        ctk.CTkButton(
            self.area_conteudo,
            text="Voltar à página inicial",
            width=220,
            height=40,
            command=self.mostrar_inicio
        ).pack(pady=10)
  

    def mostrar_cadastro(self):

        self.limpar_tela()

        self.criar_titulo(
            "Cadastrar Evidência",
            "Registre as informações descobertas durante a investigação."
        )

        formulario = ctk.CTkFrame(self.area_conteudo)
        formulario.pack(
            padx=30,
            pady=10,
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            formulario,
            text="Nome da evidência:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.campo_nome = ctk.CTkEntry(
            formulario,
            placeholder_text="Digite o nome da evidência",
            width=500
        )
        self.campo_nome.pack(anchor="w", padx=20)

        ctk.CTkLabel(
            formulario,
            text="Tipo:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.campo_tipo = ctk.CTkOptionMenu(
            formulario,
            values=[
                "Objeto",
                "Substância",
                "Documento",
                "Depoimento",
                "Registro",
                "Vestígio",
                "Observação"
            ],
            width=250
        )
        self.campo_tipo.pack(anchor="w", padx=20)

        ctk.CTkLabel(
            formulario,
            text="Descrição:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.campo_descricao = ctk.CTkTextbox(
            formulario,
            width=700,
            height=100
        )
        self.campo_descricao.pack(anchor="w", padx=20)

        ctk.CTkLabel(
            formulario,
            text="Local encontrado:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.campo_local = ctk.CTkEntry(
            formulario,
            placeholder_text="Digite o local",
            width=500
        )
        self.campo_local.pack(anchor="w", padx=20)

        ctk.CTkLabel(
            formulario,
            text="Importância:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.campo_importancia = ctk.CTkOptionMenu(
            formulario,
            values=["Alta", "Média", "Baixa"],
            width=250
        )
        self.campo_importancia.pack(anchor="w", padx=20)

        ctk.CTkButton(
            formulario,
            text="Salvar evidência",
            width=220,
            height=45,
            font=("Arial", 15, "bold"),
            command=self.cadastrar_evidencia
        ).pack(pady=20)

        ctk.CTkButton(
            self.area_conteudo,
            text="Voltar à página inicial",
            width=220,
            height=40,
            command=self.mostrar_inicio
        ).pack(pady=10)

    def cadastrar_evidencia(self):

        nome = self.campo_nome.get().strip()
        tipo = self.campo_tipo.get()
        descricao = self.campo_descricao.get("1.0", "end").strip()
        local = self.campo_local.get().strip()
        importancia = self.campo_importancia.get()

        if not nome or not descricao or not local:

            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos antes de salvar."
            )
            return

        for item in evidencias:

            if item["nome"].lower() == nome.lower():

                messagebox.showwarning(
                    "Evidência existente",
                    "Essa evidência já está cadastrada."
                )
                return

        numeros = []

        for item in evidencias:
            numeros.append(int(item["codigo"][1:]))

        codigo = "E" + str(max(numeros, default=0) + 1)

        nova_evidencia = {
            "codigo": codigo,
            "nome": nome,
            "tipo": tipo,
            "descricao": descricao,
            "local": local,
            "importancia": importancia
        }

        evidencias.append(nova_evidencia)

        if salvar_evidencias():

            self.tabela_hash.inserir(nova_evidencia)

            messagebox.showinfo(
                "Sucesso",
                "Evidência cadastrada e salva com sucesso!"
            )

            self.mostrar_inicio()

        else:
            evidencias.pop()

    
    def mostrar_mapa(self):

        self.limpar_tela()

        self.criar_titulo(
            "Mapa da Investigação",
            "Localização das evidências e do crime"
        )

        arquivo = criar_mapa()

        ctk.CTkLabel(
            self.area_conteudo,
            text=(
                "O mapa interativo foi gerado com sucesso.\n"
                "Clique abaixo para visualizar os locais e suas evidências."
            ),
            font=("Arial", 15),
            justify="center"
        ).pack(pady=30)

        ctk.CTkButton(
            self.area_conteudo,
            text="Abrir mapa interativo",
            width=250,
            height=50,
            command=lambda: webbrowser.open(
                Path(arquivo).resolve().as_uri()
            )
        ).pack(pady=15)

        ctk.CTkButton(
            self.area_conteudo,
            text="Voltar à página inicial",
            width=220,
            height=40,
            command=self.mostrar_inicio
        ).pack(pady=15)



if __name__ == "__main__":

    app = Envenamento()
    app.mainloop()
