import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

MU_0 = 4 * np.pi * 1e-7

class BobinasHelmholtz:
    '''
    Clase para calcular y analizar bobinas de Helmholtz
    
    Las bobinas de Helmholtz son dos espiras circulares idénticas,
    coaxiales, separadas por una distancia igual a su radio,
    que producen un campo magnético muy uniforme en la región central.
    '''
    
    def __init__(self, radio=None, corriente=None, separacion=None):
        '''
        radio: radio de las espiras (m)
        corriente: corriente en ambas espiras (A)
        separacion: distancia entre espiras (m). Si es None, se usa d = radio
        '''
        self.a = radio
        self.I = corriente
        self.d = separacion if separacion is not None else radio
        
    def configurar(self):
        '''Solicita los parámetros al usuario'''
        print("\n" + "="*60)
        print(" CONFIGURACIÓN DE BOBINAS DE HELMHOLTZ")
        print("="*60)
        print("\nLas bobinas de Helmholtz son dos espiras circulares idénticas")
        print("separadas por una distancia 'd'. Para máxima uniformidad del")
        print("campo magnético, la separación óptima es d = a (radio).\n")
        
        self.a = float(input("Ingrese el radio de las espiras a (en metros): "))
        self.I = float(input("Ingrese la corriente en las espiras I (en amperios): "))
        
        usar_optima = input("\n¿Usar separación óptima d = a? (s/n): ").lower()
        if usar_optima == 's':
            self.d = self.a
            print(f"Separación configurada: d = {self.d} m (óptima)")
        else:
            self.d = float(input("Ingrese la separación d (en metros): "))
            print(f"Separación configurada: d = {self.d} m")
            if abs(self.d - self.a) > 0.01:
                print("⚠ Nota: La separación no es óptima. La uniformidad será menor.")
        
        print("\n--- Resumen de configuración ---")
        print(f"Radio de espiras: a = {self.a} m")
        print(f"Corriente: I = {self.I} A")
        print(f"Separación: d = {self.d} m")
        print(f"Razón d/a = {self.d/self.a:.3f} (óptimo = 1.000)")
        
    def campo_espira_individual(self, I, a, z_bobina, x, y, z, N=5000):
        '''
        Calcula el campo magnético de una espira ubicada en z = z_bobina
        '''
        phi = np.linspace(0, 2*np.pi, N)
        dphi = phi[1] - phi[0]
        
        # Posición de cada punto de la espira
        xp = a * np.cos(phi)
        yp = a * np.sin(phi)
        zp = np.full(N, z_bobina)
        
        # Vector r desde cada elemento al punto
        rx = xp - x
        ry = yp - y
        rz = zp - z
        
        r_vec = np.vstack((rx, ry, rz))
        r_norm = np.linalg.norm(r_vec, axis=0)
        
        # Elemento de longitud dl
        dl = np.vstack((-a * np.sin(phi) * dphi,
                        a * np.cos(phi) * dphi,
                        np.zeros(N)))
        
        # Producto cruz dl × r
        cross_prod = np.cross(dl.T, r_vec.T)
        
        # Ley de Biot-Savart
        dB = (MU_0 * I / (4*np.pi)) * cross_prod / (r_norm**3)[:, None]
        
        return np.sum(dB, axis=0)
    
    def campo_helmholtz(self, x, y, z):
        '''
        Calcula el campo magnético total de las bobinas de Helmholtz
        Bobina 1 en z = -d/2
        Bobina 2 en z = +d/2
        '''
        B1 = self.campo_espira_individual(self.I, self.a, -self.d/2, x, y, z)
        B2 = self.campo_espira_individual(self.I, self.a, +self.d/2, x, y, z)
        return B1, B2, B1 + B2
    
    def calcular_campo_en_punto(self, x, y, z):
        '''Calcula y muestra el campo en un punto específico'''
        B1, B2, B_total = self.campo_helmholtz(x, y, z)
        
        print("\n" + "="*60)
        print(f"CAMPO MAGNÉTICO EN EL PUNTO ({x}, {y}, {z})")
        print("="*60)
        print(f"Bobina 1 (z=-d/2): B = ({B1[0]:.6e}, {B1[1]:.6e}, {B1[2]:.6e}) T")
        print(f"Bobina 2 (z=+d/2): B = ({B2[0]:.6e}, {B2[1]:.6e}, {B2[2]:.6e}) T")
        print(f"Total          : B = ({B_total[0]:.6e}, {B_total[1]:.6e}, {B_total[2]:.6e}) T")
        print(f"\nMagnitud total: |B| = {np.linalg.norm(B_total):.6e} T")
        
        return B_total
    
    def analizar_uniformidad(self, rango_factor=0.5, n_puntos=50):
        '''
        Analiza la uniformidad del campo en el eje Z
        rango_factor: fracción del radio para analizar
        '''
        z_vals = np.linspace(-rango_factor*self.a, rango_factor*self.a, n_puntos)
        B_magnitudes = []
        Bz_valores = []
        
        print(f"\nAnalizando uniformidad en el eje Z...")
        for z in z_vals:
            _, _, B = self.campo_helmholtz(0, 0, z)
            B_magnitudes.append(np.linalg.norm(B))
            Bz_valores.append(B[2])
        
        B_magnitudes = np.array(B_magnitudes)
        Bz_valores = np.array(Bz_valores)
        
        # Campo en el centro
        B_centro = B_magnitudes[n_puntos//2]
        
        # Calcular variación porcentual
        variacion = ((B_magnitudes - B_centro) / B_centro) * 100
        variacion_max = np.max(np.abs(variacion))
        
        print(f"\n--- Análisis de Uniformidad ---")
        print(f"Campo en el centro: {B_centro:.6e} T")
        print(f"Variación máxima: ±{variacion_max:.2f}%")
        print(f"Rango analizado: ±{rango_factor*self.a:.3f} m (±{rango_factor*100:.0f}% del radio)")
        
        # Graficar
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        
        # Magnitud del campo
        ax1.plot(z_vals, B_magnitudes*1e6, 'b-', linewidth=2)
        ax1.axhline(y=B_centro*1e6, color='r', linestyle='--', 
                   label=f'Centro: {B_centro*1e6:.2f} µT')
        ax1.axvline(x=-self.d/2, color='g', linestyle=':', alpha=0.7, label='Bobinas')
        ax1.axvline(x=self.d/2, color='g', linestyle=':', alpha=0.7)
        ax1.set_xlabel('Posición Z (m)')
        ax1.set_ylabel('|B| (µT)')
        ax1.set_title('Magnitud del Campo Magnético en el eje Z')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Variación porcentual
        ax2.plot(z_vals, variacion, 'r-', linewidth=2)
        ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax2.axvline(x=-self.d/2, color='g', linestyle=':', alpha=0.7, label='Bobinas')
        ax2.axvline(x=self.d/2, color='g', linestyle=':', alpha=0.7)
        ax2.fill_between(z_vals, -1, 1, alpha=0.2, color='green', 
                         label='Zona de alta uniformidad (±1%)')
        ax2.set_xlabel('Posición Z (m)')
        ax2.set_ylabel('Variación respecto al centro (%)')
        ax2.set_title('Uniformidad del Campo Magnético')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.show()
        
        return z_vals, B_magnitudes, variacion
    
    def comparar_separaciones(self, separaciones=[0.5, 0.8, 1.0, 1.2, 1.5], n_puntos=100):
        '''
        Compara la uniformidad para diferentes separaciones d/a
        '''
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        z_vals = np.linspace(-self.a, self.a, n_puntos)
        
        # Guardar configuración original
        d_original = self.d
        
        for factor in separaciones:
            self.d = factor * self.a
            B_magnitudes = []
            
            for z in z_vals:
                _, _, B = self.campo_helmholtz(0, 0, z)
                B_magnitudes.append(np.linalg.norm(B))
            
            B_magnitudes = np.array(B_magnitudes)
            B_centro = B_magnitudes[n_puntos//2]
            variacion = ((B_magnitudes - B_centro) / B_centro) * 100
            
            label = f'd/a = {factor:.1f}'
            if factor == 1.0:
                label += ' (óptimo)'
            
            ax1.plot(z_vals/self.a, B_magnitudes*1e6, linewidth=2, label=label)
            ax2.plot(z_vals/self.a, variacion, linewidth=2, label=label)
        
        # Restaurar configuración original
        self.d = d_original
        
        ax1.set_xlabel('Posición Z/a')
        ax1.set_ylabel('|B| (µT)')
        ax1.set_title('Comparación de Campo Magnético para diferentes separaciones')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax2.fill_between(z_vals/self.a, -1, 1, alpha=0.2, color='green')
        ax2.set_xlabel('Posición Z/a')
        ax2.set_ylabel('Variación respecto al centro (%)')
        ax2.set_title('Uniformidad del Campo - Comparación')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_ylim([-15, 15])
        
        plt.tight_layout()
        plt.show()
    
    def graficar_geometria_3d(self):
        '''Visualiza la configuración geométrica de las bobinas'''
        fig = plt.figure(figsize=(14, 6))
        
        # Vista 3D
        ax1 = fig.add_subplot(121, projection='3d')
        
        theta = np.linspace(0, 2*np.pi, 100)
        x = self.a * np.cos(theta)
        y = self.a * np.sin(theta)
        
        # Bobina 1 (abajo)
        z1 = np.full(100, -self.d/2)
        ax1.plot(x, y, z1, 'b-', linewidth=3, label='Bobina 1 (z=-d/2)')
        
        # Bobina 2 (arriba)
        z2 = np.full(100, self.d/2)
        ax1.plot(x, y, z2, 'r-', linewidth=3, label='Bobina 2 (z=+d/2)')
        
        # Eje Z
        ax1.plot([0, 0], [0, 0], [-self.d, self.d], 'k--', alpha=0.5, label='Eje Z')
        
        # Centro
        ax1.scatter([0], [0], [0], color='green', s=100, marker='o', 
                   label='Centro (campo uniforme)')
        
        ax1.set_xlabel('X (m)')
        ax1.set_ylabel('Y (m)')
        ax1.set_zlabel('Z (m)')
        ax1.set_title('Configuración 3D de Bobinas de Helmholtz')
        ax1.legend()
        ax1.set_box_aspect([1,1,1])
        
        # Vista lateral (XZ)
        ax2 = fig.add_subplot(122)
        
        # Bobinas vistas de lado
        ax2.plot([-self.a, self.a], [-self.d/2, -self.d/2], 'b-', linewidth=3)
        ax2.plot([-self.a, self.a], [self.d/2, self.d/2], 'r-', linewidth=3)
        ax2.plot([-self.a, -self.a], [-self.d/2, self.d/2], 'b--', alpha=0.3)
        ax2.plot([self.a, self.a], [-self.d/2, self.d/2], 'r--', alpha=0.3)
        
        # Indicadores
        ax2.scatter([0], [0], color='green', s=200, marker='o', 
                   label='Región uniforme', zorder=5)
        ax2.arrow(self.a*1.3, -self.d/2, 0, 0.1, head_width=0.05*self.a, 
                 head_length=0.05*self.a, fc='blue', ec='blue')
        ax2.arrow(self.a*1.3, self.d/2, 0, 0.1, head_width=0.05*self.a, 
                 head_length=0.05*self.a, fc='red', ec='red')
        ax2.text(self.a*1.5, -self.d/2, 'I →', fontsize=12, color='blue')
        ax2.text(self.a*1.5, self.d/2, 'I →', fontsize=12, color='red')
        
        # Dimensiones
        ax2.plot([0, self.a], [-self.d*0.7, -self.d*0.7], 'k-', linewidth=1)
        ax2.text(self.a/2, -self.d*0.75, f'a = {self.a} m', ha='center')
        
        ax2.plot([-self.a*1.1, -self.a*1.1], [-self.d/2, self.d/2], 'k-', linewidth=1)
        ax2.text(-self.a*1.3, 0, f'd = {self.d} m\n(d/a = {self.d/self.a:.2f})', 
                ha='center', va='center')
        
        ax2.set_xlabel('X (m)')
        ax2.set_ylabel('Z (m)')
        ax2.set_title('Vista Lateral (plano XZ)')
        ax2.axis('equal')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plt.show()
    
    def graficar_campo_2d(self, plano='xz', n_puntos=20):
        '''Grafica el campo magnético en un plano 2D'''
        rango = self.a * 1.5
        
        if plano == 'xz':
            x = np.linspace(-rango, rango, n_puntos)
            z = np.linspace(-rango, rango, n_puntos)
            X, Z = np.meshgrid(x, z)
            Y = np.zeros_like(X)
            xlabel, ylabel = 'X (m)', 'Z (m)'
        elif plano == 'yz':
            y = np.linspace(-rango, rango, n_puntos)
            z = np.linspace(-rango, rango, n_puntos)
            Y, Z = np.meshgrid(y, z)
            X = np.zeros_like(Y)
            xlabel, ylabel = 'Y (m)', 'Z (m)'
        else:  # xy
            x = np.linspace(-rango, rango, n_puntos)
            y = np.linspace(-rango, rango, n_puntos)
            X, Y = np.meshgrid(x, y)
            Z = np.zeros_like(X)
            xlabel, ylabel = 'X (m)', 'Y (m)'
        
        Bx = np.zeros_like(X)
        By = np.zeros_like(Y)
        Bz = np.zeros_like(Z)
        
        print(f"Calculando campo en plano {plano.upper()}...")
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                _, _, B = self.campo_helmholtz(X[i,j], Y[i,j], Z[i,j])
                Bx[i,j] = B[0]
                By[i,j] = B[1]
                Bz[i,j] = B[2]
        
        B_mag = np.sqrt(Bx**2 + By**2 + Bz**2)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if plano == 'xz':
            quiver = ax.quiver(X, Z, Bx, Bz, B_mag, cmap='jet', alpha=0.8)
            # Dibujar bobinas
            ax.plot([-self.a, self.a], [-self.d/2, -self.d/2], 'b-', linewidth=3)
            ax.plot([-self.a, self.a], [self.d/2, self.d/2], 'r-', linewidth=3)
        elif plano == 'yz':
            quiver = ax.quiver(Y, Z, By, Bz, B_mag, cmap='jet', alpha=0.8)
            ax.plot([-self.a, self.a], [-self.d/2, -self.d/2], 'b-', linewidth=3)
            ax.plot([-self.a, self.a], [self.d/2, self.d/2], 'r-', linewidth=3)
        else:  # xy
            quiver = ax.quiver(X, Y, Bx, By, B_mag, cmap='jet', alpha=0.8)
            theta = np.linspace(0, 2*np.pi, 100)
            ax.plot(self.a*np.cos(theta), self.a*np.sin(theta), 'b-', linewidth=2)
        
        plt.colorbar(quiver, ax=ax, label='|B| (T)')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(f'Campo Magnético - Bobinas de Helmholtz\nPlano {plano.upper()}')
        ax.axis('equal')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()