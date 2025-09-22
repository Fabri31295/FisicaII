import sys

COEFICIENTE_ELECTRICO = 9 * pow(10,9) 

class Carga:
    # Constructor
    def __init__(self, valor , pos , x, y,):
        self.valor = valor
        self.pos = pos
        self.x = x
        self.y = y

    def __str__(self):
        return f"Carga(valor={self.valor}, pos={self.pos}, x={self.x}, y={self.y})"

class Calculo:
    # Constructor
    def __init__(self):
        self.cargas = {}

    def obtener_cargas(self):
        return self.cargas

    def inicializar_cargas(self):
        nro_cargas = int(input("Ingrese la cantidad de cargas - "))
        for idx in range(1,nro_cargas+1):
            valor,coord_x, coord_y = map(int, input(f"Ingrese el valor de la carga, coordenada x e y para la carga {idx}: ").split())
            carga = Carga(valor,idx,coord_x, coord_y)
            self.cargas[idx] = carga
        return self.cargas

    def calcular_espacio_electrico(self):
        '''
        Función que calcula el campo eléctrico sobre una carga puntual
        '''
        rtdo = 0
        cargas = self.inicializar_cargas()
        idx_carga_elegida = int(input("Indique la carga a la que quiere aplicarle el campo. Ej: 1, 2 o 3 - "))
        carga_elegida = cargas.get(idx_carga_elegida)
        print(carga_elegida)
        for idx, valor in cargas.items():
            if idx != idx_carga_elegida:
                # Calculo en coordenadas x
                valor_x1 = valor.x
                distancia_x = carga_elegida.x - valor_x1

                # Calculo en coordenadas y
                valor_y1 = valor.y
                distancia_y = carga_elegida.y - valor_y1

                # Calculo r
                r = self.calcular_distancia(distancia_x, distancia_y)

                # Armamos la formula

    def calcular_potencial_electrico(self):
        print("potencial")
    
    def calcular_distancia(self, dist_x, dist_y):
        import math
        dist_x_cuadrado = pow(dist_x,2)
        dist_y_cuadrado = pow(dist_y,2)
        dist_sumada = dist_x_cuadrado + dist_y_cuadrado
        rtdo = math.sqrt(dist_sumada)
        return rtdo


def menu(sistema):
    opciones = {
        1: sistema.calcular_espacio_electrico,
        2: sistema.calcular_potencial_electrico,
        3: salir
    }

    print('Menú de opciones\n')
    print('----------------------------------\n')
    print('1: Calculo del campo eléctrico \n')
    print('2: Calculo del potencial eléctrico \n')
    print('3: Salir del programa \n')
    opcion_seleccionada = int(input('Ingrese una opción - '))
    funcion = opciones.get(opcion_seleccionada)
    funcion()

def salir():
    print("Cerrando script ...")        
    sys.exit(0)
    
def main():
    print('*******************************************\n')
    print('*******************************************\n')
    print('    Script de laboratorio computacional    \n')
    print('*******************************************\n')
    print('*******************************************\n')

    calc = Calculo()

    while True:
        menu(calc)

if __name__ == "__main__":
    main()