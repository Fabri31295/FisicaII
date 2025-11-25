import numpy as np
import matplotlib.pyplot as plt

# Constante de permeabilidad magnética del vacío
MU_0 = 4 * np.pi * 1e-7  # T·m/A

class BiotSavart:
    """
    Clase para calcular campos magnéticos usando la ley de Biot-Savart
    """
    
    def __init__(self):
        self.corriente = None
        self.punto = None
    
    def cargar_datos(self):
        """Carga los datos del usuario"""
        print("=== CÁLCULO DE CAMPO MAGNÉTICO CON BIOT-SAVART ===\n")
        
        self.corriente = float(input("Ingrese la corriente I (en amperios): "))
        
        punto_str = input("Ingrese el punto P donde calcular el campo (x y z): ")
        coords = punto_str.split()
        self.punto = np.array([float(coords[0]), float(coords[1]), float(coords[2])])
        
        print(f"\nDatos cargados:")
        print(f"Corriente: I = {self.corriente} A")
        print(f"Punto: P = ({self.punto[0]}, {self.punto[1]}, {self.punto[2]}) m")
    
    def campo_alambre_recto(self, longitud=2.0, N=5000):
        """
        Calcula el campo magnético de un alambre recto de longitud L
        usando la ley de Biot-Savart
        
        Parámetros:
        - longitud: longitud del alambre en metros (default: 2.0 m)
        - N: número de segmentos para la integración numérica
        """
        print(f"\n--- CAMPO DE ALAMBRE RECTO (L = {longitud} m) ---")
        
        # Dividir el alambre en N segmentos pequeños
        z_alambre = np.linspace(-longitud/2, longitud/2, N)
        dz = z_alambre[1] - z_alambre[0]  # longitud de cada segmento
        
        # Vector campo magnético total
        B_total = np.array([0.0, 0.0, 0.0])
        
        # Punto donde calculamos el campo
        x, y, z = self.punto[0], self.punto[1], self.punto[2]
        
        for i, z_i in enumerate(z_alambre):
            # Posición del elemento de corriente
            r_fuente = np.array([0, 0, z_i])
            
            # Vector desde el elemento de corriente hasta el punto P
            r_vector = self.punto - r_fuente
            r_magnitud = np.linalg.norm(r_vector)
            
            # Evitar división por cero
            if r_magnitud < 1e-10:
                continue
            
            # Elemento de corriente (alambre en dirección z)
            dl = np.array([0, 0, dz])
            
            # Ley de Biot-Savart: dB = (μ₀/4π) * I * (dl × r) / |r|³
            producto_cruz = np.cross(dl, r_vector)
            dB = (MU_0 / (4 * np.pi)) * self.corriente * producto_cruz / (r_magnitud**3)
            
            B_total += dB
        
        return B_total
    
    def campo_espira_circular(self, radio=3.0, N=5000):
        """
        Calcula el campo magnético de una espira circular de radio a
        usando la ley de Biot-Savart
        
        Parámetros:
        - radio: radio de la espira en metros (default: 3.0 m)
        - N: número de segmentos para la integración numérica
        """
        print(f"\n--- CAMPO DE ESPIRA CIRCULAR (a = {radio} m) ---")
        
        # Parametrizar la espira circular en el plano xy
        phi = np.linspace(0, 2*np.pi, N)
        dphi = phi[1] - phi[0]
        
        # Vector campo magnético total
        B_total = np.array([0.0, 0.0, 0.0])
        
        for i, phi_i in enumerate(phi):
            # Posición del elemento de corriente en la espira
            x_esp = radio * np.cos(phi_i)
            y_esp = radio * np.sin(phi_i)
            z_esp = 0.0
            r_fuente = np.array([x_esp, y_esp, z_esp])
            
            # Vector desde el elemento de corriente hasta el punto P
            r_vector = self.punto - r_fuente
            r_magnitud = np.linalg.norm(r_vector)
            
            # Evitar división por cero
            if r_magnitud < 1e-10:
                continue
            
            # Elemento de longitud tangente a la espira
            dl = radio * dphi * np.array([-np.sin(phi_i), np.cos(phi_i), 0])
            
            # Ley de Biot-Savart: dB = (μ₀/4π) * I * (dl × r) / |r|³
            producto_cruz = np.cross(dl, r_vector)
            dB = (MU_0 / (4 * np.pi)) * self.corriente * producto_cruz / (r_magnitud**3)
            
            B_total += dB
        
        return B_total
    
    def mostrar_resultados(self, B_alambre, B_espira):
        """Muestra los resultados de forma clara"""
        print("\n" + "="*60)
        print("RESULTADOS DEL CAMPO MAGNÉTICO")
        print("="*60)
        
        print(f"\nPunto de cálculo: P = ({self.punto[0]}, {self.punto[1]}, {self.punto[2]}) m")
        print(f"Corriente: I = {self.corriente} A")
        
        print(f"\n1. ALAMBRE RECTO (L = 2 m):")
        print(f"   Bx = {B_alambre[0]:.6e} T")
        print(f"   By = {B_alambre[1]:.6e} T") 
        print(f"   Bz = {B_alambre[2]:.6e} T")
        print(f"   |B| = {np.linalg.norm(B_alambre):.6e} T")
        
        print(f"\n2. ESPIRA CIRCULAR (a = 3 m):")
        print(f"   Bx = {B_espira[0]:.6e} T")
        print(f"   By = {B_espira[1]:.6e} T")
        print(f"   Bz = {B_espira[2]:.6e} T")
        print(f"   |B| = {np.linalg.norm(B_espira):.6e} T")
        
        print("\n¿Qué significan estos resultados?")
        print("- El campo magnético es un vector con componentes (Bx, By, Bz)")
        print("- |B| es la magnitud total del campo magnético")
        print("- Las unidades están en Tesla (T)")
    
    def calcular_campo_en_grilla(self, tipo='alambre', rango=5, resolucion=20):
        """
        Calcula el campo magnético en una grilla de puntos para visualización
        
        Parámetros:
        - tipo: 'alambre' o 'espira'
        - rango: rango espacial para la grilla
        - resolucion: número de puntos por dimensión
        """
        if tipo == 'alambre':
            # Para alambre, crear grilla en plano XY (alambre está en Z)
            x = np.linspace(-rango, rango, resolucion)
            y = np.linspace(-rango, rango, resolucion)
            X, Y = np.meshgrid(x, y)
            Z = np.zeros_like(X)  # Plano z=0
            
            Bx = np.zeros_like(X)
            By = np.zeros_like(Y)
            Bz = np.zeros_like(X)
            
            print(f"Calculando campo magnético en {resolucion}x{resolucion} puntos para alambre...")
            
            for i in range(resolucion):
                for j in range(resolucion):
                    # Guardar punto original
                    punto_original = self.punto.copy()
                    
                    # Calcular campo en este punto
                    self.punto = np.array([X[i,j], Y[i,j], Z[i,j]])
                    
                    # Evitar puntos muy cerca del alambre
                    if np.sqrt(X[i,j]**2 + Y[i,j]**2) < 0.1:
                        Bx[i,j] = By[i,j] = Bz[i,j] = 0
                    else:
                        B = self.campo_alambre_recto(longitud=2.0, N=1000)  # Menos puntos para velocidad
                        Bx[i,j] = B[0]
                        By[i,j] = B[1]
                        Bz[i,j] = B[2]
                    
                    # Restaurar punto original
                    self.punto = punto_original
            
            return X, Y, Z, Bx, By, Bz
            
        elif tipo == 'espira':
            # Para espira, crear grilla en plano XZ (espira está en XY)
            x = np.linspace(-rango, rango, resolucion)
            z = np.linspace(-rango, rango, resolucion)
            X, Z = np.meshgrid(x, z)
            Y = np.zeros_like(X)  # Plano y=0
            
            Bx = np.zeros_like(X)
            By = np.zeros_like(Y)
            Bz = np.zeros_like(Z)
            
            print(f"Calculando campo magnético en {resolucion}x{resolucion} puntos para espira...")
            
            for i in range(resolucion):
                for j in range(resolucion):
                    # Guardar punto original
                    punto_original = self.punto.copy()
                    
                    # Calcular campo en este punto
                    self.punto = np.array([X[i,j], Y[i,j], Z[i,j]])
                    
                    # Evitar puntos muy cerca de la espira
                    distancia_espira = abs(np.sqrt(X[i,j]**2 + Y[i,j]**2) - 3.0)
                    if distancia_espira < 0.2 and abs(Z[i,j]) < 0.2:
                        Bx[i,j] = By[i,j] = Bz[i,j] = 0
                    else:
                        B = self.campo_espira_circular(radio=3.0, N=1000)  # Menos puntos para velocidad
                        Bx[i,j] = B[0]
                        By[i,j] = B[1]
                        Bz[i,j] = B[2]
                    
                    # Restaurar punto original
                    self.punto = punto_original
            
            return X, Y, Z, Bx, By, Bz

    def graficar_lineas_campo_alambre(self):
        """Grafica las líneas de campo magnético del alambre recto"""
        print("Generando visualización del campo magnético para alambre recto...")
        
        # Calcular campo en grilla
        X, Y, Z, Bx, By, Bz = self.calcular_campo_en_grilla('alambre', rango=4, resolucion=15)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Gráfico 1: Vista superior (plano XY) - Vectores de campo
        magnitud = np.sqrt(Bx**2 + By**2 + Bz**2)
        magnitud[magnitud == 0] = 1e-10  # Evitar división por cero
        
        # Normalizar vectores para mejor visualización
        Bx_norm = Bx / magnitud
        By_norm = By / magnitud
        
        # Dibujar vectores de campo
        skip = 1  # Mostrar todos los vectores
        im1 = ax1.quiver(X[::skip,::skip], Y[::skip,::skip], 
                        Bx_norm[::skip,::skip], By_norm[::skip,::skip],
                        magnitud[::skip,::skip], 
                        cmap='plasma', scale=20, alpha=0.8)
        
        # En el plano z=0, el alambre se muestra como un punto en el centro
        ax1.scatter(0, 0, color='red', s=120, marker='o', zorder=5)
        
        # Dibujar punto de cálculo original
        punto_original = self.punto
        if abs(punto_original[2]) < 0.5:  # Si está cerca del plano z=0
            ax1.scatter(punto_original[0], punto_original[1], 
                       color='blue', s=150, marker='*', 
                       label=f'Punto P({punto_original[0]:.1f},{punto_original[1]:.1f},{punto_original[2]:.1f})',
                       zorder=7, edgecolor='white', linewidth=2)
        
        ax1.set_xlabel('X (m)', fontsize=12)
        ax1.set_ylabel('Y (m)', fontsize=12)
        ax1.set_title('Campo Magnético - Alambre Recto\n(Vista superior, plano Z=0)', fontsize=14)
        ax1.grid(True, alpha=0.3)
        ax1.set_aspect('equal')
        ax1.legend()
        
        # Barra de color para magnitud
        cbar1 = plt.colorbar(im1, ax=ax1)
        cbar1.set_label('|B| (T)', fontsize=12)
        
        # Gráfico 2: Líneas de campo circulares
        theta = np.linspace(0, 2*np.pi, 100)
        radios = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
        
        for r in radios:
            x_circ = r * np.cos(theta)
            y_circ = r * np.sin(theta)
            ax2.plot(x_circ, y_circ, 'b--', alpha=0.6, linewidth=1)
        
        # Dibujar alambre
        ax2.plot([0, 0], [-1, 1], 'r-', linewidth=6, label='Alambre (I)')
        ax2.plot([0, 0], [-1, 1], 'w-', linewidth=2)
        
        # Flechas indicando dirección del campo (regla de la mano derecha)
        for r in [1.0, 2.0, 3.0]:
            # Flechas cada 45 grados
            for angle in np.arange(0, 2*np.pi, np.pi/4):
                x_arrow = r * np.cos(angle)
                y_arrow = r * np.sin(angle)
                # Dirección tangencial (perpendicular al radio)
                dx = -np.sin(angle) * 0.2
                dy = np.cos(angle) * 0.2
                ax2.arrow(x_arrow, y_arrow, dx, dy, 
                         head_width=0.1, head_length=0.1, 
                         fc='green', ec='green', alpha=0.7)
        
        ax2.set_xlabel('X (m)', fontsize=12)
        ax2.set_ylabel('Y (m)', fontsize=12)
        ax2.set_title('Líneas de Campo Magnético\n(Circulares alrededor del alambre)', fontsize=14)
        ax2.grid(True, alpha=0.3)
        ax2.set_aspect('equal')
        ax2.legend()
        ax2.set_xlim(-4, 4)
        ax2.set_ylim(-4, 4)
        
        plt.tight_layout()
        plt.show()

    def graficar_lineas_campo_espira(self):
        """Grafica las líneas de campo magnético de la espira circular"""
        print("Generando visualización del campo magnético para espira circular...")
        
        # Calcular campo en grilla
        X, Y, Z, Bx, By, Bz = self.calcular_campo_en_grilla('espira', rango=6, resolucion=15)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Gráfico 1: Vista lateral (plano XZ) - Vectores de campo
        magnitud = np.sqrt(Bx**2 + By**2 + Bz**2)
        magnitud[magnitud == 0] = 1e-10  # Evitar división por cero
        
        # Normalizar vectores para mejor visualización
        Bx_norm = Bx / magnitud
        Bz_norm = Bz / magnitud
        
        # Dibujar vectores de campo
        skip = 1
        im1 = ax1.quiver(X[::skip,::skip], Z[::skip,::skip], 
                        Bx_norm[::skip,::skip], Bz_norm[::skip,::skip],
                        magnitud[::skip,::skip], 
                        cmap='plasma', scale=20, alpha=0.8)
        
        # Dibujar espira (vista lateral)
        ax1.plot([-3, 3], [0, 0], 'g-', linewidth=6, label='Espira (I)', zorder=5)
        ax1.plot([-3, 3], [0, 0], 'w-', linewidth=2, zorder=6)
        
        # Puntos en los extremos de la espira
        ax1.scatter([-3, 3], [0, 0], color='green', s=100, zorder=7)
        
        # Punto de cálculo original
        punto_original = self.punto
        if abs(punto_original[1]) < 0.5:  # Si está cerca del plano y=0
            ax1.scatter(punto_original[0], punto_original[2], 
                       color='blue', s=150, marker='*', 
                       label=f'Punto P({punto_original[0]:.1f},{punto_original[1]:.1f},{punto_original[2]:.1f})',
                       zorder=7, edgecolor='white', linewidth=2)
        
        ax1.set_xlabel('X (m)', fontsize=12)
        ax1.set_ylabel('Z (m)', fontsize=12)
        ax1.set_title('Campo Magnético - Espira Circular\n(Vista lateral, plano Y=0)', fontsize=14)
        ax1.grid(True, alpha=0.3)
        ax1.set_aspect('equal')
        ax1.legend()
        
        # Barra de color
        cbar1 = plt.colorbar(im1, ax=ax1)
        cbar1.set_label('|B| (T)', fontsize=12)
        
        # Gráfico 2: Vista superior (plano XY) mostrando la espira
        ax2_angles = np.linspace(0, 2*np.pi, 100)
        espira_x = 3 * np.cos(ax2_angles)
        espira_y = 3 * np.sin(ax2_angles)
        
        # Dibujar espira
        ax2.plot(espira_x, espira_y, 'g-', linewidth=6, label='Espira (I)')
        ax2.plot(espira_x, espira_y, 'w-', linewidth=2)
        
        # Dibujar algunas líneas de campo características de una espira
        # (patrón dipolar)
        theta_lines = np.linspace(0, 2*np.pi, 8)
        for theta in theta_lines:
            # Líneas que salen del centro hacia afuera
            r_line = np.linspace(0.5, 5, 50)
            x_line = r_line * np.cos(theta)
            y_line = r_line * np.sin(theta)
            ax2.plot(x_line, y_line, 'b--', alpha=0.4, linewidth=1)
        
        # Flechas indicando dirección del campo en el eje
        ax2.annotate('', xy=(0, 0.5), xytext=(0, -0.5),
                    arrowprops=dict(arrowstyle='->', color='red', lw=3))
        ax2.text(0.2, 0, 'B (hacia arriba)', fontsize=10, color='red')
        
        ax2.set_xlabel('X (m)', fontsize=12)
        ax2.set_ylabel('Y (m)', fontsize=12)
        ax2.set_title('Espira Circular\n(Vista superior, plano Z=0)', fontsize=14)
        ax2.grid(True, alpha=0.3)
        ax2.set_aspect('equal')
        ax2.legend()
        ax2.set_xlim(-6, 6)
        ax2.set_ylim(-6, 6)
        
        plt.tight_layout()
        plt.show()

    def graficar_configuracion(self):
        """Grafica la configuración básica del problema"""
        fig = plt.figure(figsize=(15, 5))
        
        # Gráfico 1: Alambre recto
        ax1 = fig.add_subplot(131, projection='3d')
        
        # Dibujar alambre
        z_alambre = np.linspace(-1, 1, 100)
        x_alambre = np.zeros_like(z_alambre)
        y_alambre = np.zeros_like(z_alambre)
        ax1.plot(x_alambre, y_alambre, z_alambre, 'r-', linewidth=3, label='Alambre (I)')
        
        # Dibujar punto
        ax1.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='blue', s=100, label=f'Punto P({self.punto[0]},{self.punto[1]},{self.punto[2]})')
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('Alambre Recto\n(L = 2 m)')
        ax1.legend()
        ax1.grid(True)
        
        # Gráfico 2: Espira circular
        ax2 = fig.add_subplot(132, projection='3d')
        
        # Dibujar espira
        phi = np.linspace(0, 2*np.pi, 100)
        x_esp = 3 * np.cos(phi)  # radio = 3
        y_esp = 3 * np.sin(phi)
        z_esp = np.zeros_like(phi)
        ax2.plot(x_esp, y_esp, z_esp, 'g-', linewidth=3, label='Espira (I)')
        
        # Dibujar punto
        ax2.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='blue', s=100, label=f'Punto P({self.punto[0]},{self.punto[1]},{self.punto[2]})')
        
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
        ax2.set_zlabel('Z (m)')
        ax2.set_title('Espira Circular\n(a = 3 m)')
        ax2.legend()
        ax2.grid(True)
        
        # Gráfico 3: Información
        ax3 = fig.add_subplot(133)
        ax3.axis('off')
        
        info_text = f"""
LEY DE BIOT-SAVART

dB = (μ₀/4π) × I × (dl × r) / |r|³

Donde:
• μ₀ = 4π × 10⁻⁷ T·m/A
• I = {self.corriente} A
• dl = elemento de longitud
• r = vector posición
• P = ({self.punto[0]}, {self.punto[1]}, {self.punto[2]}) m

El campo total se obtiene
integrando sobre toda la
geometría del conductor.
        """
        
        ax3.text(0.1, 0.5, info_text, fontsize=10, 
                verticalalignment='center', fontfamily='monospace')
        
        plt.tight_layout()
        plt.show()


    def graficar_lineas_campo_3d_alambre(self):
        """Grafica las líneas de campo magnético del alambre recto en 3D"""
        print("Generando visualización 3D del campo magnético para alambre recto...")
        
        fig = plt.figure(figsize=(15, 12))
        
        # Gráfico 1: Líneas de campo circulares en 3D
        ax1 = fig.add_subplot(221, projection='3d')
        
        # Dibujar alambre
        z_alambre = np.linspace(-1, 1, 100)
        x_alambre = np.zeros_like(z_alambre)
        y_alambre = np.zeros_like(z_alambre)
        ax1.plot(x_alambre, y_alambre, z_alambre, 'r-', linewidth=6, label='Alambre (I)', zorder=10)
        
        # Generar líneas de campo circulares a diferentes alturas z
        radios = [0.5, 1.0, 1.5, 2.0, 2.5]
        alturas = np.linspace(-0.8, 0.8, 5)
        theta = np.linspace(0, 2*np.pi, 100)
        
        colors = plt.cm.plasma(np.linspace(0, 1, len(radios)))
        
        for i, r in enumerate(radios):
            for z_nivel in alturas:
                x_circ = r * np.cos(theta)
                y_circ = r * np.sin(theta)
                z_circ = np.full_like(theta, z_nivel)
                
                ax1.plot(x_circ, y_circ, z_circ, color=colors[i], 
                        alpha=0.7, linewidth=2)
                
                # Agregar flechas direccionales cada 60 grados
                for angle_idx in range(0, len(theta), len(theta)//6):
                    angle = theta[angle_idx]
                    x_arrow = r * np.cos(angle)
                    y_arrow = r * np.sin(angle)
                    z_arrow = z_nivel
                    
                    # Dirección tangencial (perpendicular al radio)
                    dx = -np.sin(angle) * 0.2
                    dy = np.cos(angle) * 0.2
                    dz = 0
                    
                    ax1.quiver(x_arrow, y_arrow, z_arrow, dx, dy, dz,
                             color='green', arrow_length_ratio=0.3, alpha=0.8)
        
        # Punto de cálculo
        ax1.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='blue', s=150, marker='*', 
                   label=f'P({self.punto[0]:.1f},{self.punto[1]:.1f},{self.punto[2]:.1f})',
                   zorder=15)
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('Líneas de Campo 3D - Alambre Recto')
        ax1.legend()
        ax1.set_xlim(-3, 3)
        ax1.set_ylim(-3, 3)
        ax1.set_zlim(-1.5, 1.5)
        
        # Gráfico 2: Campo vectorial en plano XY
        ax2 = fig.add_subplot(222, projection='3d')
        
        # Crear grilla para vectores
        x_grid = np.linspace(-2.5, 2.5, 8)
        y_grid = np.linspace(-2.5, 2.5, 8)
        z_levels = [-0.5, 0, 0.5]
        
        # Dibujar alambre
        ax2.plot(x_alambre, y_alambre, z_alambre, 'r-', linewidth=6, label='Alambre (I)')
        
        for z_level in z_levels:
            X_grid, Y_grid = np.meshgrid(x_grid, y_grid)
            Z_grid = np.full_like(X_grid, z_level)
            
            Bx_grid = np.zeros_like(X_grid)
            By_grid = np.zeros_like(Y_grid)
            Bz_grid = np.zeros_like(Z_grid)
            
            punto_original = self.punto.copy()
            
            for i in range(X_grid.shape[0]):
                for j in range(X_grid.shape[1]):
                    x_pos, y_pos, z_pos = X_grid[i,j], Y_grid[i,j], Z_grid[i,j]
                    
                    # Evitar puntos muy cerca del alambre
                    if np.sqrt(x_pos**2 + y_pos**2) < 0.3:
                        continue
                    
                    self.punto = np.array([x_pos, y_pos, z_pos])
                    B = self.campo_alambre_recto(longitud=2.0, N=500)
                    
                    Bx_grid[i,j] = B[0]
                    By_grid[i,j] = B[1]
                    Bz_grid[i,j] = B[2]
            
            self.punto = punto_original
            
            # Normalizar para visualización
            B_mag = np.sqrt(Bx_grid**2 + By_grid**2 + Bz_grid**2)
            B_mag[B_mag == 0] = 1e-10
            
            scale_factor = 0.3
            ax2.quiver(X_grid, Y_grid, Z_grid, 
                      Bx_grid/B_mag*scale_factor, By_grid/B_mag*scale_factor, Bz_grid/B_mag*scale_factor,
                      color='blue' if z_level == 0 else 'cyan', alpha=0.8, arrow_length_ratio=0.2)
        
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
        ax2.set_zlabel('Z (m)')
        ax2.set_title('Campo Vectorial 3D - Alambre Recto')
        ax2.legend()
        
        # Gráfico 3: Vista superior con intensidad de campo
        ax3 = fig.add_subplot(223)
        
        # Calcular intensidad en plano z=0
        x_intensity = np.linspace(-3, 3, 50)
        y_intensity = np.linspace(-3, 3, 50)
        X_int, Y_int = np.meshgrid(x_intensity, y_intensity)
        
        B_intensity = np.zeros_like(X_int)
        punto_original = self.punto.copy()
        
        for i in range(X_int.shape[0]):
            for j in range(X_int.shape[1]):
                x_pos, y_pos = X_int[i,j], Y_int[i,j]
                
                if np.sqrt(x_pos**2 + y_pos**2) < 0.1:
                    B_intensity[i,j] = np.nan
                    continue
                
                self.punto = np.array([x_pos, y_pos, 0])
                B = self.campo_alambre_recto(longitud=2.0, N=300)
                B_intensity[i,j] = np.log10(np.linalg.norm(B) + 1e-12)
        
        self.punto = punto_original
        
        # Mapa de contorno
        contour = ax3.contourf(X_int, Y_int, B_intensity, levels=20, cmap='plasma')
        ax3.contour(X_int, Y_int, B_intensity, levels=20, colors='black', alpha=0.3, linewidths=0.5)
        
        # Líneas de campo circulares (equipotenciales magnéticas)
        for r in [0.5, 1.0, 1.5, 2.0, 2.5]:
            circle_theta = np.linspace(0, 2*np.pi, 100)
            x_circle = r * np.cos(circle_theta)
            y_circle = r * np.sin(circle_theta)
            ax3.plot(x_circle, y_circle, 'w--', alpha=0.6, linewidth=1)
        
        ax3.set_xlabel('X (m)')
        ax3.set_ylabel('Y (m)')
        ax3.set_title('Intensidad del Campo Magnético')
        ax3.set_aspect('equal')
        
        # Agregar texto indicativo de la posición del alambre
        ax3.text(0.02, 0.98, '', 
                transform=ax3.transAxes, fontsize=8, 
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        plt.colorbar(contour, ax=ax3, label='log₁₀|B| (T)')
        
        # Gráfico 4: Información y teoría
        ax4 = fig.add_subplot(224)
        ax4.axis('off')
        
        info_text = f"""
ALAMBRE RECTO - CAMPO MAGNÉTICO 3D

Ley de Biot-Savart:
dB = (μ₀/4π) × I × (dl × r) / |r|³

Características del alambre:
• Longitud: L = 2 m
• Corriente: I = {self.corriente} A
• Orientación: Eje Z

Patrón del campo:
• Líneas circulares concéntricas
• Perpendiculares al alambre
• Intensidad ∝ 1/r

Regla de la mano derecha:
• Pulgar: dirección de corriente
• Dedos: dirección del campo

Punto de cálculo:
P = ({self.punto[0]:.1f}, {self.punto[1]:.1f}, {self.punto[2]:.1f}) m

El campo es más intenso cerca
del alambre y decrece con la
distancia radial.
        """
        
        ax4.text(0.05, 0.95, info_text, fontsize=10, 
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.5))
        
        plt.tight_layout()
        plt.show()

    def graficar_lineas_campo_3d_espira(self):
        """Grafica las líneas de campo magnético de la espira circular en 3D"""
        print("Generando visualización 3D del campo magnético para espira circular...")
        
        fig = plt.figure(figsize=(16, 12))
        
        # Gráfico 1: Líneas de campo dipolar en 3D
        ax1 = fig.add_subplot(221, projection='3d')
        
        # Dibujar espira
        phi_espira = np.linspace(0, 2*np.pi, 100)
        x_espira = 3 * np.cos(phi_espira)
        y_espira = 3 * np.sin(phi_espira)
        z_espira = np.zeros_like(phi_espira)
        ax1.plot(x_espira, y_espira, z_espira, 'g-', linewidth=8, label='Espira (I)', zorder=10)
        
        # Generar líneas de campo dipolar
        # Líneas que salen del eje y se curvan
        phi_lines = np.linspace(0, 2*np.pi, 8)
        
        for phi in phi_lines:
            # Líneas desde el centro hacia afuera y curvándose
            t = np.linspace(0.1, 4, 50)
            
            # Líneas superiores (saliendo hacia arriba)
            for z_start in [0.2, 0.5, 1.0]:
                r = t
                z_line = z_start + t**0.7
                x_line = r * np.cos(phi)
                y_line = r * np.sin(phi)
                
                # Solo mostrar líneas que no intersecten la espira
                mask = (r > 3.2) | (np.abs(z_line) > 0.1)
                
                ax1.plot(x_line[mask], y_line[mask], z_line[mask], 
                        'b-', alpha=0.7, linewidth=1.5)
                
                # Líneas inferiores (entrando por abajo)
                z_line_neg = -z_start - t**0.7
                ax1.plot(x_line[mask], y_line[mask], z_line_neg[mask], 
                        'b-', alpha=0.7, linewidth=1.5)
        
        # Líneas en el eje central
        z_axis = np.linspace(-2, 2, 50)
        x_axis = np.zeros_like(z_axis)
        y_axis = np.zeros_like(z_axis)
        ax1.plot(x_axis, y_axis, z_axis, 'b-', linewidth=3, alpha=0.8)
        
        # Flechas en el eje indicando dirección
        for z_arrow in [-1.5, -1, -0.5, 0.5, 1, 1.5]:
            ax1.quiver(0, 0, z_arrow, 0, 0, 0.2,
                     color='red', arrow_length_ratio=0.5, alpha=0.9, linewidth=2)
        
        # Punto de cálculo
        ax1.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='blue', s=150, marker='*', 
                   label=f'P({self.punto[0]:.1f},{self.punto[1]:.1f},{self.punto[2]:.1f})',
                   zorder=15)
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('Líneas de Campo 3D - Espira Circular')
        ax1.legend()
        ax1.set_xlim(-5, 5)
        ax1.set_ylim(-5, 5)
        ax1.set_zlim(-3, 3)
        
        # Gráfico 2: Campo vectorial en varios planos
        ax2 = fig.add_subplot(222, projection='3d')
        
        # Dibujar espira
        ax2.plot(x_espira, y_espira, z_espira, 'g-', linewidth=8, label='Espira (I)')
        
        # Crear grilla para vectores en el plano XZ (y=0)
        x_vec = np.linspace(-4, 4, 8)
        z_vec = np.linspace(-3, 3, 6)
        X_vec, Z_vec = np.meshgrid(x_vec, z_vec)
        Y_vec = np.zeros_like(X_vec)
        
        Bx_vec = np.zeros_like(X_vec)
        By_vec = np.zeros_like(Y_vec)
        Bz_vec = np.zeros_like(Z_vec)
        
        punto_original = self.punto.copy()
        
        for i in range(X_vec.shape[0]):
            for j in range(X_vec.shape[1]):
                x_pos, y_pos, z_pos = X_vec[i,j], Y_vec[i,j], Z_vec[i,j]
                
                # Evitar puntos muy cerca de la espira
                dist_espira = abs(np.sqrt(x_pos**2 + y_pos**2) - 3.0)
                if dist_espira < 0.5 and abs(z_pos) < 0.3:
                    continue
                
                self.punto = np.array([x_pos, y_pos, z_pos])
                B = self.campo_espira_circular(radio=3.0, N=500)
                
                Bx_vec[i,j] = B[0]
                By_vec[i,j] = B[1]
                Bz_vec[i,j] = B[2]
        
        self.punto = punto_original
        
        # Normalizar vectores
        B_mag = np.sqrt(Bx_vec**2 + By_vec**2 + Bz_vec**2)
        B_mag[B_mag == 0] = 1e-10
        
        scale_factor = 0.4
        ax2.quiver(X_vec, Y_vec, Z_vec, 
                  Bx_vec/B_mag*scale_factor, By_vec/B_mag*scale_factor, Bz_vec/B_mag*scale_factor,
                  color='blue', alpha=0.8, arrow_length_ratio=0.2)
        
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
        ax2.set_zlabel('Z (m)')
        ax2.set_title('Campo Vectorial 3D - Espira Circular\n(Plano XZ, Y=0)')
        ax2.legend()
        
        # Gráfico 3: Intensidad en el plano XZ
        ax3 = fig.add_subplot(223)
        
        x_int = np.linspace(-5, 5, 40)
        z_int = np.linspace(-4, 4, 32)
        X_int, Z_int = np.meshgrid(x_int, z_int)
        
        B_intensity = np.zeros_like(X_int)
        
        for i in range(X_int.shape[0]):
            for j in range(X_int.shape[1]):
                x_pos, z_pos = X_int[i,j], Z_int[i,j]
                
                # Evitar la región de la espira
                dist_espira = abs(np.sqrt(x_pos**2) - 3.0)
                if dist_espira < 0.3 and abs(z_pos) < 0.2:
                    B_intensity[i,j] = np.nan
                    continue
                
                self.punto = np.array([x_pos, 0, z_pos])
                B = self.campo_espira_circular(radio=3.0, N=300)
                B_intensity[i,j] = np.log10(np.linalg.norm(B) + 1e-12)
        
        self.punto = punto_original
        
        # Mapa de contorno
        contour = ax3.contourf(X_int, Z_int, B_intensity, levels=20, cmap='plasma')
        ax3.contour(X_int, Z_int, B_intensity, levels=20, colors='black', alpha=0.3, linewidths=0.5)
        
        # Líneas de campo esquemáticas (solo el eje dipolar)
        ax3.annotate('', xy=(0, 1), xytext=(0, -1),
                    arrowprops=dict(arrowstyle='<->', color='white', lw=2))
        ax3.text(0.3, 0, 'Eje del dipolo', color='white', fontweight='bold')
        
        ax3.set_xlabel('X (m)')
        ax3.set_ylabel('Z (m)')
        ax3.set_title('Intensidad del Campo Magnético')
        ax3.set_aspect('equal')
        
        # Agregar texto indicativo de la posición de la espira
        ax3.text(0.02, 0.98, 'Espira: Radio=3m en Z=0\n(círculo en plano XY)', 
                transform=ax3.transAxes, fontsize=8, 
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        plt.colorbar(contour, ax=ax3, label='')
        
        # Gráfico 4: Información y teoría
        ax4 = fig.add_subplot(224)
        ax4.axis('off')
        
        info_text = f"""
ESPIRA CIRCULAR - CAMPO MAGNÉTICO 3D

Ley de Biot-Savart:
dB = (μ₀/4π) × I × (dl × r) / |r|³

Características de la espira:
• Radio: a = 3 m
• Corriente: I = {self.corriente} A
• Plano: XY (z = 0)

Patrón del campo:
• Dipolo magnético
• Líneas salen por un lado
• Entran por el otro lado
• Máximo en el eje (z)

Campo en el centro:
B₀ = μ₀I/(2a) = {(4*np.pi*1e-7*self.corriente)/(2*3):.2e} T

Campo en el eje (z ≠ 0):
B = μ₀Ia²/[2(a²+z²)^(3/2)]

Punto de cálculo:
P = ({self.punto[0]:.1f}, {self.punto[1]:.1f}, {self.punto[2]:.1f}) m

El campo es más intenso en el
centro y disminuye con la distancia.
        """
        
        ax4.text(0.05, 0.95, info_text, fontsize=9, 
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.5))
        
        plt.tight_layout()
        plt.show()

    def cargar_datos_alambre(self):
        """Carga los datos específicos para el alambre"""
        print("=== DATOS PARA ALAMBRE RECTO ===\n")
        
        self.corriente_alambre = float(input("Ingrese la corriente del alambre I (en amperios): "))
        
        punto_str = input("Ingrese el punto P donde calcular el campo (x y z): ")
        coords = punto_str.split()
        self.punto = np.array([float(coords[0]), float(coords[1]), float(coords[2])])
        
        print(f"\nDatos del alambre cargados:")
        print(f"Corriente alambre: I = {self.corriente_alambre} A")
        print(f"Punto: P = ({self.punto[0]}, {self.punto[1]}, {self.punto[2]}) m")
        print(f"Alambre: L = 2 m en eje Z")

    def cargar_datos_espira(self):
        """Carga los datos específicos para la espira"""
        print("=== DATOS PARA ESPIRA CIRCULAR ===\n")
        
        self.corriente_espira = float(input("Ingrese la corriente de la espira I (en amperios): "))
        
        punto_str = input("Ingrese el punto P donde calcular el campo (x y z): ")
        coords = punto_str.split()
        self.punto = np.array([float(coords[0]), float(coords[1]), float(coords[2])])
        
        print(f"\nDatos de la espira cargados:")
        print(f"Corriente espira: I = {self.corriente_espira} A")
        print(f"Punto: P = ({self.punto[0]}, {self.punto[1]}, {self.punto[2]}) m")
        print(f"Espira: a = 3 m en plano XY")

    def calcular_campo_alambre(self):
        """Calcula el campo magnético del alambre"""
        if not hasattr(self, 'corriente_alambre'):
            print("Error: Primero debe cargar los datos del alambre")
            return None
        
        # Configurar para cálculo del alambre
        corriente_original = getattr(self, 'corriente', None)
        self.corriente = self.corriente_alambre
        
        # Calcular campo
        self.B_alambre = self.campo_alambre_recto(longitud=2.0, N=5000)
        
        # Restaurar corriente original si existía
        if corriente_original is not None:
            self.corriente = corriente_original
        
        return self.B_alambre

    def calcular_campo_espira(self):
        """Calcula el campo magnético de la espira"""
        if not hasattr(self, 'corriente_espira'):
            print("Error: Primero debe cargar los datos de la espira")
            return None
        
        # Configurar para cálculo de la espira
        corriente_original = getattr(self, 'corriente', None)
        self.corriente = self.corriente_espira
        
        # Calcular campo
        self.B_espira = self.campo_espira_circular(radio=3.0, N=5000)
        
        # Restaurar corriente original si existía
        if corriente_original is not None:
            self.corriente = corriente_original
        
        return self.B_espira

    def mostrar_resultados_alambre(self):
        """Muestra los resultados del alambre"""
        if not hasattr(self, 'B_alambre'):
            print("Error: Primero debe calcular el campo del alambre")
            return
        
        print("\n" + "="*60)
        print("RESULTADOS DEL CAMPO MAGNÉTICO - ALAMBRE RECTO")
        print("="*60)
        
        print(f"\nPunto de cálculo: P = ({self.punto[0]}, {self.punto[1]}, {self.punto[2]}) m")
        print(f"Corriente: I = {self.corriente_alambre} A")
        print(f"Longitud: L = 2 m (eje Z)")
        
        print(f"\nCampo magnético del alambre:")
        print(f"   Bx = {self.B_alambre[0]:.6e} T")
        print(f"   By = {self.B_alambre[1]:.6e} T")
        print(f"   Bz = {self.B_alambre[2]:.6e} T")
        print(f"   |B| = {np.linalg.norm(self.B_alambre):.6e} T")
        
        print("\n¿Qué significa este resultado?")
        print("- El alambre genera un campo circular perpendicular a su eje")
        print("- La intensidad disminuye con la distancia radial al alambre")
        print("- La dirección sigue la regla de la mano derecha")

    def mostrar_resultados_espira(self):
        """Muestra los resultados de la espira"""
        if not hasattr(self, 'B_espira'):
            print("Error: Primero debe calcular el campo de la espira")
            return
        
        print("\n" + "="*60)
        print("RESULTADOS DEL CAMPO MAGNÉTICO - ESPIRA CIRCULAR")
        print("="*60)
        
        print(f"\nPunto de cálculo: P = ({self.punto[0]}, {self.punto[1]}, {self.punto[2]}) m")
        print(f"Corriente: I = {self.corriente_espira} A")
        print(f"Radio: a = 3 m (plano XY)")
        
        print(f"\nCampo magnético de la espira:")
        print(f"   Bx = {self.B_espira[0]:.6e} T")
        print(f"   By = {self.B_espira[1]:.6e} T")
        print(f"   Bz = {self.B_espira[2]:.6e} T")
        print(f"   |B| = {np.linalg.norm(self.B_espira):.6e} T")
        
        print("\n¿Qué significa este resultado?")
        print("- La espira genera un campo dipolar magnético")
        print("- El campo es máximo en el eje (componente Z)")
        print("- La intensidad disminuye con la distancia al centro")

    def graficar_configuracion_alambre(self):
        """Grafica la configuración del alambre"""
        if not hasattr(self, 'corriente_alambre'):
            print("Error: Primero debe cargar los datos del alambre")
            return
        
        fig = plt.figure(figsize=(12, 8))
        
        # Gráfico 1: Vista 3D
        ax1 = fig.add_subplot(121, projection='3d')
        
        # Dibujar alambre
        z_alambre = np.linspace(-1, 1, 100)
        x_alambre = np.zeros_like(z_alambre)
        y_alambre = np.zeros_like(z_alambre)
        ax1.plot(x_alambre, y_alambre, z_alambre, 'r-', linewidth=6, label=f'Alambre I={self.corriente_alambre}A')
        
        # Dibujar punto de cálculo
        ax1.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='blue', s=150, marker='*', 
                   label=f'P({self.punto[0]:.1f},{self.punto[1]:.1f},{self.punto[2]:.1f})')
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('Alambre Recto - Vista 3D')
        ax1.legend()
        ax1.grid(True)
        ax1.set_xlim(-2, 2)
        ax1.set_ylim(-2, 2)
        ax1.set_zlim(-1.5, 1.5)
        
        # Gráfico 2: Información
        ax2 = fig.add_subplot(122)
        ax2.axis('off')
        
        info_text = f"""
ALAMBRE RECTO - CONFIGURACIÓN

Parámetros:
• Corriente: I = {self.corriente_alambre} A
• Longitud: L = 2 m
• Orientación: Eje Z
• Punto: P = ({self.punto[0]:.1f}, {self.punto[1]:.1f}, {self.punto[2]:.1f}) m

Ley de Biot-Savart:
dB⃗ = (μ₀/4π) × I × (dl⃗ × r⃗) / |r⃗|³

Características del campo:
• Líneas circulares concéntricas
• Perpendiculares al alambre
• Intensidad ∝ 1/r (distancia radial)

Regla de la mano derecha:
• Pulgar: dirección de corriente (+Z)
• Dedos: dirección del campo (circular)
        """
        
        ax2.text(0.05, 0.95, info_text, fontsize=11, 
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.3))
        
        plt.tight_layout()
        plt.show()

    def graficar_configuracion_espira(self):
        """Grafica la configuración de la espira"""
        if not hasattr(self, 'corriente_espira'):
            print("Error: Primero debe cargar los datos de la espira")
            return
        
        fig = plt.figure(figsize=(12, 8))
        
        # Gráfico 1: Vista 3D
        ax1 = fig.add_subplot(121, projection='3d')
        
        # Dibujar espira
        phi = np.linspace(0, 2*np.pi, 100)
        x_esp = 3 * np.cos(phi)
        y_esp = 3 * np.sin(phi)
        z_esp = np.zeros_like(phi)
        ax1.plot(x_esp, y_esp, z_esp, 'g-', linewidth=6, label=f'Espira I={self.corriente_espira}A')
        
        # Dibujar punto de cálculo
        ax1.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='blue', s=150, marker='*', 
                   label=f'P({self.punto[0]:.1f},{self.punto[1]:.1f},{self.punto[2]:.1f})')
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('Espira Circular - Vista 3D')
        ax1.legend()
        ax1.grid(True)
        ax1.set_xlim(-4, 4)
        ax1.set_ylim(-4, 4)
        ax1.set_zlim(-2, 2)
        
        # Gráfico 2: Información
        ax2 = fig.add_subplot(122)
        ax2.axis('off')
        
        info_text = f"""
ESPIRA CIRCULAR - CONFIGURACIÓN

Parámetros:
• Corriente: I = {self.corriente_espira} A
• Radio: a = 3 m
• Plano: XY (z = 0)
• Punto: P = ({self.punto[0]:.1f}, {self.punto[1]:.1f}, {self.punto[2]:.1f}) m

Ley de Biot-Savart:
dB⃗ = (μ₀/4π) × I × (dl⃗ × r⃗) / |r⃗|³

Características del campo:
• Patrón dipolar magnético
• Líneas salen por un lado, entran por el otro
• Máximo en el eje (componente Z)

Campo en el centro:
B₀ = μ₀I/(2a) = {(4*np.pi*1e-7*self.corriente)/(2*3):.2e} T

Campo en el eje (z ≠ 0):
B = μ₀Ia²/[2(a²+z²)^(3/2)]
        """
        
        ax2.text(0.05, 0.95, info_text, fontsize=11, 
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.3))
        
        plt.tight_layout()
        plt.show()

    def graficar_lineas_campo_2d_alambre(self):
        """Grafica las líneas de campo 2D del alambre"""
        if not hasattr(self, 'corriente_alambre'):
            print("Error: Primero debe cargar los datos del alambre")
            return
        
        # Configurar corriente para cálculo
        corriente_original = getattr(self, 'corriente', None)
        self.corriente = self.corriente_alambre
        
        # Llamar a la función existente
        self.graficar_lineas_campo_alambre()
        
        # Restaurar corriente original
        if corriente_original is not None:
            self.corriente = corriente_original

    def graficar_lineas_campo_2d_espira(self):
        """Grafica las líneas de campo 2D de la espira"""
        if not hasattr(self, 'corriente_espira'):
            print("Error: Primero debe cargar los datos de la espira")
            return
        
        # Configurar corriente para cálculo
        corriente_original = getattr(self, 'corriente', None)
        self.corriente = self.corriente_espira
        
        # Llamar a la función existente
        self.graficar_lineas_campo_espira()
        
        # Restaurar corriente original
        if corriente_original is not None:
            self.corriente = corriente_original

    def graficar_lineas_campo_espira(self):
        """Grafica las líneas de campo magnético de la espira circular"""
        print("Generando visualización del campo magnético para espira circular...")
        
        # Calcular campo en grilla
        X, Y, Z, Bx, By, Bz = self.calcular_campo_en_grilla('espira', rango=6, resolucion=15)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Gráfico 1: Vista lateral (plano XZ) - Vectores de campo
        magnitud = np.sqrt(Bx**2 + By**2 + Bz**2)
        magnitud[magnitud == 0] = 1e-10  # Evitar división por cero
        
        # Normalizar vectores para mejor visualización
        Bx_norm = Bx / magnitud
        Bz_norm = Bz / magnitud
        
        # Dibujar vectores de campo
        skip = 1
        im1 = ax1.quiver(X[::skip,::skip], Z[::skip,::skip], 
                        Bx_norm[::skip,::skip], Bz_norm[::skip,::skip],
                        magnitud[::skip,::skip], 
                        cmap='plasma', scale=20, alpha=0.8)
        
        # Dibujar espira (vista lateral)
        ax1.plot([-3, 3], [0, 0], 'g-', linewidth=6, label='Espira (I)', zorder=5)
        ax1.plot([-3, 3], [0, 0], 'w-', linewidth=2, zorder=6)
        
        # Puntos en los extremos de la espira
        ax1.scatter([-3, 3], [0, 0], color='green', s=100, zorder=7)
        
        # Punto de cálculo original
        punto_original = self.punto
        if abs(punto_original[1]) < 0.5:  # Si está cerca del plano y=0
            ax1.scatter(punto_original[0], punto_original[2], 
                       color='blue', s=150, marker='*', 
                       label=f'Punto P({punto_original[0]:.1f},{punto_original[1]:.1f},{punto_original[2]:.1f})',
                       zorder=7, edgecolor='white', linewidth=2)
        
        ax1.set_xlabel('X (m)', fontsize=12)
        ax1.set_ylabel('Z (m)', fontsize=12)
        ax1.set_title('Campo Magnético - Espira Circular\n(Vista lateral, plano Y=0)', fontsize=14)
        ax1.grid(True, alpha=0.3)
        ax1.set_aspect('equal')
        ax1.legend()
        
        # Barra de color
        cbar1 = plt.colorbar(im1, ax=ax1)
        cbar1.set_label('|B| (T)', fontsize=12)
        
        # Gráfico 2: Vista superior (plano XY) mostrando la espira
        ax2_angles = np.linspace(0, 2*np.pi, 100)
        espira_x = 3 * np.cos(ax2_angles)
        espira_y = 3 * np.sin(ax2_angles)
        
        # Dibujar espira
        ax2.plot(espira_x, espira_y, 'g-', linewidth=6, label='Espira (I)')
        ax2.plot(espira_x, espira_y, 'w-', linewidth=2)
        
        # Dibujar algunas líneas de campo características de una espira
        # (patrón dipolar)
        theta_lines = np.linspace(0, 2*np.pi, 8)
        for theta in theta_lines:
            # Líneas que salen del centro hacia afuera
            r_line = np.linspace(0.5, 5, 50)
            x_line = r_line * np.cos(theta)
            y_line = r_line * np.sin(theta)
            ax2.plot(x_line, y_line, 'b--', alpha=0.4, linewidth=1)
        
        # Flechas indicando dirección del campo en el eje
        ax2.annotate('', xy=(0, 0.5), xytext=(0, -0.5),
                    arrowprops=dict(arrowstyle='->', color='red', lw=3))
        ax2.text(0.2, 0, 'B (hacia arriba)', fontsize=10, color='red')
        
        ax2.set_xlabel('X (m)', fontsize=12)
        ax2.set_ylabel('Y (m)', fontsize=12)
        ax2.set_title('Espira Circular\n(Vista superior, plano Z=0)', fontsize=14)
        ax2.grid(True, alpha=0.3)
        ax2.set_aspect('equal')
        ax2.legend()
        ax2.set_xlim(-6, 6)
        ax2.set_ylim(-6, 6)
        
        plt.tight_layout()
        plt.show()

    def graficar_configuracion(self):
        """Grafica la configuración básica del problema"""
        fig = plt.figure(figsize=(15, 5))
        
        # Gráfico 1: Alambre recto
        ax1 = fig.add_subplot(131, projection='3d')
        
        # Dibujar alambre
        z_alambre = np.linspace(-1, 1, 100)
        x_alambre = np.zeros_like(z_alambre)
        y_alambre = np.zeros_like(z_alambre)
        ax1.plot(x_alambre, y_alambre, z_alambre, 'r-', linewidth=3, label='Alambre (I)')
        
        # Dibujar punto
        ax1.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='blue', s=100, label=f'Punto P({self.punto[0]},{self.punto[1]},{self.punto[2]})')
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('Alambre Recto\n(L = 2 m)')
        ax1.legend()
        ax1.grid(True)
        
        # Gráfico 2: Espira circular
        ax2 = fig.add_subplot(132, projection='3d')
        
        # Dibujar espira
        phi = np.linspace(0, 2*np.pi, 100)
        x_esp = 3 * np.cos(phi)  # radio = 3
        y_esp = 3 * np.sin(phi)
        z_esp = np.zeros_like(phi)
        ax2.plot(x_esp, y_esp, z_esp, 'g-', linewidth=3, label='Espira (I)')
        
        # Dibujar punto
        ax2.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='blue', s=100, label=f'Punto P({self.punto[0]},{self.punto[1]},{self.punto[2]})')
        
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
        ax2.set_zlabel('Z (m)')
        ax2.set_title('Espira Circular\n(a = 3 m)')
        ax2.legend()
        ax2.grid(True)
        
               
        # Gráfico 3: Información
        ax3 = fig.add_subplot(133)
        ax3.axis('off')
        
        info_text = f"""
LEY DE BIOT-SAVART

dB = (μ₀/4π) × I × (dl × r) / |r|³

Donde:
• μ₀ = 4π × 10⁻⁷ T·m/A
• I = {self.corriente} A
• dl = elemento de longitud
• r = vector posición
• P = ({self.punto[0]}, {self.punto[1]}, {self.punto[2]}) m

El campo total se obtiene
integrando sobre toda la
geometría del conductor.
        """
        
        ax3.text(0.1, 0.5, info_text, fontsize=10, 
                verticalalignment='center', fontfamily='monospace')
        
        plt.tight_layout()
        plt.show()


    def graficar_lineas_campo_3d_alambre(self):
        """Grafica las líneas de campo magnético del alambre recto en 3D"""
        print("Generando visualización 3D del campo magnético para alambre recto...")
        
        fig = plt.figure(figsize=(15, 12))
        
        # Gráfico 1: Líneas de campo circulares en 3D
        ax1 = fig.add_subplot(221, projection='3d')
        
        # Dibujar alambre
        z_alambre = np.linspace(-1, 1, 100)
        x_alambre = np.zeros_like(z_alambre)
        y_alambre = np.zeros_like(z_alambre)
        ax1.plot(x_alambre, y_alambre, z_alambre, 'r-', linewidth=6, label='Alambre (I)', zorder=10)
        
        # Generar líneas de campo circulares a diferentes alturas z
        radios = [0.5, 1.0, 1.5, 2.0, 2.5]
        alturas = np.linspace(-0.8, 0.8, 5)
        theta = np.linspace(0, 2*np.pi, 100)
        
        colors = plt.cm.plasma(np.linspace(0, 1, len(radios)))
        
        for i, r in enumerate(radios):
            for z_nivel in alturas:
                x_circ = r * np.cos(theta)
                y_circ = r * np.sin(theta)
                z_circ = np.full_like(theta, z_nivel)
                
                ax1.plot(x_circ, y_circ, z_circ, color=colors[i], 
                        alpha=0.7, linewidth=2)
                
                # Agregar flechas direccionales cada 60 grados
                for angle_idx in range(0, len(theta), len(theta)//6):
                    angle = theta[angle_idx]
                    x_arrow = r * np.cos(angle)
                    y_arrow = r * np.sin(angle)
                    z_arrow = z_nivel
                    
                    # Dirección tangencial (perpendicular al radio)
                    dx = -np.sin(angle) * 0.2
                    dy = np.cos(angle) * 0.2
                    dz = 0
                    
                    ax1.quiver(x_arrow, y_arrow, z_arrow, dx, dy, dz,
                             color='green', arrow_length_ratio=0.3, alpha=0.8)
        
        # Punto de cálculo
        ax1.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='blue', s=150, marker='*', 
                   label=f'P({self.punto[0]:.1f},{self.punto[1]:.1f},{self.punto[2]:.1f})',
                   zorder=15)
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('Líneas de Campo 3D - Alambre Recto')
        ax1.legend()
        ax1.set_xlim(-3, 3)
        ax1.set_ylim(-3, 3)
        ax1.set_zlim(-1.5, 1.5)
        
        # Gráfico 2: Campo vectorial en plano XY
        ax2 = fig.add_subplot(222, projection='3d')
        
        # Crear grilla para vectores
        x_grid = np.linspace(-2.5, 2.5, 8)
        y_grid = np.linspace(-2.5, 2.5, 8)
        z_levels = [-0.5, 0, 0.5]
        
        # Dibujar alambre
        ax2.plot(x_alambre, y_alambre, z_alambre, 'r-', linewidth=6, label='Alambre (I)')
        
        for z_level in z_levels:
            X_grid, Y_grid = np.meshgrid(x_grid, y_grid)
            Z_grid = np.full_like(X_grid, z_level)
            
            Bx_grid = np.zeros_like(X_grid)
            By_grid = np.zeros_like(Y_grid)
            Bz_grid = np.zeros_like(Z_grid)
            
            punto_original = self.punto.copy()
            
            for i in range(X_grid.shape[0]):
                for j in range(X_grid.shape[1]):
                    x_pos, y_pos, z_pos = X_grid[i,j], Y_grid[i,j], Z_grid[i,j]
                    
                    # Evitar puntos muy cerca del alambre
                    if np.sqrt(x_pos**2 + y_pos**2) < 0.3:
                        continue
                    
                    self.punto = np.array([x_pos, y_pos, z_pos])
                    B = self.campo_alambre_recto(longitud=2.0, N=500)
                    
                    Bx_grid[i,j] = B[0]
                    By_grid[i,j] = B[1]
                    Bz_grid[i,j] = B[2]
            
            self.punto = punto_original
            
            # Normalizar para visualización
            B_mag = np.sqrt(Bx_grid**2 + By_grid**2 + Bz_grid**2)
            B_mag[B_mag == 0] = 1e-10
            
            scale_factor = 0.3
            ax2.quiver(X_grid, Y_grid, Z_grid, 
                      Bx_grid/B_mag*scale_factor, By_grid/B_mag*scale_factor, Bz_grid/B_mag*scale_factor,
                      color='blue' if z_level == 0 else 'cyan', alpha=0.8, arrow_length_ratio=0.2)
        
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
        ax2.set_zlabel('Z (m)')
        ax2.set_title('Campo Vectorial 3D - Alambre Recto')
        ax2.legend()
        
        # Gráfico 3: Vista superior con intensidad de campo
        ax3 = fig.add_subplot(223)
        
        # Calcular intensidad en plano z=0
        x_intensity = np.linspace(-3, 3, 50)
        y_intensity = np.linspace(-3, 3, 50)
        X_int, Y_int = np.meshgrid(x_intensity, y_intensity)
        
        B_intensity = np.zeros_like(X_int)
        punto_original = self.punto.copy()
        
        for i in range(X_int.shape[0]):
            for j in range(X_int.shape[1]):
                x_pos, y_pos = X_int[i,j], Y_int[i,j]
                
                if np.sqrt(x_pos**2 + y_pos**2) < 0.1:
                    B_intensity[i,j] = np.nan
                    continue
                
                self.punto = np.array([x_pos, y_pos, 0])
                B = self.campo_alambre_recto(longitud=2.0, N=300)
                B_intensity[i,j] = np.log10(np.linalg.norm(B) + 1e-12)
        
        self.punto = punto_original
        
        # Mapa de contorno
        contour = ax3.contourf(X_int, Y_int, B_intensity, levels=20, cmap='plasma')
        ax3.contour(X_int, Y_int, B_intensity, levels=20, colors='black', alpha=0.3, linewidths=0.5)
        
        # Líneas de campo circulares (equipotenciales magnéticas)
        for r in [0.5, 1.0, 1.5, 2.0, 2.5]:
            circle_theta = np.linspace(0, 2*np.pi, 100)
            x_circle = r * np.cos(circle_theta)
            y_circle = r * np.sin(circle_theta)
            ax3.plot(x_circle, y_circle, 'w--', alpha=0.6, linewidth=1)
        
        ax3.set_xlabel('X (m)')
        ax3.set_ylabel('Y (m)')
        ax3.set_title('Intensidad del Campo Magnético')
        ax3.set_aspect('equal')
        
        # Agregar texto indicativo de la posición del alambre
        ax3.text(0.02, 0.98, '', 
                transform=ax3.transAxes, fontsize=8, 
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        plt.colorbar(contour, ax=ax3, label='log₁₀|B| (T)')
        
        # Gráfico 4: Información y teoría
        ax4 = fig.add_subplot(224)
        ax4.axis('off')
        
        info_text = f"""
ALAMBRE RECTO - CAMPO MAGNÉTICO 3D

Ley de Biot-Savart:
dB = (μ₀/4π) × I × (dl × r) / |r|³

Características del alambre:
• Longitud: L = 2 m
• Corriente: I = {self.corriente} A
• Orientación: Eje Z

Patrón del campo:
• Líneas circulares concéntricas
• Perpendiculares al alambre
• Intensidad ∝ 1/r

Regla de la mano derecha:
• Pulgar: dirección de corriente
• Dedos: dirección del campo

Punto de cálculo:
P = ({self.punto[0]:.1f}, {self.punto[1]:.1f}, {self.punto[2]:.1f}) m

El campo es más intenso cerca
del alambre y decrece con la
distancia radial.
        """
        
        ax4.text(0.05, 0.95, info_text, fontsize=10, 
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.5))
        
        plt.tight_layout()
        plt.show()

    def graficar_lineas_campo_3d_espira(self):
        """Grafica las líneas de campo magnético de la espira circular en 3D"""
        print("Generando visualización 3D del campo magnético para espira circular...")
        
        fig = plt.figure(figsize=(16, 12))
        
        # Gráfico 1: Líneas de campo dipolar en 3D
        ax1 = fig.add_subplot(221, projection='3d')
        
        # Dibujar espira
        phi_espira = np.linspace(0, 2*np.pi, 100)
        x_espira = 3 * np.cos(phi_espira)
        y_espira = 3 * np.sin(phi_espira)
        z_espira = np.zeros_like(phi_espira)
        ax1.plot(x_espira, y_espira, z_espira, 'g-', linewidth=8, label='Espira (I)', zorder=10)
        
        # Generar líneas de campo dipolar
        # Líneas que salen del eje y se curvan
        phi_lines = np.linspace(0, 2*np.pi, 8)
        
        for phi in phi_lines:
            # Líneas desde el centro hacia afuera y curvándose
            t = np.linspace(0.1, 4, 50)
            
            # Líneas superiores (saliendo hacia arriba)
            for z_start in [0.2, 0.5, 1.0]:
                r = t
                z_line = z_start + t**0.7
                x_line = r * np.cos(phi)
                y_line = r * np.sin(phi)
                
                # Solo mostrar líneas que no intersecten la espira
                mask = (r > 3.2) | (np.abs(z_line) > 0.1)
                
                ax1.plot(x_line[mask], y_line[mask], z_line[mask], 
                        'b-', alpha=0.7, linewidth=1.5)
                
                # Líneas inferiores (entrando por abajo)
                z_line_neg = -z_start - t**0.7
                ax1.plot(x_line[mask], y_line[mask], z_line_neg[mask], 
                        'b-', alpha=0.7, linewidth=1.5)
        
        # Líneas en el eje central
        z_axis = np.linspace(-2, 2, 50)
        x_axis = np.zeros_like(z_axis)
        y_axis = np.zeros_like(z_axis)
        ax1.plot(x_axis, y_axis, z_axis, 'b-', linewidth=3, alpha=0.8)
        
        # Flechas en el eje indicando dirección
        for z_arrow in [-1.5, -1, -0.5, 0.5, 1, 1.5]:
            ax1.quiver(0, 0, z_arrow, 0, 0, 0.2,
                     color='red', arrow_length_ratio=0.5, alpha=0.9, linewidth=2)
        
        # Punto de cálculo
        ax1.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='blue', s=150, marker='*', 
                   label=f'P({self.punto[0]:.1f},{self.punto[1]:.1f},{self.punto[2]:.1f})',
                   zorder=15)
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('Líneas de Campo 3D - Espira Circular')
        ax1.legend()
        ax1.set_xlim(-5, 5)
        ax1.set_ylim(-5, 5)
        ax1.set_zlim(-3, 3)
        
        # Gráfico 2: Campo vectorial en varios planos
        ax2 = fig.add_subplot(222, projection='3d')
        
        # Dibujar espira
        ax2.plot(x_espira, y_espira, z_espira, 'g-', linewidth=8, label='Espira (I)')
        
        # Crear grilla para vectores en el plano XZ (y=0)
        x_vec = np.linspace(-4, 4, 8)
        z_vec = np.linspace(-3, 3, 6)
        X_vec, Z_vec = np.meshgrid(x_vec, z_vec)
        Y_vec = np.zeros_like(X_vec)
        
        Bx_vec = np.zeros_like(X_vec)
        By_vec = np.zeros_like(Y_vec)
        Bz_vec = np.zeros_like(Z_vec)
        
        punto_original = self.punto.copy()
        
        for i in range(X_vec.shape[0]):
            for j in range(X_vec.shape[1]):
                x_pos, y_pos, z_pos = X_vec[i,j], Y_vec[i,j], Z_vec[i,j]
                
                # Evitar puntos muy cerca de la espira
                dist_espira = abs(np.sqrt(x_pos**2 + y_pos**2) - 3.0)
                if dist_espira < 0.5 and abs(z_pos) < 0.3:
                    continue
                
                self.punto = np.array([x_pos, y_pos, z_pos])
                B = self.campo_espira_circular(radio=3.0, N=500)
                
                Bx_vec[i,j] = B[0]
                By_vec[i,j] = B[1]
                Bz_vec[i,j] = B[2]
        
        self.punto = punto_original
        
        # Normalizar vectores
        B_mag = np.sqrt(Bx_vec**2 + By_vec**2 + Bz_vec**2)
        B_mag[B_mag == 0] = 1e-10
        
        scale_factor = 0.4
        ax2.quiver(X_vec, Y_vec, Z_vec, 
                  Bx_vec/B_mag*scale_factor, By_vec/B_mag*scale_factor, Bz_vec/B_mag*scale_factor,
                  color='blue', alpha=0.8, arrow_length_ratio=0.2)
        
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
        ax2.set_zlabel('Z (m)')
        ax2.set_title('Campo Vectorial 3D - Espira Circular\n(Plano XZ, Y=0)')
        ax2.legend()
        
        # Gráfico 3: Intensidad en el plano XZ
        ax3 = fig.add_subplot(223)
        
        x_int = np.linspace(-5, 5, 40)
        z_int = np.linspace(-4, 4, 32)
        X_int, Z_int = np.meshgrid(x_int, z_int)
        
        B_intensity = np.zeros_like(X_int)
        
        for i in range(X_int.shape[0]):
            for j in range(X_int.shape[1]):
                x_pos, z_pos = X_int[i,j], Z_int[i,j]
                
                # Evitar la región de la espira
                dist_espira = abs(np.sqrt(x_pos**2) - 3.0)
                if dist_espira < 0.3 and abs(z_pos) < 0.2:
                    B_intensity[i,j] = np.nan
                    continue
                
                self.punto = np.array([x_pos, 0, z_pos])
                B = self.campo_espira_circular(radio=3.0, N=300)
                B_intensity[i,j] = np.log10(np.linalg.norm(B) + 1e-12)
        
        self.punto = punto_original
        
        # Mapa de contorno
        contour = ax3.contourf(X_int, Z_int, B_intensity, levels=20, cmap='plasma')
        ax3.contour(X_int, Z_int, B_intensity, levels=20, colors='black', alpha=0.3, linewidths=0.5)
        
        # Líneas de campo esquemáticas (solo el eje dipolar)
        ax3.annotate('', xy=(0, 1), xytext=(0, -1),
                    arrowprops=dict(arrowstyle='<->', color='white', lw=2))
        ax3.text(0.3, 0, 'Eje del dipolo', color='white', fontweight='bold')
        
        ax3.set_xlabel('X (m)')
        ax3.set_ylabel('Z (m)')
        ax3.set_title('Intensidad del Campo Magnético')
        ax3.set_aspect('equal')
        
        # Agregar texto indicativo de la posición de la espira
        ax3.text(0.02, 0.98, 'Espira: Radio=3m en Z=0\n(círculo en plano XY)', 
                transform=ax3.transAxes, fontsize=8, 
                verticalalignment='top', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        plt.colorbar(contour, ax=ax3, label='')
        
        # Gráfico 4: Información y teoría
        ax4 = fig.add_subplot(224)
        ax4.axis('off')
        
        info_text = f"""
ESPIRA CIRCULAR - CAMPO MAGNÉTICO 3D

Ley de Biot-Savart:
dB = (μ₀/4π) × I × (dl × r) / |r|³

Características de la espira:
• Radio: a = 3 m
• Corriente: I = {self.corriente} A
• Plano: XY (z = 0)

Patrón del campo:
• Dipolo magnético
• Líneas salen por un lado
• Entran por el otro lado
• Máximo en el eje (z)

Campo en el centro:
B₀ = μ₀I/(2a) = {(4*np.pi*1e-7*self.corriente)/(2*3):.2e} T

Campo en el eje (z ≠ 0):
B = μ₀Ia²/[2(a²+z²)^(3/2)]

Punto de cálculo:
P = ({self.punto[0]:.1f}, {self.punto[1]:.1f}, {self.punto[2]:.1f}) m

El campo es más intenso en el
centro y disminuye con la distancia.
        """
        
        ax4.text(0.05, 0.95, info_text, fontsize=9, 
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.5))
        
        plt.tight_layout()
        plt.show()

    def cargar_datos_combinado(self):
        """Carga los datos para la configuración combinada alambre+espira"""
        print("=== CONFIGURACIÓN COMBINADA: ALAMBRE + ESPIRA ===\n")
        
        print("El alambre estará ubicado en el eje Z (eje de la espira)")
        print("La espira estará en el plano XY con centro en el origen")
        print()
        
        self.corriente_alambre = float(input("Ingrese la corriente del alambre I1 (en amperios): "))
        self.corriente_espira = float(input("Ingrese la corriente de la espira I2 (en amperios): "))
        
        punto_str = input("Ingrese el punto P donde calcular el campo (x y z): ")
        coords = punto_str.split()
        self.punto = np.array([float(coords[0]), float(coords[1]), float(coords[2])])
        
        print(f"\nDatos cargados:")
        print(f"Corriente alambre: I1 = {self.corriente_alambre} A")
        print(f"Corriente espira: I2 = {self.corriente_espira} A")
        print(f"Punto: P = ({self.punto[0]}, {self.punto[1]}, {self.punto[2]}) m")
        print(f"Alambre: L = 2 m en eje Z")
        print(f"Espira: a = 3 m en plano XY")

    def campo_combinado(self, longitud_alambre=2.0, radio_espira=3.0, N=5000):
        """
        Calcula el campo magnético total de alambre + espira
        
        Parámetros:
        - longitud_alambre: longitud del alambre en metros
        - radio_espira: radio de la espira en metros
        - N: número de segmentos para la integración numérica
        """
        print(f"\n--- CAMPO COMBINADO: ALAMBRE (L={longitud_alambre}m) + ESPIRA (a={radio_espira}m) ---")
        
        # Calcular campo del alambre
        punto_original = self.punto.copy()
        corriente_original = getattr(self, 'corriente', None)
        
        # Configurar para alambre
        self.corriente = self.corriente_alambre
        B_alambre = self.campo_alambre_recto(longitud=longitud_alambre, N=N)
        
        # Configurar para espira
        self.corriente = self.corriente_espira
        B_espira = self.campo_espira_circular(radio=radio_espira, N=N)
        
        # Restaurar valores originales
        self.punto = punto_original
        if corriente_original is not None:
            self.corriente = corriente_original
        
        # Campo total
        B_total = B_alambre + B_espira
        
        return B_alambre, B_espira, B_total

    def mostrar_resultados_combinado(self, B_alambre, B_espira, B_total):
        """Muestra los resultados de la configuración combinada"""
        print("\n" + "="*70)
        print("RESULTADOS DEL CAMPO MAGNÉTICO COMBINADO")
        print("="*70)
        
        print(f"\nPunto de cálculo: P = ({self.punto[0]}, {self.punto[1]}, {self.punto[2]}) m")
        print(f"Corriente alambre: I1 = {self.corriente_alambre} A")
        print(f"Corriente espira: I2 = {self.corriente_espira} A")
        
        print(f"\n1. ALAMBRE RECTO (L = 2 m, eje Z):")
        print(f"   Bx = {B_alambre[0]:.6e} T")
        print(f"   By = {B_alambre[1]:.6e} T") 
        print(f"   Bz = {B_alambre[2]:.6e} T")
        print(f"   |B| = {np.linalg.norm(B_alambre):.6e} T")
        
        print(f"\n2. ESPIRA CIRCULAR (a = 3 m, plano XY):")
        print(f"   Bx = {B_espira[0]:.6e} T")
        print(f"   By = {B_espira[1]:.6e} T")
        print(f"   Bz = {B_espira[2]:.6e} T")
        print(f"   |B| = {np.linalg.norm(B_espira):.6e} T")
        
        print(f"\n3. CAMPO TOTAL (ALAMBRE + ESPIRA):")
        print(f"   Bx = {B_total[0]:.6e} T")
        print(f"   By = {B_total[1]:.6e} T")
        print(f"   Bz = {B_total[2]:.6e} T")
        print(f"   |B| = {np.linalg.norm(B_total):.6e} T")
        
        print("\n¿Qué significa esta configuración?")
        print("- El alambre genera campo circular perpendicular al eje Z")
        print("- La espira genera campo dipolar principalmente en Z")
        print("- El campo total es la superposición vectorial de ambos")
        print("- En el eje Z (x=0, y=0): domina el campo de la espira")
        print("- Fuera del eje: interacción compleja entre ambos campos")

    def graficar_configuracion_combinada(self):
        """Grafica la configuración combinada alambre+espira"""
        fig = plt.figure(figsize=(18, 6))
        
        # Gráfico 1: Vista 3D de la configuración
        ax1 = fig.add_subplot(131, projection='3d')
        
        # Dibujar alambre (eje Z)
        z_alambre = np.linspace(-1, 1, 100)
        x_alambre = np.zeros_like(z_alambre)
        y_alambre = np.zeros_like(z_alambre)
        ax1.plot(x_alambre, y_alambre, z_alambre, 'r-', linewidth=4, label=f'Alambre I1={self.corriente_alambre}A')
        
        # Dibujar espira (plano XY)
        phi = np.linspace(0, 2*np.pi, 100)
        x_esp = 3 * np.cos(phi)
        y_esp = 3 * np.sin(phi)
        z_esp = np.zeros_like(phi)
        ax1.plot(x_esp, y_esp, z_esp, 'g-', linewidth=4, label=f'Espira I2={self.corriente_espira}A')
        
        # Dibujar punto de cálculo
        ax1.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='blue', s=150, marker='*', 
                   label=f'P({self.punto[0]:.1f},{self.punto[1]:.1f},{self.punto[2]:.1f})')
        
        # Marcar intersecciones del alambre con la espira
        ax1.scatter([0, 0], [0, 0], [-3, 3], color='orange', s=100, marker='o', 
                   label='Intersecciones')
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('Configuración Combinada\nAlambre + Espira')
        ax1.legend()
        ax1.grid(True)
        ax1.set_xlim(-4, 4)
        ax1.set_ylim(-4, 4)
        ax1.set_zlim(-2, 2)
        
        # Gráfico 2: Vista superior (plano XY)
        ax2 = fig.add_subplot(132)
        
        # Dibujar espira
        ax2.plot(x_esp, y_esp, 'g-', linewidth=6, label=f'Espira I2={self.corriente_espira}A')
        ax2.plot(x_esp, y_esp, 'w-', linewidth=2)
        
        # Marcar centro (donde está el alambre)
        ax2.scatter(0, 0, color='red', s=200, marker='+', linewidth=4, 
                   label=f'Alambre I1={self.corriente_alambre}A\n(perpendicular al plano)')
        
        # Punto de cálculo (si está cerca del plano Z=0)
        if abs(self.punto[2]) < 0.5:
            ax2.scatter(self.punto[0], self.punto[1], color='blue', s=150, marker='*',
                       label=f'P({self.punto[0]:.1f},{self.punto[1]:.1f},{self.punto[2]:.1f})')
        
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
        ax2.set_title('Vista Superior\n(Plano XY, Z=0)')
        ax2.grid(True, alpha=0.3)
        ax2.set_aspect('equal')
        ax2.legend()
        ax2.set_xlim(-4, 4)
        ax2.set_ylim(-4, 4)
        
        # Gráfico 3: Vista lateral (plano XZ)
        ax3 = fig.add_subplot(133)
        
        # Dibujar alambre
        ax3.plot([0, 0], [-1, 1], 'r-', linewidth=6, label=f'Alambre I1={self.corriente_alambre}A')
        ax3.plot([0, 0], [-1, 1], 'w-', linewidth=2)
        
        # Dibujar espira (vista lateral)
        ax3.plot([-3, 3], [0, 0], 'g-', linewidth=6, label=f'Espira I2={self.corriente_espira}A')
        ax3.plot([-3, 3], [0, 0], 'w-', linewidth=2)
        ax3.scatter([-3, 3], [0, 0], color='green', s=100)
        
        # Punto de intersección
        ax3.scatter(0, 0, color='orange', s=150, marker='o', label='Intersección')
        
        # Punto de cálculo (si está cerca del plano Y=0)
        if abs(self.punto[1]) < 0.5:
            ax3.scatter(self.punto[0], self.punto[2], color='blue', s=150, marker='*',
                       label=f'P({self.punto[0]:.1f},{self.punto[1]:.1f},{self.punto[2]:.1f})')
        
        ax3.set_xlabel('X (m)')
        ax3.set_ylabel('Z (m)')
        ax3.set_title('Vista Lateral\n(Plano XZ, Y=0)')
        ax3.grid(True, alpha=0.3)
        ax3.set_aspect('equal')
        ax3.legend()
        ax3.set_xlim(-4, 4)
        ax3.set_ylim(-2, 2)
        
        plt.tight_layout()
        plt.show()

    def graficar_lineas_campo_combinado(self):
        """Grafica las líneas de campo magnético combinado en 2D y 3D solamente"""
        print("Generando visualización del campo magnético combinado...")
        print("Calculando líneas de campo 2D y 3D...")
        
        # Crear figura con solo 2 gráficos: 2D y 3D
        fig = plt.figure(figsize=(16, 8))
        fig.suptitle('LÍNEAS DE CAMPO MAGNÉTICO COMBINADO - ALAMBRE + ESPIRA', fontsize=16, fontweight='bold')
        
        # ===== VISUALIZACIÓN 2D =====
        # Gráfico 1: Líneas de campo 2D en plano XY (z=0)
        ax1 = fig.add_subplot(121)
        
        # Calcular campo 2D
        x_2d = np.linspace(-4, 4, 30)
        y_2d = np.linspace(-4, 4, 30)
        X_2d, Y_2d = np.meshgrid(x_2d, y_2d)
        
        Bx_2d = np.zeros_like(X_2d)
        By_2d = np.zeros_like(Y_2d)
        
        punto_original = self.punto.copy()
        
        for i in range(X_2d.shape[0]):
            for j in range(X_2d.shape[1]):
                x_pos, y_pos = X_2d[i,j], Y_2d[i,j]
                
                # Evitar singularidades
                dist_alambre = np.sqrt(x_pos**2 + y_pos**2)
                dist_espira = abs(np.sqrt(x_pos**2 + y_pos**2) - 3.0)
                
                if dist_alambre < 0.2 or dist_espira < 0.3:
                    Bx_2d[i,j] = By_2d[i,j] = 0
                    continue
                
                self.punto = np.array([x_pos, y_pos, 0])
                try:
                    B_alambre, B_espira, B_total = self.campo_combinado(N=100)
                    Bx_2d[i,j] = B_total[0]
                    By_2d[i,j] = B_total[1]
                except:
                    Bx_2d[i,j] = By_2d[i,j] = 0
        
        self.punto = punto_original
        
        # Streamplot 2D
        magnitud_2d = np.sqrt(Bx_2d**2 + By_2d**2)
        magnitud_2d[magnitud_2d == 0] = 1e-10
        
        stream = ax1.streamplot(X_2d, Y_2d, Bx_2d, By_2d, density=1.5, 
                               color=magnitud_2d, cmap='plasma', arrowsize=1.2)
        
        # Dibujar configuración
        theta = np.linspace(0, 2*np.pi, 100)
        x_espira = 3 * np.cos(theta)
        y_espira = 3 * np.sin(theta)
        ax1.plot(x_espira, y_espira, 'b-', linewidth=4, label='Espira')
        ax1.scatter(0, 0, color='red', s=150, marker='o', label='Alambre', zorder=5)
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_title('Líneas de Campo 2D (z=0)')
        ax1.legend()
        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        
        # ===== VISUALIZACIÓN 3D =====
        # Gráfico 2: Líneas de campo 3D calculadas numéricamente
        ax2 = fig.add_subplot(122, projection='3d')
        
        print("Calculando trayectorias de líneas de campo 3D...")
        
        # Función para calcular campo en un punto
        def calcular_campo_punto(x, y, z):
            self.punto = np.array([x, y, z])
            try:
                # Evitar singularidades
                dist_alambre = np.sqrt(x**2 + y**2)
                dist_espira = abs(np.sqrt(x**2 + y**2) - 3.0)
                
                if dist_alambre < 0.15 or (dist_espira < 0.25 and abs(z) < 0.15):
                    return np.array([0.0, 0.0, 0.0])
                
                B_alambre, B_espira, B_total = self.campo_combinado(N=80)
                return B_total
            except:
                return np.array([0.0, 0.0, 0.0])
        
        # Función para trazar línea de campo
        def trazar_linea_campo(x0, y0, z0, direccion=1, max_puntos=40, paso=0.08):
            puntos = []
            x, y, z = x0, y0, z0
            
            for _ in range(max_puntos):
                B = calcular_campo_punto(x, y, z)
                B_mag = np.linalg.norm(B)
                
                if B_mag < 1e-12:
                    break
                
                puntos.append([x, y, z])
                
                # Paso en dirección del campo
                B_norm = B / B_mag
                x += direccion * paso * B_norm[0]
                y += direccion * paso * B_norm[1]
                z += direccion * paso * B_norm[2]
                
                # Límites para evitar que se vayan muy lejos
                if abs(x) > 5 or abs(y) > 5 or abs(z) > 4:
                    break
            
            return np.array(puntos)
        
        # Generar líneas de campo del alambre (circulares)
        lineas_alambre = []
        for r in [0.6, 1.2, 1.8, 2.4]:
            for z_level in [-1.0, -0.5, 0.5, 1.0]:
                for angulo in np.linspace(0, 2*np.pi, 6, endpoint=False):
                    x0 = r * np.cos(angulo)
                    y0 = r * np.sin(angulo)
                    z0 = z_level
                    
                    if abs(z_level) > 0.2 or r != 3.0:  # Evitar espira
                        linea = trazar_linea_campo(x0, y0, z0, direccion=1, paso=0.06)
                        if len(linea) > 2:
                            lineas_alambre.append(linea)
        
        # Generar líneas de campo de la espira (dipolares)
        lineas_espira = []
        
        # Líneas desde el centro hacia afuera
        for angulo_xy in np.linspace(0, 2*np.pi, 8, endpoint=False):
            for r_inicio in [3.5, 4.0]:
                for z_inicio in [0.2, 0.5, 1.0]:
                    x0 = r_inicio * np.cos(angulo_xy)
                    y0 = r_inicio * np.sin(angulo_xy)
                    
                    # Líneas superiores
                    linea_sup = trazar_linea_campo(x0, y0, z_inicio, direccion=1, paso=0.08)
                    if len(linea_sup) > 2:
                        lineas_espira.append(linea_sup)
                    
                    # Líneas inferiores
                    linea_inf = trazar_linea_campo(x0, y0, -z_inicio, direccion=1, paso=0.08)
                    if len(linea_inf) > 2:
                        lineas_espira.append(linea_inf)
        
        # Líneas en el eje Z
        for z_start in [-3.0, -2.5, 2.5, 3.0]:
            linea_eje = trazar_linea_campo(0.05, 0, z_start, direccion=1 if z_start > 0 else -1, paso=0.1)
            if len(linea_eje) > 2:
                lineas_espira.append(linea_eje)
        
        self.punto = punto_original
        
        # Dibujar líneas de campo del alambre (rojas)
        for linea in lineas_alambre:
            if len(linea) > 1:
                ax2.plot(linea[:, 0], linea[:, 1], linea[:, 2], 
                        color='red', alpha=0.7, linewidth=1.8)
        
        # Dibujar líneas de campo de la espira (azules)
        for linea in lineas_espira:
            if len(linea) > 1:
                ax2.plot(linea[:, 0], linea[:, 1], linea[:, 2], 
                        color='blue', alpha=0.7, linewidth=1.8)
        
        # Dibujar alambre y espira
        z_alambre = np.linspace(-1, 1, 100)
        ax2.plot(np.zeros_like(z_alambre), np.zeros_like(z_alambre), z_alambre, 
                'r-', linewidth=6, label=f'Alambre I={self.corriente_alambre}A')
        
        phi_espira = np.linspace(0, 2*np.pi, 100)
        x_espira_3d = 3 * np.cos(phi_espira)
        y_espira_3d = 3 * np.sin(phi_espira)
        z_espira_3d = np.zeros_like(phi_espira)
        ax2.plot(x_espira_3d, y_espira_3d, z_espira_3d, 
                'b-', linewidth=6, label=f'Espira I={self.corriente_espira}A')
        
        # Punto de cálculo
        ax2.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='green', s=200, marker='*', label='Punto P', 
                   edgecolor='black', linewidth=1, zorder=10)
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Y (m)')
        ax2.set_zlabel('Z (m)')
        ax2.set_title('Líneas de Campo Magnético 3D\nAlambre (Rojo) + Espira (Azul)')
        ax2.legend(loc='upper left')
        ax2.set_xlim(-4, 4)
        ax2.set_ylim(-4, 4)
        ax2.set_zlim(-3, 3)
        
        plt.tight_layout()
        plt.show()
        
        print("✅ Visualización completada!")
        print("📊 Se muestran:")
        print("   • Líneas de campo 2D en plano z=0")
        print("   • Líneas de campo 3D calculadas numéricamente")

    def calcular_campo_espiras_vueltas(self, radio, corriente, vueltas, x, y ,z, z0, N):
        """Calcula el campo magnético de una bobina (muchas vueltas)."""

        # Guardar estado previo
        corriente_original = self.corriente
        punto_original = getattr(self, "punto", None)

        # Setear estado para la espira
        self.corriente = corriente
        self.punto = np.array([x, y, z])

        # Acumulador
        B_total = np.zeros(3)

        # Repetimos la espira 'vueltas' veces
        for _ in range(vueltas):

            # --- TRUCO ---
            # desplazamos artificialmente la espira en z
            # sin tocar la función original
            # sumando z0 al punto que “ve” la espira
            self.punto = np.array([x, y, z - z0])

            B_total += self.campo_espira_circular(
                radio=radio,
                N=N
            )

        # Restaurar estado
        self.corriente = corriente_original
        if punto_original is not None:
            self.punto = punto_original

        return B_total

def menu_principal():
    """Menú principal del programa"""
    biot = BiotSavart()
    
    while True:
        print("\n" + "="*60)
        print("         CALCULADORA DE CAMPO MAGNÉTICO")
        print("              Ley de Biot-Savart")
        print("="*60)
        print("1. Calcular campo magnético - ALAMBRE RECTO")
        print("2. Calcular campo magnético - ESPIRA CIRCULAR")
        print("3. Mostrar resultados anteriores")
        print("4. Graficar configuración del alambre")
        print("5. Graficar configuración de la espira")
        print("6. Graficar líneas de campo 2D - Alambre")
        print("7. Graficar líneas de campo 3D - Alambre")
        print("8. Graficar líneas de campo 2D - Espira")
        print("9. Graficar líneas de campo 3D - Espira")
        print("10. Configuración combinada (Alambre + Espira)")
        print("11. Calcular campo magnético - BOBINAS DE HELMHOLTZ")
        print("12. Graficar configuración de Bobinas de Helmholtz")
        print("13. Salir")
        print("-"*60)
        
        opcion = input("Seleccione una opción (1-11): ")
        
        if opcion == '1':
            biot.cargar_datos_alambre()
            biot.calcular_campo_alambre()
            biot.mostrar_resultados_alambre()
            
        elif opcion == '2':
            biot.cargar_datos_espira()
            biot.calcular_campo_espira()
            biot.mostrar_resultados_espira()
            
        elif opcion == '3':
            print("\n--- RESULTADOS ANTERIORES ---")
            if hasattr(biot, 'B_alambre'):
                biot.mostrar_resultados_alambre()
            if hasattr(biot, 'B_espira'):
                biot.mostrar_resultados_espira()
            if not hasattr(biot, 'B_alambre') and not hasattr(biot, 'B_espira'):
                print("No hay resultados para mostrar. Realice primero un cálculo.")
                
        elif opcion == '4':
            if hasattr(biot, 'corriente_alambre'):
                biot.graficar_configuracion_alambre()
            else:
                print("Primero debe calcular el campo del alambre (opción 1)")
                
        elif opcion == '5':
            if hasattr(biot, 'corriente_espira'):
                biot.graficar_configuracion_espira()
            else:
                print("Primero debe calcular el campo de la espira (opción 2)")
                
        elif opcion == '6':
            if hasattr(biot, 'corriente_alambre'):
                biot.graficar_lineas_campo_2d_alambre()
            else:
                print("Primero debe calcular el campo del alambre (opción 1)")
                
        elif opcion == '7':
            if hasattr(biot, 'corriente_alambre'):
                biot.graficar_lineas_campo_3d_alambre()
            else:
                print("Primero debe calcular el campo del alambre (opción 1)")
                
        elif opcion == '8':
            if hasattr(biot, 'corriente_espira'):
                biot.graficar_lineas_campo_2d_espira()
            else:
                print("Primero debe calcular el campo de la espira (opción 2)")
                
        elif opcion == '9':
            if hasattr(biot, 'corriente_espira'):
                biot.graficar_lineas_campo_3d_espira()
            else:
                print("Primero debe calcular el campo de la espira (opción 2)")
                
        elif opcion == '10':
            # Configuración combinada
            biot.cargar_datos_combinado()
            B_alambre, B_espira, B_total = biot.campo_combinado()
            biot.mostrar_resultados_combinado(B_alambre, B_espira, B_total)
            biot.graficar_configuracion_combinada()
            
            print("\n🌟 Generando visualización de líneas de campo combinado...")
            biot.graficar_lineas_campo_combinado()
        
        elif opcion == '11':
            # Cálculo del campo magnético de bobinas de Helmholtz
            a = float(input("Radio de cada bobina (m): "))
            I = float(input("Corriente en cada bobina (A): "))
            Nvueltas = int(input("Número de vueltas por bobina: "))
            d = float(input("Separación entre bobinas (m) [Helmholtz ideal = radio]: "))
            
            punto = str(input("Punto (x y z): "))
            x, y, z = map(float, punto.split())
            Nseg = int(input("Discretización por vuelta: "))

            # Calcular campo total
            B_total = np.array([0.0, 0.0, 0.0])
            
            # Bobina 1 en z = -d/2
            B_total += biot.calcular_campo_espiras_vueltas(a, I, Nvueltas, x, y, z, -d/2, Nseg)
            
            # Bobina 2 en z = +d/2
            B_total += biot.calcular_campo_espiras_vueltas(a, I, Nvueltas, x, y, z, +d/2, Nseg)

            print("\nCampo total en el punto:")
            print(f"Bx = {B_total[0]:.6e} T")
            print(f"By = {B_total[1]:.6e} T")
            print(f"Bz = {B_total[2]:.6e} T")
            print(f"|B| = {np.linalg.norm(B_total):.6e} T\n")

            print("\n¿Qué significan estos resultados?")
            print("- El campo se calcula sumando la contribución magnética de cada espira de ambas bobinas usando la ley de Biot–Savart.")
            print("- Las bobinas de Helmholtz están separadas una distancia igual a su radio para generar una región central con campo casi uniforme.")
            print("- Bx, By y Bz son las componentes del campo magnético total producido por las dos bobinas en el punto elegido.")

        elif opcion == '12':
            R = float(input("Radio de las bobinas (m): "))
            d = float(input("Separación entre las bobinas (m). Se recomienda igual al radio: "))
            N = int(input("Número de espiras por bobina: "))
            I = float(input("Corriente en las bobinas (A): "))
            z1 = -d / 2  # Posición Z de la primera bobina
            z2 = d / 2   # Posición Z de la segunda bobina
            # --- 2. Generación de las Bobinas ---
            t = np.linspace(0, 2 * np.pi, 100) # Rango angular de 0 a 2*pi

            x_coil1 = R * np.cos(t)
            y_coil1 = R * np.sin(t)
            z_coil1 = np.full_like(t, z1)

            x_coil2 = R * np.cos(t)
            y_coil2 = R * np.sin(t)
            z_coil2 = np.full_like(t, z2)

            # --- 3. Cálculo del Campo Magnético en el Eje Z ---
            # Función para calcular el campo magnético en el eje Z
            def B_field_on_axis(z_axis_points, R, d, MU_0, N, I):
                # Campo de la primera bobina
                B1 = (MU_0 * N * I * R**2) / (2 * (R**2 + (z_axis_points - d/2)**2)**(3/2))
                # Campo de la segunda bobina
                B2 = (MU_0 * N * I * R**2) / (2 * (R**2 + (z_axis_points + d/2)**2)**(3/2))
                # Campo total (suma de los componentes Z, ya que los componentes radiales se cancelan en el eje)
                return B1 + B2

            # Puntos a lo largo del eje Z para calcular el campo
            z_plot_range = np.linspace(-R * 2, R * 2, 200)
            B_z_values = B_field_on_axis(z_plot_range, R, d, MU_0, N, I)

            # --- 3. Cálculo e Impresión por Consola de la Magnitud del Campo ---

            print("\n## Magnitud del Campo Magnético en Puntos Clave ##")
            print(f"Parámetros: R = {R:.1f} m, Separación d = {d:.1f} m, N = {N}, I = {I:.1f} A")
            print("-" * 50)

            # 3.1 Campo en el centro (Z = 0)
            z_center = 0.0
            B_center = B_field_on_axis(z_center, R, d, MU_0, N, I)
            print(f"Campo en el centro (Z = {z_center:.1f} m): \t\t{B_center * 1e6:.3f} µT (Microteslas)")

            # 3.2 Campo en la posición de la Bobina 1 (Z = -R/2)
            B_coil1 = B_field_on_axis(z1, R, d, MU_0, N, I)
            print(f"Campo en la Bobina 1 (Z = {z1:.1f} m): \t\t{B_coil1 * 1e6:.3f} µT")

            # 3.3 Campo en la posición de la Bobina 2 (Z = +R/2)
            B_coil2 = B_field_on_axis(z2, R, d, MU_0, N, I)
            print(f"Campo en la Bobina 2 (Z = {z2:.1f} m): \t\t{B_coil2 * 1e6:.3f} µT")

            # 3.4 Campo en un extremo (Ej. Z = 2R)
            z_end = 2 * R
            B_end = B_field_on_axis(z_end, R, d, MU_0, N, I)
            print(f"Campo en el Extremo (Z = {z_end:.1f} m): \t\t{B_end * 1e6:.3f} µT")

            print("-" * 50)

            # --- 4. Generación de los Gráficos ---
            fig = plt.figure(figsize=(15, 6)) # Aumentar el tamaño para tres subgráficos

            # Subgráfico 1: Vista 3D de las Bobinas
            ax1 = fig.add_subplot(121, projection='3d')
            ax1.plot(x_coil1, y_coil1, z_coil1, color='blue', linewidth=2, label=f'Bobina 1 (Z={z1:.1f} m)')
            ax1.plot(x_coil2, y_coil2, z_coil2, color='red', linewidth=2, label=f'Bobina 2 (Z={z2:.1f} m)')

            # Añadir el eje de las bobinas
            ax1.plot([0, 0], [0, 0], [-R*2, R*2], color='gray', linestyle='--', linewidth=1, label='Eje Z')

            ax1.set_title(f'Bobinas de Helmholtz (3D) con R = {R:.1f}m y d = {d:.1f}m')
            ax1.set_xlabel('X (m)')
            ax1.set_ylabel('Y (m)')
            ax1.set_zlabel('Z (m)')
            ax1.set_xlim([-R * 1.5, R * 1.5]) # Ajustar límites para mejor visualización
            ax1.set_ylim([-R * 1.5, R * 1.5])
            ax1.set_zlim([-R * 1.5, R * 1.5])
            ax1.view_init(elev=20, azim=45)
            ax1.legend() # Mostrar la leyenda

            # Subgráfico 2: Campo Magnético en el Eje Z
            ax2 = fig.add_subplot(122)
            ax2.plot(z_plot_range, B_z_values, color='green', linewidth=2)
            ax2.set_title('Campo Magnético (Componente Z) en el Eje Central')
            ax2.set_xlabel('Posición Z (m)')
            ax2.set_ylabel('Magnitud del Campo B (Tesla)')
            ax2.grid(True)
            ax2.axvline(x=z1, color='blue', linestyle=':', label='Posición Bobina 1')
            ax2.axvline(x=z2, color='red', linestyle=':', label='Posición Bobina 2')
            ax2.legend()
            ax2.set_xlim([-R * 1.5, R * 1.5]) # Límites para mostrar la región central
            ax2.set_ylim([0, np.max(B_z_values) * 1.1]) # Ajustar límites Y

            # Mostrar la figura
            plt.tight_layout()
            plt.show()
        
        elif opcion == '13':
            print("¡Hasta luego!")
            break
            
        else:
            print("Opción no válida. Por favor, elija una opción entre 1 y 11.")

if __name__ == "__main__":
    menu_principal()
