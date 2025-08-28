import dado

class cacho:
    def __init__(self):
        self.dados = []
        for i in range(5):
            self.dados.append(dado.dado())