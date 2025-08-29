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
        dados_acumulados =  ArbitroRonda.contar_repeticiones_dados(cachos)
        
        if (apuesta["pinta"] != 1 and (apuesta["existencias"] > dados_acumulados[apuesta["pinta"]] + dados_acumulados[1])):
            # los Ases se cuentan como comodin si la pinta de la apuesta es distinta a As
            cachos[(turno - 1) % len(cachos)].sacar_dado()
            return True

        elif (apuesta["existencias"] > dados_acumulados[apuesta["pinta"]]):

            # jugador que puso la apuesta pierde un dado
            cachos[(turno - 1) % len(cachos)].sacar_dado()
            return True
        else:
            # jugador que duda pierde un dado
            cachos[turno].sacar_dado()
            return False
    
    @staticmethod 
    def calzar(apuesta, cachos, turno):
        pass