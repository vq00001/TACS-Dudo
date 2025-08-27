class ValidadorApuesta:
    def __init__(self):
        self._cantidad = None
        self._numero = None

    def set_apuesta(self, cantidad, numero):
        if cantidad < 1:
            raise ValueError("Cantidad debe ser positiva")
        if numero < 1 or numero > 6:
            raise ValueError("Número debe estar entre 1 y 6")
        self._cantidad = cantidad
        self._numero = numero

    def get_apuesta(self):
        if self._cantidad is None or self._numero is None:
            raise ValueError("No hay apuesta definida")
        return self._cantidad, self._numero
