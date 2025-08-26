class ContadorPintas:
    def contar_sin_comodines(self, dados, numero):
        """
        cuenta cuántas veces está el "numero"(pinta) indicada en la lista de los dados.
        !! no considera Ases(1) como comodines esta función -> 1 es un numero normal 

        """
        if len(dados) > 5:
            raise ValueError("No puede haber más de 5 dados")
        if not dados or numero < 1 or numero > 6:
            return 0
        return dados.count(numero)
    
    def contar_con_comodines(self, dados, apuesta, ases_comodines=True):
        """
        cuenta cuántas veces aparece la pinta apostada en los dados.
        !! los Ases(1) cuentan como comodines, excepto cuando la apuesta es por 1 o , ases_comodines=False

        """
        if len(dados) > 5:
            raise ValueError("No puede haber más de 5 dados")
        if not dados:
            return 0
        if apuesta < 1 or apuesta > 6:
            return sum(1 for d in dados if d == 1) if ases_comodines else 0

        contador = 0
        for d in dados:
            if d == apuesta:
                contador += 1
            elif d == 1 and apuesta != 1 and ases_comodines:
                contador += 1
        return contador