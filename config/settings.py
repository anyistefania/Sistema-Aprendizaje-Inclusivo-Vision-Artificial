"""
Configuración Global del Sistema
"""

# Configuración de Cámara
CAMERA_INDEX = 0
CAMERA_WIDTH = 800
CAMERA_HEIGHT = 600

# Configuración de Detección
MIN_AREA_BASIC = 1000  # Nivel básico
MIN_AREA_INTERMEDIATE = 800  # Nivel intermedio
MIN_AREA_ADVANCED = 600  # Nivel avanzado

# Configuración de Voz
VOICE_RATE_NORMAL = 150
VOICE_RATE_SLOW = 120
VOICE_RATE_VERY_SLOW = 100
VOICE_VOLUME = 1.0

# Configuración de Interfaz
FONT_SCALE_NORMAL = 0.9
FONT_SCALE_LARGE = 1.2
FONT_THICKNESS_NORMAL = 2
FONT_THICKNESS_BOLD = 3

# Colores de Texto (BGR)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (0, 255, 255)
COLOR_GREEN = (0, 255, 0)

# Configuración de Persistencia
SESSIONS_DIR = "sessions"
MAX_SESSION_AGE_DAYS = 90

# Configuración de Procesamiento de Imagen
GAUSSIAN_BLUR_KERNEL = (11, 11)
MORPHOLOGY_KERNEL_SIZE = (5, 5)
ADAPTIVE_THRESHOLD_BLOCK_SIZE = 11
ADAPTIVE_THRESHOLD_C = 2

# Configuración de Detección de Color
COLOR_DETECTION_THRESHOLD = 0.15  # 15% de píxeles mínimo
