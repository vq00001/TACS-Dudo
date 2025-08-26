class ContadorPintas:
    def contar_sin_comodines(self, dados, numero):
        """
        cuenta cuántas veces está el "numero"(pinta) indicada en la lista de los dados.
        !! no considera Ases(1) como comodines esta función -> 1 es un numero normal 

        """
        return dados.count(numero)
    
    def contar_con_comodines(self, dados, apuesta):
        """
        cuenta cuántas veces aparece la pinta apostada en los dados.
        !! los Ases(1) cuentan como comodines, excepto cuando la apuesta es por 1.

        """
        # Contar cuántos dados coinciden con la apuesta
        num_apostados = self.contar_sin_comodines(dados, apuesta)

        # Contar Ases como comodines si la apuesta no es 1
        num_ases = 0
        if apuesta != 1:
            num_ases = self.contar_sin_comodines(dados, 1)

        return num_apostados + num_ases
