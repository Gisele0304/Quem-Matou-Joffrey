
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

from grafos import criar_grafo

from ordenacao import (
    bubble_sort,
    insertion_sort,
    selection_sort,
    quick_sort,
    comparar_algoritmos
)

from dados import suspeitos, vitima
from estruturas import ListaSequencial, ListaEncadeada, Pilha, Fila, Deque
from tabela_hash import TabelaHash


PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

ARQUIVO_RELACOES = os.path.join(PASTA_PROJETO, "relacoes.json")
ARQUIVO_EVIDENCIAS = os.path.join(PASTA_PROJETO, "evidencias.json")


RELACOES_INICIAIS = [
    {"origem": "Sansa Stark", "destino": "E2"},
    {"origem": "Sansa Stark", "destino": "E6"},
    {"origem": "Petyr Baelish (Mindinho)", "destino": "E2"},
    {"origem": "Petyr Baelish (Mindinho)", "destino": "E6"},
    {"origem": "Olenna Tyrell", "destino": "E1"},
    {"origem": "Olenna Tyrell", "destino": "E2"},
    {"origem": "Dontos Hollard", "destino": "E2"},
    {"origem": "Dontos Hollard", "destino": "E6"},
    {"origem": "Margaery Tyrell", "destino": "E1"},
    {"origem": "Margaery Tyrell", "destino": "E5"},
    {"origem": "Tyrion Lannister", "destino": "E1"},
    {"origem": "Tyrion Lannister", "destino": "E5"}
]


def carregar_relacoes():
    if not os.path.exists(ARQUIVO_RELACOES):
        salvar_relacoes(RELACOES_INICIAIS)

    with open(ARQUIVO_RELACOES, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_relacoes(relacoes):
    with open(ARQUIVO_RELACOES, "w", encoding="utf-8") as arquivo:
        json.dump(relacoes, arquivo, ensure_ascii=False, indent=4)


def carregar_evidencias():
    if os.path.exists(ARQUIVO_EVIDENCIAS):
        with open(ARQUIVO_EVIDENCIAS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return []


def salvar_evidencias(evidencias):
    with open(ARQUIVO_EVIDENCIAS, "w", encoding="utf-8") as arquivo:
        json.dump(evidencias, arquivo, ensure_ascii=False, indent=4)


@app.route("/")
def inicio():
    evidencias = carregar_evidencias()

    return render_template(
        "index.html",
        suspeitos=suspeitos,
        evidencias=evidencias,
        vitima=vitima
    )


@app.route("/suspeitos")
def pagina_suspeitos():
    return render_template("suspeitos.html", suspeitos=suspeitos)


@app.route("/evidencias", methods=["GET", "POST"])
def pagina_evidencias():
    evidencias = carregar_evidencias()
    mensagem = ""

    if request.method == "POST":
        operacao = request.form.get("operacao")

        lista_sequencial = ListaSequencial()

        for evidencia in evidencias:
            lista_sequencial.inserir(evidencia)

        # Fila: cadastrar nova evidência
        if operacao == "cadastrar":
            nova_evidencia = {
                "codigo": request.form.get("codigo", "").strip().upper(),
                "nome": request.form.get("nome", "").strip(),
                "tipo": request.form.get("tipo", "").strip(),
                "descricao": request.form.get("descricao", "").strip(),
                "local": request.form.get("local", "").strip(),
                "importancia": request.form.get("importancia", "").strip()
            }

            tabela = TabelaHash()

            for evidencia in evidencias:
                tabela.inserir(evidencia)

            if not nova_evidencia["codigo"] or not nova_evidencia["nome"]:
                mensagem = "Preencha os campos obrigatórios."

            elif tabela.buscar(nova_evidencia["codigo"]):
                mensagem = "Já existe uma evidência com esse código."

            else:
                fila = Fila()
                fila.enfileirar(nova_evidencia)

                evidencia_processada = fila.desenfileirar()

                lista_sequencial.inserir(evidencia_processada)
                evidencias = lista_sequencial.listar()

                salvar_evidencias(evidencias)

                mensagem = "Evidência cadastrada com sucesso pela estrutura Fila."

        # Pilha: remover último cadastro
        elif operacao == "remover_ultimo":
            pilha = Pilha()

            for evidencia in evidencias:
                pilha.empilhar(evidencia)

            removida = pilha.desempilhar()

            if removida:
                evidencias = [
                    evidencia for evidencia in evidencias
                    if evidencia["codigo"] != removida["codigo"]
                ]

                salvar_evidencias(evidencias)
                mensagem = f"Último cadastro removido: {removida['nome']}."
            else:
                mensagem = "Não existem evidências para remover."

        # Lista encadeada: buscar evidência
        elif operacao == "buscar_encadeada":
            codigo = request.form.get("codigo_busca", "").strip().upper()

            lista_encadeada = ListaEncadeada()

            for evidencia in evidencias:
                lista_encadeada.inserir(evidencia["codigo"])

            resultado = lista_encadeada.buscar(codigo)

            if resultado:
                evidencia_encontrada = next(
                    evidencia for evidencia in evidencias
                    if evidencia["codigo"] == resultado
                )
                mensagem = f"Evidência encontrada: {evidencia_encontrada['nome']}."
            else:
                mensagem = "Evidência não encontrada na lista encadeada."

        # Lista encadeada: remover evidência
        elif operacao == "remover_encadeada":
            codigo = request.form.get("codigo_remover", "").strip().upper()

            lista_encadeada = ListaEncadeada()

            for evidencia in evidencias:
                lista_encadeada.inserir(evidencia["codigo"])

            resultado = lista_encadeada.remover(codigo)

            if resultado:
                evidencias = [
                    evidencia for evidencia in evidencias
                    if evidencia["codigo"] != codigo
                ]

                salvar_evidencias(evidencias)
                mensagem = f"Evidência {codigo} removida pela lista encadeada."
            else:
                mensagem = "Código não encontrado."

        # Deque: mover evidência para o início
        elif operacao == "deque_inicio":
            codigo = request.form.get("codigo_deque", "").strip().upper()

            deque = Deque()

            for evidencia in evidencias:
                deque.inserir_fim(evidencia)

            elementos = deque.listar()

            encontrada = next(
                (item for item in elementos if item["codigo"] == codigo),
                None
            )

            if encontrada:
                novo_deque = Deque()
                novo_deque.inserir_inicio(encontrada)

                for item in elementos:
                    if item["codigo"] != codigo:
                        novo_deque.inserir_fim(item)

                evidencias = novo_deque.listar()
                salvar_evidencias(evidencias)

                mensagem = f"Evidência {codigo} movida para o início."
            else:
                mensagem = "Código não encontrado."

        # Deque: mover evidência para o final
        elif operacao == "deque_fim":
            codigo = request.form.get("codigo_deque", "").strip().upper()

            deque = Deque()

            for evidencia in evidencias:
                deque.inserir_fim(evidencia)

            elementos = deque.listar()

            encontrada = next(
                (item for item in elementos if item["codigo"] == codigo),
                None
            )

            if encontrada:
                novo_deque = Deque()

                for item in elementos:
                    if item["codigo"] != codigo:
                        novo_deque.inserir_fim(item)

                novo_deque.inserir_fim(encontrada)

                evidencias = novo_deque.listar()
                salvar_evidencias(evidencias)

                mensagem = f"Evidência {codigo} movida para o final."
            else:
                mensagem = "Código não encontrado."

        # Tabela hash: buscar evidência pelo código
        elif operacao == "buscar_hash":
            codigo = request.form.get("codigo_hash", "").strip().upper()

            tabela = TabelaHash()

            for evidencia in evidencias:
                tabela.inserir(evidencia)

            resultado = tabela.buscar(codigo)

            if resultado:
                mensagem = (
                    f"Encontrada: {resultado['nome']} | "
                    f"Local: {resultado['local']} | "
                    f"Importância: {resultado['importancia']}."
                )
            else:
                mensagem = "Código não encontrado na tabela hash."

        return render_template(
            "evidencias.html",
            evidencias=evidencias,
            mensagem=mensagem
        )

    lista_sequencial = ListaSequencial()

    for evidencia in evidencias:
        lista_sequencial.inserir(evidencia)

    return render_template(
        "evidencias.html",
        evidencias=lista_sequencial.listar(),
        mensagem=mensagem
    )


@app.route("/estruturas")
def pagina_estruturas():
    return redirect(url_for("pagina_evidencias"))


@app.route("/grafos")
def pagina_grafo():
    return render_template("grafos.html")


@app.route("/api/grafo")
def dados_grafo():
    evidencias = carregar_evidencias()
    relacoes = carregar_relacoes()

    grafo = criar_grafo(suspeitos, evidencias, relacoes)

    nos = []

    for nome, dados in grafo.nodes(data=True):
        nos.append({
            "id": nome,
            "label": dados["label"],
            "group": dados["tipo"]
        })

    arestas = []

    for origem, destino in grafo.edges():
        arestas.append({
            "id": origem + "|||" + destino,
            "from": origem,
            "to": destino
        })

    return jsonify({
        "nodes": nos,
        "edges": arestas
    })


@app.route("/api/grafo/arestas", methods=["POST"])
def adicionar_aresta():
    dados = request.get_json(silent=True) or {}

    origem = dados.get("origem")
    destino = dados.get("destino")

    evidencias = carregar_evidencias()

    grafo = criar_grafo(suspeitos, evidencias, [])

    if not origem or not destino:
        return jsonify({"erro": "Selecione os dois vértices."}), 400

    if origem == destino:
        return jsonify({"erro": "Não é possível ligar um vértice a ele mesmo."}), 400

    if origem not in grafo.nodes or destino not in grafo.nodes:
        return jsonify({"erro": "Vértice não encontrado."}), 400

    if grafo.nodes[origem]["tipo"] == grafo.nodes[destino]["tipo"]:
        return jsonify({"erro": "Ligue um suspeito a uma evidência."}), 400

    relacoes = carregar_relacoes()

    existe = any(
        (r["origem"] == origem and r["destino"] == destino) or
        (r["origem"] == destino and r["destino"] == origem)
        for r in relacoes
    )

    if existe:
        return jsonify({"erro": "Essa ligação já existe."}), 400

    relacoes.append({
        "origem": origem,
        "destino": destino
    })

    salvar_relacoes(relacoes)

    return jsonify({"sucesso": True})


@app.route("/api/grafo/arestas", methods=["DELETE"])
def remover_aresta():
    dados = request.get_json(silent=True) or {}

    origem = dados.get("origem")
    destino = dados.get("destino")

    relacoes = carregar_relacoes()

    novas_relacoes = [
        r for r in relacoes
        if not (
            (r["origem"] == origem and r["destino"] == destino) or
            (r["origem"] == destino and r["destino"] == origem)
        )
    ]

    if len(novas_relacoes) == len(relacoes):
        return jsonify({"erro": "Ligação não encontrada."}), 404

    salvar_relacoes(novas_relacoes)

    return jsonify({"sucesso": True})


@app.route("/mapa")
def pagina_mapa():
    return render_template(
        "mapa.html",
        evidencias=carregar_evidencias()
    )


@app.route("/ordenacao", methods=["GET", "POST"])
def pagina_ordenacao():
    evidencias = carregar_evidencias()

    algoritmos = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "QuickSort": quick_sort
    }

    selecionado = request.form.get("algoritmo", "Bubble Sort")

    if selecionado not in algoritmos:
        selecionado = "Bubble Sort"

    ordenadas = algoritmos[selecionado](evidencias)

    tempos = comparar_algoritmos(evidencias)

    return render_template(
        "ordenacao.html",
        selecionado=selecionado,
        ordenadas=ordenadas,
        tempos=tempos
    )


if __name__ == "__main__":
    app.run(debug=True)
