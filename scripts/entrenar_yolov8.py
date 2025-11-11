#!/usr/bin/env python3
"""
Script para Entrenar YOLOv8 con Objetos Didácticos
"""

import argparse
import os
from pathlib import Path


def entrenar_modelo(dataset_path, epochs=100, batch=16, img_size=640,
                   model_size='n', device='0', project='models', name='objetos_didacticos'):
    """
    Entrena modelo YOLOv8 con dataset personalizado.

    Args:
        dataset_path: Ruta al archivo data.yaml
        epochs: Número de épocas de entrenamiento
        batch: Tamaño del batch
        img_size: Tamaño de imagen
        model_size: Tamaño del modelo (n, s, m, l, x)
        device: Dispositivo (0 para GPU, 'cpu' para CPU)
        project: Directorio del proyecto
        name: Nombre del experimento
    """
    try:
        from ultralytics import YOLO
    except ImportError:
        print("❌ Error: ultralytics no está instalado")
        print("   Instala con: pip install ultralytics")
        return

    print("\n" + "="*70)
    print("🧠 ENTRENAMIENTO DE MODELO YOLOV8")
    print("="*70)
    print(f"\n📋 CONFIGURACIÓN:")
    print(f"   Dataset: {dataset_path}")
    print(f"   Épocas: {epochs}")
    print(f"   Batch size: {batch}")
    print(f"   Tamaño imagen: {img_size}")
    print(f"   Modelo: YOLOv8{model_size}")
    print(f"   Dispositivo: {device}")
    print("="*70)

    # Verificar dataset
    if not os.path.exists(dataset_path):
        print(f"\n❌ Error: No se encontró {dataset_path}")
        print("\n📝 Asegúrate de tener la estructura:")
        print("   dataset/")
        print("   ├── train/images/")
        print("   ├── train/labels/")
        print("   ├── valid/images/")
        print("   ├── valid/labels/")
        print("   └── data.yaml")
        return

    # Seleccionar modelo base
    model_weights = f'yolov8{model_size}.pt'
    print(f"\n📦 Cargando modelo base: {model_weights}")

    try:
        model = YOLO(model_weights)
        print("✅ Modelo cargado exitosamente")
    except Exception as e:
        print(f"❌ Error al cargar modelo: {e}")
        return

    # Entrenar
    print("\n🏋️  Iniciando entrenamiento...")
    print("   (Esto puede tomar varias horas dependiendo del dataset y hardware)")
    print("   Presiona Ctrl+C para detener (se guardará el progreso)")

    try:
        results = model.train(
            data=dataset_path,
            epochs=epochs,
            imgsz=img_size,
            batch=batch,
            device=device,
            patience=20,            # Early stopping
            save=True,
            plots=True,
            project=project,
            name=name,
            exist_ok=True,
            pretrained=True,
            optimizer='Adam',
            verbose=True,
            seed=42,
            deterministic=True,
            single_cls=False,
            rect=False,
            cos_lr=False,
            close_mosaic=10,
            resume=False,
            amp=True,               # Automatic Mixed Precision
            fraction=1.0,
            profile=False,
            freeze=None,
            lr0=0.01,
            lrf=0.01,
            momentum=0.937,
            weight_decay=0.0005,
            warmup_epochs=3.0,
            warmup_momentum=0.8,
            warmup_bias_lr=0.1,
            box=7.5,
            cls=0.5,
            dfl=1.5,
            pose=12.0,
            kobj=1.0,
            label_smoothing=0.0,
            nbs=64,
            hsv_h=0.015,
            hsv_s=0.7,
            hsv_v=0.4,
            degrees=0.0,
            translate=0.1,
            scale=0.5,
            shear=0.0,
            perspective=0.0,
            flipud=0.0,
            fliplr=0.5,
            mosaic=1.0,
            mixup=0.0,
            copy_paste=0.0
        )

        print("\n✅ Entrenamiento completado!")

        # Validar
        print("\n📊 Validando modelo...")
        metrics = model.val()

        # Mostrar métricas
        print("\n" + "="*70)
        print("📈 MÉTRICAS DEL MODELO")
        print("="*70)
        print(f"   mAP@50: {metrics.box.map50:.4f}")
        print(f"   mAP@50-95: {metrics.box.map:.4f}")
        print(f"   Precision: {metrics.box.mp:.4f}")
        print(f"   Recall: {metrics.box.mr:.4f}")
        print("="*70)

        # Ruta del mejor modelo
        best_model_path = Path(project) / name / 'weights' / 'best.pt'
        print(f"\n💾 Mejor modelo guardado en: {best_model_path}")

        # Exportar modelo
        print("\n📦 Exportando modelo a formato ONNX...")
        try:
            model.export(format='onnx')
            print("✅ Modelo exportado exitosamente")
        except Exception as e:
            print(f"⚠️  No se pudo exportar a ONNX: {e}")

        # Instrucciones finales
        print("\n" + "="*70)
        print("🎉 PRÓXIMOS PASOS")
        print("="*70)
        print("1. Revisa las gráficas de entrenamiento:")
        print(f"   - Abre: {Path(project) / name}")
        print(f"   - O ejecuta: tensorboard --logdir {project}/{name}")
        print("\n2. Prueba el modelo:")
        print(f"   python scripts/probar_modelo.py --model {best_model_path}")
        print("\n3. Integra el modelo en el sistema:")
        print("   - Copia el modelo a: models/objetos_didacticos_best.pt")
        print("   - El sistema lo usará automáticamente")
        print("="*70 + "\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Entrenamiento interrumpido por el usuario")
        print("   El progreso se ha guardado y puede reanudarse")
    except Exception as e:
        print(f"\n❌ Error durante entrenamiento: {e}")
        import traceback
        traceback.print_exc()


def main():
    parser = argparse.ArgumentParser(
        description='Entrena YOLOv8 con dataset de objetos didácticos'
    )
    parser.add_argument('--data', type=str, default='dataset/data.yaml',
                       help='Ruta al archivo data.yaml')
    parser.add_argument('--epochs', type=int, default=100,
                       help='Número de épocas (default: 100)')
    parser.add_argument('--batch', type=int, default=16,
                       help='Batch size (default: 16)')
    parser.add_argument('--img-size', type=int, default=640,
                       help='Tamaño de imagen (default: 640)')
    parser.add_argument('--model', type=str, default='n',
                       choices=['n', 's', 'm', 'l', 'x'],
                       help='Tamaño del modelo: n(nano), s(small), m(medium), l(large), x(xlarge)')
    parser.add_argument('--device', type=str, default='0',
                       help='Dispositivo: 0 para GPU, cpu para CPU')
    parser.add_argument('--project', type=str, default='models',
                       help='Directorio del proyecto')
    parser.add_argument('--name', type=str, default='objetos_didacticos',
                       help='Nombre del experimento')

    args = parser.parse_args()

    entrenar_modelo(
        dataset_path=args.data,
        epochs=args.epochs,
        batch=args.batch,
        img_size=args.img_size,
        model_size=args.model,
        device=args.device,
        project=args.project,
        name=args.name
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
