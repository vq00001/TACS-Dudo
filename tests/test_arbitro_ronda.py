# Árbitro del Juego
# Implementa una clase ArbitroRonda que:
# Determine el resultado cuando un jugador "duda"
# Maneje la lógica de "calzar" (debe ser exacto)
# Decida quién pierde/gana un dado
# Valide las condiciones para "calzar" (mitad de dados en juego O jugador con un dado)
import pytest

from src.juego.arbitro_ronda import *
from src.servicios.excepciones import CalzadoInvalido

@pytest.mark.parametrize("val_dados_cachos, resultado", [
    ([[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]], [0,3,3,3,3,3,0]),
    ([[1,6,6,6,5],[1,4,5],[1,1,3,3,5]], [0,4,0,2,1,3,3])
])
def test_contar_repeticiones_dados(mocker, val_dados_cachos, resultado):
    cachos = []
    for dados in val_dados_cachos:
        mock_cacho = mocker.Mock()
        mock_cacho.ver_dados.return_value = dados
        cachos.append(mock_cacho)
    
    assert ArbitroRonda.contar_repeticiones_dados(cachos) == resultado

# val_dados_cachos: valores de retorno de ver_dados() para cada cacho
# apuesta_arr: existencias, pinta
# resultado: return de funcion, dados en jugador de turno, dados en jugador que puso la apuesta.
@pytest.mark.parametrize("val_dados_cachos, apuesta_arr, turno, resultado", [
    ([[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]], [1,2], 0, [False, 4, 5] ), # duda es incorrecta, hay mas apariciones que las propuestas en la apuesta
    ([[1,3,4],[1,3,4,5],[1,2,3,4,5]], [5,2], 1, [True, 4, 2] ),    # duda es correcta, hay menos apariciones que las propuestas en la apuesta. 
    ([[1,2,3,4],[1],[1,2,3,4]], [4,1], 2, [True, 4, 0] ),    # duda es correcta, Ases no actuan como comodines.
])
def test_dudar(mocker, val_dados_cachos, apuesta_arr, turno, resultado):

    def make_side_effect_sacar_dado(mock_cacho):
        def side_effect():
            current_dados = mock_cacho.ver_dados.return_value
            if len(current_dados) > 0:
                mock_cacho.ver_dados.return_value = current_dados[:-1]  # Remueve el último

        return side_effect
        

    cachos = [] # mockear
    for dados in val_dados_cachos:
        mock_cacho = mocker.Mock()
        mock_cacho.ver_dados.return_value = dados
        mock_cacho.get_dados_extra.return_value = 0
        mock_cacho.sacar_dado.side_effect = make_side_effect_sacar_dado(mock_cacho)
        cachos.append(mock_cacho)

    ####################################

    apuesta = {
        "existencias": apuesta_arr[0],
        "pinta": apuesta_arr[1]
    }
    
    assert ArbitroRonda.dudar(apuesta, cachos, turno) == resultado[0]
    assert len(cachos[turno].ver_dados()) == resultado[1]
    assert len(cachos[(turno - 1) % 3].ver_dados()) == resultado[2]

    

# Si el número de apariciones es exactamente el mismo la persona que calzó gana un dado, lo contrario pierde un dado. 
# Limitación: solo se puede calzar cuando este la mitad o mas de los dados en juego, o cuando el jugador que desea calzar tenga solo un dado. 
def test_calzar(mocker):

    def make_side_effect_sacar_dado(mock_cacho):
        def side_effect():
            dados_actuales = mock_cacho.ver_dados.return_value
            if mock_cacho.get_dados_extra.return_value > 0:
                mock_cacho.get_dados_extra.return_value -= 1
            elif len(dados_actuales) > 0:
                mock_cacho.ver_dados.return_value = dados_actuales[:-1]  # Remueve el último
        return side_effect

    def make_side_effect_agregar_dado(mock_cacho):
        def side_effect():
            dados_actuales = mock_cacho.ver_dados.return_value

            if len(dados_actuales) >= 5: 
                current_extra = mock_cacho.get_dados_extra.return_value
                mock_cacho.get_dados_extra.return_value = current_extra + 1  # Incrementa dados extra
            else:
                mock_cacho.ver_dados.return_value = dados_actuales.append(6)  # Agrega un dado (ej: valor 6)
        
        return side_effect

    
    cachos = [] # mockear

    for i in range(3):
        mock_cacho = mocker.Mock()
        mock_cacho.ver_dados.return_value = [1, 2, 3, 4, 5]
        mock_cacho.get_dados_extra.return_value = 0
        mock_cacho.sacar_dado.side_effect = make_side_effect_sacar_dado(mock_cacho)
        mock_cacho.agregar_dado.side_effect = make_side_effect_agregar_dado(mock_cacho)
        cachos.append(mock_cacho)

    ######################################

    # calzar es correcto. 
    # jugador gana un dado a favor.

    apuesta = {
        "existencias": 6,
        "pinta": 3
    }

    turno = 0
    
    assert ArbitroRonda.calzar(apuesta, cachos, turno) == True
    assert len(cachos[turno].ver_dados()) == 5
    assert cachos[turno].get_dados_extra() == 1

    ######################################

    # calzar es incorrecto. (Menor cantidad de dados)
    # jugador pierde un dado.

    apuesta = {
        "existencias": 2,
        "pinta": 5
    }

    turno = 1
    
    assert ArbitroRonda.calzar(apuesta, cachos, turno) == False
    assert len(cachos[turno].ver_dados()) == 4
    assert cachos[turno].get_dados_extra() == 0

    ######################################

    # calzar es incorrecto. (Mayor cantidad de dados)
    # jugador pierde un dado a favor.

    apuesta = {
        "existencias": 8,
        "pinta": 4
    }

    turno = 0
    
    assert ArbitroRonda.calzar(apuesta, cachos, turno) == False
    assert len(cachos[turno].ver_dados()) == 5
    assert len(cachos[turno].ver_dados()) == 5
    assert cachos[turno].get_dados_extra() == 0

    ######################################

    # calzar es correcto. (Menos de la mitad de dados en juego)
    # jugador tiene un solo dado.

    apuesta = {
        "existencias": 2,
        "pinta": 2
    }

    turno = 0
    
    assert ArbitroRonda.calzar(apuesta, cachos, turno) == True
    assert len(cachos[turno].ver_dados()) == 2
    assert cachos[turno].get_dados_extra() == 0


def test_calzar_excepcion(mocker):
    # calzar es incorrecto. (Menos de la mitad de dados en juego)
    # Se alza excepcion.
    cachos = []
    cachos.clear() # resetear cachos

    mock_cacho_0 = mocker.Mock()
    mock_cacho_0.dados.return_value = [1, 2]
    cachos.append(mock_cacho_0)

    mock_cacho_1 = mocker.Mock()
    mock_cacho_1.dados.return_value = [2, 3]
    cachos.append(mock_cacho_1)

    mock_cacho_2 = mocker.Mock()
    mock_cacho_2.dados.return_value = [4]
    cachos.append(mock_cacho_2)


    apuesta = {
        "existencias": 5,
        "pinta": 4
    }

    turno = 0

    with pytest.raises(CalzadoInvalido):
        assert ArbitroRonda.calzar(apuesta, cachos, turno) == False


