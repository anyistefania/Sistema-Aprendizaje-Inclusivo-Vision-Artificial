"""
Menú Principal - Capa de Presentación
Interfaz CLI para el sistema de aprendizaje inclusivo
"""

import sys
import subprocess


def check_dependencies():
    """Verifica que las dependencias estén instaladas."""
    print("🔍 Verificando dependencias...\n")

    dependencies_ok = True

    try:
        import cv2
        print("✅ OpenCV instalado")
    except ImportError:
        print("❌ OpenCV no instalado - Ejecuta: pip install opencv-python")
        dependencies_ok = False

    try:
        import numpy
        print("✅ NumPy instalado")
    except ImportError:
        print("❌ NumPy no instalado - Ejecuta: pip install numpy")
        dependencies_ok = False

    try:
        import pyttsx3
        print("✅ pyttsx3 instalado (síntesis de voz)")
    except ImportError:
        print("⚠️  pyttsx3 no instalado (la voz no funcionará) - Ejecuta: pip install pyttsx3")

    print()
    return dependencies_ok


def show_main_menu():
    """Muestra el menú principal."""
    print("\n" + "="*70)
    print("   SISTEMA DE APRENDIZAJE INCLUSIVO CON VISIÓN ARTIFICIAL")
    print("="*70)
    print("\n📚 MÓDULOS DISPONIBLES:\n")
    print("1. 🎯 Sistema de Aprendizaje Inclusivo (RECOMENDADO)")
    print("   - Diseñado específicamente para educación especial")
    print("   - Interfaz adaptativa según discapacidad")
    print("   - Registro de progreso del estudiante")
    print()
    print("2. 📐 Detector de Formas")
    print("   - Detecta formas geométricas")
    print()
    print("3. 🎨 Detector de Colores")
    print("   - Detecta colores en tiempo real")
    print()
    print("4. 🎯 Sistema Integrado")
    print("   - Formas y colores simultáneamente")
    print()
    print("5. 🔧 Instalar Dependencias")
    print()
    print("0. ❌ Salir")
    print("\n" + "="*70)


def run_module(module_path: str):
    """Ejecuta un módulo de Python."""
    try:
        print(f"\n🚀 Iniciando módulo...\n")
        subprocess.run([sys.executable, module_path])
    except FileNotFoundError:
        print(f"\n❌ Error: No se encontró el módulo")
    except Exception as e:
        print(f"\n❌ Error al ejecutar: {e}")


def install_dependencies():
    """Instala las dependencias del proyecto."""
    print("\n🔧 Instalando dependencias...\n")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\n✅ Dependencias instaladas correctamente")
    except Exception as e:
        print(f"\n❌ Error al instalar dependencias: {e}")


def main():
    """Función principal del menú."""
    print("\n" + "🎓 " * 20)
    print("   BIENVENIDO AL SISTEMA DE APRENDIZAJE INCLUSIVO")
    print("🎓 " * 20 + "\n")

    # Verificar dependencias
    if not check_dependencies():
        print("\n⚠️  Algunas dependencias no están instaladas.")
        print("   Selecciona la opción 5 del menú para instalarlas.")
        input("\nPresiona ENTER para continuar...")

    while True:
        show_main_menu()

        try:
            opcion = input("\n👉 Selecciona una opción (0-5): ").strip()

            if opcion == "0":
                print("\n👋 ¡Hasta luego! Gracias por usar el sistema.\n")
                break

            elif opcion == "1":
                run_module("src/presentation/cli/learning_interface.py")

            elif opcion == "2":
                run_module("src/infrastructure/detection/shape_detector.py")

            elif opcion == "3":
                run_module("src/infrastructure/detection/color_detector.py")

            elif opcion == "4":
                run_module("integrated_system.py")

            elif opcion == "5":
                install_dependencies()

            else:
                print("\n❌ Opción no válida. Por favor selecciona 0-5.")

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
