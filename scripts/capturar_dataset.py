#!/usr/bin/env python3
"""
Script para Capturar Dataset de Objetos Didácticos
Captura imágenes desde la webcam para entrenar modelos
"""

import cv2
import os
import time
import argparse
from datetime import datetime


def capturar_dataset(objeto, cantidad=100, output_dir='dataset'):
    """
    Captura imágenes desde la webcam para crear dataset.

    Args:
        objeto: Nombre del objeto a capturar
        cantidad: Número de imágenes a capturar
        output_dir: Directorio de salida
    """
    # Crear directorio
    objeto_dir = os.path.join(output_dir, 'images', objeto)
    os.makedirs(objeto_dir, exist_ok=True)

    # Abrir cámara
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: No se pudo abrir la cámara")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("\n" + "="*70)
    print(f"📸 CAPTURA DE DATASET: {objeto.upper()}")
    print("="*70)
    print(f"\n🎯 Objetivo: Capturar {cantidad} imágenes")
    print(f"📁 Guardando en: {objeto_dir}")
    print("\n📋 INSTRUCCIONES:")
    print("   1. Posiciona el objeto frente a la cámara")
    print("   2. Presiona ESPACIO para capturar")
    print("   3. Varía ángulos, distancias e iluminación")
    print("   4. Presiona Q para terminar antes")
    print("\n⌛ Iniciando en 3 segundos...")
    time.sleep(3)

    contador = 0
    capturadas = 0
    modo_automatico = False
    ultimo_captura = time.time()
    intervalo_auto = 0.5  # segundos entre capturas automáticas

    print("\n🎬 ¡Empezando captura!")
    print("\n💡 Consejo: Presiona 'A' para modo automático (captura cada 0.5s)")

    while capturadas < cantidad:
        ret, frame = cap.read()

        if not ret:
            print("❌ Error al leer frame")
            break

        # Voltear para efecto espejo
        frame = cv2.flip(frame, 1)

        # Crear copia para dibujar
        display = frame.copy()

        # Información en pantalla
        progreso = (capturadas / cantidad) * 100

        # Barra de progreso
        bar_width = 400
        bar_height = 30
        bar_x = (640 - bar_width) // 2
        bar_y = 20

        cv2.rectangle(display, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height),
                     (50, 50, 50), -1)

        progreso_width = int((progreso / 100) * bar_width)
        color_barra = (0, 255, 0) if progreso < 100 else (0, 255, 255)
        cv2.rectangle(display, (bar_x, bar_y), (bar_x + progreso_width, bar_y + bar_height),
                     color_barra, -1)

        # Texto de progreso
        texto = f"{capturadas}/{cantidad} ({progreso:.1f}%)"
        cv2.putText(display, texto, (bar_x + 10, bar_y + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Objeto
        cv2.putText(display, f"Objeto: {objeto}", (20, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Modo
        modo_texto = "AUTO" if modo_automatico else "MANUAL"
        modo_color = (0, 255, 0) if modo_automatico else (255, 255, 255)
        cv2.putText(display, f"Modo: {modo_texto}", (20, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, modo_color, 2)

        # Ayuda
        cv2.putText(display, "ESPACIO: Capturar | A: Auto | Q: Salir", (20, 460),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        # Mostrar
        cv2.imshow(f"Captura Dataset - {objeto}", display)

        # Captura automática
        if modo_automatico and (time.time() - ultimo_captura) >= intervalo_auto:
            # Guardar imagen
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{objeto}_{timestamp}_{capturadas:04d}.jpg"
            filepath = os.path.join(objeto_dir, filename)

            cv2.imwrite(filepath, frame)
            capturadas += 1
            ultimo_captura = time.time()

            print(f"  ✅ {capturadas}/{cantidad}: {filename}")

        # Procesar teclas
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("\n⚠️  Captura interrumpida por el usuario")
            break

        elif key == ord(' ') and not modo_automatico:
            # Captura manual
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{objeto}_{timestamp}_{capturadas:04d}.jpg"
            filepath = os.path.join(objeto_dir, filename)

            cv2.imwrite(filepath, frame)
            capturadas += 1

            print(f"  ✅ {capturadas}/{cantidad}: {filename}")

        elif key == ord('a'):
            # Alternar modo automático
            modo_automatico = not modo_automatico
            estado = "activado" if modo_automatico else "desactivado"
            print(f"\n🔄 Modo automático {estado}")
            ultimo_captura = time.time()

        contador += 1

    # Finalizar
    cap.release()
    cv2.destroyAllWindows()

    print("\n" + "="*70)
    print("📊 RESUMEN DE CAPTURA")
    print("="*70)
    print(f"   Objeto: {objeto}")
    print(f"   Imágenes capturadas: {capturadas}")
    print(f"   Directorio: {objeto_dir}")

    if capturadas >= cantidad:
        print("\n✅ ¡Captura completada exitosamente!")
    else:
        print(f"\n⚠️  Captura incompleta ({capturadas}/{cantidad})")

    print("\n📝 Próximos pasos:")
    print(f"   1. Revisa las imágenes en: {objeto_dir}")
    print("   2. Elimina imágenes borrosas o mal capturadas")
    print("   3. Etiqueta las imágenes con LabelImg o Roboflow")
    print("   4. Entrena el modelo con: python scripts/entrenar_yolov8.py")
    print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Captura dataset de objetos didácticos desde webcam'
    )
    parser.add_argument('--objeto', type=str, required=True,
                       help='Nombre del objeto a capturar (ej: manzana, perro_juguete)')
    parser.add_argument('--cantidad', type=int, default=100,
                       help='Número de imágenes a capturar (default: 100)')
    parser.add_argument('--output', type=str, default='dataset',
                       help='Directorio de salida (default: dataset)')

    args = parser.parse_args()

    # Validar nombre de objeto
    objeto_limpio = args.objeto.lower().replace(' ', '_')

    capturar_dataset(objeto_limpio, args.cantidad, args.output)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
