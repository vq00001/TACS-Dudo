import pytest
from validador_apuesta import ValidadorApuesta

def test_set_get_apuesta_valida():
    val = ValidadorApuesta()
    val.set_apuesta(3, 5)
    cantidad, numero = val.get_apuesta()
    assert cantidad == 3
    assert numero == 5

def test_set_apuesta_invalida_cantidad():
    val = ValidadorApuesta()
    with pytest.raises(ValueError):
        val.set_apuesta(-2, 4)  # cantidad negativa no válida

def test_set_apuesta_invalida_numero():
    val = ValidadorApuesta()
    with pytest.raises(ValueError):
        val.set_apuesta(2, 7)  # número fuera de rango

def test_get_apuesta_sin_definir():
    val = ValidadorApuesta()
    with pytest.raises(ValueError):
        val.get_apuesta()  # todavía no se ha definido ninguna apuesta