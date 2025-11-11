#!/usr/bin/env python3
"""
Script para Probar Modelo YOLOv8 Entrenado
Prueba el modelo con la webcam en tiempo real
"""

import cv2
import argparse
from pathlib import Path


def probar_modelo(model_path, confidence=0.5, device='0'):
    """
    Prueba modelo YOLOv8 con webcam.

    Args:
        model_path: Ruta al modelo entrenado (.pt)
        confidence: Umbral de confianza mínimo
        device: Dispositivo (0 para GPU, 'cpu' para CPU)
    """
    try:
        from ultralytics import YOLO
    except ImportError:
        print("❌ Error: ultralytics no está instalado")
        print("   Instala con: pip install ultralytics")
        return

    print("\n" + "="*70)
    print("🧪 PRUEBA DE MODELO YOLOV8")
    print("="*70)
    print(f"\n📋 CONFIGURACIÓN:")
    print(f"   Modelo: {model_path}")
    print(f"   Confianza mínima: {confidence}")
    print(f"   Dispositivo: {device}")
    print("="*70)

    # Verificar modelo
    if not Path(model_path).exists():
        print(f"\n❌ Error: No se encontró el modelo en {model_path}")
        return

    # Cargar modelo
    print(f"\n📦 Cargando modelo...")
    try:
        model = YOLO(model_path)
        print("✅ Modelo cargado exitosamente")

        # Información del modelo
        print(f"\n📊 Información del modelo:")
        print(f"   Clases: {len(model.names)}")
        print(f"   Objetos detectables:")
        for idx, name in model.names.items():
            print(f"      - {name}")

    except Exception as e:
        print(f"❌ Error al cargar modelo: {e}")
        return

    # Abrir cámara
    print(f"\n📷 Abriendo cámara...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: No se pudo abrir la cámara")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("✅ Cámara abierta")
    print("\n🎬 ¡Sistema listo!")
    print("\n📋 CONTROLES:")
    print("   Q - Salir")
    print("   S - Guardar captura")
    print("   + - Aumentar confianza")
    print("   - - Disminuir confianza")
    print("\n" + "="*70 + "\n")

    frame_count = 0
    total_detections = 0
    fps_list = []

    while True:
        ret, frame = cap.read()

        if not ret:
            print("❌ Error al leer frame")
            break

        # Voltear para efecto espejo
        frame = cv2.flip(frame, 1)

        # Medir FPS
        import time
        start_time = time.time()

        # Inferencia
        results = model(frame, conf=confidence, verbose=False, device=device)

        # Calcular FPS (evitar división por cero)
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            fps = 1.0 / elapsed_time
            fps_list.append(fps)
            if len(fps_list) > 30:
                fps_list.pop(0)

        avg_fps = sum(fps_list) / len(fps_list) if fps_list else 0.0

        # Procesar resultados
        detections_in_frame = 0

        for result in results:
            boxes = result.boxes

            for box in boxes:
                # Obtener información
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].cpu().numpy()

                x1, y1, x2, y2 = map(int, xyxy)
                class_name = model.names[cls_id]

                detections_in_frame += 1
                total_detections += 1

                # Color según confianza
                if conf > 0.8:
                    color = (0, 255, 0)  # Verde - alta confianza
                elif conf > 0.6:
                    color = (0, 255, 255)  # Amarillo - media confianza
                else:
                    color = (0, 165, 255)  # Naranja - baja confianza

                # Dibujar bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                # Etiqueta
                label = f"{class_name} {conf:.2f}"
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)

                # Fondo para etiqueta
                cv2.rectangle(frame,
                            (x1, y1 - label_size[1] - 10),
                            (x1 + label_size[0] + 10, y1),
                            color, -1)

                # Texto
                cv2.putText(frame, label, (x1 + 5, y1 - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Panel de información
        info_panel = frame.copy()
        cv2.rectangle(info_panel, (0, 0), (640, 120), (0, 0, 0), -1)

        # Información
        cv2.putText(info_panel, "PRUEBA DE MODELO - YOLOV8", (10, 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.putText(info_panel, f"FPS: {avg_fps:.1f}", (10, 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.putText(info_panel, f"Detectados: {detections_in_frame}", (10, 75),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

        cv2.putText(info_panel, f"Confianza: {confidence:.2f}", (10, 95),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 255), 1)

        cv2.putText(info_panel, "Q:Salir | S:Capturar | +/-:Conf", (10, 115),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

        # Combinar con frame
        frame = cv2.addWeighted(frame, 0.7, info_panel, 0.3, 0)

        # Mostrar
        cv2.imshow("Prueba de Modelo YOLOv8", frame)

        # Procesar teclas
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("\n👋 Saliendo...")
            break

        elif key == ord('s'):
            # Guardar captura
            filename = f"prueba_modelo_{frame_count:04d}.jpg"
            cv2.imwrite(filename, frame)
            print(f"📸 Captura guardada: {filename}")

        elif key == ord('+') or key == ord('='):
            # Aumentar confianza
            confidence = min(1.0, confidence + 0.05)
            print(f"🔼 Confianza: {confidence:.2f}")

        elif key == ord('-') or key == ord('_'):
            # Disminuir confianza
            confidence = max(0.0, confidence - 0.05)
            print(f"🔽 Confianza: {confidence:.2f}")

        frame_count += 1

    # Finalizar
    cap.release()
    cv2.destroyAllWindows()

    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE PRUEBA")
    print("="*70)
    print(f"   Frames procesados: {frame_count}")
    print(f"   Detecciones totales: {total_detections}")
    print(f"   FPS promedio: {avg_fps:.2f}")
    print(f"   Detecciones/frame: {total_detections/frame_count:.2f}" if frame_count > 0 else "   N/A")
    print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Prueba modelo YOLOv8 entrenado con webcam'
    )
    parser.add_argument('--model', type=str, required=True,
                       help='Ruta al modelo entrenado (.pt)')
    parser.add_argument('--confidence', type=float, default=0.5,
                       help='Umbral de confianza mínimo (0.0-1.0, default: 0.5)')
    parser.add_argument('--device', type=str, default='0',
                       help='Dispositivo: 0 para GPU, cpu para CPU')

    args = parser.parse_args()

    probar_modelo(args.model, args.confidence, args.device)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
