
from dados import evidencias
from ordenacao import (
    bubble_sort,
    insertion_sort,
    selection_sort,
    quick_sort,
    comparar_algoritmos
)

print("BUBBLE SORT")
lista_teste = evidencias[::-1]

print([e["codigo"] for e in bubble_sort(lista_teste)])
print("\nINSERTION SORT")
print([e["codigo"] for e in insertion_sort(lista_teste)])

print("\nSELECTION SORT")
print([e["codigo"] for e in selection_sort(lista_teste)])

print("\nQUICKSORT")
print([e["codigo"] for e in quick_sort(lista_teste)])

print("\nTEMPO DE EXECUÇÃO (ms)")
print(comparar_algoritmos(lista_teste))
