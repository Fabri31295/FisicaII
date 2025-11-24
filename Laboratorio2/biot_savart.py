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
        Bz_vec = np.zeros_like(Z_vec);
        
        punto_original = self.punto.copy();
        
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
        
        self.punto = punto_original;
        
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

    def cargar_datos_helmholtz(self):
        """Carga los datos para las bobinas de Helmholtz"""
        print("=== BOBINAS DE HELMHOLTZ ===\n")
        
        self.corriente_helmholtz = float(input("Ingrese la corriente I (en amperios): "))
        self.radio_helmholtz = float(input("Ingrese el radio de las bobinas (en metros) [default: 3.0]: ") or "3.0")
        
        # La separación óptima para bobinas de Helmholtz es igual al radio
        self.separacion_helmholtz = self.radio_helmholtz
        
        punto_str = input("Ingrese el punto P donde calcular el campo (x y z): ")
        coords = punto_str.split()
        self.punto = np.array([float(coords[0]), float(coords[1]), float(coords[2])])
        
        print(f"\nDatos cargados:")
        print(f"Corriente: I = {self.corriente_helmholtz} A")
        print(f"Radio de bobinas: R = {self.radio_helmholtz} m")
        print(f"Separación entre bobinas: d = {self.separacion_helmholtz} m")
        print(f"Punto: P = ({self.punto[0]}, {self.punto[1]}, {self.punto[2]}) m")
        
    def campo_bobinas_helmholtz(self, N=1000):
        """
        Calcula el campo magnético de las bobinas de Helmholtz
        usando la ley de Biot-Savart
        
        Las bobinas están centradas en z = ±R/2 (separación = R)
        """
        print(f"\n--- CAMPO DE BOBINAS DE HELMHOLTZ ---")
        
        # Posiciones de las bobinas (en el eje Z)
        z_bobina1 = -self.separacion_helmholtz / 2
        z_bobina2 = self.separacion_helmholtz / 2
        
        # Calcular campo de cada bobina por separado
        punto_original = self.punto.copy()
        
        # Campo de la bobina 1
        self.punto = punto_original.copy()
        B1 = self.campo_espira_en_posicion(self.radio_helmholtz, z_bobina1, N)
        
        # Campo de la bobina 2
        self.punto = punto_original.copy()
        B2 = self.campo_espira_en_posicion(self.radio_helmholtz, z_bobina2, N)
        
        # Campo total (superposición)
        B_total = B1 + B2
        
        # Restaurar punto original
        self.punto = punto_original
        
        return B1, B2, B_total
    
    def campo_espira_en_posicion(self, radio, z_espira, N=1000):
        """
        Calcula el campo magnético de una espira circular en una posición específica en Z
        """
        # Ángulos para dividir la espira
        theta = np.linspace(0, 2*np.pi, N)
        dtheta = theta[1] - theta[0]
        
        # Vector campo magnético total
        B_total = np.array([0.0, 0.0, 0.0])
        
        # Punto donde calculamos el campo
        x, y, z = self.punto[0], self.punto[1], self.punto[2]
        
        for i in range(N):
            # Posición del elemento de corriente en la espira
            x_espira = radio * np.cos(theta[i])
            y_espira = radio * np.sin(theta[i])
            
            # Vector del elemento de corriente dl
            dl = np.array([-radio * np.sin(theta[i]) * dtheta,
                          radio * np.cos(theta[i]) * dtheta,
                          0.0])
            
            # Vector desde el elemento dl hasta el punto P
            r_vector = np.array([x - x_espira, y - y_espira, z - z_espira])
            r_magnitud = np.linalg.norm(r_vector)
            
            # Evitar división por cero
            if r_magnitud < 1e-10:
                continue
                
            # Ley de Biot-Savart: dB = (μ₀/4π) * I * (dl × r) / |r|³
            dl_cross_r = np.cross(dl, r_vector)
            dB = (MU_0 / (4 * np.pi)) * self.corriente_helmholtz * dl_cross_r / (r_magnitud**3)
            
            B_total += dB
        
        return B_total
    
    def mostrar_resultados_helmholtz(self, B1, B2, B_total):
        """Muestra los resultados del cálculo de bobinas de Helmholtz"""
        print("\n" + "="*60)
        print("                    RESULTADOS")
        print("="*60)
        
        print(f"\n🔵 BOBINA 1 (z = {-self.separacion_helmholtz/2:.1f} m):")
        print(f"   Bx = {B1[0]:.6e} T")
        print(f"   By = {B1[1]:.6e} T")
        print(f"   Bz = {B1[2]:.6e} T")
        print(f"   |B1| = {np.linalg.norm(B1):.6e} T")
        
        print(f"\n🔴 BOBINA 2 (z = {self.separacion_helmholtz/2:.1f} m):")
        print(f"   Bx = {B2[0]:.6e} T")
        print(f"   By = {B2[1]:.6e} T")
        print(f"   Bz = {B2[2]:.6e} T")
        print(f"   |B2| = {np.linalg.norm(B2):.6e} T")
        
        print(f"\n🌟 CAMPO TOTAL (SUPERPOSICIÓN):")
        print(f"   Bx = {B_total[0]:.6e} T")
        print(f"   By = {B_total[1]:.6e} T")
        print(f"   Bz = {B_total[2]:.6e} T")
        print(f"   |B_total| = {np.linalg.norm(B_total):.6e} T")
        
        # Comparar magnitudes
        reduccion_x = abs(B_total[0]) / max(abs(B1[0]), abs(B2[0])) if max(abs(B1[0]), abs(B2[0])) > 0 else 0
        reduccion_y = abs(B_total[1]) / max(abs(B1[1]), abs(B2[1])) if max(abs(B1[1]), abs(B2[1])) > 0 else 0
        
        print(f"\n📊 ANÁLISIS DE UNIFORMIDAD:")
        print(f"   • En el centro (0,0,0), el campo es muy uniforme")
        print(f"   • Componentes transversales muy reducidas")
        print(f"   • Campo principalmente en dirección Z")
        print(f"   • Configuración óptima para campo uniforme")
        
        print("\n" + "="*60)

    def graficar_configuracion_helmholtz(self):
        """Grafica la configuración de las bobinas de Helmholtz"""
        fig = plt.figure(figsize=(15, 10))
        
        # Vista 3D
        ax1 = fig.add_subplot(221, projection='3d')
        
        # Dibujar las bobinas de Helmholtz
        theta = np.linspace(0, 2*np.pi, 100)
        
        # Bobina 1 (z = -R/2)
        x1 = self.radio_helmholtz * np.cos(theta)
        y1 = self.radio_helmholtz * np.sin(theta)
        z1 = np.full_like(theta, -self.separacion_helmholtz/2)
        ax1.plot(x1, y1, z1, 'b-', linewidth=4, label='Bobina 1')
        
        # Bobina 2 (z = +R/2)
        x2 = self.radio_helmholtz * np.cos(theta)
        y2 = self.radio_helmholtz * np.sin(theta)
        z2 = np.full_like(theta, self.separacion_helmholtz/2)
        ax1.plot(x2, y2, z2, 'r-', linewidth=4, label='Bobina 2')
        
        # Punto de cálculo
        ax1.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='green', s=100, marker='*', label='Punto P')
        
        # Líneas de conexión para mostrar la estructura
        ax1.plot([0, 0], [0, 0], [-self.separacion_helmholtz/2, self.separacion_helmholtz/2], 
                'k--', alpha=0.5, linewidth=1)
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('Bobinas de Helmholtz - Vista 3D')
        ax1.legend()
        
        # Vista lateral (XZ)
        ax2 = fig.add_subplot(222)
        
        # Bobinas vistas de lado
        ax2.plot([-self.radio_helmholtz, self.radio_helmholtz], 
                [-self.separacion_helmholtz/2, -self.separacion_helmholtz/2], 'b-', linewidth=6, label='Bobina 1')
        ax2.plot([-self.radio_helmholtz, self.radio_helmholtz], 
                [self.separacion_helmholtz/2, self.separacion_helmholtz/2], 'r-', linewidth=6, label='Bobina 2')
        
        # Punto de cálculo
        ax2.scatter(self.punto[0], self.punto[2], color='green', s=100, marker='*', label='Punto P')
        
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Z (m)')
        ax2.set_title('Vista Lateral (XZ)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_aspect('equal')
        
        # Vista superior (XY)
        ax3 = fig.add_subplot(223)
        
        # Proyección de las bobinas
        circle1 = plt.Circle((0, 0), self.radio_helmholtz, fill=False, color='blue', linewidth=3, alpha=0.7)
        circle2 = plt.Circle((0, 0), self.radio_helmholtz, fill=False, color='red', linewidth=3, alpha=0.7, linestyle='--')
        ax3.add_patch(circle1)
        ax3.add_patch(circle2)
        
        # Punto de cálculo
        ax3.scatter(self.punto[0], self.punto[1], color='green', s=100, marker='*', label='Punto P')
        
        ax3.set_xlabel('X (m)')
        ax3.set_ylabel('Y (m)')
        ax3.set_title('Vista Superior (XY)')
        ax3.grid(True, alpha=0.3)
        ax3.legend(['Bobina 1', 'Bobina 2', 'Punto P'])
        ax3.set_aspect('equal')
        ax3.set_xlim(-self.radio_helmholtz*1.5, self.radio_helmholtz*1.5)
        ax3.set_ylim(-self.radio_helmholtz*1.5, self.radio_helmholtz*1.5)
        
        # Información
        ax4 = fig.add_subplot(224)
        ax4.axis('off')
        
        info_text = f"""
BOBINAS DE HELMHOLTZ

Características:
• Radio: R = {self.radio_helmholtz} m
• Separación: d = {self.separacion_helmholtz} m
• Corriente: I = {self.corriente_helmholtz} A
• Punto: P = ({self.punto[0]:.1f}, {self.punto[1]:.1f}, {self.punto[2]:.1f}) m

Propiedades especiales:
• d = R (separación óptima = radio)
• Campo muy uniforme en la región central
• Gradiente de campo mínimo
• Configuración estándar en laboratorios

Aplicaciones:
• Calibración de instrumentos magnéticos
• Experimentos de física atómica
• Anulación del campo magnético terrestre
• Estudios de propiedades magnéticas

Campo en el centro:
B₀ = (8μ₀IR²)/(5√5 R³) = (8μ₀I)/(5√5 R)

Las bobinas de Helmholtz son la configuración
estándar para generar campos magnéticos
uniformes en el laboratorio.
        """
        
        ax4.text(0.05, 0.95, info_text, fontsize=9, 
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcyan', alpha=0.8))
        
        plt.tight_layout()
        plt.show()

    def graficar_lineas_campo_helmholtz(self):
        """Grafica las líneas de campo magnético de las bobinas de Helmholtz"""
        print("Generando visualización del campo magnético para bobinas de Helmholtz...")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Calcular campo en grilla para visualización
        X, Z, Bx, Bz = self.calcular_campo_helmholtz_grilla()
        
        # Gráfico 1: Líneas de campo (vista XZ)
        magnitud = np.sqrt(Bx**2 + Bz**2)
        magnitud[magnitud == 0] = 1e-10  # Evitar división por cero
        
        # Dibujar líneas de campo usando streamplot
        ax1.streamplot(X, Z, Bx, Bz, density=1.5, color=magnitud, cmap='plasma', arrowsize=1.5)
        
        # Dibujar las bobinas
        ax1.plot([-self.radio_helmholtz, self.radio_helmholtz], 
                [-self.separacion_helmholtz/2, -self.separacion_helmholtz/2], 'b-', linewidth=8, label='Bobina 1')
        ax1.plot([-self.radio_helmholtz, self.radio_helmholtz], 
                [self.separacion_helmholtz/2, self.separacion_helmholtz/2], 'r-', linewidth=8, label='Bobina 2')
        
        ax1.set_xlabel('X (m)', fontsize=12)
        ax1.set_ylabel('Z (m)', fontsize=12)
        ax1.set_title('Líneas de Campo Magnético\n(Vista Lateral XZ)', fontsize=14)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.set_aspect('equal')
        
        # Gráfico 2: Intensidad del campo
        im2 = ax2.contourf(X, Z, magnitud, levels=20, cmap='viridis')
        ax2.plot([-self.radio_helmholtz, self.radio_helmholtz], 
                [-self.separacion_helmholtz/2, -self.separacion_helmholtz/2], 'w-', linewidth=6)
        ax2.plot([-self.radio_helmholtz, self.radio_helmholtz], 
                [self.separacion_helmholtz/2, self.separacion_helmholtz/2], 'w-', linewidth=6)
        
        ax2.set_xlabel('X (m)', fontsize=12)
        ax2.set_ylabel('Z (m)', fontsize=12)
        ax2.set_title('Intensidad del Campo |B|', fontsize=14)
        cbar2 = plt.colorbar(im2, ax=ax2)
        cbar2.set_label('|B| (T)', fontsize=12)
        ax2.set_aspect('equal')
        
        # Gráfico 3: Campo a lo largo del eje Z
        z_axis = np.linspace(-self.radio_helmholtz*2, self.radio_helmholtz*2, 100)
        B_axis = []
        
        punto_original = self.punto.copy()
        for z_val in z_axis:
            self.punto = np.array([0, 0, z_val])
            _, _, B_total = self.campo_bobinas_helmholtz(N=500)
            B_axis.append(np.linalg.norm(B_total))
        
        self.punto = punto_original  # Restaurar punto original
        
        ax3.plot(z_axis, B_axis, 'g-', linewidth=3, label='|B| en eje Z')
        ax3.axvline(-self.separacion_helmholtz/2, color='blue', linestyle='--', alpha=0.7, label='Bobina 1')
        ax3.axvline(self.separacion_helmholtz/2, color='red', linestyle='--', alpha=0.7, label='Bobina 2')
        ax3.axvline(0, color='black', linestyle='-', alpha=0.5, label='Centro')
        
        ax3.set_xlabel('Z (m)', fontsize=12)
        ax3.set_ylabel('|B| (T)', fontsize=12)
        ax3.set_title('Campo Magnético a lo largo del Eje Z', fontsize=14)
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # Gráfico 4: Análisis de uniformidad
        ax4.axis('off')
        
        # Calcular campo en el centro
        self.punto = np.array([0, 0, 0])
        _, _, B_centro = self.campo_bobinas_helmholtz(N=1000)
        self.punto = punto_original
        
        analysis_text = f"""
ANÁLISIS DE UNIFORMIDAD

Campo en el centro (0,0,0):
• Bx = {B_centro[0]:.6e} T
• By = {B_centro[1]:.6e} T  
• Bz = {B_centro[2]:.6e} T
• |B| = {np.linalg.norm(B_centro):.6e} T

Características del campo:
✓ Región central muy uniforme
✓ Campo principalmente en dirección Z
✓ Componentes transversales mínimas
✓ Gradiente muy pequeño cerca del centro

Comparación con campo teórico:
B₀_teórico = (8μ₀I)/(5√5·R)
B₀_teórico = {(8*MU_0*self.corriente_helmholtz)/(5*np.sqrt(5)*self.radio_helmholtz):.6e} T

Error relativo: {abs(np.linalg.norm(B_centro) - (8*MU_0*self.corriente_helmholtz)/(5*np.sqrt(5)*self.radio_helmholtz)) / ((8*MU_0*self.corriente_helmholtz)/(5*np.sqrt(5)*self.radio_helmholtz)) * 100:.2f}%

Las bobinas de Helmholtz proporcionan
el campo más uniforme posible con
dos bobinas circulares coaxiales.
        """
        
        ax4.text(0.05, 0.95, analysis_text, fontsize=10, 
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.8))
        
        plt.tight_layout()
        plt.show()

    def calcular_campo_helmholtz_grilla(self, rango=5, resolucion=25):
        """Calcula el campo magnético en una grilla para visualización"""
        x = np.linspace(-rango, rango, resolucion)
        z = np.linspace(-rango, rango, resolucion)
        X, Z = np.meshgrid(x, z)
        
        Bx = np.zeros_like(X)
        Bz = np.zeros_like(Z)
        
        print(f"Calculando campo magnético en {resolucion}x{resolucion} puntos...")
        
        punto_original = self.punto.copy()
        
        for i in range(resolucion):
            for j in range(resolucion):
                self.punto = np.array([X[i,j], 0, Z[i,j]])  # Plano y=0
                
                try:
                    _, _, B_total = self.campo_bobinas_helmholtz(N=200)  # Menos puntos para velocidad
                    Bx[i,j] = B_total[0]
                    Bz[i,j] = B_total[2]
                except:
                    Bx[i,j] = Bz[i,j] = 0
        
        self.punto = punto_original  # Restaurar punto original
        return X, Z, Bx, Bz

    def graficar_lineas_campo_combinado(self):
        """Grafica las líneas de campo magnético de la configuración combinada alambre+espira"""
        print("Generando visualización de líneas de campo para configuración combinada...")
        print("Esto puede tomar un momento, por favor espere...")
        
        fig = plt.figure(figsize=(20, 12))
        
        # Gráfico 1: Vista 3D con líneas de campo combinadas
        ax1 = fig.add_subplot(221, projection='3d')
        
        # Dibujar alambre (eje Z)
        z_alambre = np.linspace(-1, 1, 100)
        x_alambre = np.zeros_like(z_alambre)
        y_alambre = np.zeros_like(z_alambre)
        ax1.plot(x_alambre, y_alambre, z_alambre, 'r-', linewidth=6, 
                label=f'Alambre I1={self.corriente_alambre}A', zorder=10)
        
        # Dibujar espira (plano XY)
        phi_espira = np.linspace(0, 2*np.pi, 100)
        x_espira = 3 * np.cos(phi_espira)
        y_espira = 3 * np.sin(phi_espira)
        z_espira = np.zeros_like(phi_espira)
        ax1.plot(x_espira, y_espira, z_espira, 'g-', linewidth=8, 
                label=f'Espira I2={self.corriente_espira}A', zorder=10)
        
        # Generar líneas de campo combinadas
        # Campo del alambre: líneas circulares
        radios_alambre = [0.5, 1.0, 1.5, 2.0, 2.5]
        alturas_alambre = np.linspace(-0.8, 0.8, 5)
        theta = np.linspace(0, 2*np.pi, 100)
        
        for r in radios_alambre:
            for z_nivel in alturas_alambre:
                # Evitar la región de la espira
                if abs(z_nivel) > 0.1 or r > 3.3 or r < 2.7:
                    x_circ = r * np.cos(theta)
                    y_circ = r * np.sin(theta)
                    z_circ = np.full_like(theta, z_nivel)
                    ax1.plot(x_circ, y_circ, z_circ, 'blue', alpha=0.4, linewidth=1)
        
        # Campo de la espira: líneas dipolares
        phi_dipolo = np.linspace(0, 2*np.pi, 8)
        for phi in phi_dipolo:
            t = np.linspace(0.5, 4, 40)
            
            # Líneas superiores
            for z_start in [0.3, 0.7, 1.2]:
                r = t
                z_line = z_start + t**0.8
                x_line = r * np.cos(phi)
                y_line = r * np.sin(phi)
                
                # Evitar intersección con espira y alambre
                mask = (r > 3.4) & (np.abs(z_line) > 0.2)
                if np.any(mask):
                    ax1.plot(x_line[mask], y_line[mask], z_line[mask], 
                            'purple', alpha=0.6, linewidth=1.5)
                
                # Líneas inferiores
                z_line_neg = -z_start - t**0.8
                mask_neg = (r > 3.4) & (np.abs(z_line_neg) > 0.2)
                if np.any(mask_neg):
                    ax1.plot(x_line[mask_neg], y_line[mask_neg], z_line_neg[mask_neg], 
                            'purple', alpha=0.6, linewidth=1.5)
        
        # Líneas en el eje Z (dominadas por la espira)
        z_axis = np.linspace(-2.5, 2.5, 60)
        x_axis = np.zeros_like(z_axis)
        y_axis = np.zeros_like(z_axis)
        # Evitar la región del alambre
        mask_eje = np.abs(z_axis) > 1.1
        ax1.plot(x_axis[mask_eje], y_axis[mask_eje], z_axis[mask_eje], 
                'purple', linewidth=3, alpha=0.8)
        
        # Flechas direccionales en el eje
        for z_arrow in [-2, -1.5, 1.5, 2]:
            ax1.quiver(0, 0, z_arrow, 0, 0, 0.3,
                     color='red', arrow_length_ratio=0.3, alpha=0.9, linewidth=2)
        
        # Punto de cálculo
        ax1.scatter(self.punto[0], self.punto[1], self.punto[2], 
                   color='orange', s=200, marker='*', 
                   label=f'P({self.punto[0]:.1f},{self.punto[1]:.1f},{self.punto[2]:.1f})',
                   zorder=15, edgecolor='black', linewidth=2)
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('Líneas de Campo 3D - Configuración Combinada')
        ax1.legend()
        ax1.set_xlim(-4, 4)
        ax1.set_ylim(-4, 4)
        ax1.set_zlim(-3, 3)
        
        # Gráfico 2: Campo vectorial combinado en plano XZ
        ax2 = fig.add_subplot(222, projection='3d')
        
        # Dibujar configuración
        ax2.plot(x_alambre, y_alambre, z_alambre, 'r-', linewidth=6, label='Alambre')
        ax2.plot([-3, 3], [0, 0], [0, 0], 'g-', linewidth=6, label='Espira (vista lateral)')
        
        # Calcular campo vectorial combinado
        x_vec = np.linspace(-4, 4, 10)
        z_vec = np.linspace(-2.5, 2.5, 8)
        X_vec, Z_vec = np.meshgrid(x_vec, z_vec)
        Y_vec = np.zeros_like(X_vec)
        
        Bx_total = np.zeros_like(X_vec)
        By_total = np.zeros_like(Y_vec)
        Bz_total = np.zeros_like(Z_vec);
        
        punto_original = self.punto.copy();
        
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
        
        self.punto = punto_original;
        
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
        ax2.set_title('Campo Vectorial Combinado\n(Plano XZ, Y=0)')
        ax2.legend()
        
        # Gráfico 3: Intensidad del campo combinado en plano XY
        ax3 = fig.add_subplot(223)
        
        x_int = np.linspace(-5, 5, 40)
        y_int = np.linspace(-5, 5, 40)
        X_int, Y_int = np.meshgrid(x_int, y_int)
        
        B_intensity = np.zeros_like(X_int)
        
        for i in range(X_int.shape[0]):
            for j in range(X_int.shape[1]):
                x_pos, y_pos = X_int[i,j], Y_int[i,j]
                
                # Evitar la región del alambre y la espira
                dist_alambre = np.sqrt(x_pos**2 + y_pos**2)
                dist_espira = abs(np.sqrt(x_pos**2 + y_pos**2) - 3.0)
                
                if dist_alambre < 0.2 or dist_espira < 0.2:
                    B_intensity[i,j] = np.nan
                    continue
                
                self.punto = np.array([x_pos, y_pos, 0])
                B_alambre, B_espira, B_total = self.campo_combinado(N=200)
                B_intensity[i,j] = np.log10(np.linalg.norm(B_total) + 1e-12)
        
        self.punto = punto_original
        
        # Mapa de contorno
        contour = ax3.contourf(X_int, Y_int, B_intensity, levels=25, cmap='plasma')
        ax3.contour(X_int, Y_int, B_intensity, levels=25, colors='black', alpha=0.2, linewidths=0.5)
        

        
        # Líneas de campo esquemáticas
        theta_lines = np.linspace(0, 2*np.pi, 12)
        for theta in theta_lines:
            r_line = np.linspace(3.5, 4.8, 20)
            x_line = r_line * np.cos(theta)
            y_line = r_line * np.sin(theta)
            ax3.plot(x_line, y_line, 'w--', alpha=0.5, linewidth=1)
        
        ax3.set_xlabel('X (m)')
        ax3.set_ylabel('Y (m)')
        ax3.set_title('Intensidad del Campo Combinado\n(Plano XY, Z=0)')
        ax3.set_aspect('equal')
        
        plt.colorbar(contour, ax=ax3, label='log₁₀|B| (T)')
        
        # Gráfico 4: Información
        ax4 = fig.add_subplot(224)
        ax4.axis('off')
        
        info_text = f"""
CONFIGURACIÓN COMBINADA
ALAMBRE + ESPIRA

Características:
• Alambre: I1 = {self.corriente_alambre} A, L = 2 m (eje Z)
• Espira: I2 = {self.corriente_espira} A, a = 3 m (plano XY)
• Punto: P = ({self.punto[0]:.1f}, {self.punto[1]:.1f}, {self.punto[2]:.1f}) m

Patrón del campo combinado:
• Cerca del alambre: líneas circulares dominantes
• En el eje Z: campo dipolar de la espira
• Región intermedia: superposición compleja

Interacciones:
• Los campos se suman vectorialmente
• En algunos puntos se refuerzan
• En otros se debilitan o anulan
• Patrón muy complejo y rico

Ley de superposición:
B⃗_total = B⃗_alambre + B⃗_espira

El campo resultante muestra la belleza
de la interacción electromagnética entre
diferentes geometrías de corriente.
        """
        
        ax4.text(0.05, 0.95, info_text, fontsize=10, 
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.8))
        
        plt.tight_layout()
        plt.show()



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
        print("12. Salir")
        print("-"*60)
        
        opcion = input("Seleccione una opción (1-12): ")
        
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
            # Bobinas de Helmholtz
            biot.cargar_datos_helmholtz()
            B1, B2, B_total = biot.campo_bobinas_helmholtz()
            biot.mostrar_resultados_helmholtz(B1, B2, B_total)
            
            print("\n🌟 Generando visualización de configuración...")
            biot.graficar_configuracion_helmholtz()
            
            print("\n🌟 Generando visualización de líneas de campo...")
            biot.graficar_lineas_campo_helmholtz()
            
        elif opcion == '12':
            print("¡Hasta luego!")
            break
            
        else:
            print("Opción no válida. Por favor, elija una opción entre 1 y 12.")

if __name__ == "__main__":
    menu_principal()
