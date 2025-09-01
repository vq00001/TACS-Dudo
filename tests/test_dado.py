import pytest
from src.juego.dado import dado

def test_tirar_dado(mocker):
   obj_dado = dado()
   mock_random = mocker.patch('dado.random.randint')
   mock_random.return_value = 2

   resultado = obj_dado.tirar()

   assert resultado == 2

def test_tirar_multiples_dados(mocker):
   obj_dado1 = dado()
   obj_dado2 = dado()

   mock_random1 = mocker.patch('dado.random.randint')
   mock_random1.return_value = 1

   resultado1 = obj_dado1.tirar()
   
   mock_random2 = mocker.patch('dado.random.randint')
   mock_random2.return_value = 3

   resultado2 = obj_dado2.tirar()
   
   assert resultado1 == 1
   assert resultado2 == 3

def test_ver_dado():
   obj_dado = dado()
   resultado = obj_dado.tirar()

   assert obj_dado.ver() == resultado