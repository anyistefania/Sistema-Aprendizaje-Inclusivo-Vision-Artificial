"""
Sistema de Aprendizaje Inclusivo con Visión Artificial
Proyecto: Reconocimiento de Objetos Didácticos en Educación Especial
Autor: Semillero de Investigación
Fecha: Noviembre 2025

Sistema especializado para estudiantes con necesidades educativas especiales:
- Retroalimentación multimodal (visual, auditiva, textual)
- Adaptación según tipo de discapacidad
- Actividades didácticas progresivas
- Seguimiento del progreso del estudiante
"""

import cv2
import numpy as np
import pyttsx3
import time
import json
from datetime import datetime
from collections import Counter


class AdaptiveLearningSystem:
    """
    Sistema adaptativo de aprendizaje para educación especial.
    
    Características:
    - Retroalimentación personalizada
    - Niveles de dificultad progresivos
    - Refuerzo positivo constante
    - Registro de progreso
    """
    
    def __init__(self, student_profile):
        """
        Inicializa el sistema con el perfil del estudiante.
        
        Args:
            student_profile: dict con información del estudiante
                - nombre: str
                - edad: int
                - discapacidad: str ('visual', 'auditiva', 'cognitiva', 'lenguaje', 'multiple')
                - nivel: int (1-5)
        """
        self.student = student_profile
        self.session_start = datetime.now()
        self.progress = {
            'aciertos': 0,
            'intentos': 0,
            'tiempo_total': 0,
            'objetos_reconocidos': []
        }
        
        # Configurar sistema de voz
        try:
            self.engine = pyttsx3.init()
            # Voz más lenta para mejor comprensión
            self.engine.setProperty('rate', 130)
            self.engine.setProperty('volume', 1.0)
            
            # Intentar usar una voz femenina (más cálida)
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'spanish' in voice.name.lower() or 'spanish' in voice.languages[0].lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        except Exception as e:
            print(f"⚠️  Advertencia: No se pudo inicializar el motor de voz: {e}")
            self.engine = None
        
        # Colores en HSV optimizados para mejor detección
        self.color_ranges = {
            'rojo': {
                'ranges': [
                    {'lower': np.array([0, 120, 70]), 'upper': np.array([10, 255, 255])},
                    {'lower': np.array([170, 120, 70]), 'upper': np.array([180, 255, 255])}
                ],
                'bgr': (0, 0, 255),
                'descripcion': 'rojo como una manzana'
            },
            'azul': {
                'ranges': [{'lower': np.array([100, 150, 50]), 'upper': np.array([130, 255, 255])}],
                'bgr': (255, 0, 0),
                'descripcion': 'azul como el cielo'
            },
            'verde': {
                'ranges': [{'lower': np.array([40, 40, 40]), 'upper': np.array([80, 255, 255])}],
                'bgr': (0, 255, 0),
                'descripcion': 'verde como las plantas'
            },
            'amarillo': {
                'ranges': [{'lower': np.array([20, 100, 100]), 'upper': np.array([35, 255, 255])}],
                'bgr': (0, 255, 255),
                'descripcion': 'amarillo como el sol'
            },
            'naranja': {
                'ranges': [{'lower': np.array([10, 100, 100]), 'upper': np.array([20, 255, 255])}],
                'bgr': (0, 165, 255),
                'descripcion': 'naranja como la fruta'
            },
            'morado': {
                'ranges': [{'lower': np.array([130, 50, 50]), 'upper': np.array([160, 255, 255])}],
                'bgr': (255, 0, 255),
                'descripcion': 'morado como las uvas'
            }
        }
        
        # Formas geométricas
        self.shapes = {
            'circulo': 'círculo, como una pelota',
            'triangulo': 'triángulo, como un tejado',
            'cuadrado': 'cuadrado, como una ventana',
            'rectangulo': 'rectángulo, como una puerta',
            'pentagono': 'pentágono, tiene cinco lados'
        }
        
        print(f"\n{'='*70}")
        print(f"🎓 BIENVENIDO/A {self.student['nombre'].upper()}")
        print(f"{'='*70}")
        print(f"📋 Perfil del estudiante:")
        print(f"   • Edad: {self.student['edad']} años")
        print(f"   • Tipo de apoyo: {self.student['discapacidad']}")
        print(f"   • Nivel actual: {self.student['nivel']}")
        print(f"{'='*70}\n")
    
    def speak(self, text, wait=True):
        """
        Síntesis de voz adaptada para educación especial.
        
        Args:
            text: Texto a sintetizar
            wait: Si True, espera a que termine de hablar
        """
        if self.engine and self.student['discapacidad'] != 'auditiva':
            try:
                self.engine.say(text)
                if wait:
                    self.engine.runAndWait()
            except:
                pass
    
    def detect_shape(self, contour):
        """
        Detecta la forma geométrica con descripciones educativas.
        """
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        vertices = len(approx)
        
        if vertices == 3:
            return 'triangulo'
        elif vertices == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            return 'cuadrado' if 0.85 <= aspect_ratio <= 1.15 else 'rectangulo'
        elif vertices == 5:
            return 'pentagono'
        else:
            area = cv2.contourArea(contour)
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            if circularity > 0.7:
                return 'circulo'
        
        return 'desconocido'
    
    def detect_color(self, hsv_roi):
        """
        Detecta el color predominante en una región.
        """
        max_pixels = 0
        detected_color = None
        
        for color_name, color_data in self.color_ranges.items():
            color_pixels = 0
            
            for range_data in color_data['ranges']:
                mask = cv2.inRange(hsv_roi, range_data['lower'], range_data['upper'])
                color_pixels += cv2.countNonZero(mask)
            
            if color_pixels > max_pixels:
                max_pixels = color_pixels
                detected_color = color_name
        
        # Requiere al menos 15% del área
        total_pixels = hsv_roi.shape[0] * hsv_roi.shape[1]
        if max_pixels < total_pixels * 0.15:
            return None
        
        return detected_color
    
    def give_positive_feedback(self):
        """
        Proporciona refuerzo positivo constante.
        """
        feedbacks = [
            "¡Muy bien!",
            "¡Excelente!",
            "¡Lo estás haciendo genial!",
            "¡Perfecto!",
            "¡Sigue así!",
            "¡Eres increíble!",
            "¡Qué bien lo haces!"
        ]
        import random
        feedback = random.choice(feedbacks)
        self.speak(feedback, wait=False)
        return feedback
    
    def adaptive_interface(self, frame, objects, show_detailed_help=True):
        """
        Interfaz adaptada según el tipo de discapacidad.
        
        Args:
            frame: Frame de video
            objects: Lista de objetos detectados
            show_detailed_help: Si muestra ayuda detallada
        """
        height, width = frame.shape[:2]
        
        # Fondo para panel de información (más grande para mejor visibilidad)
        panel_height = 180
        cv2.rectangle(frame, (0, 0), (width, panel_height), (0, 0, 0), -1)
        
        # Adaptaciones según discapacidad
        if self.student['discapacidad'] == 'visual':
            # Texto más grande, mayor contraste
            font_scale = 1.2
            thickness = 3
            text_color = (0, 255, 255)  # Amarillo brillante
            
        elif self.student['discapacidad'] == 'cognitiva':
            # Interfaz más simple, iconos claros
            font_scale = 1.0
            thickness = 2
            text_color = (255, 255, 255)
            
        else:
            # Configuración estándar
            font_scale = 0.9
            thickness = 2
            text_color = (255, 255, 255)
        
        # Título con nombre del estudiante
        cv2.putText(frame, f"Hola {self.student['nombre']}!", 
                   (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale, (0, 255, 255), thickness)
        
        # Contador de objetos con emoji
        cv2.putText(frame, f"Objetos encontrados: {len(objects)}", 
                   (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.8, (0, 255, 0), 2)
        
        # Puntuación
        if self.progress['intentos'] > 0:
            porcentaje = int((self.progress['aciertos'] / self.progress['intentos']) * 100)
            cv2.putText(frame, f"Aciertos: {self.progress['aciertos']}/{self.progress['intentos']} ({porcentaje}%)", 
                       (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (255, 100, 255), 2)
        
        # Tiempo de sesión
        elapsed = int((datetime.now() - self.session_start).total_seconds())
        mins, secs = divmod(elapsed, 60)
        cv2.putText(frame, f"Tiempo: {mins:02d}:{secs:02d}", 
                   (20, 155), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (100, 255, 255), 2)
        
        # Ayuda adaptativa en la parte inferior
        if show_detailed_help:
            help_y = height - 80
            cv2.rectangle(frame, (0, help_y - 10), (width, height), (0, 0, 0), -1)
            
            cv2.putText(frame, "CONTROLES:", 
                       (20, help_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.6, (0, 255, 255), 2)
            
            cv2.putText(frame, "ESPACIO: Identificar objeto | Q: Salir | H: Ayuda", 
                       (20, help_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (200, 200, 200), 1)
        
        return frame
    
    def save_progress(self):
        """
        Guarda el progreso del estudiante en un archivo JSON.
        """
        session_data = {
            'fecha': self.session_start.isoformat(),
            'estudiante': self.student['nombre'],
            'duracion_minutos': (datetime.now() - self.session_start).total_seconds() / 60,
            'estadisticas': self.progress,
            'nivel': self.student['nivel']
        }
        
        filename = f"progreso_{self.student['nombre']}_{self.session_start.strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=4, ensure_ascii=False)
            print(f"\n✅ Progreso guardado en: {filename}")
        except Exception as e:
            print(f"\n⚠️  Error al guardar progreso: {e}")


def run_inclusive_learning_system():
    """
    Ejecuta el sistema de aprendizaje inclusivo completo.
    """
    print("\n" + "="*70)
    print("   SISTEMA DE APRENDIZAJE INCLUSIVO CON VISIÓN ARTIFICIAL")
    print("="*70)
    print("\n📝 CONFIGURACIÓN DEL ESTUDIANTE\n")
    
    # Recopilar información del estudiante
    nombre = input("Nombre del estudiante: ").strip() or "Estudiante"
    
    try:
        edad = int(input("Edad: ").strip() or "8")
    except:
        edad = 8
    
    print("\nTipo de apoyo necesario:")
    print("  1. Baja visión")
    print("  2. Discapacidad auditiva")
    print("  3. Discapacidad cognitiva")
    print("  4. Trastornos del lenguaje")
    print("  5. Discapacidad múltiple")
    
    tipo_opcion = input("\nSeleccione (1-5): ").strip() or "3"
    tipos = {
        '1': 'visual',
        '2': 'auditiva',
        '3': 'cognitiva',
        '4': 'lenguaje',
        '5': 'multiple'
    }
    discapacidad = tipos.get(tipo_opcion, 'cognitiva')
    
    print("\nNivel de dificultad:")
    print("  1. Básico (formas y colores primarios)")
    print("  2. Intermedio (más formas y colores)")
    print("  3. Avanzado (combinaciones complejas)")
    
    nivel = int(input("\nSeleccione (1-3): ").strip() or "1")
    
    # Crear perfil del estudiante
    student_profile = {
        'nombre': nombre,
        'edad': edad,
        'discapacidad': discapacidad,
        'nivel': nivel
    }
    
    # Inicializar sistema
    system = AdaptiveLearningSystem(student_profile)
    
    # Mensaje de bienvenida por voz
    system.speak(f"Hola {nombre}, bienvenido al sistema de aprendizaje. Vamos a aprender juntos sobre formas y colores.")
    
    # Inicializar cámara
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: No se pudo abrir la cámara")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    
    # Variables de control
    show_help = True
    last_objects = []
    last_announcement_time = 0
    announcement_cooldown = 4.0  # Más tiempo entre anuncios
    learning_mode = True
    
    print("\n🎮 MODO DE USO:")
    print("   • El sistema detectará automáticamente formas y colores")
    print("   • Presiona ESPACIO para que el sistema identifique el objeto más grande")
    print("   • Presiona H para mostrar/ocultar ayuda")
    print("   • Presiona Q para salir y guardar progreso")
    print("\n🚀 ¡Sistema listo! Presiona Q para salir.\n")
    
    system.speak("Muestra objetos de colores frente a la cámara. Presiona la barra espaciadora cuando quieras que los identifique.")
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Error al capturar frame")
            break
        
        frame = cv2.flip(frame, 1)
        
        # Procesamiento de imagen
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        # Umbralización adaptativa
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 11, 2)
        
        # Operaciones morfológicas para limpiar
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 
                                      cv2.CHAIN_APPROX_SIMPLE)
        
        detected_objects = []
        
        # Procesar contornos
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filtro de área según nivel
            min_area = 1000 if nivel == 1 else 800
            if area < min_area:
                continue
            
            # Calcular centro
            M = cv2.moments(contour)
            if M["m00"] == 0:
                continue
            
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            
            # Obtener bounding box
            x, y, w, h = cv2.boundingRect(contour)
            
            # Detectar forma
            shape = system.detect_shape(contour)
            
            # Detectar color
            roi_hsv = hsv[max(0, y-5):min(hsv.shape[0], y+h+5), 
                         max(0, x-5):min(hsv.shape[1], x+w+5)]
            color = system.detect_color(roi_hsv)
            
            if shape == 'desconocido' or color is None:
                continue
            
            # Color para visualización
            draw_color = system.color_ranges[color]['bgr']
            
            # Dibujar contorno grueso para mejor visibilidad
            cv2.drawContours(frame, [contour], -1, draw_color, 4)
            
            # Dibujar rectángulo
            cv2.rectangle(frame, (x, y), (x + w, y + h), draw_color, 3)
            
            # Dibujar centro con círculo grande
            cv2.circle(frame, (cX, cY), 12, (255, 255, 255), -1)
            cv2.circle(frame, (cX, cY), 10, draw_color, -1)
            
            # Etiqueta grande y clara
            shape_name = system.shapes[shape].split(',')[0]
            label = f"{shape_name.upper()}"
            
            # Fondo para la etiqueta
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
            cv2.rectangle(frame, 
                         (x, y - label_size[1] - 20),
                         (x + label_size[0] + 10, y - 5),
                         draw_color, -1)
            
            # Texto de la forma
            text_color = (0, 0, 0) if color in ['amarillo'] else (255, 255, 255)
            cv2.putText(frame, label, (x + 5, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, text_color, 2)
            
            # Etiqueta de color debajo
            color_label = color.upper()
            cv2.rectangle(frame, 
                         (x, y + h + 5),
                         (x + label_size[0] + 10, y + h + label_size[1] + 20),
                         draw_color, -1)
            
            cv2.putText(frame, color_label, (x + 5, y + h + label_size[1] + 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, text_color, 2)
            
            detected_objects.append({
                'forma': shape,
                'color': color,
                'centro': (cX, cY),
                'area': area,
                'posicion': (x, y, w, h)
            })
        
        # Actualizar interfaz adaptativa
        frame = system.adaptive_interface(frame, detected_objects, show_help)
        
        # Mostrar ventanas
        cv2.imshow("Sistema de Aprendizaje Inclusivo", frame)
        
        # Mostrar procesamiento (útil para docentes)
        if show_help:
            thresh_display = cv2.resize(thresh, (200, 150))
            cv2.imshow("Procesamiento (para el docente)", thresh_display)
        
        # Procesar teclas
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\n📊 Finalizando sesión...")
            break
        
        elif key == ord(' '):  # Barra espaciadora
            if detected_objects:
                # Identificar el objeto más grande
                largest = max(detected_objects, key=lambda x: x['area'])
                shape = largest['forma']
                color = largest['color']
                
                # Descripción completa
                shape_desc = system.shapes[shape]
                color_desc = system.color_ranges[color]['descripcion']
                
                announcement = f"Veo un {shape_desc} de color {color_desc}"
                
                print(f"\n🎯 {announcement}")
                system.speak(announcement)
                
                # Refuerzo positivo
                time.sleep(1)
                feedback = system.give_positive_feedback()
                print(f"   {feedback}")
                
                # Registrar progreso
                system.progress['aciertos'] += 1
                system.progress['intentos'] += 1
                system.progress['objetos_reconocidos'].append(f"{shape}_{color}")
                
                # Mostrar mensaje en pantalla
                x, y, w, h = largest['posicion']
                cv2.putText(frame, feedback, (x, y - 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                cv2.imshow("Sistema de Aprendizaje Inclusivo", frame)
                cv2.waitKey(1500)  # Mostrar feedback por 1.5 segundos
            else:
                system.speak("No veo ningún objeto. Por favor, muestra un objeto de color.")
                print("\n⚠️  No se detectaron objetos")
        
        elif key == ord('h'):
            show_help = not show_help
            if not show_help:
                cv2.destroyWindow("Procesamiento (para el docente)")
        
        elif key == ord('s'):
            filename = f"sesion_{nombre}_{int(time.time())}.png"
            cv2.imwrite(filename, frame)
            print(f"📸 Captura guardada: {filename}")
    
    # Finalizar sesión
    cap.release()
    cv2.destroyAllWindows()
    
    # Guardar progreso
    system.save_progress()
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN DE LA SESIÓN")
    print("="*70)
    print(f"   Estudiante: {nombre}")
    print(f"   Duración: {int((datetime.now() - system.session_start).total_seconds() / 60)} minutos")
    print(f"   Objetos identificados: {system.progress['aciertos']}")
    print(f"   Intentos totales: {system.progress['intentos']}")
    
    if system.progress['intentos'] > 0:
        porcentaje = (system.progress['aciertos'] / system.progress['intentos']) * 100
        print(f"   Porcentaje de éxito: {porcentaje:.1f}%")
    
    print("="*70)
    
    # Mensaje de despedida
    despedida = f"Muy bien {nombre}, has hecho un excelente trabajo. Hasta la próxima sesión."
    system.speak(despedida)
    print(f"\n👋 {despedida}\n")


if __name__ == "__main__":
    try:
        run_inclusive_learning_system()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
