import pytest
import sys
sys.path.append('src/juego')
import dado

def test_tirar_dado(mocker):
   dado = dado.dado()
   mock_random = mocker.patch('dado.random.randint')
   mock_random.return_value = 2

   resultado = dado.tirar()

   assert resultado == 2

def test_tirar_multiples_dados(mocker):
   dado1 = dado.dado()
   dado2 = dado.dado()

   mock_random1 = mocker.patch('dado.random.randint')
   mock_random1.return_value = 1

   resultado1 = dado1.tirar()
   
   mock_random2 = mocker.patch('dado.random.randint')
   mock_random2.return_value = 3

   resultado2 = dado2.tirar()
   
   assert resultado1 == 1
   assert resultado2 == 3

def test_ver_dado():
   dado = dado.dado()
   resultado = dado.tirar()

   assert dado.ver() == resultado