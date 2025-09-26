from calculo import Calculo
from carga import Carga


if __name__ == "__main__":
    Q = 1e-6  # 1 microC
    
    calc = Calculo()
    calc.cargas = {
        1: Carga(pos= 1, x=-3, y=0,valor= 9 * Q),
        2: Carga(pos= 2, x=0, y=0,valor= -8 * Q),
        3: Carga(pos= 3, x=3, y=0,valor= 1 * Q),
    }

    calc.calcular_espacio_electrico()
    calc.calcular_potencial_electrico()