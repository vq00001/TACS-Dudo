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
    gp = GestorPartida(3, True)
    
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

def test_preguntar_apuesta(mocker):
    gp = GestorPartida(3, True)
    
    mocker.patch('src.juego.gestor_partida.os.system')
    mocker.patch('builtins.print')
    mocker.patch('time.sleep')
    
    apuesta_inicial = {"existencias": 2, "pinta": 3}
    
    mock_input = mocker.patch('builtins.input', side_effect=["abc", "invalido", "5", "ases"])
            
    resultado = gp.preguntar_apuesta(apuesta_inicial)
    
    # Verificar que se llamó input las veces esperadas (para existencias y pinta)
    assert mock_input.call_count == 4  # abc, 5, invalido, ases
    
    # Verificar el resultado (con las entradas mockeadas: "5" y "ases")
    assert resultado["existencias"] == 5
    assert resultado["pinta"] == 1



@pytest.mark.parametrize("nombre_cachos, valor_dados, direccion, orden_final", [
    (["a", "b", "c", "d"], [1,2,3,4], "izquierda", ["d", "c", "b", "a"]),       # izquierda
    (["a", "b", "c", "d"], [6,5,3,4], "derecha", ["a", "b", "c", "d"])          # derecha
    # (["a", "b", "c", "d"], [3,1,5,3], "derecha", ["c", "d", "a", "b"]),         # numero no mayor repetido
    # (["a", "b", "c", "d"], [2,4,4,1,3,2], "izquierda", ["b", "a", "d", "c"]),   # numero mayor repetido
    # (["a", "b", "c", "d"], [4,4,4,1,3,2,1], "izquierda", ["b", "a", "d", "c"]), # mas de un numero mayor repetido
])
def test_decidir_turnos(mocker, nombre_cachos, valor_dados, direccion, orden_final):
    jugadores = 4
    gp = GestorPartida(jugadores, True)
    gp.cachos.clear()
    for i in range(len(nombre_cachos)): 
        cacho = mocker.Mock()
        cacho.nombre = nombre_cachos[i]
        gp.cachos.append(cacho)

    mocker.patch('builtins.print')                                                      # eliminar los printss
    mocker.patch('random.randint', side_effect=valor_dados)                             # tirar un dado por jugador
    mocker.patch('builtins.input', side_effect=["", "", "", "", direccion])             # preguntar al ganador la direccion del juego

    # retorna el cacho del primer jugador
    primer_jugador = gp.decidir_turnos()
    assert primer_jugador.nombre == orden_final[0]
    
    # verifica que el orden del resto de jugadores sea correcto
    for i in range(len(nombre_cachos)):
        assert gp.cachos[(gp.turno + i) % jugadores].nombre == orden_final[i]
    
@pytest.mark.parametrize("cantidad_dados, resultado", [
    ([5,5,5,5,5], False),
    ([1,2,0,0], False),
    ([0,0,1,0], True),
    ([1,2], False),
    ([0,1], True)
])
def test_validar_fin_juego(mocker, cantidad_dados, resultado):
    gp = GestorPartida(len(cantidad_dados), True)
    gp.cachos.clear()
    
    for i in range(len(cantidad_dados)):
        mock_cacho = mocker.Mock()
        mock_cacho.get_cantidad.return_value = cantidad_dados[i]
        gp.cachos.append(mock_cacho)

    assert gp.validar_fin_juego() == resultado

