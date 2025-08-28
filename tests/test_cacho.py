import pytest
import sys
sys.path.append('src/juego')
import cacho

def test_creacion_cacho():
    obj_cacho = cacho.cacho()
    assert len(obj_cacho.dados) == 5

def test_tirar_dados():
    obj_cacho = cacho.cacho()
    dados = obj_cacho.tirar_dados()

    for dado in dados:
        valor = dado.ver()
        assert valor >=1 and valor <= 6 and valor is not None