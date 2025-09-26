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
    
    def _cargas_numpy(self):
        if self.calculo:
            cargas = self.calculo.obtener_cargas()
        else:
            raise ValueError("No se ha proporcionado un objeto Calculo")
        
        qs  = np.array([float(c.valor) for c in cargas.values()], dtype=float)
        xqs = np.array([float(c.x)     for c in cargas.values()], dtype=float)
        yqs = np.array([float(c.y)     for c in cargas.values()], dtype=float)
        return qs, xqs, yqs
    
    def _crear_nombre_archivo(self, tipo_grafico):
        if not os.path.exists('Graficos'):
            os.makedirs('Graficos')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"Graficos/{tipo_grafico}_{timestamp}.png"
        return nombre_archivo


    def graficar_lineas_campo(self):
        qs, xqs, yqs = self._cargas_numpy()

        x = np.linspace(-10.0, 10.0, 300)
        y = np.linspace(-10.0, 10.0, 300)
        X, Y = np.meshgrid(x, y)

        dx = X[..., None] - xqs[None, None, :]
        dy = Y[..., None] - yqs[None, None, :]
        r  = np.sqrt(dx**2 + dy**2)
        r[r == 0] = np.inf

        Ex = (COEFICIENTE_ELECTRICO * qs[None, None, :] * dx / (r**3)).sum(axis=-1)
        Ey = (COEFICIENTE_ELECTRICO * qs[None, None, :] * dy / (r**3)).sum(axis=-1)

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.streamplot(X, Y, Ex, Ey, density=2, linewidth=0.8)

        for j in range(qs.size):
            color = "turquoise" if qs[j] > 0 else "red"
            ax.scatter([xqs[j]], [yqs[j]], s=120, c=color, edgecolors="k", zorder=3)
            
            signo = "+" if qs[j] > 0 else "−"
            ax.text(xqs[j], yqs[j], signo, fontsize=14, fontweight='bold', 
                   ha='center', va='center', color='white', zorder=4)
            
            ax.text(xqs[j] + 0.2, yqs[j] + 0.2, f"q{j+1}", fontsize=9)

        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.set_title("Líneas de campo eléctrico (superposición)")
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, alpha=0.2)
        plt.tight_layout()
        
        archivo = self._crear_nombre_archivo("lineas_campo_electrico")
        plt.savefig(archivo, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado como '{archivo}'")
        
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
            dx[np.isclose(dx, 0.0)] = np.nan  # evitar /0
            Ex = k * c.valor * dx / (np.abs(dx)**3)
            Ex_individuales.append(Ex)
            Ex_total += np.nan_to_num(Ex, nan=0.0)

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

        if mostrar in ("individual", "ambos"):
            for i, V in enumerate(V_individuales, start=1):
                c = cargas[i-1]
                q_microC = cargas[i-1].valor*1e6
                plt.plot(x, V, linewidth=1.5,
                        label=f"V carga {i} (q={q_microC:.0f} μC, x={c.x} m)")

        if mostrar in ("total", "ambos"):
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
        plt.show()

    def graficar_equipotenciales(self):
        """
        Grafica las líneas equipotenciales en una región 2D
        """
        qs, xqs, yqs = self._cargas_numpy()

        # Crear malla 2D para el cálculo del potencial
        x = np.linspace(-8.0, 8.0, 400)
        y = np.linspace(-8.0, 8.0, 400)
        X, Y = np.meshgrid(x, y)

        # Calcular distancias a cada carga
        dx = X[..., None] - xqs[None, None, :]
        dy = Y[..., None] - yqs[None, None, :]
        r = np.sqrt(dx**2 + dy**2)
        
        # Evitar división por cero cerca de las cargas
        r[r < 0.1] = 0.1
        
        # Calcular potencial total
        V_total = (COEFICIENTE_ELECTRICO * qs[None, None, :] / r).sum(axis=-1)

        # Crear el gráfico de equipotenciales
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Dibujar líneas equipotenciales
        levels = np.logspace(8, 12, 20)  # Niveles de potencial
        levels = np.concatenate([-levels[::-1], levels])  # Incluir valores negativos
        
        contour = ax.contour(X, Y, V_total, levels=levels, colors='blue', alpha=0.6, linewidths=1)
        ax.clabel(contour, inline=True, fontsize=8, fmt='%.1e')
        
        # Marcar las cargas
        for j in range(qs.size):
            color = "red" if qs[j] > 0 else "blue"
            ax.scatter([xqs[j]], [yqs[j]], s=200, c=color, edgecolors="black", zorder=3)
            
            signo = "+" if qs[j] > 0 else "−"
            ax.text(xqs[j], yqs[j], signo, fontsize=16, fontweight='bold', 
                   ha='center', va='center', color='white', zorder=4)
            
            ax.text(xqs[j] + 0.3, yqs[j] + 0.3, f"q{j+1}={qs[j]}", fontsize=10, 
                   bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))

        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.set_title("Líneas Equipotenciales (Superposición de todas las cargas)")
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        archivo = self._crear_nombre_archivo("equipotenciales")
        plt.savefig(archivo, dpi=300, bbox_inches='tight')
        print(f"Gráfico de equipotenciales guardado como '{archivo}'")
        plt.show()
