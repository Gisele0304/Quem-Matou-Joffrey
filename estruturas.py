
class ListaSequencial:
    def __init__(self):
        self.elementos = []

    def inserir(self, elemento):
        self.elementos.append(elemento)

    def remover(self, elemento):
        if elemento in self.elementos:
            self.elementos.remove(elemento)
            return True
        return False

    def buscar(self, elemento):
        if elemento in self.elementos:
            return self.elementos.index(elemento)
        return -1

    def listar(self):
        return self.elementos.copy()


class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class ListaEncadeada:
    def __init__(self):
        self.inicio = None

    def inserir(self, dado):
        novo = No(dado)

        if self.inicio is None:
            self.inicio = novo
            return

        atual = self.inicio

        while atual.proximo is not None:
            atual = atual.proximo

        atual.proximo = novo

    def remover(self, dado):
        atual = self.inicio
        anterior = None

        while atual is not None:
            if atual.dado == dado:
                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo

                return True

            anterior = atual
            atual = atual.proximo

        return False

    def buscar(self, dado):
        atual = self.inicio

        while atual is not None:
            if atual.dado == dado:
                return atual.dado

            atual = atual.proximo

        return None

    def listar(self):
        elementos = []
        atual = self.inicio

        while atual is not None:
            elementos.append(atual.dado)
            atual = atual.proximo

        return elementos


class Pilha:
    def __init__(self):
        self.elementos = []

    def empilhar(self, elemento):
        self.elementos.append(elemento)

    def desempilhar(self):
        if not self.esta_vazia():
            return self.elementos.pop()
        return None

    def topo(self):
        if not self.esta_vazia():
            return self.elementos[-1]
        return None

    def esta_vazia(self):
        return len(self.elementos) == 0

    def listar(self):
        return self.elementos.copy()


class Fila:
    def __init__(self):
        self.elementos = []

    def enfileirar(self, elemento):
        self.elementos.append(elemento)

    def desenfileirar(self):
        if not self.esta_vazia():
            return self.elementos.pop(0)
        return None

    def frente(self):
        if not self.esta_vazia():
            return self.elementos[0]
        return None

    def esta_vazia(self):
        return len(self.elementos) == 0

    def listar(self):
        return self.elementos.copy()


class Deque:
    def __init__(self):
        self.elementos = []

    def inserir_inicio(self, elemento):
        self.elementos.insert(0, elemento)

    def inserir_fim(self, elemento):
        self.elementos.append(elemento)

    def remover_inicio(self):
        if not self.esta_vazia():
            return self.elementos.pop(0)
        return None

    def remover_fim(self):
        if not self.esta_vazia():
            return self.elementos.pop()
        return None

    def esta_vazia(self):
        return len(self.elementos) == 0

    def listar(self):
        return self.elementos.copy()
