"""
Script de Inicio Rápido
Sistema de Aprendizaje Inclusivo con Visión Artificial

Este script facilita el inicio del sistema para usuarios no técnicos.
"""

import sys
import subprocess
import os


def check_dependencies():
    """Verifica que las dependencias estén instaladas."""
    print("🔍 Verificando dependencias...\n")
    
    try:
        import cv2
        print("✅ OpenCV instalado")
    except ImportError:
        print("❌ OpenCV no instalado")
        print("   Ejecuta: pip install opencv-python")
        return False
    
    try:
        import numpy
        print("✅ NumPy instalado")
    except ImportError:
        print("❌ NumPy no instalado")
        print("   Ejecuta: pip install numpy")
        return False
    
    try:
        import imutils
        print("✅ imutils instalado")
    except ImportError:
        print("❌ imutils no instalado")
        print("   Ejecuta: pip install imutils")
        return False
    
    try:
        import pyttsx3
        print("✅ pyttsx3 instalado (síntesis de voz)")
    except ImportError:
        print("⚠️  pyttsx3 no instalado (la voz no funcionará)")
        print("   Ejecuta: pip install pyttsx3")
    
    print("\n✅ Todas las dependencias principales están instaladas\n")
    return True


def show_menu():
    """Muestra el menú principal."""
    print("\n" + "="*70)
    print("   SISTEMA DE APRENDIZAJE INCLUSIVO CON VISIÓN ARTIFICIAL")
    print("="*70)
    print("\n📚 MÓDULOS DISPONIBLES:\n")
    print("1. 🎯 Sistema de Aprendizaje Inclusivo (RECOMENDADO)")
    print("   - Diseñado específicamente para educación especial")
    print("   - Interfaz adaptativa según discapacidad")
    print("   - Registro de progreso del estudiante")
    print("   - Retroalimentación multimodal")
    print()
    print("2. 📐 Detector de Formas")
    print("   - Detecta círculos, triángulos, cuadrados, etc.")
    print("   - Modo imagen o tiempo real")
    print()
    print("3. 🎨 Detector de Colores")
    print("   - Detecta colores en tiempo real")
    print("   - Retroalimentación por voz")
    print()
    print("4. 🎯 Sistema Integrado")
    print("   - Detección de formas y colores simultánea")
    print("   - Múltiples modos de operación")
    print()
    print("5. 🖼️  Generar Imágenes de Prueba")
    print("   - Crea imágenes para probar sin objetos físicos")
    print()
    print("6. 📖 Ver Manual de Usuario")
    print()
    print("7. 🔧 Instalar Dependencias")
    print()
    print("0. ❌ Salir")
    print("\n" + "="*70)


def run_script(script_name):
    """Ejecuta un script de Python."""
    try:
        print(f"\n🚀 Iniciando {script_name}...\n")
        subprocess.run([sys.executable, script_name])
    except FileNotFoundError:
        print(f"\n❌ Error: No se encontró el archivo {script_name}")
        print("   Asegúrate de estar en la carpeta correcta del proyecto")
    except Exception as e:
        print(f"\n❌ Error al ejecutar el script: {e}")


def install_dependencies():
    """Instala las dependencias del proyecto."""
    print("\n🔧 Instalando dependencias...\n")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✅ Dependencias instaladas correctamente")
    except Exception as e:
        print(f"\n❌ Error al instalar dependencias: {e}")


def show_manual():
    """Muestra el manual de usuario."""
    if os.path.exists("MANUAL_USUARIO.md"):
        print("\n📖 Abriendo manual de usuario...\n")
        try:
            if sys.platform == "win32":
                os.startfile("MANUAL_USUARIO.md")
            elif sys.platform == "darwin":
                subprocess.run(["open", "MANUAL_USUARIO.md"])
            else:
                subprocess.run(["xdg-open", "MANUAL_USUARIO.md"])
        except:
            print("No se pudo abrir automáticamente. Abre el archivo 'MANUAL_USUARIO.md' manualmente.")
    else:
        print("\n❌ No se encontró el archivo MANUAL_USUARIO.md")


def main():
    """Función principal."""
    print("\n" + "🎓 " * 20)
    print("   BIENVENIDO AL SISTEMA DE APRENDIZAJE INCLUSIVO")
    print("🎓 " * 20 + "\n")
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n⚠️  Algunas dependencias no están instaladas.")
        print("   Selecciona la opción 7 del menú para instalarlas.")
        input("\nPresiona ENTER para continuar...")
    
    while True:
        show_menu()
        
        try:
            opcion = input("\n👉 Selecciona una opción (0-7): ").strip()
            
            if opcion == "0":
                print("\n👋 ¡Hasta luego! Gracias por usar el sistema.\n")
                break
            
            elif opcion == "1":
                run_script("inclusive_learning_system.py")
            
            elif opcion == "2":
                run_script("shape_detector.py")
            
            elif opcion == "3":
                run_script("color_detector.py")
            
            elif opcion == "4":
                run_script("integrated_system.py")
            
            elif opcion == "5":
                run_script("generar_imagenes_prueba.py")
            
            elif opcion == "6":
                show_manual()
            
            elif opcion == "7":
                install_dependencies()
            
            else:
                print("\n❌ Opción no válida. Por favor selecciona 0-7.")
            
            input("\n✨ Presiona ENTER para volver al menú...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPresiona ENTER para continuar...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        input("\nPresiona ENTER para salir...")
