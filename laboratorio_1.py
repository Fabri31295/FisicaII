import sys
from carga import Carga
from calculo import Calculo
from grafico import Grafico

def menu(calculo, grafico):
    opciones = {
        1: calculo.calcular_espacio_electrico,
        2: calculo.calcular_potencial_electrico,
        3: grafico.graficar_Ex_sobre_eje_x,
        4: grafico.graficar_lineas_campo,
        5: calculo.reingresar_cargas,
        6: salir
    }

    cargas = calculo.obtener_cargas()
    print(" " * 30)
    print("-" * 30)
    print(" "*12 + "MENÚ" + " "*12)
    print("-" * 30)
    if cargas and len(cargas) > 0:
        msg = "Cargas cargadas: "
        for _, carga in cargas.items():
            msg += carga.__str__() + " - "
        print(msg)
    print("1: Calculo del campo eléctrico")
    print("2: Calculo del potencial eléctrico")
    print("3: Graficar E_x(x) (individuales + superposición")
    print("4: Graficar líneas de campo resultant")
    print("5: Reingresar carga")
    print("6: Salir del programa")
    print("-" * 30)
    
    entrada = input('Ingrese una opción - ').strip()
    if not entrada:
        print("Opcion ingresada no válida . Intente de nuevo")
    else:
        opcion_seleccionada = int(entrada)
        funcion = opciones.get(opcion_seleccionada)
        if funcion:
            funcion()

def salir():
    print("Cerrando script ...")
    sys.exit(0)

def main():
    calc = Calculo()
    graf = Grafico()

    while True:
        menu(calc, graf)

if __name__ == "__main__":
    main()