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
        cargas = self.inicializar_cargas()
        cant_cargas = len(self.cargas)
        idx_carga_elegida = int(input("Indique la carga a la que quiere aplicarle el campo. Ej: 1, 2 o 3 - "))
        if idx_carga_elegida > cant_cargas:
            print('Carga elegida no disponible')
        else:
            carga_elegida = cargas.get(idx_carga_elegida)
        
            campo_x_total = 0
            campo_y_total = 0
        
            for idx, carga_fuente in cargas.items():
                if idx != idx_carga_elegida:
                    # Vector distancia desde la carga fuente hacia la carga elegida
                    distancia_x = carga_elegida.x - carga_fuente.x
                    distancia_y = carga_elegida.y - carga_fuente.y
                
                    # Magnitud de la distancia
                    r = self.calcular_distancia(distancia_x, distancia_y)
                
                    print(f"Carga fuente {idx}: valor={carga_fuente.valor}")
                    print(f"Distancia x: {distancia_x}")
                    print(f"Distancia y: {distancia_y}")
                    print(f"Distancia r: {r}")

                    campo_x = COEFICIENTE_ELECTRICO * carga_fuente.valor * distancia_x / pow(r, 3)
                    campo_y = COEFICIENTE_ELECTRICO * carga_fuente.valor * distancia_y / pow(r, 3)

                    campo_x_total += campo_x
                    campo_y_total += campo_y
                    print("-" * 30)
        
            # Magnitud total del campo
            magnitud_total = self.calcular_distancia(campo_x_total, campo_y_total)
            
            print(f"Campo total Ex: {campo_x_total} mC")
            print(f"Campo total Ey: {campo_y_total} mC")
            print(f"Magnitud del campo eléctrico: {magnitud_total} mC")
            print(f"Vector del campo eléctrico: E(x,y) = {campo_x_total} mC * i + {campo_y_total} * j")

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
    entrada = input('Ingrese una opción - ').strip()
    if not entrada:
        print("Opcion ingresada no válida .")
    else:
        print(entrada)
        opcion_seleccionada = int(entrada)
        funcion = opciones.get(opcion_seleccionada)
        if funcion:
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