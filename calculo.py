from grafico import Grafico
from utils import COEFICIENTE_ELECTRICO
from carga import Punto

class Calculo:

    def __init__(self):
        self.cargas = {}

    def calcular_espacio_electrico(self):
        '''
        Función que calcula el campo eléctrico sobre un punto X,Y
        '''
        cargas = self.cargas
        punto_valores = str(input("Indique el punto sobre el que quiera calcular en la forma X Y (Ej: 1 2) - "))
        punto_valores = punto_valores.split()

        punto = Punto(int(punto_valores[0]), int(punto_valores[1]))

        campo_x_total = 0
        campo_y_total = 0

        grafico = Grafico(self)
        
        for idx, carga_puntual in cargas.items():
            distancia_x = punto.x - carga_puntual.x
            distancia_y = punto.y - carga_puntual.y
            r = self.calcular_distancia(distancia_x, distancia_y)

            if r == 0:
                continue
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
        cargas = self.cargas
        punto_valores = str(input("Indique el punto sobre el que quiera calcular el potencial en la forma X Y (Ej: 1 2) - "))
        punto_valores = punto_valores.split()

        punto = Punto(int(punto_valores[0]), int(punto_valores[1]))
   
        potencial_total = 0
        grafico = Grafico(self)
        
        for idx, carga_puntual in cargas.items():
           
                distancia_x = punto.x - carga_puntual.x
                distancia_y = punto.y - carga_puntual.y
                r = self.calcular_distancia(distancia_x, distancia_y)

                if r == 0:
                    continue
                else:
                    potencial_individual = COEFICIENTE_ELECTRICO * carga_puntual.valor / r
                    
                    # Mostrar información del potencial individual
                    print(f"Carga {idx}: q={carga_puntual.valor} C en ({carga_puntual.x}, {carga_puntual.y})")
                    print(f"  Potencial sobre punto X={punto.x}, Y={punto.y}: V={potencial_individual:.2e} V")
                    
                    potencial_total += potencial_individual

        print(f"\n" + "="*50)
        print(f"RESULTADO FINAL - Potencial eléctrico en punto X={punto.x}, Y={punto.y}:")
        print(f"V = {potencial_total:.2e} V")
        print("="*50)
        
        # Generar gráficos de individuales, superposición y equipotenciales
        print(f"\nGenerando gráficos ...")
        grafico.graficar_potencial_electrico(mostrar="individual")
        grafico.graficar_potencial_electrico(mostrar="total")
        grafico.graficar_equipotenciales()
        
        input("\nPresione Enter para continuar...")
        

    def calcular_distancia(self, dist_x, dist_y):
        import math
        dist_x_cuadrado = pow(dist_x,2)
        dist_y_cuadrado = pow(dist_y,2)
        dist_sumada = dist_x_cuadrado + dist_y_cuadrado
        rtdo = math.sqrt(dist_sumada)
        return rtdo