
import time


def valor_importancia(evidencia):
    prioridades = {
        "Alta": 1,
        "Média": 2,
        "Baixa": 3
    }

    return prioridades.get(evidencia["importancia"], 4)


def bubble_sort(lista):
    dados = lista.copy()
    tamanho = len(dados)

    for i in range(tamanho):
        for j in range(0, tamanho - i - 1):
            if valor_importancia(dados[j]) > valor_importancia(dados[j + 1]):
                dados[j], dados[j + 1] = dados[j + 1], dados[j]

    return dados


def insertion_sort(lista):
    dados = lista.copy()

    for i in range(1, len(dados)):
        atual = dados[i]
        j = i - 1

        while j >= 0 and valor_importancia(dados[j]) > valor_importancia(atual):
            dados[j + 1] = dados[j]
            j -= 1

        dados[j + 1] = atual

    return dados


def selection_sort(lista):
    dados = lista.copy()
    tamanho = len(dados)

    for i in range(tamanho):
        menor = i

        for j in range(i + 1, tamanho):
            if valor_importancia(dados[j]) < valor_importancia(dados[menor]):
                menor = j

        dados[i], dados[menor] = dados[menor], dados[i]

    return dados


def quick_sort(lista):
    dados = lista.copy()

    def ordenar(inicio, fim):
        if inicio < fim:
            pivo = valor_importancia(dados[fim])
            i = inicio - 1

            for j in range(inicio, fim):
                if valor_importancia(dados[j]) <= pivo:
                    i += 1
                    dados[i], dados[j] = dados[j], dados[i]

            dados[i + 1], dados[fim] = dados[fim], dados[i + 1]
            posicao = i + 1

            ordenar(inicio, posicao - 1)
            ordenar(posicao + 1, fim)

    ordenar(0, len(dados) - 1)

    return dados


def comparar_algoritmos(lista):
    algoritmos = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Selection Sort": selection_sort,
        "QuickSort": quick_sort
    }

    resultados = {}

    for nome, algoritmo in algoritmos.items():
        inicio = time.perf_counter()
        algoritmo(lista)
        fim = time.perf_counter()

        resultados[nome] = (fim - inicio) * 1000

    return resultados
