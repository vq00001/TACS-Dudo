import pytest
from juego.validador_apuesta import ValidadorApuesta, Apuesta, ApuestaInvalidaError

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
    validador = ValidadorApuesta(primera_apuesta_ronda=True)
    apuesta = Apuesta(cantidad=3, numero=1)

    with pytest.raises(ApuestaInvalidaError, match="La primera apuesta no puede ser al número 1"):
        validador.validar(apuesta, dados_jugador=5)


def test_primera_apuesta_puede_ser_as_si_tiene_un_dado():
    validador = ValidadorApuesta(primera_apuesta_ronda=True)
    apuesta = Apuesta(cantidad=1, numero=1)
    validador.validar(apuesta, dados_jugador=1)  #si tiene 1 dado deberia poder empezar la ronda con ases (caso ronda cerrada o abierta)


def test_subida_apostando_a_uno_aumentando_cantidad():
    validador = ValidadorApuesta(primera_apuesta_ronda=False)
    apuesta_anterior = Apuesta(cantidad=2, numero=1)
    apuesta_nueva = Apuesta(cantidad=3, numero=1)
    # intento aumentar la cantidad pero sigo manteniendo la pinta as -> deberia ser valido
    validador.validar_subida(apuesta_anterior, apuesta_nueva)


def test_subida_de_uno_a_otro_numero_debe_ser_doble_mas_uno():
    validador = ValidadorApuesta(primera_apuesta_ronda=False)
    apuesta_anterior = Apuesta(cantidad=2, numero=1)
    apuesta_invalida = Apuesta(cantidad=4, numero=5)  # debería fallar (mínimo es 5)
    apuesta_valida = Apuesta(cantidad=5, numero=5)    # debería pasar

    with pytest.raises(ApuestaInvalidaError, match="La cantidad minima al cambiar de 1 es el doble mas uno"):
        validador.validar_subida(apuesta_anterior, apuesta_invalida)

    validador.validar_subida(apuesta_anterior, apuesta_valida)  #espero error