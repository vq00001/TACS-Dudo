# Árbitro del Juego
# Implementa una clase ArbitroRonda que:
# Determine el resultado cuando un jugador "duda"
# Maneje la lógica de "calzar" (debe ser exacto)
# Decida quién pierde/gana un dado
# Valide las condiciones para "calzar" (mitad de dados en juego O jugador con un dado)
import pytest

from src.juego.arbitro_ronda import *

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

def test_dudar(mocker):

    cachos = [] # mockear

    for i in range(3):
        mock_cacho = mocker.Mock()
        mock_cacho.dados.return_value = [1, 2, 3, 4, 5]
        mock_cacho.dados_a_favor.return_value = 0
        cachos.append(mock_cacho)
    
    # dudar devolvera true or false dependiendo si la duda acierta o no.
    # los dados de los cachos serán modificados dentro de la funcion
    
    ####################################

    # duda es incorrecta, hay mas apariciones que las propuestas en la apuesta

    apuesta = {
        "existencias": 1,
        "pinta": 2
    }
    turno = 0
    
    assert ArbitroRonda.dudar(apuesta, cachos, turno) == False

    assert cachos[turno].dados.length() == 4
    assert cachos[(turno - 1) % 3].dados.length() == 5

    #####################################

    # duda es correcta, hay menos apariciones que las propuestas en la apuesta. 
    # se toman en cuenta los Ases, que actuan como comodin. 
    # jugador que puso la apuesta pierde un dado

    apuesta = {
        "existencias": 7,
        "pinta": 4
    }

    turno = 2
    
    assert ArbitroRonda.dudar(apuesta, cachos, turno) == True
    assert cachos[turno].dados.length() == 5 
    assert cachos[turno].dados_a_favor == 1
    assert cachos[(turno - 1) % 3].dados.length() == 4

    ######################################

    # duda es incorrecta, jugador pierde un dado a favor y queda con 5
    # Ases no actuan como comodines, si no como pinta.
    apuesta = {
        "existencias": 3,
        "pinta": 1
    }

    turno = 2
    
    assert ArbitroRonda.dudar(apuesta, cachos, turno) == True
    assert cachos[turno].dados.length() == 5
    assert cachos[turno].dados_a_favor == 0
    assert cachos[(turno - 1) % 3].dados.length() == 4 # mantiene los dados



# Si el número de apariciones es exactamente el mismo la persona que calzó gana un dado, lo contrario pierde un dado. 
# Limitación: solo se puede calzar cuando este la mitad o mas de los dados en juego, o cuando el jugador que desea calzar tenga solo un dado. 
def test_calzar(mocker):

    
    cachos = [] # mockear

    for i in range(3):
        mock_cacho = mocker.Mock()
        mock_cacho.dados.return_value = [1, 2, 3, 4, 5]
        mock_cacho.dados_a_favor.return_value = 0
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
    assert cachos[turno].dados.length() == 5
    assert cachos[turno].dados_a_favor == 1

    ######################################

    # calzar es incorrecto. (Menor cantidad de dados)
    # jugador pierde un dado.

    apuesta = {
        "existencias": 2,
        "pinta": 5
    }

    turno = 1
    
    assert ArbitroRonda.calzar(apuesta, cachos, turno) == False
    assert cachos[turno].dados.length() == 4
    assert cachos[turno].dados_a_favor == 0

    ######################################

    # calzar es incorrecto. (Mayor cantidad de dados)
    # jugador pierde un dado a favor.

    apuesta = {
        "existencias": 8,
        "pinta": 4
    }

    turno = 0
    
    assert ArbitroRonda.calzar(apuesta, cachos, turno) == False
    assert cachos[turno].dados.length() == 5
    assert cachos[turno].dados_a_favor == 0

    ######################################

    # calzar es incorrecto. (Menos de la mitad de dados en juego)
    # Se alza excepcion.

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

    ######################################

    # calzar es correcto. (Menos de la mitad de dados en juego)
    # jugador tiene un solo dado.

    apuesta = {
        "existencias": 2,
        "pinta": 2
    }

    turno = 0
    
    assert ArbitroRonda.calzar(apuesta, cachos, turno) == True
    assert cachos[turno].dados.length() == 2
    assert cachos[turno].dados_a_favor == 0


    


