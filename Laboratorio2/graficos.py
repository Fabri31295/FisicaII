import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def graficar_configuracion_geometrica(campo_obj):
    '''
    Dibuja la geometría del sistema (alambre + espira)
    '''
    fig = plt.figure(figsize=(12, 5))
    
    # Vista 3D
    ax1 = fig.add_subplot(121, projection='3d')
    
    # Dibujar alambre
    z_alambre = np.linspace(-campo_obj.L/2, campo_obj.L/2, 100)
    ax1.plot([0]*100, [0]*100, z_alambre, 'b-', linewidth=3, label='Alambre')
    
    # Dibujar espira
    theta = np.linspace(0, 2*np.pi, 100)
    x_espira = campo_obj.a * np.cos(theta)
    y_espira = campo_obj.a * np.sin(theta)
    z_espira = np.zeros(100)
    ax1.plot(x_espira, y_espira, z_espira, 'r-', linewidth=3, label='Espira')
    
    ax1.set_xlabel('X (m)')
    ax1.set_ylabel('Y (m)')
    ax1.set_zlabel('Z (m)')
    ax1.set_title('Configuración 3D del Sistema')
    ax1.legend()
    ax1.grid(True)
    
    # Vista 2D (plano XY)
    ax2 = fig.add_subplot(122)
    ax2.plot(x_espira, y_espira, 'r-', linewidth=3, label='Espira')
    ax2.plot(0, 0, 'bo', markersize=10, label='Alambre (eje Z)')
    ax2.set_xlabel('X (m)')
    ax2.set_ylabel('Y (m)')
    ax2.set_title('Vista desde arriba (plano XY)')
    ax2.axis('equal')
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

def graficar_campo_2d(campo_obj, plano='xy', tipo='total', n_puntos=20):
    '''
    Grafica el campo magnético en un plano 2D con vectores
    plano: 'xy', 'xz', o 'yz'
    tipo: 'alambre', 'espira', o 'total'
    '''
    # Determinar rango de la grilla
    rango = max(campo_obj.L, campo_obj.a * 2) * 1.2
    
    if plano == 'xy':
        x = np.linspace(-rango, rango, n_puntos)
        y = np.linspace(-rango, rango, n_puntos)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        xlabel, ylabel = 'X (m)', 'Y (m)'
        titulo = 'Campo Magnético en el plano XY (z=0)'
        
    elif plano == 'xz':
        x = np.linspace(-rango, rango, n_puntos)
        z = np.linspace(-rango, rango, n_puntos)
        X, Z = np.meshgrid(x, z)
        Y = np.zeros_like(X)
        
        xlabel, ylabel = 'X (m)', 'Z (m)'
        titulo = 'Campo Magnético en el plano XZ (y=0)'
        
    else:  # yz
        y = np.linspace(-rango, rango, n_puntos)
        z = np.linspace(-rango, rango, n_puntos)
        Y, Z = np.meshgrid(y, z)
        X = np.zeros_like(Y)
        
        xlabel, ylabel = 'Y (m)', 'Z (m)'
        titulo = 'Campo Magnético en el plano YZ (x=0)'
    
    # Calcular campo
    Bx = np.zeros_like(X)
    By = np.zeros_like(Y)
    Bz = np.zeros_like(Z)
    
    print(f"Calculando campo en plano {plano.upper()}...")
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if tipo == 'alambre':
                B = campo_obj.campo_alambre(campo_obj.I1, campo_obj.L, 
                                           X[i,j], Y[i,j], Z[i,j])
            elif tipo == 'espira':
                B = campo_obj.campo_espira(campo_obj.I2, campo_obj.a, 
                                          X[i,j], Y[i,j], Z[i,j])
            else:  # total
                _, _, B = campo_obj.campo_total(campo_obj.I1, campo_obj.I2, 
                                               campo_obj.L, campo_obj.a,
                                               X[i,j], Y[i,j], Z[i,j])
            
            Bx[i,j] = B[0]
            By[i,j] = B[1]
            Bz[i,j] = B[2]
    
    # Graficar
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Magnitud del campo para el color
    B_mag = np.sqrt(Bx**2 + By**2 + Bz**2)
    
    if plano == 'xy':
        quiver = ax.quiver(X, Y, Bx, By, B_mag, cmap='jet', alpha=0.8)
        # Dibujar geometría
        theta = np.linspace(0, 2*np.pi, 100)
        ax.plot(campo_obj.a * np.cos(theta), campo_obj.a * np.sin(theta), 
                'r-', linewidth=2, label='Espira')
        ax.plot(0, 0, 'bo', markersize=8, label='Alambre')
        
    elif plano == 'xz':
        quiver = ax.quiver(X, Z, Bx, Bz, B_mag, cmap='jet', alpha=0.8)
        # Dibujar geometría
        ax.plot([0, 0], [-campo_obj.L/2, campo_obj.L/2], 
                'b-', linewidth=3, label='Alambre')
        ax.plot([-campo_obj.a, campo_obj.a], [0, 0], 
                'r-', linewidth=3, label='Espira')
        
    else:  # yz
        quiver = ax.quiver(Y, Z, By, Bz, B_mag, cmap='jet', alpha=0.8)
        # Dibujar geometría
        ax.plot([0, 0], [-campo_obj.L/2, campo_obj.L/2], 
                'b-', linewidth=3, label='Alambre')
        ax.plot([-campo_obj.a, campo_obj.a], [0, 0], 
                'r-', linewidth=3, label='Espira')
    
    plt.colorbar(quiver, ax=ax, label='|B| (T)')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(f'{titulo}\nTipo: {tipo.capitalize()}')
    ax.axis('equal')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.show()

def graficar_campo_3d(campo_obj, tipo='total', n_puntos=8):
    '''
    Grafica el campo magnético en 3D con vectores
    tipo: 'alambre', 'espira', o 'total'
    '''
    rango = max(campo_obj.L, campo_obj.a * 2) * 0.8
    
    x = np.linspace(-rango, rango, n_puntos)
    y = np.linspace(-rango, rango, n_puntos)
    z = np.linspace(-rango, rango, n_puntos)
    
    X, Y, Z = np.meshgrid(x, y, z)
    
    Bx = np.zeros_like(X)
    By = np.zeros_like(Y)
    Bz = np.zeros_like(Z)
    
    print(f"Calculando campo 3D ({n_puntos}³ = {n_puntos**3} puntos)...")
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            for k in range(X.shape[2]):
                if tipo == 'alambre':
                    B = campo_obj.campo_alambre(campo_obj.I1, campo_obj.L, 
                                               X[i,j,k], Y[i,j,k], Z[i,j,k])
                elif tipo == 'espira':
                    B = campo_obj.campo_espira(campo_obj.I2, campo_obj.a, 
                                              X[i,j,k], Y[i,j,k], Z[i,j,k])
                else:  # total
                    _, _, B = campo_obj.campo_total(campo_obj.I1, campo_obj.I2, 
                                                   campo_obj.L, campo_obj.a,
                                                   X[i,j,k], Y[i,j,k], Z[i,j,k])
                
                Bx[i,j,k] = B[0]
                By[i,j,k] = B[1]
                Bz[i,j,k] = B[2]
    
    # Graficar
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Magnitud para el color
    B_mag = np.sqrt(Bx**2 + By**2 + Bz**2)
    
    # Vectores del campo
    ax.quiver(X, Y, Z, Bx, By, Bz, 
             length=rango*0.3, normalize=True, 
             color=plt.cm.jet(B_mag/B_mag.max()), alpha=0.7)
    
    # Dibujar geometría
    z_alambre = np.linspace(-campo_obj.L/2, campo_obj.L/2, 100)
    ax.plot([0]*100, [0]*100, z_alambre, 'b-', linewidth=4, label='Alambre')
    
    theta = np.linspace(0, 2*np.pi, 100)
    x_espira = campo_obj.a * np.cos(theta)
    y_espira = campo_obj.a * np.sin(theta)
    ax.plot(x_espira, y_espira, [0]*100, 'r-', linewidth=4, label='Espira')
    
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title(f'Campo Magnético 3D\nTipo: {tipo.capitalize()}')
    ax.legend()
    
    plt.tight_layout()
    plt.show()

def graficar_magnitud_en_eje(campo_obj, eje='z', tipo='total', n_puntos=100):
    '''
    Grafica la magnitud del campo magnético a lo largo de un eje
    '''
    rango = max(campo_obj.L, campo_obj.a * 2) * 1.5
    puntos = np.linspace(-rango, rango, n_puntos)
    
    B_mag = []
    
    for p in puntos:
        if eje == 'z':
            x, y, z = 0, 0, p
        elif eje == 'x':
            x, y, z = p, 0, 0
        else:  # y
            x, y, z = 0, p, 0
        
        if tipo == 'alambre':
            B = campo_obj.campo_alambre(campo_obj.I1, campo_obj.L, x, y, z)
        elif tipo == 'espira':
            B = campo_obj.campo_espira(campo_obj.I2, campo_obj.a, x, y, z)
        else:  # total
            _, _, B = campo_obj.campo_total(campo_obj.I1, campo_obj.I2, 
                                           campo_obj.L, campo_obj.a, x, y, z)
        
        B_mag.append(np.linalg.norm(B))
    
    plt.figure(figsize=(10, 6))
    plt.plot(puntos, B_mag, 'b-', linewidth=2)
    plt.xlabel(f'{eje.upper()} (m)')
    plt.ylabel('|B| (T)')
    plt.title(f'Magnitud del Campo Magnético a lo largo del eje {eje.upper()}\nTipo: {tipo.capitalize()}')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()