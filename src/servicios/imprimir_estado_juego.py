
from time import sleep
from src.servicios.borrar_lineas import borrar_lineas


def imprimir_pantalla_juego(gp):
    nombres_pintas_singular = ["As", "Tonto", "Tren", "Cuarta", "Quina", "Sexto"]
    nombres_pintas = ["Ases", "Tontos", "Trenes", "Cuartas", "Quinas", "Sextos"]

    if not gp.debug:
        print("_" * 60)

        print(f"{'Jugador':<10} {'Dados':<7} {'A favor':<8}")

        # Filas por jugador
        for cacho in gp.cachos:
            print(f"{cacho.nombre:<10} {cacho.get_cantidad():<7} {cacho.get_dados_extra():<8}")

        print("_" * 60)


        if gp.apuesta["existencias"] > 0 and gp.apuesta["pinta"] > 0:
        # Info de turno y apuesta
            if gp.apuesta["existencias"] > 1:
                print(
                    f"TURNO: {gp.cachos[gp.turno].nombre:<10} "
                    f"APUESTA: {gp.apuesta['existencias']} {nombres_pintas[gp.apuesta['pinta']-1]}"
                )
            else:
                print(
                    f"TURNO: {gp.cachos[gp.turno].nombre:<10} "
                    f"APUESTA: {gp.apuesta['existencias']} {nombres_pintas_singular[gp.apuesta['pinta']-1]}"
                )
        else:
            print(f"TURNO: {gp.cachos[gp.turno].nombre:<10} SIN APUESTA")

        print("_"*60)

# imprimir los dados en los cachos de cada jugador.
def mostrar_dados(gp):
    borrar_lineas(6)

    if gp.tipo_ronda == "normal":

        # en una ronda normal los jugadores pueden ver solo sus propios dadoss
        print(f"mostrando dados de {gp.cachos[gp.turno].nombre}")
        sleep(3)
        print(gp.cachos[gp.turno].ver_dados())
        input("presionar para seguir jugando.")
        borrar_lineas(3)

    elif gp.tipo_ronda == "abierta":

        # si la ronda es abierta todos los jugadores pueden ver los cachos del resto, pero no los suyos.
        print(f"mostrando dados de todos menos {gp.cachos[gp.turno].nombre}.")
        sleep(3)

        for cacho in gp.cachos:
            if cacho != gp.cachos[gp.turno]:
                print(f"{cacho.nombre}: {cacho.ver_dados()}")

        input("presionar para seguir jugando.")
        borrar_lineas(2 + len(gp.cachos))

    elif gp.tipo_ronda == "cerrada":

        # si la ronda es cerrada solo el jugador que obliga puede ver sus propios dados.
        if gp.jugador_que_obliga == gp.turno:
            print(f"mostrando dados de {gp.cachos[gp.turno].nombre}")
            sleep(3)
            print(gp.cachos[gp.turno].ver_dados())
            input("presionar para seguir jugando.")
            borrar_lineas(3)
        else:
            print(f"se esta jugando una ronda cerrada, por lo que solo {gp.cachos[gp.jugador_que_obliga].nombre} puede ver sus dados.")
            sleep(3)
            borrar_lineas(1)