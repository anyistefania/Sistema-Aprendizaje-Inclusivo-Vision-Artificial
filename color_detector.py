"""
Detector de Colores en Tiempo Real
Proyecto: Entornos de Aprendizaje Inclusivos con Visión Artificial
Autor: Semillero de Investigación
Fecha: Noviembre 2025

Este módulo implementa la detección de colores en tiempo real
utilizando la cámara web y el espacio de color HSV.
"""

import cv2
import numpy as np
import pyttsx3
from collections import Counter
import time


class ColorDetector:
    """
    Clase para detectar y clasificar colores en imágenes usando espacio HSV.
    
    Colores detectados:
    - Rojo
    - Azul
    - Verde
    - Amarillo
    - Naranja
    - Morado
    - Blanco
    - Negro
    """
    
    def __init__(self, use_voice=True):
        """
        Inicializa el detector de colores.
        
        Args:
            use_voice: Si True, activa la retroalimentación por voz
        """
        # Definir rangos de colores en espacio HSV
        self.color_ranges = {
            'rojo1': {
                'lower': np.array([0, 100, 100]),
                'upper': np.array([10, 255, 255]),
                'bgr': (0, 0, 255),
                'name': 'rojo'
            },
            'rojo2': {
                'lower': np.array([170, 100, 100]),
                'upper': np.array([180, 255, 255]),
                'bgr': (0, 0, 255),
                'name': 'rojo'
            },
            'azul': {
                'lower': np.array([100, 150, 50]),
                'upper': np.array([130, 255, 255]),
                'bgr': (255, 0, 0),
                'name': 'azul'
            },
            'verde': {
                'lower': np.array([40, 50, 50]),
                'upper': np.array([80, 255, 255]),
                'bgr': (0, 255, 0),
                'name': 'verde'
            },
            'amarillo': {
                'lower': np.array([20, 100, 100]),
                'upper': np.array([35, 255, 255]),
                'bgr': (0, 255, 255),
                'name': 'amarillo'
            },
            'naranja': {
                'lower': np.array([10, 100, 100]),
                'upper': np.array([20, 255, 255]),
                'bgr': (0, 165, 255),
                'name': 'naranja'
            },
            'morado': {
                'lower': np.array([130, 50, 50]),
                'upper': np.array([170, 255, 255]),
                'bgr': (255, 0, 255),
                'name': 'morado'
            },
            'blanco': {
                'lower': np.array([0, 0, 200]),
                'upper': np.array([180, 30, 255]),
                'bgr': (255, 255, 255),
                'name': 'blanco'
            },
            'negro': {
                'lower': np.array([0, 0, 0]),
                'upper': np.array([180, 255, 50]),
                'bgr': (0, 0, 0),
                'name': 'negro'
            }
        }
        
        # Inicializar motor de síntesis de voz
        self.use_voice = use_voice
        if use_voice:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 150)
                self.engine.setProperty('volume', 0.9)
            except Exception as e:
                print(f"Advertencia: No se pudo inicializar el motor de voz: {e}")
                self.use_voice = False
    
    def detect_color(self, hsv_image, mask_area):
        """
        Detecta el color predominante en una región de la imagen.
        
        Args:
            hsv_image: Imagen en espacio HSV
            mask_area: Máscara binaria del área a analizar
            
        Returns:
            str: Nombre del color detectado
        """
        max_pixels = 0
        detected_color = "desconocido"
        
        for color_key, color_data in self.color_ranges.items():
            # Crear máscara para este color
            mask = cv2.inRange(hsv_image, color_data['lower'], color_data['upper'])
            
            # Combinar con la máscara del área
            combined_mask = cv2.bitwise_and(mask, mask_area)
            
            # Contar píxeles del color
            pixels = cv2.countNonZero(combined_mask)
            
            if pixels > max_pixels:
                max_pixels = pixels
                detected_color = color_data['name']
        
        return detected_color
    
    def get_color_bgr(self, color_name):
        """
        Obtiene el valor BGR de un color por su nombre.
        
        Args:
            color_name: Nombre del color
            
        Returns:
            tuple: Valor BGR
        """
        for color_data in self.color_ranges.values():
            if color_data['name'] == color_name:
                return color_data['bgr']
        return (128, 128, 128)  # Gris por defecto
    
    def speak(self, text):
        """
        Sintetiza voz para dar retroalimentación auditiva.
        
        Args:
            text: Texto a sintetizar
        """
        if self.use_voice:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass


def detect_colors_camera():
    """
    Detecta colores en tiempo real desde la cámara web.
    
    Controles:
    - 'q': Salir
    - 's': Capturar y guardar
    - 'v': Activar/desactivar voz
    - 'h': Mostrar ayuda
    """
    # Inicializar cámara
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara")
        return
    
    # Configurar resolución
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Inicializar detector de colores
    color_detector = ColorDetector(use_voice=True)
    
    # Variables de control
    voice_enabled = True
    show_help = True
    last_voice_time = 0
    voice_cooldown = 2.0  # segundos entre anuncios de voz
    
    print("=" * 60)
    print("DETECTOR DE COLORES EN TIEMPO REAL")
    print("=" * 60)
    print("\nControles:")
    print("  'q' - Salir")
    print("  's' - Capturar imagen")
    print("  'v' - Activar/Desactivar voz")
    print("  'h' - Mostrar/Ocultar ayuda")
    print("  'c' - Limpiar pantalla de terminal")
    print("-" * 60)
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: No se pudo leer el frame")
            break
        
        # Voltear horizontalmente para efecto espejo
        frame = cv2.flip(frame, 1)
        
        # Aplicar desenfoque para reducir ruido
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        
        # Convertir a espacio HSV
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        # Crear diccionario para contar colores
        color_masks = {}
        combined_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        
        # Detectar cada color
        for color_key, color_data in color_detector.color_ranges.items():
            mask = cv2.inRange(hsv, color_data['lower'], color_data['upper'])
            
            # Aplicar operaciones morfológicas para reducir ruido
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            color_name = color_data['name']
            if color_name not in color_masks:
                color_masks[color_name] = np.zeros_like(mask)
            
            color_masks[color_name] = cv2.bitwise_or(color_masks[color_name], mask)
        
        # Encontrar contornos y etiquetar colores
        detected_colors = []
        
        for color_name, mask in color_masks.items():
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, 
                                          cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Filtrar contornos pequeños
                if area < 1000:
                    continue
                
                # Calcular centro y dimensiones
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                else:
                    continue
                
                # Obtener bounding box
                x, y, w, h = cv2.boundingRect(contour)
                
                # Dibujar contorno
                color_bgr = color_detector.get_color_bgr(color_name)
                cv2.drawContours(frame, [contour], -1, color_bgr, 3)
                
                # Dibujar rectángulo
                cv2.rectangle(frame, (x, y), (x + w, y + h), color_bgr, 2)
                
                # Dibujar centro
                cv2.circle(frame, (cX, cY), 7, color_bgr, -1)
                
                # Etiqueta de color con fondo
                label = f"{color_name.upper()}"
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 
                                                0.8, 2)
                
                # Fondo para el texto
                cv2.rectangle(frame, 
                            (x, y - label_size[1] - 10),
                            (x + label_size[0], y),
                            color_bgr, -1)
                
                # Texto (blanco o negro según el color de fondo)
                text_color = (0, 0, 0) if color_name in ['blanco', 'amarillo'] else (255, 255, 255)
                cv2.putText(frame, label, (x, y - 5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)
                
                detected_colors.append(color_name)
        
        # Información en pantalla
        info_y = 30
        cv2.rectangle(frame, (0, 0), (640, 150), (0, 0, 0), -1)
        
        cv2.putText(frame, "DETECTOR DE COLORES", (10, info_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        info_y += 30
        
        # Contar colores detectados
        if detected_colors:
            color_counts = Counter(detected_colors)
            colors_text = ", ".join([f"{color}: {count}" for color, count in color_counts.items()])
            cv2.putText(frame, f"Detectados: {colors_text}", (10, info_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Retroalimentación por voz (con cooldown)
            current_time = time.time()
            if voice_enabled and (current_time - last_voice_time) > voice_cooldown:
                if len(color_counts) == 1:
                    most_common = list(color_counts.keys())[0]
                    color_detector.speak(f"Detecto el color {most_common}")
                    last_voice_time = current_time
        else:
            cv2.putText(frame, "No se detectan colores", (10, info_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        info_y += 30
        
        # Estado de la voz
        voice_status = "ACTIVADA" if voice_enabled else "DESACTIVADA"
        cv2.putText(frame, f"Voz: {voice_status}", (10, info_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) if voice_enabled else (0, 0, 255), 1)
        
        info_y += 25
        
        # Ayuda
        if show_help:
            cv2.putText(frame, "Q:Salir | S:Capturar | V:Voz | H:Ayuda", (10, info_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
        
        # Mostrar frame
        cv2.imshow("Detector de Colores - Camara en Vivo", frame)
        
        # Procesar teclas
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\nSaliendo del programa...")
            break
            
        elif key == ord('s'):
            filename = f"captura_colores_{int(time.time())}.png"
            cv2.imwrite(filename, frame)
            print(f"✓ Imagen guardada: {filename}")
            
        elif key == ord('v'):
            voice_enabled = not voice_enabled
            status = "activada" if voice_enabled else "desactivada"
            print(f"Voz {status}")
            
        elif key == ord('h'):
            show_help = not show_help
            
        elif key == ord('c'):
            print("\n" * 50)
    
    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        detect_colors_camera()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
