import pytest
import sys
sys.path.append('src/juego')
import cacho

def test_creacion_cacho():
    obj_cacho = cacho.cacho()
    assert len(obj_cacho.dados) == 5