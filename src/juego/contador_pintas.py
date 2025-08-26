class ContadorPintas:
    def contar(self, dados, numero):
        """
        cuenta cuántas veces está el "numero"(pinta) indicada en la lista de los dados.
        !!no considera ases(1) como comodines para esta version de los test -> 1 es un numero normal por ahora, aun no es un comodin

        """
        return dados.count(numero)
    
    def contar_pintas(self, dados, apuesta, ases_comodines=True):
        """
        Cuenta cuantas veces aparece la pinta apostada en la lista de dados.
        - Los Ases (1) cuentan como comodines, excepto cuando la apuesta es por 1.
        - Si ases_comodines=False, los Ases no cuentan como comodines. -> Se refiere a la ronda especial cuando un jugador queda por primera vez con un dado
        """
        contador = 0
        for d in dados:
            if d == apuesta:
                contador += 1
            elif d == 1 and apuesta != 1 and ases_comodines:
                contador += 1
        return contador

