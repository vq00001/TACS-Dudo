# REQUISITOS:
# Administre múltiples jugadores y sus dados
# Determine quién inicia cada ronda
# Maneje el flujo de turnos
# Detecte cuándo alguien queda con un dado (para activar reglas especiales)


import pytest
from src.juego.gestor_partida import *
from src.servicios.excepciones import EstadoJuegoInvalido
import random

jugadores = 4

def test_preguntar_accion(mocker):
    gp = GestorPartida(3)
    
    # Setup mock cachos
    for i in range(3):
        mock_cacho = mocker.Mock()
        mock_cacho.get_cantidad.return_value = 5
        gp.cachos.append(mock_cacho)
    
    # evitar efectos secundarios
    mocker.patch('src.juego.gestor_partida.os.system')
    mocker.patch('time.sleep')
    mocker.patch('builtins.print')
    
    mock_input = mocker.patch('builtins.input', side_effect=["otro","ap", "apuesta"])
    
    gp.preguntar_accion()
    
    assert mock_input.call_count == 3


@pytest.mark.parametrize("nombre_cachos, valor_dados, direccion, orden_final", [
    (["a", "b", "c", "d"], [1,2,3,4], "izquierda", ["d", "c", "b", "a"]),       # izquierda
    (["a", "b", "c", "d"], [6,5,3,4], "derecha", ["a", "b", "c", "d"]),         # derecha
    # (["a", "b", "c", "d"], [3,1,5,3], "derecha", ["c", "d", "a", "b"]),         # numero no mayor repetido
    # (["a", "b", "c", "d"], [2,4,4,1,3,2], "izquierda", ["b", "a", "d", "c"]),   # numero mayor repetido
    # (["a", "b", "c", "d"], [4,4,4,1,3,2,1], "izquierda", ["b", "a", "d", "c"]), # mas de un numero mayor repetido
] )
def test_decidir_turnos(mocker, nombre_cachos, valor_dados, direccion, orden_final):
    
    gp = GestorPartida(jugadores)

    for i in range(len(nombre_cachos)): 
        cacho = mocker.Mock()
        gp.cachos.append(cacho)

    mocker.patch('builtins.input', side_effect=nombre_cachos) # preguntar los nombres de los jugadores
    mocker.patch('random.randint', side_effect=valor_dados)  # tirar un dado por jugador
    mocker.patch('builtin.input', side_effect=direccion)     # preguntar al ganador la direccion del juego

    # retorna el cacho del primer jugador
    primer_jugador = gp.decidir_turnos()
    assert  primer_jugador.nombre() == orden_final[0]
    
    # verifica que el orden del resto de jugadores sea correcto
    for i in range(len(nombre_cachos)):
        assert gp.cachos[i].nombre == orden_final[i]
    
@pytest.mark.parametrize("cachos, resultado", [
    ([[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]], False),
    ([[1],[1,2],[],[]], False),
    ([[],[],[1],[]], True),
    ([[1],[2]], False),
    ([[],[5]], True)
] )
def test_validar_fin_juego(mocker, cachos, resultado):
    gp = GestorPartida(len(cachos))

    for i in range(len(cachos)):
        mock_cacho = mocker.Mock()
        mock_cacho.ver_dados.return_value = cachos[i]
        gp.cachos.append(mock_cacho)

    assert gp.validar_fin_juego() == resultado

