class ValidadorApuesta:
    def __init__(self):
        self._cantidad = None
        self._numero = None
        self._primera = True
        self._jugador_un_dado = False

    def set_apuesta(self, cantidad, numero, jugador_un_dado=False):
        if cantidad < 1:
            raise ValueError("Cantidad debe ser positiva")
        if numero < 1 or numero > 6:
            raise ValueError("Número debe estar entre 1 y 6")
        # regla: primera apuesta de la ronda no puede ser con 1, solo si el jugador tiene un dado
        if self._primera and numero == 1 and not jugador_un_dado:
            raise ValueError("La primera apuesta de la ronda no puede ser con Ases")

        self._cantidad = cantidad
        self._numero = numero
        self._primera = False
        self._jugador_un_dado = jugador_un_dado

    def get_apuesta(self):
        if self._cantidad is None or self._numero is None:
            raise ValueError("No hay apuesta definida")
        return self._cantidad, self._numero

    def validar_subida(self, nueva_cantidad, nuevo_numero):
        
        # da TRUE si la apuesta nueva es valida y puede aumentar la anterior
        if self._cantidad is None or self._numero is None:
            return False  # no hay apuesta anterior
        
        # caso especial: si la apuesta anterior fue con 1
        if self._numero == 1:
            # Caso 1: mantener pinta 1, solo subiendo cantidad
            if nuevo_numero == 1 and nueva_cantidad > self._cantidad:
                return True
            # Caso 2: cambiar a otro número (regla del doble mas uno)
            if nuevo_numero > 1 and nueva_cantidad >= (self._cantidad * 2 + 1):
                return True
            return False
        
        # reglas generales:
        # Caso 1: aumentar cantidad con pinta igual o mayor
        if nueva_cantidad > self._cantidad and nuevo_numero >= self._numero:
            return True
        
        # Caso 2: aumentar pinta con cantidad igual o mayor
        if nueva_cantidad >= self._cantidad and nuevo_numero > self._numero:
            return True
        
        return False

    def obtener_apuesta_desde_consola(self):
        entrada = input("Ingrese la apuesta (ej: '3 4') !Primer numero es la cantidad y segundo la pinta: ")
        partes = entrada.split()
        cantidad = int(partes[0])
        numero = int(partes[1])
        self.set_apuesta(cantidad, numero)