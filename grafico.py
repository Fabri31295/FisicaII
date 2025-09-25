import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from utils import COEFICIENTE_ELECTRICO

class Grafico:
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
    
    def graficar_campo_electrico(self, campo_x_total, campo_y_total, magnitud_total, punto_x, punto_y, idx_carga):
        qs, xqs, yqs = self._cargas_numpy()
        
        x = np.linspace(-10.0, 10.0, 1000)
        dx = x[:, None] - xqs[None, :]
        dy = 0.0 - yqs[None, :]
        r = np.sqrt(dx**2 + dy**2)
        r[r == 0] = np.inf
        
        # Calcular campo de cada carga individual
        Ex_each = COEFICIENTE_ELECTRICO * qs[None, :] * dx / (r**3)
        
        # Para la superposición, excluir la carga elegida (comportamiento físico correcto)
        Ex_each_superposicion = Ex_each.copy()
        Ex_each_superposicion[:, idx_carga - 1] = 0  # Excluir la carga elegida
        Ex_total = Ex_each_superposicion.sum(axis=1)
        
        # Encontrar puntos de equilibrio (donde E_x = 0)
        puntos_cero = []
        for i in range(len(Ex_total)-1):
            if Ex_total[i] * Ex_total[i+1] < 0:
                x_cero = x[i] - Ex_total[i] * (x[i+1] - x[i]) / (Ex_total[i+1] - Ex_total[i])
                if -5 <= x_cero <= 5:  # Rango de interés
                    puntos_cero.append(x_cero)
        
        # PRIMER GRÁFICO: Cargas individuales que contribuyen
        fig1 = plt.figure(figsize=(14, 8))
        for j in range(qs.size):
            if j != idx_carga - 1:  # Solo mostrar cargas que contribuyen
                plt.plot(x, Ex_each[:, j], linewidth=2, alpha=0.7,
                         label=f"E_x carga {j+1} (q={qs[j]}, x={xqs[j]}, y={yqs[j]})")
        
        # Marcar posición donde se calculó el campo
        plt.axvline(punto_x, color='purple', linestyle=':', linewidth=2, alpha=0.8,
                   label=f'Punto calculado (carga {idx_carga})')
        
        plt.axhline(0, linestyle="--", linewidth=0.8, color='black', alpha=0.5)
        plt.xlabel("x [m]")
        plt.ylabel("E_x(x) [N/C]")
        plt.title(f"Campos Individuales que Actúan sobre Carga {idx_carga}")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xlim(-5, 5)
        plt.tight_layout()
        
        imagen_1 = self._crear_nombre_archivo("campos_individuales_superposicion")
        plt.savefig(imagen_1, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado como '{imagen_1}'")
        plt.show()
        
        # SEGUNDO GRÁFICO: Superposición total con puntos de equilibrio
        fig2 = plt.figure(figsize=(14, 8))
        plt.plot(x, Ex_total, linewidth=3, color='red', 
                 label="E_x SUPERPOSICIÓN (todas las cargas contribuyentes)")
        
        # Marcar posición donde se calculó el campo
        plt.axvline(punto_x, color='purple', linestyle=':', linewidth=2, alpha=0.8,
                   label=f'Punto calculado: x={punto_x}m')
        
        # Marcar puntos de equilibrio
        for i, x_cero in enumerate(puntos_cero):
            plt.axvline(x_cero, color='lightblue', linestyle=':', linewidth=2, alpha=0.7,
                       label='Puntos E_x = 0' if i == 0 else "")
            plt.plot(x_cero, 0, 'go', markersize=12, zorder=5)
            plt.text(x_cero, plt.ylim()[1]*0.15 if plt.ylim()[1] > 0 else plt.ylim()[0]*0.15, 
                    f'x={x_cero:.2f}m', 
                    ha='center', va='bottom' if plt.ylim()[1] > 0 else 'top',
                    color='green', fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="lightgreen", alpha=0.8))
        
        plt.axhline(0, linestyle="--", linewidth=0.8, color='black', alpha=0.5)
        plt.xlabel("x [m]")
        plt.ylabel("E_x(x) [N/C]")
        plt.title(f"Superposición Total - Campo sobre Carga {idx_carga}\n"
                  f"Resultado: E_x={campo_x_total:.2e} N/C, E_y={campo_y_total:.2e} N/C, |E|={magnitud_total:.2e} N/C")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xlim(-5, 5)
        plt.tight_layout()
        
        imagen_2 = self._crear_nombre_archivo("superposicion_total")
        plt.savefig(imagen_2, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado como '{imagen_2}'")
        plt.show()
        
        # Mostrar información de puntos de equilibrio
        if puntos_cero:
            print(f"\n=== PUNTOS DE EQUILIBRIO ===")
            print(f"Puntos encontrados donde E_x = 0:")
            for i, x_cero in enumerate(puntos_cero):
                print(f"  Punto {i+1}: x = {x_cero:.3f} m")
        else:
            print("\nNo se encontraron puntos de equilibrio en el rango [-5, 5] m")
    
    def graficar_potencial_individual(self, q_valor, q_x, q_y, idx_carga, potencial_punto):
        """
        Grafica el potencial eléctrico producido por una carga individual en función de x
        
        Parámetros:
        - q_valor: valor de la carga
        - q_x, q_y: posición de la carga
        - idx_carga: índice de la carga
        - potencial_punto: potencial calculado en el punto específico
        """
        x = np.linspace(-10.0, 10.0, 1000)
        
        # Calcular el potencial de esta carga individual a lo largo del eje x (y=0)
        dx = x - q_x
        dy = 0.0 - q_y
        r = np.sqrt(dx**2 + dy**2)
        r[r == 0] = np.inf  # Evitar división por cero
        
        V_individual = COEFICIENTE_ELECTRICO * q_valor / r
        
        # Crear el gráfico
        plt.figure(figsize=(12, 6))
        plt.plot(x, V_individual, linewidth=2, color='green',
                 label=f"V de carga {idx_carga} (q={q_valor}, pos=({q_x},{q_y}))")
        
        # Marcar la posición de la carga
        plt.axvline(q_x, color='red', linestyle='--', alpha=0.7, 
                   label=f'Posición carga {idx_carga}')
        
        plt.axhline(0, linestyle="--", linewidth=0.8, color='black', alpha=0.5)
        plt.xlabel("x [m]")
        plt.ylabel("V(x) [V]")
        plt.title(f"Potencial Individual V(x) - Carga {idx_carga}\n"
                  f"Potencial calculado: V={potencial_punto:.2e} V")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xlim(-5, 5)
        plt.tight_layout()
        
        # Guardar gráfico
        imagen = self._crear_nombre_archivo(f"potencial_individual_carga_{idx_carga}")
        plt.savefig(imagen, dpi=300, bbox_inches='tight')
        print(f"Gráfico individual guardado como '{imagen}'")
        plt.show()

    def graficar_potencial_electrico(self, potencial_total, punto_x, punto_y, idx_carga):
        """
        Grafica la superposición de todos los potenciales y las equipotenciales
        
        Parámetros:
        - potencial_total: potencial total calculado
        - punto_x, punto_y: posición donde se calculó el potencial
        - idx_carga: índice de la carga sobre la cual se calculó el potencial
        """
        qs, xqs, yqs = self._cargas_numpy()
        
        x = np.linspace(-10.0, 10.0, 1000)
        dx = x[:, None] - xqs[None, :]
        dy = 0.0 - yqs[None, :]
        r = np.sqrt(dx**2 + dy**2)
        r[r == 0] = np.inf
        
        # Calcular potencial de cada carga individual
        V_each = COEFICIENTE_ELECTRICO * qs[None, :] / r
        
        # Para la superposición, excluir la carga elegida
        V_each_superposicion = V_each.copy()
        V_each_superposicion[:, idx_carga - 1] = 0  # Excluir la carga elegida
        V_total = V_each_superposicion.sum(axis=1)
        
        # PRIMER GRÁFICO: Potenciales individuales que contribuyen
        fig1 = plt.figure(figsize=(14, 8))
        for j in range(qs.size):
            if j != idx_carga - 1:  # Solo mostrar cargas que contribuyen
                plt.plot(x, V_each[:, j], linewidth=2, alpha=0.7,
                         label=f"V carga {j+1} (q={qs[j]}, x={xqs[j]}, y={yqs[j]})")
        
        # Marcar posición donde se calculó el potencial
        plt.axvline(punto_x, color='purple', linestyle=':', linewidth=2, alpha=0.8,
                   label=f'Punto calculado (carga {idx_carga})')
        
        plt.axhline(0, linestyle="--", linewidth=0.8, color='black', alpha=0.5)
        plt.xlabel("x [m]")
        plt.ylabel("V(x) [V]")
        plt.title(f"Potenciales Individuales que Actúan sobre Carga {idx_carga}")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xlim(-5, 5)
        plt.tight_layout()
        
        imagen_1 = self._crear_nombre_archivo("potenciales_individuales_superposicion")
        plt.savefig(imagen_1, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado como '{imagen_1}'")
        plt.show()
        
        # SEGUNDO GRÁFICO: Superposición total
        fig2 = plt.figure(figsize=(14, 8))
        plt.plot(x, V_total, linewidth=3, color='blue', 
                 label="V SUPERPOSICIÓN (todas las cargas contribuyentes)")
        
        # Marcar posición donde se calculó el potencial
        plt.axvline(punto_x, color='purple', linestyle=':', linewidth=2, alpha=0.8,
                   label=f'Punto calculado: x={punto_x}m')
        
        plt.axhline(0, linestyle="--", linewidth=0.8, color='black', alpha=0.5)
        plt.xlabel("x [m]")
        plt.ylabel("V(x) [V]")
        plt.title(f"Superposición Total - Potencial sobre Carga {idx_carga}\n"
                  f"Resultado: V={potencial_total:.2e} V")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xlim(-5, 5)
        plt.tight_layout()
        
        imagen_2 = self._crear_nombre_archivo("potencial_superposicion_total")
        plt.savefig(imagen_2, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado como '{imagen_2}'")
        plt.show()
        
        # TERCER GRÁFICO: Equipotenciales en 2D
        self.graficar_equipotenciales()

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
