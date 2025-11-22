from campo_magnetico import CampoMagnetico
from helmholtz import BobinasHelmholtz
import graficos

def menu_principal():
    print("\n" + "="*60)
    print(" ANÁLISIS DE CAMPO MAGNÉTICO")
    print("="*60)
    print("\n--- Sistema Alambre + Espira ---")
    print("1. Ingresar datos del sistema")
    print("2. Calcular campo en un punto específico")
    print("3. Visualizar configuración geométrica")
    print("4. Graficar campo 2D (plano XY)")
    print("5. Graficar campo 2D (plano XZ)")
    print("6. Graficar campo 2D (plano YZ)")
    print("7. Graficar campo 3D")
    print("8. Gráfico de magnitud a lo largo de un eje")
    print("9. Generar todos los gráficos")
    print("\n--- Bobinas de Helmholtz ---")
    print("10. Configurar bobinas de Helmholtz")
    print("11. Analizar uniformidad del campo")
    print("12. Comparar diferentes separaciones")
    print("13. Visualizar geometría de Helmholtz")
    print("14. Campo magnético 2D de Helmholtz")
    print("15. Calcular campo en un punto (Helmholtz)")
    print("\n0. Salir")
    print("="*60)

def submenu_tipo():
    print("\nSeleccione el tipo de configuración:")
    print("1. Solo alambre")
    print("2. Solo espira")
    print("3. Total (alambre + espira)")
    opcion = input("Opción: ")
    
    tipos = {'1': 'alambre', '2': 'espira', '3': 'total'}
    return tipos.get(opcion, 'total')

def main():
    campo = CampoMagnetico()
    helmholtz = BobinasHelmholtz()
    datos_cargados = False
    helmholtz_configurado = False
    
    while True:
        menu_principal()
        opcion = input("\nSeleccione una opción: ")
        
        # --- SISTEMA ALAMBRE + ESPIRA ---
        if opcion == '1':
            campo.carga_de_datos()
            datos_cargados = True
            print("\n✓ Datos cargados correctamente")
            
        elif opcion == '2':
            if not datos_cargados:
                print("\n⚠ Primero debe ingresar los datos del sistema (opción 1)")
            else:
                campo.calcular_campo_en_punto()
                
        elif opcion == '3':
            if not datos_cargados:
                print("\n⚠ Primero debe ingresar los datos del sistema (opción 1)")
            else:
                graficos.graficar_configuracion_geometrica(campo)
                
        elif opcion in ['4', '5', '6']:
            if not datos_cargados:
                print("\n⚠ Primero debe ingresar los datos del sistema (opción 1)")
            else:
                tipo = submenu_tipo()
                planos = {'4': 'xy', '5': 'xz', '6': 'yz'}
                graficos.graficar_campo_2d(campo, plano=planos[opcion], tipo=tipo)
                
        elif opcion == '7':
            if not datos_cargados:
                print("\n⚠ Primero debe ingresar los datos del sistema (opción 1)")
            else:
                tipo = submenu_tipo()
                print("\n⚠ Nota: El cálculo 3D puede tardar varios segundos...")
                graficos.graficar_campo_3d(campo, tipo=tipo, n_puntos=6)
                
        elif opcion == '8':
            if not datos_cargados:
                print("\n⚠ Primero debe ingresar los datos del sistema (opción 1)")
            else:
                tipo = submenu_tipo()
                print("\nSeleccione el eje:")
                print("1. Eje X")
                print("2. Eje Y")
                print("3. Eje Z")
                eje_opt = input("Opción: ")
                ejes = {'1': 'x', '2': 'y', '3': 'z'}
                eje = ejes.get(eje_opt, 'z')
                graficos.graficar_magnitud_en_eje(campo, eje=eje, tipo=tipo)
                
        elif opcion == '9':
            if not datos_cargados:
                print("\n⚠ Primero debe ingresar los datos del sistema (opción 1)")
            else:
                print("\n⚠ Generando todos los gráficos (esto puede tardar)...")
                tipo = submenu_tipo()
                
                print("\n[1/5] Configuración geométrica...")
                graficos.graficar_configuracion_geometrica(campo)
                
                print("[2/5] Campo en plano XY...")
                graficos.graficar_campo_2d(campo, plano='xy', tipo=tipo)
                
                print("[3/5] Campo en plano XZ...")
                graficos.graficar_campo_2d(campo, plano='xz', tipo=tipo)
                
                print("[4/5] Campo en plano YZ...")
                graficos.graficar_campo_2d(campo, plano='yz', tipo=tipo)
                
                print("[5/5] Magnitud en eje Z...")
                graficos.graficar_magnitud_en_eje(campo, eje='z', tipo=tipo)
                
                print("\n✓ Todos los gráficos generados")
        
        # --- BOBINAS DE HELMHOLTZ ---
        elif opcion == '10':
            helmholtz.configurar()
            helmholtz_configurado = True
            print("\n✓ Bobinas de Helmholtz configuradas")
            
        elif opcion == '11':
            if not helmholtz_configurado:
                print("\n⚠ Primero debe configurar las bobinas (opción 10)")
            else:
                helmholtz.analizar_uniformidad()
                
        elif opcion == '12':
            if not helmholtz_configurado:
                print("\n⚠ Primero debe configurar las bobinas (opción 10)")
            else:
                print("\nComparando diferentes separaciones d/a...")
                helmholtz.comparar_separaciones()
                
        elif opcion == '13':
            if not helmholtz_configurado:
                print("\n⚠ Primero debe configurar las bobinas (opción 10)")
            else:
                helmholtz.graficar_geometria_3d()
                
        elif opcion == '14':
            if not helmholtz_configurado:
                print("\n⚠ Primero debe configurar las bobinas (opción 10)")
            else:
                print("\nSeleccione el plano:")
                print("1. XY")
                print("2. XZ")
                print("3. YZ")
                plano_opt = input("Opción: ")
                planos_helm = {'1': 'xy', '2': 'xz', '3': 'yz'}
                plano = planos_helm.get(plano_opt, 'xz')
                helmholtz.graficar_campo_2d(plano=plano)
                
        elif opcion == '15':
            if not helmholtz_configurado:
                print("\n⚠ Primero debe configurar las bobinas (opción 10)")
            else:
                punto = input("\nIngrese el punto (X Y Z): ").split()
                x, y, z = float(punto[0]), float(punto[1]), float(punto[2])
                helmholtz.calcular_campo_en_punto(x, y, z)
                
        elif opcion == '0':
            print("\n¡Hasta luego!")
            break
            
        else:
            print("\n⚠ Opción no válida")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()