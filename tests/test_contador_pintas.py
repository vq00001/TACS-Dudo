from juego.contador_pintas import ContadorPintas

def test_contar_sin_ases():
    dados = [2, 3, 4, 5, 6]
    contador = ContadorPintas()
    assert contador.contar(dados, 2) == 1
    assert contador.contar(dados, 3) == 1
    assert contador.contar(dados, 1) == 0  # sin ases

def test_contar_valores_repetidos():
    dados = [2, 2, 3, 3, 3]
    contador = ContadorPintas()
    assert contador.contar(dados, 2) == 2
    assert contador.contar(dados, 3) == 3
    assert contador.contar(dados, 4) == 0

def test_contar_sin_repetidos():
    dados = [2, 3, 4, 5, 6]
    contador = ContadorPintas()
    assert contador.contar(dados, 2) == 1
    assert contador.contar(dados, 3) == 1
    assert contador.contar(dados, 4) == 1
    assert contador.contar(dados, 5) == 1
    assert contador.contar(dados, 6) == 1

def test_contar_todas_pintas_distintas():
    dados = [1, 2, 3, 4, 5]
    contador = ContadorPintas()
    for i in range(1, 6):
        assert contador.contar(dados, i) == 1

def test_contar_todas_pintas_iguales():
    dados = [3, 3, 3, 3, 3]
    contador = ContadorPintas()
    assert contador.contar(dados, 3) == 5
    assert contador.contar(dados, 2) == 0  # sin ases

