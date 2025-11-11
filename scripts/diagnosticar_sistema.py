#!/usr/bin/env python3
"""
Script de Diagnóstico del Sistema
Diagnostica problemas comunes de voz y detección
"""

import sys

def diagnosticar_voz():
    """Diagnostica problemas con el sistema de voz"""
    print("\n" + "="*70)
    print("🔊 DIAGNÓSTICO DE VOZ")
    print("="*70)

    # 1. Verificar instalación de pyttsx3
    try:
        import pyttsx3
        print("✅ pyttsx3 instalado correctamente")
    except ImportError:
        print("❌ pyttsx3 NO está instalado")
        print("\n📝 SOLUCIÓN:")
        print("   pip install pyttsx3")
        return False

    # 2. Intentar inicializar motor
    try:
        engine = pyttsx3.init()
        print("✅ Motor de voz inicializado")
    except Exception as e:
        print(f"❌ Error al inicializar motor: {e}")
        print("\n📝 SOLUCIÓN en Windows:")
        print("   pip install pypiwin32")
        return False

    # 3. Verificar voces disponibles
    try:
        voices = engine.getProperty('voices')
        print(f"\n📢 Voces disponibles: {len(voices)}")

        voces_espanol = []
        for i, voice in enumerate(voices):
            print(f"\n   Voz {i+1}:")
            print(f"      ID: {voice.id}")
            print(f"      Nombre: {voice.name}")

            # Verificar idioma
            if hasattr(voice, 'languages') and voice.languages:
                print(f"      Idiomas: {voice.languages}")
                if any('spanish' in str(lang).lower() or 'es' in str(lang).lower() for lang in voice.languages):
                    voces_espanol.append(i)

            # Verificar si hay "spanish" en el nombre
            if 'spanish' in voice.name.lower() or 'español' in voice.name.lower():
                voces_espanol.append(i)

        if voces_espanol:
            print(f"\n✅ Voces en español encontradas: {len(set(voces_espanol))}")
        else:
            print(f"\n⚠️  No se encontraron voces en español")
            print("   El sistema usará la voz por defecto")

    except Exception as e:
        print(f"❌ Error al obtener voces: {e}")

    # 4. Prueba de síntesis
    print("\n🎤 Probando síntesis de voz...")
    try:
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)

        # Probar con voz en español si existe
        if voces_espanol:
            engine.setProperty('voice', voices[voces_espanol[0]].id)
            print(f"   Usando voz: {voices[voces_espanol[0]].name}")

        engine.say("Hola, esta es una prueba del sistema de voz")
        engine.runAndWait()

        print("✅ Prueba de voz completada")
        print("\n❓ ¿Escuchaste la voz? (s/n): ", end="")
        respuesta = input().strip().lower()

        if respuesta == 's':
            print("✅ Sistema de voz funcionando correctamente")
            return True
        else:
            print("⚠️  No se escuchó la voz")
            print("\n📝 POSIBLES SOLUCIONES:")
            print("   1. Verifica que los altavoces estén encendidos")
            print("   2. Sube el volumen del sistema")
            print("   3. Prueba con auriculares")
            print("   4. En Windows, instala: pip install pypiwin32")
            return False

    except Exception as e:
        print(f"❌ Error en prueba de voz: {e}")
        print("\n📝 SOLUCIÓN en Windows:")
        print("   pip install pypiwin32")
        print("   pip install comtypes")
        return False


def diagnosticar_deteccion():
    """Diagnostica problemas de detección"""
    print("\n" + "="*70)
    print("📹 DIAGNÓSTICO DE DETECCIÓN")
    print("="*70)

    # 1. Verificar OpenCV
    try:
        import cv2
        print(f"✅ OpenCV instalado - Versión: {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV NO está instalado")
        print("   pip install opencv-python")
        return False

    # 2. Verificar cámara
    print("\n📷 Probando cámara...")
    try:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("❌ No se pudo abrir la cámara")
            print("\n📝 SOLUCIONES:")
            print("   1. Verifica que la cámara esté conectada")
            print("   2. Cierra otras aplicaciones que usen la cámara")
            print("   3. Prueba con otra cámara USB")
            return False

        ret, frame = cap.read()

        if ret:
            h, w = frame.shape[:2]
            print(f"✅ Cámara funcionando - Resolución: {w}x{h}")

            # Verificar iluminación
            import numpy as np
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brillo_promedio = np.mean(gray)

            print(f"\n💡 Brillo promedio: {brillo_promedio:.1f}/255")

            if brillo_promedio < 50:
                print("⚠️  Iluminación MUY BAJA")
                print("   Recomendación: Enciende más luces")
            elif brillo_promedio < 100:
                print("⚠️  Iluminación baja")
                print("   Recomendación: Mejora la iluminación")
            elif brillo_promedio > 200:
                print("⚠️  Iluminación MUY ALTA")
                print("   Recomendación: Reduce la luz directa")
            else:
                print("✅ Iluminación adecuada")

            # Mostrar frame de prueba
            cv2.imshow("Prueba de Cámara - Presiona Q para salir", frame)
            print("\n👁️  Ventana de prueba abierta. Presiona 'Q' para continuar...")
            cv2.waitKey(3000)
            cv2.destroyAllWindows()

        cap.release()

    except Exception as e:
        print(f"❌ Error al probar cámara: {e}")
        return False

    print("\n📊 RECOMENDACIONES PARA MEJOR DETECCIÓN:")
    print("   1. Iluminación uniforme (evita sombras)")
    print("   2. Fondo contrastante (preferiblemente blanco)")
    print("   3. Objetos con colores sólidos y brillantes")
    print("   4. Distancia de 30-60 cm de la cámara")
    print("   5. Evita movimientos bruscos")

    return True


def diagnosticar_rendimiento():
    """Diagnostica el rendimiento del sistema"""
    print("\n" + "="*70)
    print("⚡ DIAGNÓSTICO DE RENDIMIENTO")
    print("="*70)

    import numpy as np
    import cv2
    import time

    # Prueba de procesamiento
    print("\n🔄 Probando velocidad de procesamiento...")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ No se pudo abrir cámara para prueba")
        return False

    fps_list = []

    for i in range(30):
        start = time.time()

        ret, frame = cap.read()
        if not ret:
            break

        # Simular procesamiento
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        elapsed = time.time() - start
        if elapsed > 0:
            fps_list.append(1.0 / elapsed)

    cap.release()

    avg_fps = np.mean(fps_list) if fps_list else 0

    print(f"\n📊 FPS promedio: {avg_fps:.1f}")

    if avg_fps >= 25:
        print("✅ Rendimiento excelente")
    elif avg_fps >= 15:
        print("✅ Rendimiento bueno")
    elif avg_fps >= 10:
        print("⚠️  Rendimiento aceptable")
    else:
        print("❌ Rendimiento bajo")
        print("\n📝 SOLUCIONES:")
        print("   1. Cierra otras aplicaciones")
        print("   2. Reduce resolución de cámara")
        print("   3. Actualiza drivers de cámara")

    return True


def main():
    """Ejecuta todos los diagnósticos"""
    print("\n" + "🎓 " * 20)
    print("   DIAGNÓSTICO DEL SISTEMA DE APRENDIZAJE INCLUSIVO")
    print("🎓 " * 20)

    resultados = {
        'voz': False,
        'deteccion': False,
        'rendimiento': False
    }

    # Diagnósticos
    resultados['voz'] = diagnosticar_voz()
    resultados['deteccion'] = diagnosticar_deteccion()
    resultados['rendimiento'] = diagnosticar_rendimiento()

    # Resumen
    print("\n" + "="*70)
    print("📋 RESUMEN DEL DIAGNÓSTICO")
    print("="*70)

    print(f"\n   {'✅' if resultados['voz'] else '❌'} Sistema de Voz")
    print(f"   {'✅' if resultados['deteccion'] else '❌'} Sistema de Detección")
    print(f"   {'✅' if resultados['rendimiento'] else '❌'} Rendimiento")

    if all(resultados.values()):
        print("\n✅ Sistema completamente funcional")
    else:
        print("\n⚠️  Algunos componentes requieren atención")
        print("\n📝 Revisa las soluciones sugeridas arriba")

    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Diagnóstico interrumpido")
    except Exception as e:
        print(f"\n❌ Error en diagnóstico: {e}")
        import traceback
        traceback.print_exc()
