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

#-------------------------------------------------------------------------------------------
#subir apuesta (numero=pinta)

def test_subir_apuesta_cantidad_mayor():
    val = ValidadorApuesta()
    val.set_apuesta(2, 3)
    nueva_cantidad, nuevo_numero = 3, 3  # intento subir cantidad (2 trenes->3 trenes, deberia ser valido)
    assert val.validar_subida(nueva_cantidad, nuevo_numero) 

def test_subir_apuesta_mismo_numero():
    val = ValidadorApuesta()
    val.set_apuesta(2, 3)
    nueva_cantidad, nuevo_numero = 2, 4  # intento subir número manteniendo cantidad (2 trenes->2 cuartos, deberia ser valido)
    assert val.validar_subida(nueva_cantidad, nuevo_numero)  

def test_subir_apuesta_tanto_numero_como_cantidad():
    val = ValidadorApuesta()
    val.set_apuesta(2, 3)
    nueva_cantidad, nuevo_numero = 3, 4  # intento subir ambos
    assert val.validar_subida(nueva_cantidad, nuevo_numero) 

#casos invalidos
def test_subir_apuesta_invalida_numero_menor():
    val = ValidadorApuesta()
    val.set_apuesta(3, 4)
    nueva_cantidad, nuevo_numero = 4, 3  # aumento cantidad pero bajo el número -> invalido
    assert not val.validar_subida(nueva_cantidad, nuevo_numero) #espero un FALSE

def test_subir_apuesta_invalida_cantidad_menor():
    val = ValidadorApuesta()
    val.set_apuesta(3, 4)
    nueva_cantidad, nuevo_numero = 2, 5  # disminuyo cantidad -> invalido
    assert not val.validar_subida(nueva_cantidad, nuevo_numero) #espero un FALSE

def test_subir_apuesta_sin_apuesta_previa():
    val = ValidadorApuesta()
    nueva_cantidad, nuevo_numero = 2, 3
    assert not val.validar_subida(nueva_cantidad, nuevo_numero) # no hay apuesta previa->espero un FALSE

#-------------------------------------------------------------------------------------------
#apuestas con ases

def test_primera_apuesta_no_puede_ser_as_si_tiene_mas_de_un_dado():
    val = ValidadorApuesta()
    # intento de apuesta inicial con 1(As) cuando el jugador tiene mas de un dado
    try:
        val.set_apuesta(cantidad=2, numero=1, jugador_un_dado=False)
        assert False, "Espero un ValueError"
    except ValueError as e:
        assert "La primera apuesta de la ronda no puede ser con Ases" in str(e)
        assert val._primera is True, "El estado de _primera no debe cambiar en un error"

def test_primera_apuesta_puede_ser_as_si_tiene_un_dado():
    val = ValidadorApuesta()
    
    # apuesta inicial con 1(As) cuando el jugador efectivamente tiene un unico dado
    val.set_apuesta(cantidad=2, numero=1, jugador_un_dado=True)
    assert val.get_apuesta() == (2, 1)

def test_subida_apostando_a_ases_aumentando_cantidad():
    val = ValidadorApuesta()
    val.set_apuesta(cantidad=2, numero=1, jugador_un_dado=True)
    nueva_cantidad, nuevo_numero = 3, 1 # aumento la cantidad pero mantengo la pinta=1
    assert val.validar_subida(nueva_cantidad, nuevo_numero) is True #valido
    
    nueva_cantidad_invalida, nuevo_numero_invalido = 2, 1
    assert val.validar_subida(nueva_cantidad_invalida, nuevo_numero_invalido) is False #invalido

def test_subida_de_uno_a_otro_numero_debe_ser_doble_mas_uno():
    val = ValidadorApuesta()
    val.set_apuesta(cantidad=3, numero=1, jugador_un_dado=True)
    
    # la nueva cantidad debe ser (3 * 2) + 1 = 7 o más
    nueva_cantidad, nuevo_numero = 7, 2
    assert val.validar_subida(nueva_cantidad, nuevo_numero) is True
    
    # un caso es inválido, ya que la cantidad es menor a 7
    nueva_cantidad_invalida, nuevo_numero_invalido = 6, 2
    assert val.validar_subida(nueva_cantidad_invalida, nuevo_numero_invalido) is False