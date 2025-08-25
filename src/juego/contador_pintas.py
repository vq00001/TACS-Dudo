class ContadorPintas:
    def contar(self, dados, numero):
        """
        cuenta cuántas veces está el "numero"(pinta) indicada en la lista de los dados.
        !!no considera ases(1) como comodines para esta version de los test -> 1 es un numero normal por ahora, aun no es un comodin
        
        """
        return dados.count(numero)
