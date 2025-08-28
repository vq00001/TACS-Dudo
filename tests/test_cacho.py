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

def test_ver_dados():
    obj_cacho = cacho.cacho()
    dados = obj_cacho.tirar_dados()

    for dado in obj_cacho.ver_dados():
        assert dado >=1 and dado <=6 and dado is not None

def test_sacar_dado():
    obj_cacho = cacho.cacho()
    oldlen = len(obj_cacho.dados)
    newlen = len(obj_cacho.sacar_dado())
    assert newlen == oldlen - 1

def test_agregar_dado_caso_5_o_mayor():
    obj_cacho = cacho.cacho()
    oldlen = len(obj_cacho.dados)
    newlen = len(obj_cacho.agregar_dado())
    assert newlen == oldlen
    assert obj_cacho.dados_extra == 1

def test_agregar_dado_caso_menor_que_5():
    obj_cacho = cacho.cacho()
    oldlen = len(obj_cacho.sacar_dado())
    newlen = len(obj_cacho.agregar_dado())
    assert newlen == oldlen + 1