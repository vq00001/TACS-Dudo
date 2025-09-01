
from src.juego.gestor_partida import GestorPartida

if __name__ == "__main__":
    jugadores = input("Cantidad de jugadores: ")
    gp = GestorPartida(int(jugadores))
    gp.loop_juego()