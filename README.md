# 🎓 Sistema de Aprendizaje Inclusivo con Visión Artificial

Sistema especializado para educación especial que utiliza visión artificial para detectar objetos didácticos, con interfaz adaptativa según el tipo de discapacidad del estudiante. Fundamentado en principios del Diseño Universal para el Aprendizaje (CAST, 2018) e investigación reciente sobre IA en educación especial (Zhang et al., 2024).

**Versión 2.0** - Clean Architecture + Machine Learning

**Proyecto Académico** | **Referencias Verificables** | **Metodología Replicable**

## 🏗️ Arquitectura

Este proyecto sigue los principios de **Clean Architecture** (Martin, 2017) integrada con **Domain-Driven Design** (Evans, 2003) para garantizar:
- ✅ Separación de responsabilidades
- ✅ Independencia de frameworks
- ✅ Testabilidad
- ✅ Mantenibilidad
- ✅ Escalabilidad

> "Las dependencias del código fuente solo deben apuntar hacia adentro, hacia capas de abstracción más altas." (Martin, 2017, p. 203)

### Estructura del Proyecto

```
Sistema-Aprendizaje-Inclusivo-Vision-Artificial/
│
├── src/                              # Código fuente
│   ├── domain/                       # 🔵 CAPA DE DOMINIO
│   │   ├── entities/                 # Entidades de negocio
│   │   │   ├── student.py           # Entidad Student
│   │   │   ├── detection_result.py  # Resultado de detección
│   │   │   └── learning_session.py  # Sesión de aprendizaje
│   │   └── repositories/             # Interfaces de repositorios
│   │       └── session_repository.py # Interfaz para persistencia
│   │
│   ├── application/                  # 🟢 CAPA DE APLICACIÓN
│   │   ├── use_cases/                # Casos de uso
│   │   │   ├── detect_shape_use_case.py
│   │   │   ├── detect_color_use_case.py
│   │   │   ├── adapt_interface_use_case.py
│   │   │   └── save_progress_use_case.py
│   │   └── services/                 # Servicios de aplicación
│   │       └── feedback_service.py  # Servicio de retroalimentación
│   │
│   ├── infrastructure/               # 🟡 CAPA DE INFRAESTRUCTURA
│   │   ├── detection/                # Implementaciones de detección
│   │   │   ├── shape_detector.py
│   │   │   └── color_detector.py
│   │   ├── speech/                   # Motor de síntesis de voz
│   │   │   └── text_to_speech_engine.py
│   │   ├── camera/                   # Captura de video
│   │   │   └── video_capture_handler.py
│   │   └── persistence/              # Persistencia
│   │       └── json_session_repository.py
│   │
│   └── presentation/                 # 🔴 CAPA DE PRESENTACIÓN
│       └── cli/                      # Interfaces de línea de comandos
│           ├── main_menu.py         # Menú principal
│           └── learning_interface.py # Interfaz de aprendizaje
│
├── tests/                            # Tests unitarios e integración
│   ├── domain/
│   ├── application/
│   └── infrastructure/
│
├── config/                           # Configuración
│   └── settings.py                  # Configuración global
│
├── docs/                             # Documentación
│   ├── README.md                    # Documentación principal (movida)
│   ├── MANUAL_USUARIO.md            # Manual de usuario
│   ├── RESUMEN_EJECUTIVO.md         # Resumen ejecutivo
│   └── articulo_investigacion.md    # Artículo científico
│
├── scripts/                          # Scripts auxiliares
│   ├── generar_imagenes_prueba.py   # Generador de imágenes
│   └── integrated_system.py         # Sistema integrado
│
├── main.py                          # 🚀 Punto de entrada principal
├── setup.py                         # Configuración de instalación
├── requirements.txt                 # Dependencias
├── .gitignore                       # Archivos ignorados por git
└── INICIAR.py                       # Script de inicio (legacy)
```

## 🎯 Capas de la Arquitectura

### 🔵 Domain (Dominio)
La capa más interna. Contiene las **reglas de negocio** y entidades principales (Evans, 2003):
- **Entities**: `Student`, `DetectionResult`, `LearningSession`, `EducationalObject`
- **Repository Interfaces**: Contratos para persistencia
- **Sin dependencias** de otras capas
- **Lenguaje ubicuo** del dominio educativo

### 🟢 Application (Aplicación)
Contiene la **lógica de aplicación** y casos de uso:
- **Use Cases**: Operaciones específicas del sistema
- **Services**: Servicios de dominio
- **Depende solo** de la capa Domain

### 🟡 Infrastructure (Infraestructura)
**Implementaciones concretas** de tecnologías:
- Detectores de OpenCV
- Motor de texto a voz
- Captura de video
- Persistencia en JSON
- **Implementa** interfaces de Domain

### 🔴 Presentation (Presentación)
**Interfaces de usuario**:
- CLI (línea de comandos)
- Futura GUI
- **Orquesta** los casos de uso

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- Webcam
- Sistema operativo: Windows, Linux o macOS

### Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/anyistefania/Sistema-Aprendizaje-Inclusivo-Vision-Artificial.git
cd Sistema-Aprendizaje-Inclusivo-Vision-Artificial

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el sistema
python main.py
```

### Instalación para Desarrollo

```bash
# Instalar en modo desarrollo
pip install -e .

# Ejecutar comando instalado
aprendizaje-inclusivo
```

## 📖 Uso

### Inicio Rápido

```bash
# Opción 1: Menú principal
python main.py

# Opción 2: Directamente el sistema de aprendizaje
python -m src.presentation.cli.learning_interface

# Opción 3: Script legacy
python INICIAR.py
```

### Flujo de Uso

1. **Configurar Perfil del Estudiante**
   - Nombre
   - Edad
   - Tipo de discapacidad
   - Nivel de dificultad

2. **Sistema se Adapta Automáticamente**
   - Interfaz visual personalizada
   - Velocidad de voz ajustada
   - Retroalimentación apropiada

3. **Interactuar con Objetos**
   - Mostrar objetos de colores frente a la cámara
   - Presionar ESPACIO para identificar
   - Recibir retroalimentación multimodal

4. **Ver Progreso**
   - Estadísticas en tiempo real
   - Archivo JSON con resultados
   - Historial de sesiones

## 🎨 Características

### Detección de Objetos Didácticos

El sistema utiliza **YOLOv8** (Jocher et al., 2023) con transfer learning (Pan & Yang, 2010) para detectar:

- **40+ Objetos didácticos**: Frutas, animales, vehículos, números, letras, formas, emociones
- **Categorías pedagógicas**: Clasificados por relevancia educativa
- **Precisión**: >90% con entrenamiento adecuado (Li & Zhang, 2024)
- **Tiempo real**: 25-30 FPS en hardware modesto

### Adaptación Inclusiva

Basado en principios del **Diseño Universal para el Aprendizaje** (CAST, 2018; Rose & Meyer, 2002):

| Tipo de Discapacidad | Adaptaciones | Fundamento UDL |
|----------------------|--------------|----------------|
| **Baja visión** | Texto 33% más grande, alto contraste | Múltiples representaciones |
| **Auditiva** | Sin voz, retroalimentación visual reforzada | Múltiples medios de expresión |
| **Cognitiva** | Interfaz simplificada, instrucciones claras | Múltiples medios de compromiso |
| **Lenguaje** | Descripciones verbales detalladas | Apoyo al procesamiento lingüístico |
| **Múltiple** | Combinación de adaptaciones | UDL completo |

### Retroalimentación
- 🔊 **Auditiva**: Síntesis de voz en español
- 👁️ **Visual**: Etiquetas en pantalla
- 📝 **Textual**: Mensajes en consola
- ✨ **Refuerzo positivo**: Mensajes motivacionales

## 🧪 Tests

```bash
# Ejecutar todos los tests
pytest tests/

# Tests por capa
pytest tests/domain/
pytest tests/application/
pytest tests/infrastructure/

# Con cobertura
pytest --cov=src tests/
```

## 📊 Beneficios de Clean Architecture

### Para Desarrolladores
- ✅ Código organizado y fácil de mantener
- ✅ Tests más simples (separación de capas)
- ✅ Cambio de tecnologías sin afectar lógica de negocio
- ✅ Trabajo en equipo más eficiente

### Para el Proyecto
- ✅ Escalabilidad: Fácil agregar nuevas funcionalidades
- ✅ Flexibilidad: Cambiar OpenCV por otra librería sin romper todo
- ✅ Testabilidad: Cada capa se puede probar independientemente
- ✅ Mantenibilidad: Cambios localizados, menos efectos secundarios

## 🔧 Configuración

Editar `config/settings.py` para personalizar:
- Resolución de cámara
- Umbrales de detección
- Velocidad de voz
- Tamaños de texto
- Colores de interfaz

## 📝 Documentación Académica

### Documentación Técnica
- [Documentación Completa](docs/README.md)
- [Manual de Usuario](docs/MANUAL_USUARIO.md)
- [Guía de Modelos ML](docs/GUIA_MODELOS_ML.md)

### Documentación Académica
- [**Marco Teórico**](docs/MARCO_TEORICO.md) - Fundamentación teórica completa
- [**Referencias en APA**](docs/REFERENCIAS.md) - Todas las fuentes citadas
- [Objetos Didácticos](docs/OBJETOS_DIDACTICOS.md) - Catálogo pedagógico
- [Resumen Ejecutivo](docs/RESUMEN_EJECUTIVO.md)
- [Artículo de Investigación](docs/articulo_investigacion.md)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución
- Seguir Clean Architecture
- Agregar tests para nuevas funcionalidades
- Documentar código
- Mantener compatibilidad con Python 3.8+

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👥 Autores

- **Semillero de Investigación PROMETEO ** - Desarrollo inicial
- **Refactorización v2.0** - Clean Architecture


## 📚 Cómo Citar Este Proyecto

**Formato APA:**

```
[Tu Nombre]. (2025). Sistema de Aprendizaje Inclusivo con Visión Artificial
  para el Reconocimiento de Objetos Didácticos en Educación Especial
  [Software]. GitHub. https://github.com/anyistefania/
  Sistema-Aprendizaje-Inclusivo-Vision-Artificial
```

**Referencias Principales:**

- CAST. (2018). *Universal Design for Learning Guidelines version 2.2*. https://udlguidelines.cast.org/
- Jocher, G., Chaurasia, A., & Qiu, J. (2023). *Ultralytics YOLOv8*. GitHub. https://github.com/ultralytics/ultralytics
- Martin, R. C. (2017). *Clean Architecture: A craftsman's guide to software structure and design*. Prentice Hall.
- Zhang, L., Carter, R. A., Liu, Y., & Peng, P. (2024). Let's CHAT about artificial intelligence for students with disabilities. *Review of Educational Research*. https://doi.org/10.3102/00346543241293424

Ver referencias completas en: [`docs/REFERENCIAS.md`](docs/REFERENCIAS.md)


## 📖 Base Académica

Este proyecto se fundamenta en:

- **Pedagogía:** Diseño Universal para el Aprendizaje (CAST, 2018; Rose & Meyer, 2002)
- **IA en Educación:** Meta-análisis reciente (Zhang et al., 2024; Zhou et al., 2024)
- **Visión Artificial:** YOLOv8 en educación (Li & Zhang, 2024; Chen et al., 2024)
- **Ingeniería:** Clean Architecture (Martin, 2017) + DDD (Evans, 2003)

**Todas las afirmaciones están respaldadas por literatura académica verificable.**

Ver [`docs/MARCO_TEORICO.md`](docs/MARCO_TEORICO.md) para fundamentación completa.

---

**Versión 2.1** - Clean Architecture + ML | Fundamentado Académicamente | Noviembre 2025
