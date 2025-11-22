import numpy as np

MU_0 = 4 * np.pi * 1e-7

class CampoMagnetico:
    def __init__(self):
        self.L = None
        self.I1 = None
        self.a = None
        self.I2 = None
        self.punto = None

    def carga_de_datos(self):
        '''
        Función que carga los datos del sistema
        '''
        print("=== Datos del sistema: alambre recto + espira circular ===")

        # Datos del alambre
        self.L = float(input("Ingrese la longitud del alambre L (en metros): "))
        self.I1 = float(input("Ingrese la corriente en el alambre I1 (en amperios): "))

        # Datos de la espira
        self.a = float(input("Ingrese el radio de la espira a (en metros): "))
        self.I2 = float(input("Ingrese la corriente en la espira I2 (en amperios): "))

        print("\n--- Resumen de los datos ingresados ---")
        print(f"Longitud del alambre: L = {self.L} m")
        print(f"Corriente en el alambre: I1 = {self.I1} A")
        print(f"Radio de la espira: a = {self.a} m")
        print(f"Corriente en la espira: I2 = {self.I2} A")

        punto = str(input("\nIngrese el punto para calcular el campo magnético (X Y Z): "))
        self.punto = punto.split()
    
    def calcular_campo_en_punto(self):
        '''
        Calcula el campo magnético en el punto especificado
        '''
        if self.punto is None:
            print("Error: Primero debe cargar los datos")
            return
        
        x = float(self.punto[0])
        y = float(self.punto[1])
        z = float(self.punto[2])

        B_al, B_es, B_tot = self.campo_total(self.I1, self.I2, self.L, self.a, x, y, z)

        print("\n" + "="*50)
        print("CAMPO MAGNÉTICO EN EL PUNTO ({}, {}, {})".format(x, y, z))
        print("="*50)
        print(f"Alambre: B = ({B_al[0]:.6e}, {B_al[1]:.6e}, {B_al[2]:.6e}) T")
        print(f"Espira : B = ({B_es[0]:.6e}, {B_es[1]:.6e}, {B_es[2]:.6e}) T")
        print(f"Total  : B = ({B_tot[0]:.6e}, {B_tot[1]:.6e}, {B_tot[2]:.6e}) T")
        print(f"\nMagnitud del campo total: |B| = {np.linalg.norm(B_tot):.6e} T")

    # ------------------- CAMPO DEL ALAMBRE -------------------

    def campo_alambre(self, I1, L, x, y, z, N=5000):
        '''
        Calcula el campo magnético de un alambre recto
        '''
        z_vals = np.linspace(-L/2, L/2, N)
        dz = z_vals[1] - z_vals[0]

        rx = -x
        ry = -y
        rz = z_vals - z

        r_vec = np.vstack((np.full(N, rx),
                        np.full(N, ry),
                        rz))

        r_norm = np.linalg.norm(r_vec, axis=0)

        dl = np.array([[0], [0], [dz]])
        cross_prod = np.cross(dl.T, r_vec.T)

        dB = (MU_0 * I1 / (4*np.pi)) * cross_prod / (r_norm**3)[:, None]

        return np.sum(dB, axis=0)

    # ------------------- CAMPO DE LA ESPIRA -------------------

    def campo_espira(self, I2, a, x, y, z, N=5000):
        '''
        Calcula el campo magnético de una espira circular
        '''
        phi = np.linspace(0, 2*np.pi, N)
        dphi = phi[1] - phi[0]

        xp = a * np.cos(phi)
        yp = a * np.sin(phi)
        zp = np.zeros(N)

        rx = xp - x
        ry = yp - y
        rz = zp - z

        r_vec = np.vstack((rx, ry, rz))
        r_norm = np.linalg.norm(r_vec, axis=0)

        dl = np.vstack((-a * np.sin(phi) * dphi,
                        a * np.cos(phi) * dphi,
                        np.zeros(N)))

        cross_prod = np.cross(dl.T, r_vec.T)

        dB = (MU_0 * I2 / (4*np.pi)) * cross_prod / (r_norm**3)[:, None]

        return np.sum(dB, axis=0)

    # ------------------- CAMPO TOTAL -------------------

    def campo_total(self, I1, I2, L, a, x, y, z):
        '''
        Calcula el campo magnético total (alambre + espira)
        '''
        B1 = self.campo_alambre(I1, L, x, y, z)
        B2 = self.campo_espira(I2, a, x, y, z)
        return B1, B2, B1 + B2
    
    # ------------------- CAMPO EN GRILLA -------------------
    
    def campo_en_grilla(self, x_range, y_range, z_range, tipo='total'):
        '''
        Calcula el campo magnético en una grilla de puntos
        tipo: 'alambre', 'espira', o 'total'
        '''
        X, Y, Z = np.meshgrid(x_range, y_range, z_range)
        Bx = np.zeros_like(X)
        By = np.zeros_like(Y)
        Bz = np.zeros_like(Z)
        
        total_points = X.size
        print(f"Calculando campo en {total_points} puntos...")
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                for k in range(X.shape[2]):
                    x, y, z = X[i,j,k], Y[i,j,k], Z[i,j,k]
                    
                    if tipo == 'alambre':
                        B = self.campo_alambre(self.I1, self.L, x, y, z)
                    elif tipo == 'espira':
                        B = self.campo_espira(self.I2, self.a, x, y, z)
                    else:  # total
                        _, _, B = self.campo_total(self.I1, self.I2, self.L, self.a, x, y, z)
                    
                    Bx[i,j,k] = B[0]
                    By[i,j,k] = B[1]
                    Bz[i,j,k] = B[2]
        
        print("Cálculo completado.")
        return X, Y, Z, Bx, By, Bz