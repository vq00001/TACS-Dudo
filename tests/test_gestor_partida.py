# REQUISITOS:
# Administre múltiples jugadores y sus dados
# Determine quién inicia cada ronda
# Maneje el flujo de turnos
# Detecte cuándo alguien queda con un dado (para activar reglas especiales)


import pytest
from unittest.mock import MagicMock
from src.juego.gestor_partida import *
from src.servicios.excepciones import EstadoJuegoInvalido
import random

jugadores = 4

def test_preguntar_apuesta_simple(mocker):
    
    gp = GestorPartida(3, debug=True)
    gp.apuesta = {"existencias": 0, "pinta": 0}

    # Mockear las funciones de la consola
    mocker.patch('src.juego.gestor_partida.borrar_lineas', MagicMock())
    mocker.patch('src.juego.gestor_partida.os.system', MagicMock())
    mocker.patch('builtins.print', MagicMock())
    mocker.patch('time.sleep', MagicMock())

    mock_input = mocker.patch('builtins.input', side_effect=['3 4']) #simular

    # 3. Llamar al método a probar
    resultado = gp.preguntar_apuesta() #llamar al metodo a probar

    assert resultado == {"accion": "apostar", "cantidad": 3, "pinta": 4} #esperar resultados
    assert mock_input.call_count == 1 #esperar que se llame al input una vez


@pytest.mark.parametrize("nombre_cachos, valor_dados, direccion, orden_final", [
    (["a", "b", "c", "d"], [1,2,3,4], "izquierda", ["d", "c", "b", "a"]),
    (["a", "b", "c", "d"], [6,5,3,4], "derecha", ["a", "b", "c", "d"])
    # ... otros casos de prueba
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


def test_obligar(mocker):
    
    gp = GestorPartida(2, True)
    gp.cachos.clear()

    # Mock cacho con un solo dado y primer_unico_dado en True
    mock_cacho = mocker.Mock()
    mock_cacho.get_cantidad.return_value = 1
    mock_cacho.primer_unico_dado = True
    gp.cachos.append(mock_cacho)

    # Otro cacho cualquiera
    otro_cacho = mocker.Mock()
    otro_cacho.get_cantidad.return_value = 5
    otro_cacho.primer_unico_dado = False
    gp.cachos.append(otro_cacho)

    gp.turno = 0

    # Simular input para elegir ronda abierta
    mocker.patch('builtins.input', side_effect=["1"])
    mocker.patch('src.juego.gestor_partida.borrar_lineas')
    mocker.patch('builtins.print')
    mocker.patch('time.sleep')

    gp.obligar()

    assert gp.tipo_ronda == "abierta"
    assert gp.jugador_que_obliga == 0
    assert mock_cacho.primer_unico_dado is False

    # simular ronda cerrada
    mock_cacho.primer_unico_dado = True                      # resetear primer unico dado
    gp.tipo_ronda = "normal"                                 # resetear tipo de ronda
    gp.jugador_que_obliga = -1
    mocker.patch('builtins.input', side_effect=["2"])

    gp.obligar()
    assert gp.tipo_ronda == "cerrada"
    assert gp.jugador_que_obliga == 0
    assert mock_cacho.primer_unico_dado is False

    # simular ronda normal
    mock_cacho.primer_unico_dado = True
    gp.tipo_ronda = "cerrada"
    gp.jugador_que_obliga = -1
    mocker.patch('builtins.input', side_effect=["3"])

    gp.obligar()
    assert gp.tipo_ronda == "normal"
    assert gp.jugador_que_obliga == -1

