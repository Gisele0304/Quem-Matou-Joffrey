
class TabelaHash:

    def __init__(self, tamanho=10):
        self.tamanho = tamanho
        self.tabela = [[] for i in range(tamanho)]

    def funcao_hash(self, codigo):
        return sum(ord(letra) for letra in codigo) % self.tamanho

    def inserir(self, evidencia):

        codigo = evidencia["codigo"]
        indice = self.funcao_hash(codigo)

        for item in self.tabela[indice]:

            if item["codigo"] == codigo:
                return False

        self.tabela[indice].append(evidencia)
        return True

    def buscar(self, codigo):

        indice = self.funcao_hash(codigo)

        for item in self.tabela[indice]:

            if item["codigo"] == codigo:
                return item

        return None

    def remover(self, codigo):

        indice = self.funcao_hash(codigo)

        for item in self.tabela[indice]:

            if item["codigo"] == codigo:
                self.tabela[indice].remove(item)
                return True

        return False

    def listar(self):

        elementos = []

        for lista in self.tabela:
            for item in lista:
                elementos.append(item)

        return elementos

    
if __name__ == "__main__":

    tabela = TabelaHash()

    evidencia1 = {
        "codigo": "E1",
        "nome": "Taça de Joffrey"
    }

    evidencia2 = {
        "codigo": "E2",
        "nome": "Rede de cabelo de Sansa"
    }

    tabela.inserir(evidencia1)
    tabela.inserir(evidencia2)

    print("Busca por E1:")
    print(tabela.buscar("E1"))

    print("\nTodas as evidências:")
    print(tabela.listar())

    print("\nRemovendo E2:")
    print(tabela.remover("E2"))

    print("\nEvidências restantes:")
    print(tabela.listar())