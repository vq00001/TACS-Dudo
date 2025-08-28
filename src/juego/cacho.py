import dado

class cacho:
    def __init__(self):
        self.dados = []
        for i in range(5):
            self.dados.append(dado.dado())

    def tirar_dados(self):
        for i in range(len(self.dados)):
            self.dados[i].tirar()
        return self.dados