class ContadorPintas:
    def contar(self, dados, numero):
        # contar cuántas veces aparece "numero" en los dados
        total = 0
        for d in dados:
            total += d.count(numero)
        return total
