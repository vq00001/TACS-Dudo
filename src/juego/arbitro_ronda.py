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
        pinta = apuesta["pinta"]
        if (pinta == 1 and (dados_acumulados[pinta] < apuesta["existencias"])):

            # los Ases no cuentan como comodin si la pinta de la apuesta es As
            # jugador que puso la apuesta pierde un dado
            cachos[(turno - 1) % len(cachos)].sacar_dado()
            return True
        
        elif (dados_acumulados[pinta] + dados_acumulados[1] < apuesta["existencias"]):
            # jugador que puso la apuesta pierde un dado
            cachos[(turno - 1) % len(cachos)].sacar_dado()
            return True

        else:
            # jugador que duda pierde un dado
            cachos[turno].sacar_dado()
            return False
    
    @staticmethod 
    def calzar(apuesta, cachos, turno):
        dados_acumulados = ArbitroRonda.contar_repeticiones_dados(cachos)

        pinta = apuesta["pinta"]
        if(pinta == 1 and (dados_acumulados[pinta] == apuesta["existencias"])):
            cachos[turno].agregar_dado()
            return True
        elif(dados_acumulados[pinta] + dados_acumulados[1] == apuesta["existencias"]):
            cachos[turno].agregar_dado()
            return True
        else:
            cachos[turno].sacar_dado()
            return False
        