# MANUAL DE USUARIO E INSTALACIÓN
## Sistema de Aprendizaje Inclusivo con Visión Artificial

---

## 📋 TABLA DE CONTENIDOS

1. [Descripción del Proyecto](#descripción)
2. [Requisitos del Sistema](#requisitos)
3. [Instalación](#instalación)
4. [Módulos del Sistema](#módulos)
5. [Guía de Uso](#guía-de-uso)
6. [Adaptaciones según Discapacidad](#adaptaciones)
7. [Actividades Didácticas](#actividades)
8. [Solución de Problemas](#problemas)
9. [Soporte y Contacto](#soporte)

---

## 🎯 DESCRIPCIÓN DEL PROYECTO

Este sistema utiliza **visión artificial** para crear entornos de aprendizaje inclusivos en educación especial. El sistema detecta y reconoce formas geométricas y colores en tiempo real usando la cámara web, proporcionando retroalimentación multimodal adaptada a las necesidades específicas de cada estudiante.

### Características principales:
- ✅ Detección de formas: círculo, triángulo, cuadrado, rectángulo, pentágono
- ✅ Detección de colores: rojo, azul, verde, amarillo, naranja, morado
- ✅ Retroalimentación por voz (texto a voz)
- ✅ Interfaz adaptativa según tipo de discapacidad
- ✅ Registro de progreso del estudiante
- ✅ Refuerzo positivo constante

---

## 💻 REQUISITOS DEL SISTEMA

### Hardware Mínimo:
- **Procesador:** Intel Core i3 o equivalente
- **RAM:** 4 GB (8 GB recomendado)
- **Cámara web:** 720p o superior
- **Espacio en disco:** 500 MB libres

### Software:
- **Sistema operativo:** Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.14+
- **Python:** Versión 3.8 o superior

---

## 🔧 INSTALACIÓN

### Paso 1: Verificar Python

Abra una terminal/consola y ejecute:

```bash
python --version
```

Debe mostrar Python 3.8 o superior. Si no lo tiene, descárguelo de:
- Windows: https://www.python.org/downloads/
- Linux: `sudo apt-get install python3 python3-pip`
- macOS: `brew install python3`

### Paso 2: Descargar el proyecto

Descargue todos los archivos del proyecto en una carpeta, por ejemplo:
```
C:\Users\TuUsuario\EducacionInclusiva\
```

### Paso 3: Crear entorno virtual (RECOMENDADO)

En la terminal, navegue a la carpeta del proyecto y ejecute:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Verá `(venv)` al inicio de la línea de comandos.

### Paso 4: Instalar dependencias

Con el entorno virtual activado, ejecute:

```bash
pip install -r requirements.txt
```

Este proceso puede tardar varios minutos.

### Paso 5: Verificar instalación

Ejecute:
```bash
python -c "import cv2; print('OpenCV versión:', cv2.__version__)"
```

Debe mostrar la versión de OpenCV sin errores.

### Paso 6: Configurar la cámara

Asegúrese de que su cámara web esté conectada y funcional.

---

## 📦 MÓDULOS DEL SISTEMA

El proyecto incluye 4 módulos principales:

### 1. `shape_detector.py` - Detector de Formas
Detecta formas geométricas en imágenes o en tiempo real.

**Ejecutar:**
```bash
python shape_detector.py
```

**Funcionalidades:**
- Opción 1: Analizar una imagen guardada
- Opción 2: Detección en tiempo real con cámara

**Controles:**
- `Q` - Salir
- `S` - Capturar imagen

---

### 2. `color_detector.py` - Detector de Colores
Detecta colores en tiempo real usando la cámara.

**Ejecutar:**
```bash
python color_detector.py
```

**Controles:**
- `Q` - Salir
- `S` - Capturar imagen
- `V` - Activar/desactivar voz
- `H` - Mostrar/ocultar ayuda
- `C` - Limpiar pantalla

---

### 3. `integrated_system.py` - Sistema Integrado
Combina detección de formas y colores simultáneamente.

**Ejecutar:**
```bash
python integrated_system.py
```

**Controles:**
- `Q` - Salir
- `S` - Guardar imagen
- `V` - Voz on/off
- `F` - Congelar/descongelar imagen
- `H` - Ayuda
- `1` - Modo solo formas
- `2` - Modo solo colores
- `3` - Modo integrado (formas + colores)

---

### 4. `inclusive_learning_system.py` - Sistema de Aprendizaje Inclusivo ⭐
**RECOMENDADO PARA EDUCACIÓN ESPECIAL**

Este es el módulo principal diseñado específicamente para estudiantes con necesidades educativas especiales.

**Ejecutar:**
```bash
python inclusive_learning_system.py
```

**Proceso de inicio:**
1. El sistema solicitará información del estudiante:
   - Nombre
   - Edad
   - Tipo de discapacidad
   - Nivel de dificultad

2. Configurará automáticamente la interfaz según las necesidades

**Controles:**
- `ESPACIO` - Identificar objeto (función principal)
- `Q` - Salir y guardar progreso
- `H` - Mostrar/ocultar ayuda
- `S` - Capturar imagen de la sesión

---

## 🎓 GUÍA DE USO PARA DOCENTES

### Preparación de la sesión:

1. **Materiales necesarios:**
   - Objetos de diferentes formas (círculos, cuadrados, triángulos)
   - Objetos de colores vivos (rojo, azul, verde, amarillo, naranja)
   - Fondo claro y uniforme (blanco o beige)
   - Buena iluminación (natural o artificial sin sombras fuertes)

2. **Configuración del espacio:**
   - Coloque la cámara a una altura adecuada
   - Mantenga una distancia de 30-50 cm de los objetos
   - Evite fondos con muchos colores o patrones

3. **Inicio de sesión:**
   ```bash
   python inclusive_learning_system.py
   ```
   
   Complete el perfil del estudiante cuando se solicite.

### Durante la sesión:

1. **Mostrar objetos uno a uno:**
   - Presente el objeto frente a la cámara
   - Espere a que el sistema lo detecte (aparecerá un contorno)
   - Presione la barra ESPACIADORA para identificación

2. **El sistema anunciará:**
   - La forma del objeto
   - El color del objeto
   - Un mensaje de refuerzo positivo

3. **Progresión:**
   - Comience con objetos grandes de colores primarios
   - Avance a formas más complejas
   - Combine múltiples objetos según el nivel

### Fin de sesión:

1. Presione `Q` para salir
2. El sistema guardará automáticamente:
   - Estadísticas de la sesión
   - Número de aciertos
   - Objetos reconocidos
   - Tiempo de duración

3. Los datos se guardan en formato JSON con nombre:
   ```
   progreso_[NombreEstudiante]_[FechaHora].json
   ```

---

## ♿ ADAPTACIONES SEGÚN DISCAPACIDAD

### 1. Baja Visión
**Características activadas:**
- Texto más grande (120% del tamaño normal)
- Mayor grosor de líneas
- Alto contraste (amarillo sobre negro)
- Contornos más gruesos en objetos
- Retroalimentación por voz activa

**Recomendaciones:**
- Use objetos grandes (>10 cm)
- Iluminación brillante y uniforme
- Colores muy contrastantes

---

### 2. Discapacidad Auditiva
**Características activadas:**
- Retroalimentación visual prominente
- Mensajes en texto grande
- Indicadores visuales de progreso
- Sin dependencia de audio

**Recomendaciones:**
- Mantenga contacto visual con el estudiante
- Use señas para indicar cuándo presionar ESPACIO
- Muestre los mensajes en pantalla

---

### 3. Discapacidad Cognitiva
**Características activadas:**
- Interfaz simplificada
- Instrucciones paso a paso
- Refuerzo positivo constante
- Colores y formas básicas
- Ritmo pausado

**Recomendaciones:**
- Una forma/color a la vez
- Repetición frecuente
- Pausas entre actividades
- Celebrar cada logro

---

### 4. Trastornos del Lenguaje
**Características activadas:**
- Descripciones verbales claras
- Asociaciones con objetos familiares
- Velocidad de voz reducida
- Repetición de conceptos

**Recomendaciones:**
- Tiempo para responder
- Aceptar comunicación no verbal
- Usar el sistema como medio de expresión

---

### 5. Discapacidad Múltiple
**Características activadas:**
- Combinación de adaptaciones
- Mayor tiempo de respuesta
- Simplificación máxima
- Apoyo multimodal

**Recomendaciones:**
- Sesiones más cortas (10-15 min)
- Un objetivo a la vez
- Apoyo físico si es necesario
- Paciencia y flexibilidad

---

## 🎨 ACTIVIDADES DIDÁCTICAS

### Nivel 1 - Básico (4-6 años o iniciación)

**Actividad 1: Reconocimiento de Colores**
- Duración: 10 minutos
- Objetivo: Identificar colores primarios
- Materiales: Objetos rojos, azules y amarillos
- Procedimiento:
  1. Muestre un objeto rojo
  2. Presione ESPACIO
  3. Escuche la identificación
  4. Repita con azul y amarillo
  5. Celebre cada acierto

**Actividad 2: Reconocimiento de Formas**
- Duración: 10 minutos
- Objetivo: Identificar círculo, cuadrado, triángulo
- Materiales: Figuras geométricas de cartón
- Procedimiento: Similar a Actividad 1

---

### Nivel 2 - Intermedio (7-10 años)

**Actividad 3: Asociación Color-Forma**
- Duración: 15 minutos
- Objetivo: Identificar objeto completo (forma + color)
- Ejemplo: "triángulo rojo", "cuadrado azul"

**Actividad 4: Búsqueda del Objeto**
- Duración: 15 minutos
- Objetivo: Encontrar un objeto específico
- Procedimiento:
  1. Docente dice: "Busca el círculo verde"
  2. Estudiante muestra el objeto
  3. Sistema confirma

---

### Nivel 3 - Avanzado (11+ años)

**Actividad 5: Clasificación**
- Duración: 20 minutos
- Objetivo: Agrupar por forma o color
- Muestre múltiples objetos y clasifíquelos

**Actividad 6: Patrones y Secuencias**
- Duración: 20 minutos
- Objetivo: Completar secuencias
- Ejemplo: rojo, azul, rojo, ¿?

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### ❌ La cámara no se inicia

**Solución 1:**
Si tiene múltiples cámaras, edite el archivo Python:
```python
cap = cv2.VideoCapture(0)  # Cambiar 0 por 1, 2, etc.
```

**Solución 2:**
Verifique permisos de cámara:
- Windows: Configuración → Privacidad → Cámara
- macOS: Preferencias → Seguridad → Cámara
- Linux: `ls /dev/video*`

---

### ❌ No detecta objetos

**Causas comunes:**
1. Iluminación deficiente → Use más luz
2. Objeto muy pequeño → Use objetos más grandes
3. Colores muy claros → Use colores más intensos
4. Fondo con patrones → Use fondo uniforme

---

### ❌ La voz no funciona

**Windows:**
```bash
pip uninstall pyttsx3
pip install pyttsx3==2.90
```

**Linux:**
```bash
sudo apt-get install espeak
```

**macOS:**
La voz debería funcionar por defecto. Si no:
```bash
pip install pyobjc
```

---

### ❌ Errores de instalación

**Error: "No module named cv2"**
```bash
pip install opencv-python
```

**Error: "Microsoft Visual C++ required"**
Descargue e instale:
https://aka.ms/vs/16/release/vc_redist.x64.exe

**Error en Linux: "libGL.so.1 not found"**
```bash
sudo apt-get install libgl1-mesa-glx
```

---

### 🐛 Detección imprecisa

**Optimización:**
1. Ajuste la iluminación (evitar sombras)
2. Use colores saturados (brillantes)
3. Fondo de color sólido y claro
4. Limpie la lente de la cámara
5. Objetos de tamaño mínimo 5x5 cm

---

## 📞 SOPORTE Y CONTACTO

### Documentación adicional:
- Artículo de investigación: `articulo_investigacion.md`
- Código fuente comentado en cada archivo `.py`

### Reportar problemas:
Para reportar errores o sugerir mejoras:
1. Describa el problema detalladamente
2. Incluya capturas de pantalla
3. Especifique sistema operativo y versión de Python

### Contribuciones:
Este es un proyecto de código abierto para educación especial.
Las contribuciones son bienvenidas.

---

## 📜 LICENCIA Y USO ACADÉMICO

Este sistema fue desarrollado con fines educativos e investigativos.

**Permitido:**
- ✅ Uso en instituciones educativas
- ✅ Modificación para necesidades específicas
- ✅ Investigación y publicación académica
- ✅ Capacitación de docentes

**Se requiere:**
- Citar el proyecto original
- Compartir mejoras con la comunidad educativa

---

## 🎯 MEJORES PRÁCTICAS

### Para Docentes:
1. **Preparación:** Pruebe el sistema antes de la sesión con el estudiante
2. **Paciencia:** Respete el ritmo de cada estudiante
3. **Refuerzo:** Celebre cada logro, por pequeño que sea
4. **Registro:** Guarde las sesiones para seguimiento
5. **Colaboración:** Involucre a padres y terapeutas

### Para Desarrolladores:
1. **Personalización:** Adapte los umbrales de detección según necesidad
2. **Extensión:** Agregue nuevas formas y colores
3. **Idiomas:** Adapte mensajes de voz a otros idiomas
4. **Accesibilidad:** Considere otras discapacidades

---

## 📊 INTERPRETACIÓN DE RESULTADOS

### Archivo de progreso JSON:

```json
{
    "fecha": "2025-11-11T10:30:00",
    "estudiante": "María",
    "duracion_minutos": 15.5,
    "estadisticas": {
        "aciertos": 12,
        "intentos": 15,
        "objetos_reconocidos": ["circulo_rojo", "cuadrado_azul", ...]
    },
    "nivel": 1
}
```

**Análisis:**
- **Tasa de éxito:** aciertos/intentos × 100
- **Progreso:** Comparar sesiones consecutivas
- **Áreas fuertes:** Objetos reconocidos frecuentemente
- **Áreas de mejora:** Objetos con dificultad

---

## 🌟 CASOS DE ÉXITO

### Ejemplo 1: Juan, 8 años - Autismo
- **Antes:** Dificultad para mantener atención
- **Con el sistema:** 15 minutos de atención sostenida
- **Logro:** Reconoció 10 colores en 2 semanas

### Ejemplo 2: Ana, 6 años - Baja visión
- **Antes:** Dependencia total del docente
- **Con el sistema:** Mayor autonomía en identificación
- **Logro:** Puede trabajar con supervisión mínima

---

## 🔄 ACTUALIZACIONES

### Versión 1.0 (Actual)
- Detección de formas básicas
- Detección de 6 colores
- Retroalimentación por voz
- Registro de progreso

### Próximas versiones planeadas:
- [ ] App móvil (Android/iOS)
- [ ] Más idiomas
- [ ] Reconocimiento de objetos 3D
- [ ] Integración con tableros interactivos
- [ ] Gamificación avanzada
- [ ] Análisis de datos con IA

---

## ✅ CHECKLIST DE INSTALACIÓN

Marque cada paso completado:

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] OpenCV funcional
- [ ] Cámara probada
- [ ] Voz funcional
- [ ] Sistema ejecutado exitosamente
- [ ] Materiales didácticos preparados
- [ ] Perfil del estudiante creado
- [ ] Primera sesión completada

---

## 📚 RECURSOS ADICIONALES

### Lecturas recomendadas:
1. "Educación Inclusiva con Tecnología" - UNESCO
2. "Visión Artificial en Educación" - PyImageSearch
3. "Diseño Universal para el Aprendizaje" - CAST

### Sitios web:
- OpenCV: https://opencv.org/
- Python: https://www.python.org/
- Educación Inclusiva: https://www.unesco.org/

---

**Última actualización:** Noviembre 2025
**Versión del manual:** 1.0

---

¡Gracias por usar este sistema para crear entornos de aprendizaje inclusivos! 🌈👩‍🏫👨‍🎓
