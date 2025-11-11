# 🔧 Guía de Solución de Problemas

Esta guía te ayuda a resolver los problemas más comunes del sistema.

---

## 🔊 Problema 1: La Voz No Funciona ("No Dice Nada")

### Diagnóstico Rápido

```bash
# Ejecutar script de diagnóstico
python scripts/diagnosticar_sistema.py
```

### Causas Comunes y Soluciones

#### ❌ Causa 1: pyttsx3 no instalado

**Síntoma:** Mensaje "⚠️ Advertencia: No se pudo inicializar el motor de voz"

**Solución:**
```bash
pip install pyttsx3
```

#### ❌ Causa 2: En Windows falta pypiwin32

**Síntoma:** Error al inicializar motor de voz en Windows

**Solución:**
```bash
pip install pypiwin32
pip install comtypes
```

#### ❌ Causa 3: No hay voces en español instaladas

**Síntoma:** La voz habla en inglés o con acento extraño

**Solución en Windows 10/11:**

1. Abre **Configuración** → **Hora e idioma** → **Voz**
2. En "Administrar voces", descarga **Español (México)** o **Español (España)**
3. Reinicia el programa

**Solución en Linux:**
```bash
sudo apt-get install espeak
```

#### ❌ Causa 4: Volumen del sistema bajo

**Síntoma:** El código no muestra errores pero no se escucha nada

**Solución:**
1. Sube el volumen de Windows
2. Verifica que los altavoces estén encendidos
3. Prueba con auriculares

### Solución Definitiva para Windows

```bash
# Instalar todas las dependencias de voz
pip uninstall pyttsx3
pip install pyttsx3==2.90
pip install pypiwin32
pip install comtypes

# Luego reinicia Python/VSCode
```

### Verificar que Funciona

```python
# Prueba rápida en Python
import pyttsx3

engine = pyttsx3.init()
engine.say("Hola, esta es una prueba")
engine.runAndWait()

# Si escuchas la voz, ¡funciona!
```

---

## 🎯 Problema 2: Detección No Precisa

### Causas Comunes y Soluciones

#### ❌ Causa 1: Mala iluminación

**Síntoma:** No detecta objetos o los detecta mal

**Solución:**
- ✅ Ilumina la escena uniformemente
- ✅ Evita sombras fuertes
- ✅ Evita luz directa del sol (causa sobresaturación)
- ✅ Usa luz natural difusa o luz LED blanca

**Iluminación ideal:**
```
         💡 Luz cenital difusa
            ↓
    ┌─────────────────┐
    │                 │
📷 →│   📦 Objeto    │← Fondo blanco/neutro
    │                 │
    └─────────────────┘
```

#### ❌ Causa 2: Colores poco saturados

**Síntoma:** Detecta la forma pero no el color

**Solución:**
- ✅ Usa objetos con colores BRILLANTES y sólidos
- ✅ Evita colores pastel o apagados
- ✅ Preferible: rojo, azul, verde, amarillo intensos
- ❌ Evita: rosa claro, gris, beige

**Ajustar sensibilidad de color:**

Edita `inclusive_learning_system.py` línea 185:

```python
# ANTES (más restrictivo):
if max_pixels < total_pixels * 0.15:  # 15% mínimo
    return None

# DESPUÉS (más permisivo):
if max_pixels < total_pixels * 0.08:  # 8% mínimo
    return None
```

#### ❌ Causa 3: Objetos muy pequeños

**Síntoma:** No detecta objetos pequeños

**Solución:**
- ✅ Acerca los objetos a la cámara (30-50 cm)
- ✅ Usa objetos de mínimo 5x5 cm
- ✅ Reduce el área mínima

**Ajustar tamaño mínimo:**

Edita `inclusive_learning_system.py` línea 419:

```python
# ANTES (área mínima grande):
min_area = 1000 if nivel == 1 else 800

# DESPUÉS (área mínima menor):
min_area = 500 if nivel == 1 else 400  # Detecta objetos más pequeños
```

#### ❌ Causa 4: Fondo confuso

**Síntoma:** Detecta cosas que no son objetos

**Solución:**
- ✅ Usa un fondo liso y claro (cartulina blanca)
- ✅ Evita fondos con patrones o colores mezclados
- ✅ Mantén el fondo despejado

#### ❌ Causa 5: Movimiento rápido

**Síntoma:** Detecta intermitentemente

**Solución:**
- ✅ Mantén el objeto quieto al presionar ESPACIO
- ✅ Evita movimientos bruscos
- ✅ Espera 1-2 segundos antes de identificar

---

## 🎨 Mejorar Precisión de Colores

### Rangos HSV Optimizados

Si ciertos colores no se detectan bien, ajusta los rangos:

**Archivo:** `inclusive_learning_system.py` líneas 72-106

```python
# Para ROJO más permisivo:
'rojo': {
    'ranges': [
        {'lower': np.array([0, 100, 70]), 'upper': np.array([10, 255, 255])},
        {'lower': np.array([165, 100, 70]), 'upper': np.array([180, 255, 255])}
    ],
    # ...
}

# Para AZUL más permisivo:
'azul': {
    'ranges': [{'lower': np.array([90, 120, 50]), 'upper': np.array([135, 255, 255])}],
    # ...
}

# Para VERDE más permisivo:
'verde': {
    'ranges': [{'lower': np.array([35, 30, 30]), 'upper': np.array([85, 255, 255])}],
    # ...
}
```

### Calibración Personalizada

1. **Muestra el objeto a la cámara**
2. **Presiona 'H' para ocultar ayuda** y ver mejor
3. **Ajusta hasta que el color se detecte bien**
4. **Guarda los cambios**

---

## 📹 Optimizar Rendimiento

### Si el sistema va lento (< 15 FPS):

**1. Reducir resolución:**

Edita líneas 366-367:

```python
# ANTES:
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

# DESPUÉS:
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Más rápido
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

**2. Simplificar procesamiento:**

Edita línea 405:

```python
# ANTES:
kernel = np.ones((5, 5), np.uint8)

# DESPUÉS:
kernel = np.ones((3, 3), np.uint8)  # Más rápido
```

**3. Cerrar otras aplicaciones:**
- Cierra navegadores
- Cierra otras apps que usen cámara
- Libera RAM

---

## 🛠️ Configuración Recomendada

### Setup Ideal para Educación Especial

```
Iluminación:
- 2 luces LED blancas a los lados
- Luz difusa (no directa)
- Brillo uniforme

Fondo:
- Cartulina blanca tamaño A3
- O tela blanca lisa
- Sin patrones ni arrugas

Objetos:
- Tamaño: 5-15 cm
- Colores: Brillantes y sólidos
- Material: Plástico, goma EVA, cartón

Cámara:
- Distancia: 40-60 cm
- Ángulo: Ligeramente desde arriba
- Resolución: 640x480 o superior

Espacio:
- Mesa despejada
- Sin distracciones visuales
- Ventanas con cortinas (evitar sol directo)
```

---

## 🔍 Checklist de Diagnóstico

Antes de reportar un problema, verifica:

- [ ] ✅ Dependencias instaladas (`pip list | grep -E "opencv|pyttsx3|numpy"`)
- [ ] ✅ Cámara funciona (prueba con otra app)
- [ ] ✅ Iluminación adecuada
- [ ] ✅ Fondo liso y claro
- [ ] ✅ Objetos con colores brillantes
- [ ] ✅ Volumen del sistema alto
- [ ] ✅ Voces en español instaladas (Windows)
- [ ] ✅ pypiwin32 instalado (Windows)
- [ ] ✅ Objeto a 40-60 cm de cámara
- [ ] ✅ Objeto quieto al identificar

---

## 📞 Obtener Ayuda

Si los problemas persisten:

**1. Ejecuta diagnóstico:**
```bash
python scripts/diagnosticar_sistema.py
```

**2. Copia la salida completa**

**3. Reporta en:** https://github.com/anyistefania/Sistema-Aprendizaje-Inclusivo-Vision-Artificial/issues

Incluye:
- Sistema operativo y versión
- Versión de Python (`python --version`)
- Salida del diagnóstico
- Descripción del problema
- Foto del setup (opcional)

---

## 🎯 Soluciones Rápidas

| Problema | Solución Rápida |
|----------|----------------|
| Sin voz | `pip install pypiwin32` (Windows) |
| Voz en inglés | Instalar voces español en Windows |
| No detecta colores | Mejora iluminación + colores brillantes |
| No detecta formas | Usa fondo blanco + acerca objeto |
| Va lento | Reduce resolución a 640x480 |
| Detecta cosas raras | Usa fondo liso sin patrones |

---

**Última actualización:** Noviembre 2025
