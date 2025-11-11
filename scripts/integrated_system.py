"""
Sistema Integrado de Detección de Formas y Colores
Proyecto: Entornos de Aprendizaje Inclusivos con Visión Artificial
Autor: Semillero de Investigación
Fecha: Noviembre 2025

Sistema completo que detecta simultáneamente formas geométricas
y colores en tiempo real usando la cámara web.
"""

import cv2
import numpy as np
import imutils
import pyttsx3
import time
from collections import Counter


class IntegratedDetector:
    """
    Detector integrado que combina reconocimiento de formas y colores.
    """
    
    def __init__(self, use_voice=True):
        """
        Inicializa el detector integrado.
        
        Args:
            use_voice: Si True, activa retroalimentación por voz
        """
        # Rangos de colores en HSV
        self.color_ranges = {
            'rojo1': {'lower': np.array([0, 100, 100]), 'upper': np.array([10, 255, 255]), 
                     'bgr': (0, 0, 255), 'name': 'rojo'},
            'rojo2': {'lower': np.array([170, 100, 100]), 'upper': np.array([180, 255, 255]), 
                     'bgr': (0, 0, 255), 'name': 'rojo'},
            'azul': {'lower': np.array([100, 150, 50]), 'upper': np.array([130, 255, 255]), 
                    'bgr': (255, 0, 0), 'name': 'azul'},
            'verde': {'lower': np.array([40, 50, 50]), 'upper': np.array([80, 255, 255]), 
                     'bgr': (0, 255, 0), 'name': 'verde'},
            'amarillo': {'lower': np.array([20, 100, 100]), 'upper': np.array([35, 255, 255]), 
                        'bgr': (0, 255, 255), 'name': 'amarillo'},
            'naranja': {'lower': np.array([10, 100, 100]), 'upper': np.array([20, 255, 255]), 
                       'bgr': (0, 165, 255), 'name': 'naranja'},
            'morado': {'lower': np.array([130, 50, 50]), 'upper': np.array([170, 255, 255]), 
                      'bgr': (255, 0, 255), 'name': 'morado'},
            'rosa': {'lower': np.array([145, 50, 50]), 'upper': np.array([170, 255, 255]), 
                    'bgr': (203, 192, 255), 'name': 'rosa'},
        }
        
        # Inicializar motor de voz
        self.use_voice = use_voice
        if use_voice:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 150)
                self.engine.setProperty('volume', 0.9)
            except Exception as e:
                print(f"Advertencia: No se pudo inicializar voz: {e}")
                self.use_voice = False
        
        self.last_announcement = ""
        self.last_announcement_time = 0
        self.announcement_cooldown = 3.0
    
    def detect_shape(self, contour):
        """
        Detecta la forma geométrica de un contorno.
        
        Args:
            contour: Contorno de OpenCV
            
        Returns:
            str: Nombre de la forma
        """
        shape = "desconocido"
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        vertices = len(approx)
        
        if vertices == 3:
            shape = "triangulo"
        elif vertices == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            shape = "cuadrado" if 0.90 <= aspect_ratio <= 1.10 else "rectangulo"
        elif vertices == 5:
            shape = "pentagono"
        elif vertices == 6:
            shape = "hexagono"
        else:
            area = cv2.contourArea(contour)
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            if circularity > 0.75:
                shape = "circulo"
        
        return shape
    
    def detect_color(self, hsv_roi):
        """
        Detecta el color predominante en una región HSV.
        
        Args:
            hsv_roi: Región de interés en espacio HSV
            
        Returns:
            str: Nombre del color detectado
        """
        max_pixels = 0
        detected_color = "desconocido"
        
        for color_key, color_data in self.color_ranges.items():
            mask = cv2.inRange(hsv_roi, color_data['lower'], color_data['upper'])
            pixels = cv2.countNonZero(mask)
            
            if pixels > max_pixels:
                max_pixels = pixels
                detected_color = color_data['name']
        
        # Requiere al menos 10% de píxeles del color
        total_pixels = hsv_roi.shape[0] * hsv_roi.shape[1]
        if max_pixels < total_pixels * 0.1:
            detected_color = "sin color"
        
        return detected_color
    
    def get_color_bgr(self, color_name):
        """Obtiene el valor BGR de un color."""
        for color_data in self.color_ranges.values():
            if color_data['name'] == color_name:
                return color_data['bgr']
        return (200, 200, 200)
    
    def speak(self, text):
        """Sintetiza voz para retroalimentación auditiva."""
        if self.use_voice:
            current_time = time.time()
            if text != self.last_announcement or \
               (current_time - self.last_announcement_time) > self.announcement_cooldown:
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                    self.last_announcement = text
                    self.last_announcement_time = current_time
                except:
                    pass


def run_integrated_system():
    """
    Ejecuta el sistema integrado de detección en tiempo real.
    
    Controles:
    - 'q': Salir
    - 's': Capturar imagen
    - 'v': Activar/desactivar voz
    - 'f': Congelar frame
    - 'h': Mostrar/ocultar ayuda
    - '1': Modo formas
    - '2': Modo colores
    - '3': Modo integrado
    """
    # Inicializar cámara
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: No se pudo abrir la cámara")
        return
    
    # Configurar resolución
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    
    # Inicializar detector
    detector = IntegratedDetector(use_voice=True)
    
    # Variables de control
    voice_enabled = True
    frozen = False
    frozen_frame = None
    show_help = True
    detection_mode = 3  # 1=formas, 2=colores, 3=integrado
    
    # Estadísticas
    object_count = 0
    fps_list = []
    
    print("=" * 70)
    print("   SISTEMA INTEGRADO DE RECONOCIMIENTO DE FORMAS Y COLORES")
    print("=" * 70)
    print("\n📷 Cámara iniciada correctamente")
    print("\n🎮 CONTROLES:")
    print("   Q - Salir del programa")
    print("   S - Capturar y guardar imagen")
    print("   V - Activar/Desactivar voz")
    print("   F - Congelar/Descongelar frame")
    print("   H - Mostrar/Ocultar ayuda")
    print("   1 - Modo solo formas")
    print("   2 - Modo solo colores")
    print("   3 - Modo integrado (formas + colores)")
    print("=" * 70)
    print("\n🚀 Sistema listo. Presiona 'Q' para salir.\n")
    
    while True:
        if not frozen:
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Error al leer frame")
                break
            
            # Voltear para efecto espejo
            frame = cv2.flip(frame, 1)
            frozen_frame = frame.copy()
        else:
            frame = frozen_frame.copy()
        
        # Medición de FPS
        start_time = time.time()
        
        # Preprocesamiento
        blurred = cv2.GaussianBlur(frame, (7, 7), 0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        # Umbralización
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 11, 2)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 
                                      cv2.CHAIN_APPROX_SIMPLE)
        
        # Lista de objetos detectados
        detected_objects = []
        object_count = 0
        
        # Procesar cada contorno
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filtrar contornos pequeños
            if area < 800:
                continue
            
            object_count += 1
            
            # Calcular centro
            M = cv2.moments(contour)
            if M["m00"] == 0:
                continue
            
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            
            # Obtener bounding box
            x, y, w, h = cv2.boundingRect(contour)
            
            shape = "?"
            color = "?"
            
            # Detectar forma (modos 1 y 3)
            if detection_mode in [1, 3]:
                shape = detector.detect_shape(contour)
            
            # Detectar color (modos 2 y 3)
            if detection_mode in [2, 3]:
                # Extraer ROI en HSV
                roi_hsv = hsv[y:y+h, x:x+w]
                color = detector.detect_color(roi_hsv)
            
            # Color para dibujar
            if color != "?" and color != "sin color":
                draw_color = detector.get_color_bgr(color)
            else:
                draw_color = (0, 255, 0)
            
            # Dibujar contorno
            cv2.drawContours(frame, [contour], -1, draw_color, 3)
            
            # Dibujar rectángulo
            cv2.rectangle(frame, (x, y), (x + w, y + h), draw_color, 2)
            
            # Dibujar centro
            cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
            cv2.circle(frame, (cX, cY), 5, draw_color, -1)
            
            # Crear etiqueta
            if detection_mode == 1:
                label = f"{shape}"
            elif detection_mode == 2:
                label = f"{color}"
            else:
                label = f"{shape} {color}"
            
            # Fondo para texto
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, 
                         (x, y - label_size[1] - 10),
                         (x + label_size[0] + 10, y),
                         draw_color, -1)
            
            # Texto
            text_color = (0, 0, 0) if color in ['amarillo', 'blanco'] else (255, 255, 255)
            cv2.putText(frame, label, (x + 5, y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
            
            # Guardar objeto detectado
            detected_objects.append({
                'forma': shape,
                'color': color,
                'centro': (cX, cY),
                'area': area
            })
        
        # Calcular FPS
        fps = 1.0 / (time.time() - start_time)
        fps_list.append(fps)
        if len(fps_list) > 30:
            fps_list.pop(0)
        avg_fps = sum(fps_list) / len(fps_list)
        
        # Panel de información
        panel_height = 140
        cv2.rectangle(frame, (0, 0), (800, panel_height), (0, 0, 0), -1)
        
        # Título
        cv2.putText(frame, "SISTEMA DE RECONOCIMIENTO", (10, 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Modo actual
        modes = {1: "FORMAS", 2: "COLORES", 3: "INTEGRADO"}
        mode_text = f"Modo: {modes[detection_mode]}"
        cv2.putText(frame, mode_text, (10, 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Objetos detectados
        cv2.putText(frame, f"Objetos: {object_count}", (10, 85),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # FPS
        cv2.putText(frame, f"FPS: {avg_fps:.1f}", (10, 115),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 100, 100), 2)
        
        # Estado voz
        voice_status = "VOZ: ON" if voice_enabled else "VOZ: OFF"
        voice_color = (0, 255, 0) if voice_enabled else (0, 0, 255)
        cv2.putText(frame, voice_status, (250, 55),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, voice_color, 2)
        
        # Estado congelado
        if frozen:
            cv2.putText(frame, "CONGELADO", (250, 85),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
        
        # Ayuda
        if show_help:
            help_text = "Q:Salir | S:Guardar | V:Voz | F:Congelar | 1-3:Modos | H:Ayuda"
            cv2.putText(frame, help_text, (10, frame.shape[0] - 15),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Anuncio por voz
        if voice_enabled and object_count > 0 and not frozen:
            # Anunciar el objeto más grande
            if detected_objects:
                largest = max(detected_objects, key=lambda x: x['area'])
                announcement = f"{largest['forma']} {largest['color']}"
                detector.speak(announcement)
        
        # Mostrar frame
        cv2.imshow("Sistema Integrado - Vision Artificial", frame)
        
        # Mostrar umbralización en ventana pequeña
        thresh_small = cv2.resize(thresh, (200, 150))
        cv2.imshow("Procesamiento", thresh_small)
        
        # Procesar teclas
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\n👋 Cerrando sistema...")
            break
            
        elif key == ord('s'):
            filename = f"captura_{int(time.time())}.png"
            cv2.imwrite(filename, frame)
            print(f"✅ Imagen guardada: {filename}")
            
        elif key == ord('v'):
            voice_enabled = not voice_enabled
            detector.use_voice = voice_enabled
            status = "activada 🔊" if voice_enabled else "desactivada 🔇"
            print(f"Voz {status}")
            
        elif key == ord('f'):
            frozen = not frozen
            status = "⏸️  Congelado" if frozen else "▶️  Reanudado"
            print(status)
            
        elif key == ord('h'):
            show_help = not show_help
            
        elif key == ord('1'):
            detection_mode = 1
            print("📐 Modo: Solo FORMAS")
            
        elif key == ord('2'):
            detection_mode = 2
            print("🎨 Modo: Solo COLORES")
            
        elif key == ord('3'):
            detection_mode = 3
            print("🎯 Modo: INTEGRADO (formas + colores)")
    
    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n" + "=" * 70)
    print("📊 ESTADÍSTICAS FINALES")
    print("=" * 70)
    print(f"   FPS promedio: {avg_fps:.2f}")
    print(f"   Último conteo de objetos: {object_count}")
    print("=" * 70)
    print("\n✨ ¡Gracias por usar el sistema!")


if __name__ == "__main__":
    try:
        run_integrated_system()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
