class CalzadoInvalido(Exception):
    # Excepción personalizada para indicar un calzado inválido.
    def __init__(self, mensaje="Calzado inválido."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class EstadoJuegoInvalido(Exception):
    # Excepción personalizada para indicar un calzado inválido.
    def __init__(self, mensaje="Estado de juego inválido."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

