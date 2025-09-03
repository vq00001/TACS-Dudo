
import os
from time import sleep
from src.juego.arbitro_ronda import ArbitroRonda
from src.juego.gestor_partida import GestorPartida
from src.servicios.imprimir_estado_juego import * 

if __name__ == "__main__":
    jugadores = input("Cantidad de jugadores: ")
    gp = GestorPartida(int(jugadores))
    os.system('cls')
    gp.decidir_turnos()
    
    os.system('cls')
    print("\nINICIO JUEGO\n")
    sleep(2)

    while(not gp.validar_fin_juego()):
        
        # reiniciar la apuesta
        gp.apuesta = {
            "existencias": 0,
            "pinta": 0
        } 

        # tirar los dados de todos los jugadores
        for cacho in gp.cachos:
            cacho.tirar_dados()

        ronda = True
        while(ronda):
            os.system('cls')

            # imprimir estado juego
            imprimir_pantalla_juego(gp)

            # Preguntar si se quiere jugar ronda obligatoria si se cumplen las condiciones
            
            gp.obligar()
                
            # Preguntar por la accion del turno (apostar, calzar, dudar, pasar)
            accion = gp.preguntar_accion()

            if (accion == "apostar"):
                gp.apuesta = gp.preguntar_apuesta()

            elif (accion == "dudar"):
                if gp.pasar_flag == False: 

                    resultado = ArbitroRonda.dudar(gp.apuesta, gp.cachos, gp.turno) 

                    # imprimir resultado
                    if resultado:
                        print(f"exito. {gp.cachos[(gp.turno - 1)%gp.numero_jugadores].nombre} pierde un dado.")

                        # en la siguiente ronda parte el jugador que perdio un dado
                        gp.turno = (gp.turno - 1) % gp.numero_jugadores  

                    else:
                        print(f"fallo. {gp.cachos[gp.turno].nombre} pierde un dado.")

                    sleep(3)
                    break
                    
                else:  # si se duda un "pase" se termina la ronda sin perdidas ni ganancias 
                    print("se dudo un pase. se comienza la siguiente ronda.")
                    sleep(3)
                    break

            elif (accion == "calzar"):
                jugando = False
                resultado = ArbitroRonda.calzar(gp.apuesta, gp.cachos, gp.turno) 

                # imprimir resultado
                if resultado:
                    print(f"exito. {gp.cachos[gp.turno].nombre} gana un dado.")
                else:
                    print(f"fallo. {gp.cachos[gp.turno].nombre} pierde un dado.")
                sleep(3)
                break

            elif (accion == "pasar"):
                gp.pasar_flag = True
                sleep(3)
            else:
                # si no coincide ninguna acción, volver a repetir el turno
                continue
            
            # una vez termino el turno, se pasa al siguiente jugador
            gp.turno = (gp.turno + 1) % gp.numero_jugadores

        # resetear el tipo de ronda y el jugador que obliga
        gp.tipo_ronda = "normal"
        gp.jugador_que_obliga = -1

    # imprimir el ganador
    os.system("cls")
    imprimir_pantalla_juego(gp)
    for cacho in gp.cachos:
        if cacho.get_cantidad() > 0:
            print(f"¡HA GANADO {gp.cachos[gp.turno].nombre}!")
            break

    print("fin del juego.")
