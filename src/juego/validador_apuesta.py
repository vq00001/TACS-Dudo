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

    def validar_subida(self, nueva_cantidad, nuevo_numero):
        # da TRUE si la apuesta nueva es valida y puede aumentar la anterior

        if self._cantidad is None or self._numero is None:
            return False  # no hay apuesta anterior
        
        # Caso 1: aumentar cantidad con pinta igual o mayor
        if nueva_cantidad > self._cantidad and nuevo_numero >= self._numero:
            return True
        
        # Caso 2: aumentar pinta con cantidad igual o mayor
        if nueva_cantidad >= self._cantidad and nuevo_numero > self._numero:
            return True
        
        return False
