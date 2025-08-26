from juego.contador_pintas import ContadorPintas

#-------------------------------------------------------------------------------------------
#casos comunes

def test_contar_sin_ases():
    dados = [2, 3, 4, 5, 6]
    contador = ContadorPintas()
    assert contador.contar_sin_comodines(dados, 2) == 1
    assert contador.contar_sin_comodines(dados, 3) == 1
    assert contador.contar_sin_comodines(dados, 1) == 0  # sin ases

def test_contar_valores_repetidos():
    dados = [2, 2, 3, 3, 3]
    contador = ContadorPintas()
    assert contador.contar_sin_comodines(dados, 2) == 2
    assert contador.contar_sin_comodines(dados, 3) == 3
    assert contador.contar_sin_comodines(dados, 4) == 0

def test_contar_sin_repetidos():
    dados = [2, 3, 4, 5, 6]
    contador = ContadorPintas()
    for numero in dados:
        assert contador.contar_sin_comodines(dados, numero) == 1

def test_contar_todas_pintas_distintas_sin_considerar_ases():
    dados = [1, 2, 3, 4, 5]
    contador = ContadorPintas()
    for i in range(1, 6):
        assert contador.contar_sin_comodines(dados, i) == 1

def test_contar_todas_pintas_iguales_sin_conciderar_ases():
    dados = [3, 3, 3, 3, 3]
    contador = ContadorPintas()
    assert contador.contar_sin_comodines(dados, 3) == 5
    assert contador.contar_sin_comodines(dados, 2) == 0  # sin ases

#-------------------------------------------------------------------------------------------
#casos con ases

def test_un_solo_as():
    dados = [1, 3, 5, 2, 6]
    contador = ContadorPintas()
    assert contador.contar_con_comodines(dados, 3) == 2 #apostando a 3 debe sumar el 3 real + el As comodín


def test_ases_comodines_varios():
    dados = [1, 1, 4, 6, 2]
    contador = ContadorPintas()
    assert contador.contar_con_comodines(dados, 4) == 3  # apostando a 4 -> 1 (real) + 2 (ases) = 3
    assert contador.contar_con_comodines(dados, 2) == 3  # apostando a 2 -> 1 (real) + 2 (ases) = 3


def test_as_no_comodin_en_ronda_de_un_dado():
    # Caso donde jugador de un dado acepta ronda especial y el As NO es comodín esa ronda
    dados = [1]
    contador = ContadorPintas()
    assert contador.contar_sin_comodines(dados, 5) == 0  # si apuesto a 5 -> 0
    assert contador.contar_sin_comodines(dados, 1) == 1  # si apuesto a 1 -> 1


def test_todos_ases():
    dados = [1, 1, 1, 1, 1]
    contador = ContadorPintas()
    assert contador.contar_con_comodines(dados, 6) == 5  # apostando a 6 -> todos los Ases cuentan como comodín -> 5
    assert contador.contar_con_comodines(dados, 1) == 5   # apostando a 1 -> también 5 (As cuenta como sí mismo y comodín)

def test_contar_pintas_numero_no_en_dados_con_ases():
    # Caso donde el numero al que se apostó no aparece niuna vez pero hay Ases que sirven de comodin
    dados = [1, 6, 1, 2, 3]  # el número 5 NO está
    contador = ContadorPintas()
    apuesta = 5
    resultado = contador.contar_con_comodines(dados, apuesta)
    # Como hay 2 ases, deberían contarse como 2 pintas de "5"
    assert resultado == 2

#-------------------------------------------------------------------------------------------
#casos borde

def test_lista_vacia():
    dados = []
    contador = ContadorPintas()
    assert contador.contar_sin_comodines(dados, 3) == 0
    assert contador.contar_con_comodines(dados, 3) == 0

def test_numero_no_aparece():
    dados = [2, 4, 5, 6, 1]
    contador = ContadorPintas()
    assert contador.contar_sin_comodines(dados, 3) == 0
    # Con comodines (1 es comodín)
    assert contador.contar_con_comodines(dados, 3) == 1

def test_todos_dados_iguales():
    dados = [4, 4, 4, 4, 4]
    contador = ContadorPintas()
    assert contador.contar_sin_comodines(dados, 4) == 5
    assert contador.contar_con_comodines(dados, 4) == 5

    dados_as = [1, 1, 1, 1, 1]
    assert contador.contar_sin_comodines(dados_as, 1) == 5
    assert contador.contar_con_comodines(dados_as, 2) == 5  # todos los ases cuentan como comodines

def test_full_especial():
    # caso especial del "FULL", cuando el jugador aun tiene los 5 dados y obtiene un trio de pintas iguales y las otras dos restantes tienen igual pinta entre ellas 
    dados = [3, 3, 3, 4, 4]
    contador = ContadorPintas()
    # Apostando a 3
    assert contador.contar_con_comodines(dados, 3) == 3
    # Apostando a 4
    assert contador.contar_con_comodines(dados, 4) == 2

def test_invalido_numero_cero():
    dados = [1, 2, 3, 4, 5]
    contador = ContadorPintas()
    assert contador.contar_sin_comodines(dados, 0) == 0
    assert contador.contar_con_comodines(dados, 0) == 1  

def test_invalido_numero_negativo():
    dados = [1, 2, 3, 4, 5]
    contador = ContadorPintas()
    assert contador.contar_sin_comodines(dados, -1) == 0
    assert contador.contar_con_comodines(dados, -1) == 1

def test_invalido_numero_mayor_6():
    dados = [1, 2, 3, 4, 5]
    contador = ContadorPintas()
    assert contador.contar_sin_comodines(dados, 7) == 0
    assert contador.contar_con_comodines(dados, 7) == 1
    