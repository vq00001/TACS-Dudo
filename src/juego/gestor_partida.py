import os
from time import sleep
from .arbitro_ronda import *
from .contador_pintas  import *

class GestorPartida:
    numero_jugadores = 0 # numero de cachos
    cachos = []
    turno = 0
    pasar_flag = False

    def __init__(self, numero_jugadores):
        self.numero_jugadores = numero_jugadores
    
    # tirar dado para todos los jugadores
    # mayor numero empieza
    # decidir orientacion (izq, der)

    def decidir_turnos(self):
        pass
    
    def preguntar_accion(self):
        
        accion_valida = False

        while(not accion_valida):
            os.system("cls")
            print("1.apostar \n2.dudar \n3.calzar \n4.pasar")

            accion = input("Accion: ").lower()
            accion = accion.strip()

            if accion == "apuesta" or accion == "1" or accion == "apostar":
                accion = "apostar"
            
            elif accion == "dudar" or accion == "dudo" or accion == "2":
                accion = "dudar"
            
            elif accion == "calzar" or accion == "3":
                accion = "calzar"

            elif accion == "pasar" or accion == "3":
                accion = "pasar"
                
            else:
                print("Accion invalida, elegir una de las siguientes opciones.")
                continue

            numero_total_dados = 0
            for cacho in self.cachos:
                cacho.get_cantidad()

                
            if accion == "calzar" and numero_total_dados <= self.numero_jugadores*5*0.2:
                print("Calzar no es permitido, ya que quedan menos de la mitad de dados en juego.")
                sleep(3)
                continue

            elif accion == "pasar" and not ContadorPintas.es_full(self.cachos[self.turno].ver_dados()):
                print("Jugador no cumple condiciones para pasar de turno.")
                sleep(3)
                continue
                

            accion_valida = True


    def preguntar_apuesta(self):
        print("apuesta?")
        pass

    def obligar(self):
        pass

    def validar_fin_juego(self):
        pass

    # controlar rondas
    def loop_juego(self):

        jugando = True
         

        while(jugando):

            print("\nINICIO JUEGO\n")

            apuesta = {
                "existencias": 0,
                "pinta": 0
            }

            ronda = True
            while(ronda):

                # Preguntar si se quiere jugar ronda obligatoria si se cumplen las condiciones
                if (self.cachos[turno].dados == 1 and self.cachos[turno].primer_unico_dado):
                    result = self.obligar()
                    
                    # si se jugó la ronda obligatoria se pasa al siguiente turno, de lo contrario se 
                    if result == True:
                        turno = (turno + 1) % self.numero_jugadores
                        continue
                

                # Preguntar por la accion del turno (apostar, calzar, dudar, pasar)

                accion = self.preguntar_accion()
                accion = "apostar"

                if (accion == "calzar"):
                    jugando = False
                    ArbitroRonda.calzar() # mock

                elif (accion == "dudar"):
                    if self.pasar_flag == False: 
                        ArbitroRonda.dudar() # mock
                
                elif (accion == "apostar"):
                    self.apuesta = self.preguntar_apuesta()
                
                elif (accion == "pasar"): # validar full por implementar
                    self.pasar_flag = True
                
                else:
                    continue
                
                turno = (turno + 1) % self.numero_jugadores

                print(f'turno: ${self.cachos[self.turno].nombre}, apuesta: ${apuesta}')

            if self.validar_fin_juego():
                jugando = False

        print("Fin del juego")
