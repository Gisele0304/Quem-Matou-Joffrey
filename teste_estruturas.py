
from estruturas import (
    ListaSequencial,
    ListaEncadeada,
    Pilha,
    Fila,
    Deque
)

lista = ListaSequencial()
lista.inserir("E1")
lista.inserir("E2")
lista.inserir("E3")
print("Lista:", lista.listar())
print("Busca:", lista.buscar("E2"))

encadeada = ListaEncadeada()
encadeada.inserir("E1")
encadeada.inserir("E2")
encadeada.inserir("E3")
print("\nLista encadeada:", encadeada.listar())
encadeada.remover("E2")
print("Após remoção:", encadeada.listar())

pilha = Pilha()
pilha.empilhar("E1")
pilha.empilhar("E2")
pilha.empilhar("E3")
print("\nPilha:", pilha.listar())
print("Desempilhado:", pilha.desempilhar())

fila = Fila()
fila.enfileirar("E1")
fila.enfileirar("E2")
fila.enfileirar("E3")
print("\nFila:", fila.listar())
print("Desenfileirado:", fila.desenfileirar())

deque = Deque()
deque.inserir_inicio("E1")
deque.inserir_fim("E2")
deque.inserir_inicio("E3")
print("\nDeque:", deque.listar())
print("Removido do início:", deque.remover_inicio())
print("Removido do fim:", deque.remover_fim())
print("Deque final:", deque.listar())
