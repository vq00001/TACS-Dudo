import os
from time import sleep
from src.juego.arbitro_ronda import *
from src.juego.contador_pintas import *
from src.juego.cacho import *
from src.juego.validador_apuesta import ValidadorApuesta
from src.servicios.borrar_lineas import borrar_lineas
 
class GestorPartida:

    def __init__(self, numero_jugadores, debug=False):
        
        self.numero_jugadores = numero_jugadores
        self.debug = debug
        self.cachos = []
        self.turno = 0
        self.apuesta = {"existencias": 0, "pinta": 0}
        self.pasar_flag = False
        self.tipo_ronda = "normal"                                # opciones: normal, abierta, cerrada
        self.jugador_que_obliga = -1                              # index de jugador que hace la ronda obligada

        for i in range(numero_jugadores):
            c = cacho()

            if debug == False:
                c.nombre = input(f"nombre jugador {i + 1}: ")
            self.cachos.append(c)    

    def decidir_turnos(self):
        
        print("decidir el primer jugador...")
        sleep(2)
        
        repetidos = [] 
        dado_var = dado()
        val_mayor_dado = 0
        primer_jugador = -1

        # tirar dado para todos los jugadores
        for jugador in range(self.numero_jugadores):
    
            input(f"\n{self.cachos[jugador].nombre}, apreta para tirar dado...")

            dado_var.tirar()

            print(f"¡has sacado un {dado_var.ver()}!")

            # si el valor ya aparecio se agrega a repetidos para el desempate, si no se asigna el primer jugador.
            if dado_var.ver() == val_mayor_dado:
                repetidos.append(jugador)

            elif dado_var.ver() > val_mayor_dado:
                val_mayor_dado = dado_var.ver()
                primer_jugador = jugador
        
        val_mayor_dado = 0
        
        # si hay jugadores empatados se repite el proceso hasta que se decida un ganador.
        while(len(repetidos) > 0):
            nuevos_repetidos = []

            for jugador in repetidos:
                dado_var.tirar()
                if dado_var.ver() == val_mayor_dado:
                    nuevos_repetidos.append(jugador)
                elif dado_var.ver() > val_mayor_dado:
                    val_mayor_dado = dado_var.ver()
                    primer_jugador = jugador
            
            val_mayor_dado = 0
            repetidos = nuevos_repetidos

        print(f"\ncomienza {self.cachos[primer_jugador].nombre}.")

        # decidir sentido del juego
        sentido = input("\n¿El sentido del juego ira hacia la izquierda o derecha? ").lower()
        sentido = sentido.strip()

        self.turno = primer_jugador  # asignar el turno al jugador que empieza.
        if sentido == "izquierda" or sentido == "izq":   # modificar la lista de modo que quede en la direccion correcta.
            self.cachos.reverse()
            self.turno = self.numero_jugadores - 1 - self.turno  # recalcular index de turno

        sleep(3)
        return self.cachos[self.turno] # devolver el cacho del primer jugador 

    # imprimir los dados en los cachos de cada jugador.
    def mostrar_dados(self):
        borrar_lineas(6)

        if self.tipo_ronda == "normal":

            # en una ronda normal los jugadores pueden ver solo sus propios dadoss
            print(f"mostrando dados de {self.cachos[self.turno].nombre}")
            sleep(3)
            print(self.cachos[self.turno].ver_dados())
            input("presionar para seguir jugando.")
            borrar_lineas(3)

        elif self.tipo_ronda == "abierta":

            # si la ronda es abierta todos los jugadores pueden ver los cachos del resto, pero no los suyos.
            print(f"mostrando dados de todos menos {self.cachos[self.turno].nombre}.")
            sleep(3)

            for cacho in self.cachos:
                if cacho != self.cachos[self.turno]:
                    print(f"{cacho.nombre}: {cacho.ver_dados()}")

            input("presionar para seguir jugando.")
            borrar_lineas(2 + len(self.cachos))

        elif self.tipo_ronda == "cerrada":

            # si la ronda es cerrada solo el jugador que obliga puede ver sus propios dados.
            if self.jugador_que_obliga == self.turno:
                print(f"mostrando dados de {self.cachos[self.turno].nombre}")
                sleep(3)
                print(self.cachos[self.turno].ver_dados())
                input("presionar para seguir jugando.")
                borrar_lineas(3)
            else:
                print(f"se esta jugando una ronda cerrada, por lo que solo {self.cachos[self.jugador_que_obliga].nombre} puede ver sus dados.")
                sleep(3)
                borrar_lineas(1)
        
     
    # preguntar al usuario por la accion de su turno.
    def preguntar_accion(self):
        apuesta_valida = True
        if self.apuesta["existencias"] == 0 or self.apuesta["pinta"] == 0:
            apuesta_valida = False

        accion_valida = False
        accion = ""

        while(not accion_valida):
            print("1.apostar \n2.dudar \n3.calzar \n4.pasar \n5.ver dados")

            accion = input("Accion: ").lower()
            accion = accion.strip()

            if accion == "apuesta" or accion == "1" or accion == "apostar":
                accion = "apostar"
            
            elif accion == "dudar" or accion == "dudo" or accion == "2":
                accion = "dudar"
            
            elif accion == "calzar" or accion == "3":
                accion = "calzar"

            elif accion == "pasar" or accion == "4":
                accion = "pasar"
            
            elif accion == "ver dados" or accion == "5":
                self.mostrar_dados()
            else:
                print("accion invalida, elegir una de las siguientes opciones.")
                sleep(3)
                borrar_lineas(7)
                continue

            numero_total_dados = 0
            for cacho in self.cachos:
                numero_total_dados += cacho.get_cantidad()
                
            if (accion == "calzar" or accion == "dudar") and (not apuesta_valida):
                print("aun no se hace ninguna apuesta. Accion invalida.")
                sleep(3)
                borrar_lineas(7)
                continue

            elif accion == "calzar" and numero_total_dados < self.numero_jugadores*5*0.2:
                print("calzar no es permitido, ya que quedan menos de la mitad de dados en juego.")
                sleep(3)
                borrar_lineas(7)
                continue

            elif accion == "pasar" and not ContadorPintas.es_full(self.cachos[self.turno].ver_dados()):
                print("jugador no cumple condiciones para pasar de turno.")
                sleep(3)
                borrar_lineas(7)
                continue
            elif accion == "apuesta" and not ValidadorApuesta.validar(self.apuesta):
                sleep(3)
                borrar_lineas(7)
                continue
                
            return accion

    # preguntar al usuario por la apuesta.
    def preguntar_apuesta(self):
        nombres_pintas_singular = ["As", "Tonto", "Tren", "Cuarta", "Quina", "Sexto"]
        nombres_pintas = ["Ases", "Tontos", "Trenes", "Cuartas", "Quinas", "Sextos"]
        apuesta_valida = False

        while(not apuesta_valida):
            
            # imprimir la apuesta actual y las pintas que se pueden escoger
            borrar_lineas(6)

            i = 0
            for p in nombres_pintas_singular:
                print(f"{i + 1} - {p}")
                i += 1

            # leer el numero de existencias de la apuesta.
            existencias = input("Existencias: ").lower()
            existencias = existencias.strip()

            if not existencias.isdigit():
                print("numero de existencias debe ser un entero entre 1 y 6.")
                sleep(3)
                borrar_lineas(2)
                continue
            
            # leer la pinta de la apuesta y mapearla a un numero.
            pinta = input("Pinta: ").lower()
            pinta = pinta.strip()

            if pinta == "as" or pinta == "ases" or pinta == "1":
                pinta = 1

            elif pinta == "tonto" or pinta == "tontos" or pinta == "2":
                pinta = 2

            elif pinta == "tren" or pinta == "trenes" or pinta == "3":
                pinta = 3

            elif pinta == "cuarta" or pinta == "cuartas" or pinta == "4":
                pinta = 4

            elif pinta == "quina" or pinta == "quinas" or pinta == "5":
                pinta = 5
            
            elif pinta == "sexto" or pinta == "sextos" or pinta == "6":
                pinta = 6
            else:
                print("pinta no valida.")
                sleep(3)
                borrar_lineas(3)
                continue
            
            # formatear la apuesta como diccionario
            nueva_apuesta = {
                "existencias": int(existencias),
                "pinta": pinta
            }

            return nueva_apuesta

    # preguntar si se quiere hacer una ronda obligada.
    def obligar(self):
        cacho_actual = self.cachos[self.turno]
        if (cacho_actual.get_cantidad() == 1 and cacho_actual.primer_unico_dado):
            cacho_actual.primer_unico_dado = False
            
            # preguntar hasta obtener una respuesta valida
            while(True):
                print("¿quieres hacer una ronda obligada? \n1.ronda abierta \n2.ronda cerrada \n3.ronda normal")
                ronda = input("ronda: ")
                ronda = ronda.strip()
            
                if ronda == "ronda abierta" or ronda == "abierta" or ronda == "1":
                    self.tipo_ronda = "abierta"
                    self.jugador_que_obliga = self.turno
                    borrar_lineas(5)
                    break

                elif ronda == "ronda cerrada" or ronda == "cerrada" or ronda == "2":
                    self.tipo_ronda = "cerrada"
                    self.jugador_que_obliga = self.turno
                    borrar_lineas(5)
                    break

                elif ronda == "ronda normal" or ronda == "normal" or ronda == "3":
                    self.tipo_ronda = "normal"
                    borrar_lineas(5)
                    break   

                print("opcion no valida, intenta de nuevo.")
                sleep(3)
                borrar_lineas(6)


    def validar_fin_juego(self):
       
        cant_jugadores = 0
        for cacho in self.cachos:
            if cacho.get_cantidad() > 0:
                cant_jugadores += 1
        
        if cant_jugadores == 1:
            return True  
        else:
            return False

    # controlar rondas
    def loop_juego(self):
        self.decidir_turnos()

        print("\nINICIO JUEGO\n")
        sleep(2)

        while(not self.validar_fin_juego()):
            
            # reiniciar la apuesta
            self.apuesta = {
                "existencias": 0,
                "pinta": 0
            } 

            # tirar los dados de todos los jugadores
            for cacho in self.cachos:
                cacho.tirar_dados()

            ronda = True
            while(ronda):
                os.system('cls')

                # imprimir estado juego
                self.imprimir_estado_juego()

                # Preguntar si se quiere jugar ronda obligatoria si se cumplen las condiciones
                
                self.obligar()
                    
                # Preguntar por la accion del turno (apostar, calzar, dudar, pasar)
                accion = self.preguntar_accion()

                if (accion == "apostar"):
                    self.apuesta = self.preguntar_apuesta()

                elif (accion == "dudar"):
                    if self.pasar_flag == False: 

                        resultado = ArbitroRonda.dudar(self.apuesta, self.cachos, self.turno) 

                        # imprimir resultado
                        if resultado:
                            print(f"exito. {self.cachos[(self.turno - 1)%self.numero_jugadores].nombre} pierde un dado.")

                            # en la siguiente ronda parte el jugador que perdio un dado
                            self.turno = (self.turno - 1) % self.numero_jugadores  

                        else:
                            print(f"fallo. {self.cachos[self.turno].nombre} pierde un dado.")

                        sleep(3)
                        break
                        
                    else:  # si se duda un "pase" se termina la ronda sin perdidas ni ganancias 
                        print("se dudo un pase. se comienza la siguiente ronda.")
                        sleep(3)
                        break

                elif (accion == "calzar"):
                    jugando = False
                    resultado = ArbitroRonda.calzar(self.apuesta, self.cachos, self.turno) 

                    # imprimir resultado
                    if resultado:
                        print(f"exito. {self.cachos[self.turno].nombre} gana un dado.")
                    else:
                        print(f"fallo. {self.cachos[self.turno].nombre} pierde un dado.")
                    sleep(3)
                    break

                elif (accion == "pasar"):
                    self.pasar_flag = True
                    sleep(3)
                else:
                    # si no coincide ninguna acción, volver a repetir el turno
                    continue
                
                # una vez termino el turno, se pasa al siguiente jugador
                self.turno = (self.turno + 1) % self.numero_jugadores

            # resetear el tipo de ronda y el jugador que obliga
            self.tipo_ronda = "normal"
            self.jugador_que_obliga = -1

        # imprimir el ganador
        os.system("cls")
        self.imprimir_estado_juego()
        for cacho in self.cachos:
            if cacho.get_cantidad() > 0:
                print(f"¡HA GANADO {self.cachos[self.turno].nombre}!")
                break

        print("fin del juego.")

    def imprimir_estado_juego(self):
        nombres_pintas_singular = ["As", "Tonto", "Tren", "Cuarta", "Quina", "Sexto"]
        nombres_pintas = ["Ases", "Tontos", "Trenes", "Cuartas", "Quinas", "Sextos"]

        if not self.debug:
            print("_" * 60)

            print(f"{'Jugador':<10} {'Dados':<7} {'A favor':<8}")

            # Filas por jugador
            for cacho in self.cachos:
                print(f"{cacho.nombre:<10} {cacho.get_cantidad():<7} {cacho.get_dados_extra():<8}")

            print("_" * 60)

   
            if self.apuesta["existencias"] > 0 and self.apuesta["pinta"] > 0:
            # Info de turno y apuesta
                if self.apuesta["existencias"] > 1:
                    print(
                        f"TURNO: {self.cachos[self.turno].nombre:<10} "
                        f"APUESTA: {self.apuesta['existencias']} {nombres_pintas[self.apuesta['pinta']-1]}"
                    )
                else:
                    print(
                        f"TURNO: {self.cachos[self.turno].nombre:<10} "
                        f"APUESTA: {self.apuesta['existencias']} {nombres_pintas_singular[self.apuesta['pinta']-1]}"
                    )
            else:
                print(f"TURNO: {self.cachos[self.turno].nombre:<10} SIN APUESTA")

            print("_"*60)
