from juego.contador_pintas import ContadorPintas

def test_contar_pintas_sin_ases():
    dados = [[2, 3], [4, 2]]  # total de dos "2"
    contador = ContadorPintas()
    assert contador.contar(dados, 2) == 2
