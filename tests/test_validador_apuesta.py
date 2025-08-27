import pytest
from juego.validador_apuesta import ValidadorApuesta

#-------------------------------------------------------------------------------------------
#casos comunes

def test_set_get_apuesta_valida():
    val = ValidadorApuesta()
    val.set_apuesta(3, 5)
    cantidad, numero = val.get_apuesta()
    assert cantidad == 3
    assert numero == 5
#-------------------------------------------------------------------------------------------
#casos invalidos/erroneos
def test_set_apuesta_invalida_cantidad():
    val = ValidadorApuesta()
    with pytest.raises(ValueError):
        val.set_apuesta(-2, 4)  # cantidad negativa no válida

def test_set_apuesta_invalida_cantidad_cero():
    val = ValidadorApuesta()
    with pytest.raises(ValueError):
        val.set_apuesta(0, 3)  # cantidad 0 no es válida

def test_set_apuesta_invalida_numero_mayor_a_seis():
    val = ValidadorApuesta()
    with pytest.raises(ValueError):
        val.set_apuesta(2, 7)  # numero referente a pinta fuera de rango 

def test_set_apuesta_invalida_numero_cero():
    val = ValidadorApuesta()
    with pytest.raises(ValueError):
        val.set_apuesta(3, 0)  # pinta 0 no existe

def test_set_apuesta_invalida_numero_negativo():
    val = ValidadorApuesta()
    with pytest.raises(ValueError):
        val.set_apuesta(2, -1)

def test_get_apuesta_sin_definir():
    val = ValidadorApuesta()
    with pytest.raises(ValueError):
        val.get_apuesta()  # todavía no se ha definido ninguna apuesta