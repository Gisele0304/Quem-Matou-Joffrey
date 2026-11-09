
import networkx as nx
from dados import suspeitos, evidencias


def criar_grafo():
    G = nx.Graph()

    for suspeito in suspeitos:
        G.add_node(
            suspeito["nome"],
            tipo="suspeito"
        )

    for evidencia in evidencias:
        G.add_node(
            evidencia["codigo"],
            nome=evidencia["nome"],
            tipo="evidencia"
        )

    relacoes = {
        "Sansa Stark": ["E2", "E6"],
        "Petyr Baelish (Mindinho)": ["E2", "E6"],
        "Olenna Tyrell": ["E1", "E2"],
        "Dontos Hollard": ["E2", "E6"],
        "Margaery Tyrell": ["E1", "E5"],
        "Tyrion Lannister": ["E1", "E5"]
    }

    for suspeito, codigos in relacoes.items():
        for codigo in codigos:
            if G.has_node(suspeito) and G.has_node(codigo):
                G.add_edge(suspeito, codigo)

    return G


def desenhar_grafo(grafo, ax, posicoes=None, selecionados=None):
    ax.clear()

    if posicoes is None:
        posicoes = nx.spring_layout(
            grafo,
            seed=42,
            k=2.5,
            iterations=200
        )

    if selecionados is None:
        selecionados = []

    suspeitos_grafo = [
        no for no, dados in grafo.nodes(data=True)
        if dados["tipo"] == "suspeito"
    ]

    evidencias_grafo = [
        no for no, dados in grafo.nodes(data=True)
        if dados["tipo"] == "evidencia"
    ]

    ax.set_facecolor("#F4F6F8")

    nx.draw_networkx_edges(
        grafo,
        posicoes,
        ax=ax,
        edge_color="#566573",
        width=3,
        alpha=0.9
    )

    nx.draw_networkx_nodes(
        grafo,
        posicoes,
        nodelist=suspeitos_grafo,
        node_color="#922B21",
        node_size=6000,
        ax=ax,
        edgecolors="#641E16",
        linewidths=2
    )

    nx.draw_networkx_nodes(
        grafo,
        posicoes,
        nodelist=evidencias_grafo,
        node_color="#21618C",
        node_size=3500,
        node_shape="s",
        ax=ax,
        edgecolors="#154360",
        linewidths=2
    )

    if selecionados:
        nx.draw_networkx_nodes(
            grafo,
            posicoes,
            nodelist=selecionados,
            node_color="#F1C40F",
            node_size=6500,
            ax=ax,
            edgecolors="#B7950B",
            linewidths=3
        )

    nx.draw_networkx_labels(
        grafo,
        posicoes,
        font_size=9,
        font_weight="bold",
        font_color="white",
        ax=ax
    )

    ax.set_title(
        "Conexões entre suspeitos e evidências",
        fontsize=17,
        fontweight="bold",
        color="#17202A",
        pad=20
    )

    ax.axis("off")

    return posicoes
