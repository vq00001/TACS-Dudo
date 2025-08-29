class ArbitroRonda():
    def __init__(self):
        pass

    @staticmethod 
    def contar_repeticiones_dados(cachos):
        valores_dados = [0,0,0,0,0,0,0]
        
        for cacho in cachos:
            dados = cacho.ver_dados()
            for i in dados:
                valores_dados[i] += 1

        return valores_dados
    
    @staticmethod 
    def dudar(apuesta, cachos, turno):
        
        pass
    
    @staticmethod 
    def calzar():
        pass