import pytest

def test_tirar_dado(mocker):
   mock_random = mocker.patch('dado.random.randint')
   mock_random.return_value = 2

   resultado = dado.tirar()

   assert resultado == 2
