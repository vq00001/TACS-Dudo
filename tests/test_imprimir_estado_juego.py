import pytest
from src.servicios import imprimir_estado_juego

class MockCacho:
    def __init__(self, nombre, dados):
        self.nombre = nombre
        self._dados = dados
    def ver_dados(self):
        return self._dados

class MockGestorPartida:
    def __init__(self, cachos, turno=0, tipo_ronda="normal", jugador_que_obliga=0):
        self.cachos = cachos
        self.turno = turno
        self.tipo_ronda = tipo_ronda
        self.jugador_que_obliga = jugador_que_obliga

@pytest.fixture
def cachos():
    return [
        MockCacho("Ana", [1,2,3]),
        MockCacho("Luis", [4,5,6])
    ]

def test_mostrar_dados_normal(capsys, cachos, mocker):
    mocker.patch('builtins.input', return_value="") 
    gp = MockGestorPartida(cachos, turno=0, tipo_ronda="normal")
    imprimir_estado_juego.mostrar_dados(gp)
    out = capsys.readouterr().out
    assert "mostrando dados de Ana" in out
    assert str(cachos[0].ver_dados()) in out

def test_mostrar_dados_abierta(capsys, cachos, mocker):
    mocker.patch('builtins.input', return_value="") 
    gp = MockGestorPartida(cachos, turno=0, tipo_ronda="abierta")
    imprimir_estado_juego.mostrar_dados(gp)
    out = capsys.readouterr().out
    assert "mostrando dados de todos menos Ana" in out
    assert "Luis: [4, 5, 6]" in out

def test_mostrar_dados_cerrada_obliga(capsys, cachos, mocker):
    mocker.patch('builtins.input', return_value="") 
    gp = MockGestorPartida(cachos, turno=1, tipo_ronda="cerrada", jugador_que_obliga=1)
    imprimir_estado_juego.mostrar_dados(gp)
    out = capsys.readouterr().out
    assert "mostrando dados de Luis" in out
    assert str(cachos[1].ver_dados()) in out

def test_mostrar_dados_cerrada_no_obliga(capsys, cachos, mocker):
    mocker.patch('builtins.input', return_value="") 
    gp = MockGestorPartida(cachos, turno=0, tipo_ronda="cerrada", jugador_que_obliga=1)
    imprimir_estado_juego.mostrar_dados(gp)
    out = capsys.readouterr().out
    assert "solo Luis puede ver sus dados" in out