import os
from time import sleep
from src.juego.arbitro_ronda import *
from src.juego.contador_pintas import *
from src.juego.cacho import *
from src.juego.validador_apuesta import ValidadorApuesta
from src.servicios.borrar_lineas import borrar_lineas
 
class GestorPartida:

    def __init__(self, numero_jugadores, debug=False):
        
        self.validador_apuesta = ValidadorApuesta()
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
    def preguntar_apuesta(self):
        # Nombres de las pintas (mantén esta parte)
        nombres_pintas_singular = ["As", "Tonto", "Tren", "Cuarta", "Quina", "Sexto"]
        nombres_pintas = ["Ases", "Tontos", "Trenes", "Cuartas", "Quinas", "Sextos"]

        while True:
            # Mostrar la apuesta actual y las pintas disponibles (mantén la lógica de impresión)
            borrar_lineas(6)
            i = 0
            for p in nombres_pintas_singular:
                print(f"{i + 1} - {p}")
                i += 1
            print("-" * 20)
            if self.apuesta["existencias"] > 0:
                print(f"Apuesta anterior: {self.apuesta['existencias']} {nombres_pintas[self.apuesta['pinta'] - 1]}")
            print("-" * 20)

            # Pedir la apuesta
            entrada = input("Ingrese su apuesta (cantidad y pinta) ej: '3 4': ").lower()
            
            partes = entrada.split()
            if len(partes) != 2:
                print("Formato incorrecto. Por favor, ingrese dos números separados por un espacio.")
                sleep(2)
                continue
            
            try:
                nueva_cantidad = int(partes[0])
                nuevo_numero = int(partes[1])
            except ValueError:
                print("Entrada inválida. Por favor, ingrese solo números.")
                sleep(2)
                continue
            
            # Primero, si no hay apuesta previa, usa set_apuesta para validar la primera apuesta
            if self.apuesta["existencias"] == 0:
                try:
                    self.validador_apuesta.set_apuesta(
                        nueva_cantidad,
                        nuevo_numero,
                        jugador_un_dado=(self.cachos[self.turno].get_cantidad() == 1)
                    )
                    # Si la validación pasa, actualiza la apuesta de la partida
                    self.apuesta["existencias"] = nueva_cantidad
                    self.apuesta["pinta"] = nuevo_numero
                    return {"accion": "apostar"} # Devolver la acción como un diccionario
                except ValueError as e:
                    print(f"Apuesta inválida: {e}. Intente de nuevo.")
                    sleep(2)
                    continue
            else:
                # Si ya hay una apuesta, usa validar_subida o validar_bajada
                valida_subida = self.validador_apuesta.validar_subida(nueva_cantidad, nuevo_numero)
                valida_bajada = self.validador_apuesta.validar_bajada(nueva_cantidad, nuevo_numero)
                
                if valida_subida or valida_bajada:
                    # Si es válida, actualiza el estado del validador y de la partida
                    self.validador_apuesta.set_apuesta(
                        nueva_cantidad,
                        nuevo_numero,
                        jugador_un_dado=(self.cachos[self.turno].get_cantidad() == 1)
                    )
                    self.apuesta["existencias"] = nueva_cantidad
                    self.apuesta["pinta"] = nuevo_numero
                    return {"accion": "apostar"}
                else:
                    print("Apuesta inválida. No es una subida o bajada permitida.")
                    sleep(2)
                    continue

    # preguntar al usuario por la apuesta.
    def preguntar_apuesta(self):
        # Nombres de las pintas
        nombres_pintas_singular = ["As", "Tonto", "Tren", "Cuarta", "Quina", "Sexto"]
        nombres_pintas = ["Ases", "Tontos", "Trenes", "Cuartas", "Quinas", "Sextos"]

        # Bucle para asegurar que se ingresa una apuesta válida
        while True:
            # Imprimir la apuesta actual y las pintas que se pueden escoger
            borrar_lineas(6)
            
            i = 0
            for p in nombres_pintas_singular:
                print(f"{i + 1} - {p}")
                i += 1
            
            print("-" * 20)
            
            # Si hay una apuesta anterior, mostrarla
            if self.apuesta["existencias"] > 0:
                print(f"Apuesta anterior: {self.apuesta['existencias']} {nombres_pintas[self.apuesta['pinta'] - 1]}")
            
            print("-" * 20)
            
            # Pedir la nueva apuesta al jugador
            entrada = input("Ingrese su apuesta (cantidad y pinta) ej: '3 4' o 'duda' o 'calza': ").lower()
            
            if entrada.strip() == "duda" or entrada.strip() == "dudar":
                return {"accion": "dudar"}
            elif entrada.strip() == "calza" or entrada.strip() == "calzar":
                return {"accion": "calzar"}
            
            partes = entrada.split()
            
            if len(partes) != 2:
                print("Formato incorrecto. Por favor, ingrese dos números separados por un espacio.")
                sleep(2)
                continue
            
            try:
                nueva_cantidad = int(partes[0])
                nuevo_numero = int(partes[1])
            except ValueError:
                print("Entrada inválida. Por favor, ingrese solo números.")
                sleep(2)
                continue
            
            # Integrar la lógica de validación de ValidadorApuesta
            # Aquí es donde conectas la clase que revisamos
            if self.apuesta["existencias"] == 0:
                # Primera apuesta de la ronda
                try:
                    self.validador_apuesta.set_apuesta(
                        nueva_cantidad,
                        nuevo_numero,
                        jugador_un_dado=(self.cachos[self.turno].get_cantidad() == 1)
                    )
                    return {"accion": "apostar", "cantidad": nueva_cantidad, "pinta": nuevo_numero}
                except ValueError as e:
                    print(f"Apuesta inválida: {e}. Intente de nuevo.")
                    sleep(2)
                    continue
            else:
                # Subir o bajar la apuesta
                # Usar los métodos validar_subida y validar_bajada
                valida_subida = self.validador_apuesta.validar_subida(nueva_cantidad, nuevo_numero)
                valida_bajada = self.validador_apuesta.validar_bajada(nueva_cantidad, nuevo_numero)
                
                if valida_subida or valida_bajada:
                    self.validador_apuesta.set_apuesta(
                        nueva_cantidad,
                        nuevo_numero,
                        jugador_un_dado=(self.cachos[self.turno].get_cantidad() == 1)
                    )
                    return {"accion": "apostar", "cantidad": nueva_cantidad, "pinta": nuevo_numero}
                else:
                    print("Apuesta inválida. No es una subida o bajada permitida.")
                    sleep(2)
                    continue

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
                    
                # Decidir qué opciones se muestran
                if self.apuesta["existencias"] == 0:
                    print("1. Apostar / 2. Ver Dados")
                else:
                    print("1. Apostar / 2. Dudar / 3. Calzar / 4. Pasar / 5. Ver Dados")
                
                accion = input("Accion: ").lower().strip()

                if accion in ["apostar", "1"]:
                    nueva_apuesta = self.preguntar_apuesta() 
                    if "cantidad" in nueva_apuesta and "pinta" in nueva_apuesta:
                        self.apuesta["existencias"] = nueva_apuesta["cantidad"]
                        self.apuesta["pinta"] = nueva_apuesta["pinta"]
                    # No salimos del bucle, solo actualizamos la apuesta y continuamos el turno
                    self.turno = (self.turno + 1) % self.numero_jugadores

                elif accion in ["dudar", "2"]:
                    if self.apuesta["existencias"] == 0:
                        print("Aún no se ha hecho ninguna apuesta. Acción inválida.")
                        sleep(2)
                        continue
                    
                    if self.pasar_flag == False:
                        resultado = ArbitroRonda.dudar(self.apuesta, self.cachos, self.turno)

                        if resultado:
                            print(f"Éxito. {self.cachos[(self.turno - 1)%self.numero_jugadores].nombre} pierde un dado.")
                            self.turno = (self.turno - 1) % self.numero_jugadores
                        else:
                            print(f"Fallo. {self.cachos[self.turno].nombre} pierde un dado.")
                        
                        sleep(3)
                        break
                    else:
                        print("Se dudó un pase. Se comienza la siguiente ronda.")
                        sleep(3)
                        break

                elif accion in ["calzar", "3"]:
                    if self.apuesta["existencias"] == 0:
                        print("Aún no se ha hecho ninguna apuesta. Acción inválida.")
                        sleep(2)
                        continue
                    
                    jugando = False
                    resultado = ArbitroRonda.calzar(self.apuesta, self.cachos, self.turno)

                    if resultado:
                        print(f"Éxito. {self.cachos[self.turno].nombre} gana un dado.")
                    else:
                        print(f"Fallo. {self.cachos[self.turno].nombre} pierde un dado.")
                    
                    sleep(3)
                    break

                elif accion in ["pasar", "4"]:
                    if not ContadorPintas.es_full(self.cachos[self.turno].ver_dados()):
                        print("Jugador no cumple condiciones para pasar de turno.")
                        sleep(2)
                        continue
                    self.pasar_flag = True
                    sleep(3)
                    self.turno = (self.turno + 1) % self.numero_jugadores

                elif accion in ["ver dados", "5"]:
                    self.mostrar_dados()
                    continue
                
                else:
                    print("Acción inválida. Por favor, elige una de las siguientes opciones.")
                    sleep(2)
                    continue
                
                # Pasar al siguiente jugador si la ronda no terminó
                if accion not in ["dudar", "calzar"]:
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

        print("Fin del juego.")

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
