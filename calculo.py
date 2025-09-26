from carga import Carga
from grafico import Grafico
from utils import COEFICIENTE_ELECTRICO

class Calculo:

    def __init__(self):
        self.cargas = {}

    def obtener_cargas(self):
        return self.cargas

    def inicializar_cargas(self):
        nro_cargas = int(input("Ingrese la cantidad de cargas - "))
        for idx in range(1, nro_cargas + 1):
            valor, coord_x, coord_y = map(int, input(f"Ingrese el valor de la carga, coordenada x e y para la carga {idx}: ").split())
            carga = Carga(valor, idx, coord_x, coord_y)
            self.cargas[idx] = carga
        return self.cargas


    def calcular_espacio_electrico(self):
        '''
        Función que calcula el campo eléctrico sobre una carga puntual
        '''
        cargas = self.obtener_cargas()
        cant_cargas = len(cargas)
        idx_carga_elegida = int(input("Indique la carga a la que quiere aplicarle el campo. Ej: 1, 2 o 3 - "))
        
        if idx_carga_elegida > cant_cargas:
            print('Carga elegida no disponible')
            return
            
        carga_elegida = cargas.get(idx_carga_elegida)
        campo_x_total = 0
        campo_y_total = 0

        grafico = Grafico(self)
        
        for idx, carga_puntual in cargas.items():
            if idx != idx_carga_elegida:
                distancia_x = carga_elegida.x - carga_puntual.x
                distancia_y = carga_elegida.y - carga_puntual.y
                r = self.calcular_distancia(distancia_x, distancia_y)

                if r == 0:
                    print('Error: Se está calculando el campo sobre la misma carga elegida!')
                    return
                else:
                    campo_x = COEFICIENTE_ELECTRICO * carga_puntual.valor * distancia_x / pow(r, 3)
                    campo_y = COEFICIENTE_ELECTRICO * carga_puntual.valor * distancia_y / pow(r, 3)
                    
                    campo_x_total += campo_x
                    campo_y_total += campo_y

        magnitud_total = self.calcular_distancia(campo_x_total, campo_y_total)

        print(f"-" * 20)
        print(f"Magnitud = {magnitud_total:.2e} N/C")
        print(f"Vector: E = {campo_x_total:.2e} i + {campo_y_total:.2e} j")
        
        grafico.graficar_campo_electrico("individual")
        grafico.graficar_campo_electrico("total")
        grafico.graficar_lineas_campo()
        
        input("\nPresione Enter para continuar...")

    def calcular_potencial_electrico(self):
        '''
        Función que calcula el potencial eléctrico sobre una carga puntual y genera gráficos
        '''
        cargas = self.obtener_cargas()
        cant_cargas = len(cargas)
        idx_carga_elegida = int(input("Indique la carga a la que quiere aplicarle el potencial. Ej: 1, 2 o 3 - "))
        
        if idx_carga_elegida > cant_cargas:
            print('Carga elegida no disponible')
            return
            
        carga_elegida = cargas.get(idx_carga_elegida)
        potencial_total = 0
        grafico = Grafico(self)
        
        for idx, carga_puntual in cargas.items():
            if idx != idx_carga_elegida:
                distancia_x = carga_elegida.x - carga_puntual.x
                distancia_y = carga_elegida.y - carga_puntual.y
                r = self.calcular_distancia(distancia_x, distancia_y)

                if r == 0:
                    print('Error: Se está calculando el potencial sobre la misma carga elegida!')
                    return
                else:
                    potencial_individual = COEFICIENTE_ELECTRICO * carga_puntual.valor / r
                    
                    # Mostrar información del potencial individual
                    print(f"Carga {idx}: q={carga_puntual.valor} C en ({carga_puntual.x}, {carga_puntual.y})")
                    print(f"  Potencial sobre carga {idx_carga_elegida}: V={potencial_individual:.2e} V")
                    
                    # Graficar potencial individual
                    #grafico.graficar_potencial_individual(carga_puntual.valor, carga_puntual.x, carga_puntual.y,
                    #                                    idx, potencial_individual)
                    
                    potencial_total += potencial_individual

        print(f"\n" + "="*50)
        print(f"RESULTADO FINAL - Potencial eléctrico en la carga {idx_carga_elegida}:")
        print(f"V = {potencial_total:.2e} V")
        print("="*50)
        
        # Generar gráficos de superposición y equipotenciales
        print(f"\nGenerando gráficos de superposición y equipotenciales...")
        grafico.graficar_potencial_electrico(potencial_total, carga_elegida.x, carga_elegida.y, idx_carga_elegida)
        
        input("\nPresione Enter para continuar...")
        

    def calcular_distancia(self, dist_x, dist_y):
        import math
        dist_x_cuadrado = pow(dist_x,2)
        dist_y_cuadrado = pow(dist_y,2)
        dist_sumada = dist_x_cuadrado + dist_y_cuadrado
        rtdo = math.sqrt(dist_sumada)
        return rtdo