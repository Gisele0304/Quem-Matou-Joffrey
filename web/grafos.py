
import networkx as nx


def criar_grafo(suspeitos_lista, evidencias_lista, relacoes):
    G = nx.Graph()

    for suspeito in suspeitos_lista:
        G.add_node(
            suspeito["nome"],
            tipo="suspeito",
            label=suspeito["nome"]
        )

    for evidencia in evidencias_lista:
        G.add_node(
            evidencia["codigo"],
            tipo="evidencia",
            label=f'{evidencia["codigo"]} - {evidencia["nome"]}'
        )

    for relacao in relacoes:
        origem = relacao["origem"]
        destino = relacao["destino"]

        if G.has_node(origem) and G.has_node(destino):
            G.add_edge(origem, destino)

    return G
