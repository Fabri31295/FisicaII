class Carga:
    def __init__(self, valor, pos, x, y):
        self.valor = valor
        self.pos = pos
        self.x = x
        self.y = y

    def __str__(self):
        return f"Carga{self.pos}(valor={self.valor}, x={self.x}, y={self.y})"