import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from utils import COEFICIENTE_ELECTRICO

class Grafico:

    rango_x=(-10,10)
    n_puntos=2000
    ylim=(-8e4,8e4)

    def __init__(self, calculo=None):
        self.calculo = calculo
    
    def _crear_nombre_archivo(self, tipo_grafico):
        if not os.path.exists('Graficos'):
            os.makedirs('Graficos')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"Graficos/{tipo_grafico}_{timestamp}.png"
        return nombre_archivo

    def _guardar_archivo(self, plt, titulo):
        archivo = self._crear_nombre_archivo(titulo)
        plt.savefig(archivo, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado como '{archivo}'")

    def graficar_lineas_campo(self):
        """
        Grafica las líneas de campo eléctrico (streamlines) para un conjunto de cargas puntuales en 2D.
        """

        k = COEFICIENTE_ELECTRICO
        cargas = list(self.calculo.cargas.values())

        # Malla 2D
        x = np.linspace(self.rango_x[0], self.rango_x[1], 500)
        y = np.linspace(self.rango_x[0], self.rango_x[1], 500)
        X, Y = np.meshgrid(x, y)

        # Componentes del campo
        Ex = np.zeros_like(X, dtype=float)
        Ey = np.zeros_like(Y, dtype=float)

        for c in cargas:
            dx = X - c.x
            dy = Y - c.y
            r2 = dx**2 + dy**2
            r3 = np.power(r2, 1.5)
            r3[r3 == 0] = np.nan  # evitar /0

            Ex += k * c.valor * dx / r3
            Ey += k * c.valor * dy / r3

        # Graficar líneas de campo
        plt.figure(figsize=(8,6))
        plt.streamplot(X, Y, Ex, Ey, color="darkgrey", linewidth=1, density=1.5, arrowsize=1.2)

        # Dibujar las cargas
        for c in cargas:
            col = "red" if c.valor > 0 else "blue"
            plt.scatter(c.x, c.y, c=col, s=60, edgecolors="k", zorder=5)

        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        plt.title("Líneas de campo eléctrico")
        plt.axhline(0, color="gray", linewidth=0.5)
        plt.axvline(0, color="gray", linewidth=0.5)
        plt.gca().set_aspect("equal", adjustable="box")
        plt.grid(alpha=0.2)
        self._guardar_archivo(plt, "lineas_campo_electrico")
        plt.show()
    
    def graficar_campo_electrico(self, mostrar="individual"):
        k = COEFICIENTE_ELECTRICO
        cargas = list(self.calculo.cargas.values())

        x = np.linspace(self.rango_x[0], self.rango_x[1], self.n_puntos)
        Ex_total = np.zeros_like(x)
        Ex_individuales = []

        # Calcular campos
        for c in cargas:
            dx = x - c.x
            dx[np.isclose(dx, 0.0, atol=1e-2)] = np.nan  # evitar /0
            Ex = k * c.valor * dx / (np.abs(dx)**3)
            Ex_individuales.append(Ex)
            Ex_total += Ex

        # Graficar
        plt.figure(figsize=(10,6))

        if mostrar=="individual":
            for i, Ex in enumerate(Ex_individuales, start=1):
                c = cargas[i-1]
                q_microC = c.valor *1e6
                plt.plot(x, Ex, linewidth=1.5,
                        label=f"E_x carga {i} (q={q_microC:.0f} μC, x={c.x} m)")

        if mostrar=="total":
            plt.plot(x, Ex_total, 'k', linewidth=2, label="E_x total (superposición)")

        puntos_equilibrio = []

        # Detectar TODOS los cambios de signo (incluyendo asíntotas)
        cambios_de_signo_indices = np.where(np.diff(np.sign(Ex_total)))[0]

        # Iterar sobre los cambios y filtrar singularidades
        for i in cambios_de_signo_indices:
            x_eq = np.nan
            
            # --- FILTRO CLAVE: Ignorar los cambios de signo que son asíntotas ---
            # Verificamos si el punto 'i' o 'i+1' está cerca de alguna carga.
            es_singularidad = False
            for c in cargas:
                # Si el punto de cruce está a menos de 0.05 m de una carga (ajusta este valor si es necesario)
                if np.abs(x[i] - c.x) < 5e-2 or np.abs(x[i+1] - c.x) < 5e-2:
                    es_singularidad = True
                    break
            
            if es_singularidad:
                continue # ¡Salta esta iteración porque es un pico!
            # --------------------------------------------------------------------
            
            # Si pasa el filtro, es un Punto de Equilibrio real (cruce por cero)
            
            # Interpolación lineal (como antes)
            x1, x2 = x[i], x[i+1]
            y1, y2 = Ex_total[i], Ex_total[i+1]
            x_eq = x1 - y1 * (x2 - x1) / (y2 - y1)
            
            # Filtrar duplicados
            if all(np.abs(x_eq - p) > 1e-4 for p in puntos_equilibrio): # Usar 1e-4 para mayor precisión
                puntos_equilibrio.append(x_eq)

        # Marcar los puntos en el gráfico (Solo si mostramos la superposición)
        if mostrar == "total" and puntos_equilibrio:
            for i, x_eq in enumerate(puntos_equilibrio):
                plt.plot(x_eq, 0, 'go', markersize=8, 
                         label="Punto de Equilibrio" if i == 0 else None)
                plt.axvline(x_eq, color='g', linestyle='--', linewidth=0.7)
                print(f"Punto de Equilibrio encontrado: x = {x_eq:.4f} m")

        # Referencias visuales
        plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
        for c in cargas:
            plt.axvline(c.x, color="red" if c.valor>0 else "blue",
                        linestyle=":", linewidth=1)

        plt.xlim(self.rango_x)
        plt.ylim(self.ylim)
        plt.xlabel("x [m]")
        plt.ylabel("E_x(x) [N/C]")
        plt.title(f"Campo eléctrico sobre el eje x ({mostrar})")
        plt.legend()
        plt.grid(alpha=0.3)

        self._guardar_archivo(plt, f"Ex_{mostrar}")
        plt.show()

    def graficar_potencial_electrico(self, mostrar="individual"):
        """
        Grafica el potencial eléctrico V(x) sobre el eje x para un conjunto de cargas puntuales.

        Parámetros:
        -----------

        mostrar : str
            "individual" → solo potenciales de cada carga
            "total"      → solo potencial total
        """
        cargas = list(self.calculo.cargas.values())
        
        k = COEFICIENTE_ELECTRICO
        x = np.linspace(self.rango_x[0], self.rango_x[1], self.n_puntos)

        V_total = np.zeros_like(x)
        V_individuales = []

        # Calcular potenciales
        for c in cargas:
            dx = x - c.x
            dx[np.isclose(dx, 0.0)] = np.nan  # evitar división por cero
            V = k * c.valor / np.abs(dx)
            V_individuales.append(V)
            V_total += np.nan_to_num(V, nan=0.0)
  
        # Graficar
        plt.figure(figsize=(10,6))

        if mostrar in "individual":
            for i, V in enumerate(V_individuales, start=1):
                c = cargas[i-1]
                q_microC = cargas[i-1].valor*1e6
                plt.plot(x, V, linewidth=1.5,
                        label=f"V carga {i} (q={q_microC:.0f} μC, x={c.x} m)")

        if mostrar in "total":
            plt.plot(x, V_total, 'k', linewidth=2, label="V total (superposición)")

        # Referencias visuales
        plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
        for c in cargas:
            plt.axvline(c.x, color="red" if c.valor>0 else "blue",
                        linestyle=":", linewidth=1)

        plt.xlim(self.rango_x)
        plt.ylim(self.ylim)
        plt.xlabel("x [m]")
        plt.ylabel("V(x) [Voltios]")
        plt.title("Potencial eléctrico sobre el eje x")
        plt.legend()
        plt.grid(alpha=0.3)
        self._guardar_archivo(plt, f"Vx_{mostrar}")
        plt.show()


    def graficar_equipotenciales(self):
        """
        Grafica el mapa de equipotenciales (contorno) para un conjunto de cargas puntuales en 2D.

        Parámetros:
        -----------
        """

        k = COEFICIENTE_ELECTRICO
        cargas = list(self.calculo.cargas.values())

        # Crear malla 2D
        x = np.linspace(self.rango_x[0], self.rango_x[1], 500)
        y = np.linspace(self.rango_x[0], self.rango_x[1], 500)
        X, Y = np.meshgrid(x, y)

        # Calcular potencial total
        V_total = np.zeros_like(X, dtype=float)
        for c in cargas:
            dx = X - c.x
            dy = Y - c.y
            r = np.sqrt(dx**2 + dy**2)
            r[r == 0] = np.nan  # evitar div 0
            V_total += k * c.valor / r

        # Graficar contornos
        # Recortar rango de potencial para evitar saturación cerca de las cargas
        levels = np.logspace(2, 9, 30)
        levels = np.concatenate([-levels[::-1], levels])

        plt.figure(figsize=(8,6))
        cont = plt.contour(X, Y, V_total, levels=levels, colors='blue', alpha=0.6, linewidths=1)
        plt.clabel(cont, inline=True, fontsize=7, fmt="%.0e")

        # Dibujar las cargas
        for c in cargas:
            color = "red" if c.valor > 0 else "blue"
            plt.scatter(c.x, c.y, c=color, s=60, edgecolors="k", zorder=5)

        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        plt.title("Líneas equipotenciales")
        plt.axhline(0, color="gray", linewidth=0.5)
        plt.axvline(0, color="gray", linewidth=0.5)
        plt.gca().set_aspect("equal", adjustable="box")
        plt.grid(alpha=0.2)
        self._guardar_archivo(plt, "equipotencial")
        plt.show()
