from src.juego.contador_pintas import ContadorPintas
from src.servicios.excepciones import CalzadoInvalido

class ArbitroRonda():
    def __init__(self):
        pass

    # @staticmethod 
    # def contar_repeticiones_dados(cachos):
    #    # Devuelve una lista con la cantidad de cada pinta (índice 1 a 6)
    #     valores_dados = [0, 0, 0, 0, 0, 0, 0]
    #     for cacho in cachos:
    #         dados = cacho.ver_dados()
    #         for pinta in range(1, 7):
    #             valores_dados[pinta] += ContadorPintas.contar_sin_comodines(dados, pinta)
    #     return valores_dados
    
    @staticmethod 
    def contar_repeticiones_dados(cachos, pinta):
        contador = ContadorPintas()
        repeticiones = 0
        for cacho in cachos:
            if pinta != 1:
                repeticiones += contador.contar_con_comodines(cacho.ver_dados(), pinta)
            else:
                repeticiones += contador.contar_sin_comodines(cacho.ver_dados(), pinta)

        return repeticiones

    
    @staticmethod 
    def dudar(apuesta, cachos, turno):
        pinta = apuesta["pinta"]
        # calcular las existencias de la pinta. Si la pinta no es As, estos se usan como comodines. 
        dados_acumulados = ArbitroRonda.contar_repeticiones_dados(cachos, pinta)
       
        if (dados_acumulados < apuesta["existencias"]):
            # jugador que puso la apuesta pierde un dado
            cachos[(turno - 1) % len(cachos)].sacar_dado()
            return True
        else:
            # jugador que duda pierde un dado
            cachos[turno].sacar_dado()
            return False
    
    @staticmethod 
    def calzar(apuesta, cachos, turno):
        pinta = apuesta["pinta"]
        dados_acumulados = ArbitroRonda.contar_repeticiones_dados(cachos, pinta)
        total_dados = sum(len(c.ver_dados()) for c in cachos)
        dados_jugador = len(cachos[turno].ver_dados())
        # si las existencias son iguales a las de las apostadas el jugador que calzo gana un dado
        if not (dados_jugador == 1 or ((len(cachos)*5 // 2) <= total_dados)):
            raise CalzadoInvalido("No se puede calzar en esta situación.")

        if (dados_acumulados == apuesta["existencias"]): 
            cachos[turno].agregar_dado()                    
            return True
        else:
            # de lo contrario pierde un dado
            cachos[turno].sacar_dado()
            return False
        