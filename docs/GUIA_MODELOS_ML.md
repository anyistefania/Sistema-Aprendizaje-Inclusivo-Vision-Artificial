# 🧠 Guía para Integrar Modelos de Machine Learning

Esta guía explica cómo entrenar e integrar modelos de ML para detectar objetos didácticos específicos en el sistema de aprendizaje inclusivo.

## 📋 Índice

1. [Opciones de Modelos](#opciones-de-modelos)
2. [Opción Recomendada: YOLOv8](#opción-recomendada-yolov8)
3. [Preparación del Dataset](#preparación-del-dataset)
4. [Entrenamiento del Modelo](#entrenamiento-del-modelo)
5. [Integración con Clean Architecture](#integración-con-clean-architecture)
6. [Alternativas sin Entrenar](#alternativas-sin-entrenar)

---

## 🎯 Opciones de Modelos

### 1. **YOLOv8 (Recomendado)** ⭐
- ✅ Rápido y preciso
- ✅ Fácil de entrenar
- ✅ Soporta objetos personalizados
- ✅ Funciona en CPU (lento) y GPU (rápido)

### 2. **TensorFlow Object Detection API**
- ✅ Muy flexible
- ✅ Múltiples arquitecturas
- ⚠️  Más complejo de configurar

### 3. **MobileNet SSD**
- ✅ Optimizado para dispositivos móviles
- ✅ Rápido en CPU
- ⚠️  Menos preciso que YOLO

### 4. **Detectron2 (Facebook)**
- ✅ Estado del arte
- ✅ Muy preciso
- ⚠️  Requiere GPU potente

---

## ⭐ Opción Recomendada: YOLOv8

### Por qué YOLOv8 es ideal para este proyecto:

1. **Educación Especial**: Detección en tiempo real necesaria
2. **Objetos didácticos**: Puede entrenarse con pocas imágenes
3. **Facilidad**: Instalación y entrenamiento simples
4. **Rendimiento**: Balance entre velocidad y precisión

---

## 📸 Preparación del Dataset

### Paso 1: Definir Objetos Didácticos

```python
# Objetos a detectar (ejemplo)
clases = [
    'manzana',
    'platano',
    'naranja',
    'perro_juguete',
    'gato_juguete',
    'carro_juguete',
    'numero_1',
    'numero_2',
    'numero_3',
    'letra_A',
    'letra_B',
    'circulo',
    'triangulo',
    'cuadrado'
]
```

### Paso 2: Recolectar Imágenes

**Cantidad recomendada por objeto:**
- Mínimo: 50 imágenes
- Recomendado: 200-500 imágenes
- Ideal: 1000+ imágenes

**Variaciones importantes:**
- ✅ Diferentes ángulos
- ✅ Diferentes iluminaciones
- ✅ Diferentes fondos
- ✅ Diferentes distancias
- ✅ Diferentes tamaños

**Herramientas para recolectar:**
```bash
# Script para capturar imágenes desde webcam
python scripts/capturar_dataset.py --objeto manzana --cantidad 100
```

### Paso 3: Etiquetar Imágenes

**Herramientas de etiquetado:**

1. **LabelImg** (Recomendado) ⭐
```bash
pip install labelImg
labelImg
```

2. **Roboflow** (Online, fácil)
- https://roboflow.com
- ✅ Etiquetado en la nube
- ✅ Aumentación automática
- ✅ Exporta a múltiples formatos

3. **CVAT** (Computer Vision Annotation Tool)
- https://cvat.org
- ✅ Gratuito y open source
- ✅ Colaborativo

**Formato de etiquetas para YOLO:**
```
# cada archivo .txt contiene:
# clase x_centro y_centro ancho alto (normalizados 0-1)
0 0.5 0.5 0.3 0.4
1 0.2 0.3 0.15 0.2
```

### Paso 4: Estructura del Dataset

```
dataset_objetos_didacticos/
├── train/
│   ├── images/
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   └── labels/
│       ├── img001.txt
│       ├── img002.txt
│       └── ...
├── valid/
│   ├── images/
│   └── labels/
├── test/
│   ├── images/
│   └── labels/
└── data.yaml
```

**Archivo data.yaml:**
```yaml
train: ./train/images
val: ./valid/images
test: ./test/images

nc: 14  # número de clases
names: ['manzana', 'platano', 'naranja', 'perro_juguete',
        'gato_juguete', 'carro_juguete', 'numero_1', 'numero_2',
        'numero_3', 'letra_A', 'letra_B', 'circulo',
        'triangulo', 'cuadrado']
```

---

## 🏋️ Entrenamiento del Modelo

### Instalación de YOLOv8

```bash
pip install ultralytics
```

### Script de Entrenamiento

```python
# scripts/entrenar_yolov8.py
from ultralytics import YOLO

# Cargar modelo pre-entrenado (transfer learning)
model = YOLO('yolov8n.pt')  # nano (más rápido)
# model = YOLO('yolov8s.pt')  # small
# model = YOLO('yolov8m.pt')  # medium (más preciso)

# Entrenar
results = model.train(
    data='dataset_objetos_didacticos/data.yaml',
    epochs=100,              # Número de épocas
    imgsz=640,               # Tamaño de imagen
    batch=16,                # Batch size
    device='0',              # GPU (usar 'cpu' si no tienes GPU)
    patience=20,             # Early stopping
    save=True,
    project='modelos',
    name='objetos_didacticos_v1'
)

# Validar
metrics = model.val()

# Exportar modelo
model.export(format='onnx')  # Para mayor compatibilidad
```

### Ejecutar Entrenamiento

```bash
# Con GPU
python scripts/entrenar_yolov8.py

# Con CPU (más lento)
python scripts/entrenar_yolov8.py --device cpu
```

### Monitorear Entrenamiento

```bash
# Ver progreso en TensorBoard
tensorboard --logdir runs/detect/objetos_didacticos_v1
```

---

## 🏗️ Integración con Clean Architecture

### Paso 1: Crear Implementación del Modelo

```python
# src/infrastructure/detection/yolo_detector.py
from ultralytics import YOLO
import numpy as np
from typing import List
from ...domain.repositories.object_detection_model import (
    ObjectDetectionModel,
    ObjectDetectionResult
)
from ...domain.entities.educational_object import (
    get_educational_object,
    CATALOGO_OBJETOS_DIDACTICOS
)


class YOLOv8Detector(ObjectDetectionModel):
    """Implementación usando YOLOv8"""

    def __init__(self, model_path: str = 'models/best.pt'):
        """
        Args:
            model_path: Ruta al modelo entrenado
        """
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        """Carga el modelo"""
        try:
            self.model = YOLO(self.model_path)
            print(f"✅ Modelo YOLO cargado: {self.model_path}")
        except Exception as e:
            print(f"❌ Error al cargar modelo: {e}")
            self.model = None

    def detect(self, image: np.ndarray,
               confidence_threshold: float = 0.5) -> List[ObjectDetectionResult]:
        """Detecta objetos en la imagen"""
        if not self.is_ready():
            return []

        # Ejecutar inferencia
        results = self.model(image, conf=confidence_threshold, verbose=False)

        detections = []

        for result in results:
            boxes = result.boxes

            for box in boxes:
                # Obtener información
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                xyxy = box.xyxy[0].cpu().numpy()

                # Convertir a formato (x, y, w, h)
                x1, y1, x2, y2 = xyxy
                bbox = (int(x1), int(y1), int(x2-x1), int(y2-y1))

                # Obtener nombre de clase
                class_name = self.model.names[cls_id]

                # Buscar objeto educativo
                obj_educativo = get_educational_object(class_name)

                if obj_educativo:
                    detection = ObjectDetectionResult(
                        objeto=obj_educativo,
                        bbox=bbox,
                        confianza=conf
                    )
                    detections.append(detection)

        return detections

    def get_supported_objects(self) -> List[str]:
        """Lista de objetos que puede detectar"""
        if not self.is_ready():
            return []
        return list(self.model.names.values())

    def is_ready(self) -> bool:
        """Verifica si está listo"""
        return self.model is not None

    def get_model_info(self) -> dict:
        """Información del modelo"""
        return {
            'nombre': 'YOLOv8',
            'path': self.model_path,
            'clases': len(self.get_supported_objects()),
            'listo': self.is_ready()
        }
```

### Paso 2: Crear Caso de Uso

```python
# src/application/use_cases/detect_educational_objects_use_case.py
from typing import List
import numpy as np
from ...domain.repositories.object_detection_model import (
    ObjectDetectionModel,
    ObjectDetectionResult
)


class DetectEducationalObjectsUseCase:
    """Caso de uso para detectar objetos didácticos"""

    def __init__(self, model: ObjectDetectionModel):
        """
        Args:
            model: Implementación del modelo de detección
        """
        self.model = model

    def execute(self, image: np.ndarray,
                confidence: float = 0.5) -> List[ObjectDetectionResult]:
        """
        Ejecuta la detección de objetos educativos.

        Args:
            image: Imagen BGR
            confidence: Umbral de confianza mínimo

        Returns:
            Lista de objetos detectados
        """
        if not self.model.is_ready():
            raise RuntimeError("El modelo no está listo")

        return self.model.detect(image, confidence)

    def get_available_objects(self) -> List[str]:
        """Obtiene objetos disponibles"""
        return self.model.get_supported_objects()
```

### Paso 3: Usar en la Presentación

```python
# En src/presentation/cli/learning_interface.py
# Agregar al __init__:

from ...infrastructure.detection.yolo_detector import YOLOv8Detector
from ...application.use_cases.detect_educational_objects_use_case import (
    DetectEducationalObjectsUseCase
)

# Si existe modelo entrenado, usarlo
try:
    yolo_model = YOLOv8Detector('models/objetos_didacticos_best.pt')
    self.detect_objects_uc = DetectEducationalObjectsUseCase(yolo_model)
    print("✅ Usando modelo YOLO entrenado")
except:
    # Fallback al detector basado en reglas
    print("⚠️  Usando detector basado en reglas (sin ML)")
    self.detect_objects_uc = None
```

---

## 🚀 Alternativas SIN Entrenar (Inicio Rápido)

### Opción 1: Usar Modelos Pre-entrenados

```python
# Usar YOLOv8 pre-entrenado en COCO dataset
from ultralytics import YOLO

model = YOLO('yolov8n.pt')  # Descarga automática

# Detecta 80 objetos comunes: personas, perros, gatos,
# manzanas, pelotas, libros, etc.
```

**Objetos COCO útiles para educación:**
- person, cat, dog, horse, bird
- apple, banana, orange
- car, bus, truck
- book, laptop, cell phone
- teddy bear, sports ball

### Opción 2: API de Detección (Google, Azure, AWS)

```python
# Ejemplo con Google Cloud Vision
from google.cloud import vision

client = vision.ImageAnnotatorClient()

# Detectar objetos
response = client.object_localization(image=image)

# Objetos detectados con etiquetas
```

### Opción 3: Mejorar Detector Actual (Sin ML)

Agregar más rangos de colores, formas y patrones específicos para objetos didácticos reales.

---

## 📊 Métricas de Evaluación

Después de entrenar, evalúa:

- **mAP@50**: Precisión promedio al 50% IoU (objetivo: >0.7)
- **Precision**: % de detecciones correctas (objetivo: >0.8)
- **Recall**: % de objetos encontrados (objetivo: >0.7)
- **FPS**: Frames por segundo (objetivo: >15 para tiempo real)

```python
# Evaluar modelo
metrics = model.val()
print(f"mAP@50: {metrics.box.map50}")
print(f"Precision: {metrics.box.mp}")
print(f"Recall: {metrics.box.mr}")
```

---

## 🎓 Próximos Pasos

1. **Recolectar dataset** de objetos didácticos reales
2. **Etiquetar** con LabelImg o Roboflow
3. **Entrenar YOLOv8** con transfer learning
4. **Evaluar** precisión en set de prueba
5. **Integrar** modelo en la arquitectura limpia
6. **Ajustar** adaptaciones pedagógicas según resultados

---

## 📚 Recursos Adicionales

- [Ultralytics YOLOv8 Docs](https://docs.ultralytics.com/)
- [Roboflow Tutorial](https://blog.roboflow.com/how-to-train-yolov8-on-a-custom-dataset/)
- [Dataset de Objetos Educativos](https://universe.roboflow.com/search?q=educational+objects)
- [Google Colab para Entrenar](https://colab.research.google.com/)

---

**¿Necesitas ayuda?** Abre un issue en el repositorio con:
- Descripción de objetos a detectar
- Cantidad de imágenes disponibles
- Hardware disponible (CPU/GPU)
