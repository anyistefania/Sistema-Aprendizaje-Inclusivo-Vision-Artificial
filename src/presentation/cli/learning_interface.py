"""
Interfaz de Aprendizaje - Capa de Presentación
Interfaz principal del sistema de aprendizaje inclusivo con Clean Architecture
"""

import cv2
import time
from datetime import datetime

# Importar capas de dominio
from ...domain.entities.student import Student
from ...domain.entities.detection_result import DetectionResult
from ...domain.entities.learning_session import LearningSession

# Importar capas de aplicación
from ...application.use_cases.detect_shape_use_case import DetectShapeUseCase
from ...application.use_cases.detect_color_use_case import DetectColorUseCase
from ...application.use_cases.adapt_interface_use_case import AdaptInterfaceUseCase
from ...application.use_cases.save_progress_use_case import SaveProgressUseCase
from ...application.services.feedback_service import FeedbackService

# Importar capas de infraestructura
from ...infrastructure.speech.text_to_speech_engine import TextToSpeechEngine
from ...infrastructure.camera.video_capture_handler import VideoCaptureHandler
from ...infrastructure.persistence.json_session_repository import JsonSessionRepository


class LearningInterface:
    """
    Interfaz principal del sistema de aprendizaje inclusivo.

    Esta clase orquesta todos los componentes del sistema siguiendo
    Clean Architecture.
    """

    def __init__(self, student: Student):
        """
        Inicializa la interfaz.

        Args:
            student: Entidad Student con información del estudiante
        """
        self.student = student
        self.session = LearningSession(estudiante_nombre=student.nombre)

        # Casos de uso
        self.detect_shape_uc = DetectShapeUseCase()
        self.detect_color_uc = DetectColorUseCase()
        self.adapt_interface_uc = AdaptInterfaceUseCase()

        # Repositorio y caso de uso de progreso
        repository = JsonSessionRepository()
        self.save_progress_uc = SaveProgressUseCase(repository)

        # Servicios
        self.feedback_service = FeedbackService()

        # Configuración de interfaz adaptada
        self.ui_config = self.adapt_interface_uc.execute(student)

        # Motor de voz
        self.tts = None
        if self.ui_config['use_voice']:
            self.tts = TextToSpeechEngine(rate=self.ui_config['voice_rate'])

        # Captura de video
        self.video = VideoCaptureHandler()

        print(f"\n{'='*70}")
        print(f"🎓 BIENVENIDO/A {self.student.nombre.upper()}")
        print(f"{'='*70}")
        print(f"📋 Perfil del estudiante:")
        print(f"   • Edad: {self.student.edad} años")
        print(f"   • Tipo de apoyo: {self.student.discapacidad}")
        print(f"   • Nivel actual: {self.student.nivel}")
        print(f"{'='*70}\n")

    def speak(self, text: str):
        """Sintetiza voz si está disponible"""
        if self.tts and self.tts.is_available:
            self.tts.speak(text)

    def draw_adaptive_interface(self, frame, objects, show_help=True):
        """
        Dibuja la interfaz adaptada en el frame.

        Args:
            frame: Frame de video
            objects: Lista de objetos detectados
            show_help: Si muestra la ayuda

        Returns:
            Frame con interfaz dibujada
        """
        height, width = frame.shape[:2]

        # Panel superior
        panel_height = 180
        cv2.rectangle(frame, (0, 0), (width, panel_height), (0, 0, 0), -1)

        # Configuración adaptada
        font_scale = self.ui_config['font_scale']
        thickness = self.ui_config['thickness']
        text_color = self.ui_config['text_color']

        # Título con nombre
        cv2.putText(frame, f"Hola {self.student.nombre}!",
                   (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                   font_scale, (0, 255, 255), thickness)

        # Contador de objetos
        cv2.putText(frame, f"Objetos encontrados: {len(objects)}",
                   (20, 85), cv2.FONT_HERSHEY_SIMPLEX,
                   0.8, (0, 255, 0), 2)

        # Puntuación
        if self.session.intentos > 0:
            porcentaje = int(self.session.porcentaje_aciertos)
            cv2.putText(frame, f"Aciertos: {self.session.aciertos}/{self.session.intentos} ({porcentaje}%)",
                       (20, 120), cv2.FONT_HERSHEY_SIMPLEX,
                       0.7, (255, 100, 255), 2)

        # Tiempo de sesión
        elapsed = int((datetime.now() - self.session.fecha_inicio).total_seconds())
        mins, secs = divmod(elapsed, 60)
        cv2.putText(frame, f"Tiempo: {mins:02d}:{secs:02d}",
                   (20, 155), cv2.FONT_HERSHEY_SIMPLEX,
                   0.7, (100, 255, 255), 2)

        # Ayuda en la parte inferior
        if show_help:
            help_y = height - 80
            cv2.rectangle(frame, (0, help_y - 10), (width, height), (0, 0, 0), -1)

            cv2.putText(frame, "CONTROLES:",
                       (20, help_y + 20), cv2.FONT_HERSHEY_SIMPLEX,
                       0.6, (0, 255, 255), 2)

            cv2.putText(frame, "ESPACIO: Identificar | Q: Salir | H: Ayuda",
                       (20, help_y + 50), cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, (200, 200, 200), 1)

        return frame

    def run(self):
        """Ejecuta el sistema de aprendizaje"""
        # Mensaje de bienvenida por voz
        self.speak(f"Hola {self.student.nombre}, bienvenido al sistema de aprendizaje. "
                  "Vamos a aprender juntos sobre formas y colores.")

        # Abrir cámara
        if not self.video.open():
            print("❌ Error: No se pudo abrir la cámara")
            return

        show_help = True
        min_area = 1000 if self.student.nivel == 1 else 800

        print("\n🎮 MODO DE USO:")
        print("   • El sistema detectará automáticamente formas y colores")
        print("   • Presiona ESPACIO para identificar el objeto más grande")
        print("   • Presiona H para mostrar/ocultar ayuda")
        print("   • Presiona Q para salir y guardar progreso")
        print("\n🚀 ¡Sistema listo!\n")

        self.speak("Muestra objetos de colores frente a la cámara. "
                  "Presiona la barra espaciadora cuando quieras que los identifique.")

        while True:
            ret, frame = self.video.read_frame()

            if not ret:
                print("❌ Error al capturar frame")
                break

            # Preprocesar frame
            processed = self.video.preprocess_frame(frame)
            if not processed:
                continue

            # Encontrar contornos
            contours = self.video.find_contours(processed['thresh'])

            detected_objects = []

            # Procesar cada contorno
            for contour in contours:
                area = self.detect_shape_uc.get_area(contour)

                if area < min_area:
                    continue

                # Detectar forma
                shape = self.detect_shape_uc.execute(contour)

                if shape == 'desconocido':
                    continue

                # Obtener región para detectar color
                x, y, w, h = cv2.boundingRect(contour)
                roi_hsv = processed['hsv'][max(0, y-5):min(processed['hsv'].shape[0], y+h+5),
                                          max(0, x-5):min(processed['hsv'].shape[1], x+w+5)]

                # Detectar color
                color = self.detect_color_uc.execute(roi_hsv)

                if not color:
                    continue

                # Obtener centro
                centro = self.detect_shape_uc.get_center(contour)

                # Crear resultado de detección
                detection = DetectionResult(
                    forma=shape,
                    color=color,
                    centro=centro,
                    area=area
                )

                if not detection.es_valido():
                    continue

                # Dibujar en el frame
                draw_color = self.detect_color_uc.get_color_bgr(color)

                cv2.drawContours(processed['original'], [contour], -1, draw_color, 4)
                cv2.rectangle(processed['original'], (x, y), (x + w, y + h), draw_color, 3)
                cv2.circle(processed['original'], centro, 12, (255, 255, 255), -1)
                cv2.circle(processed['original'], centro, 10, draw_color, -1)

                # Etiqueta
                label = f"{shape.upper()}"
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
                cv2.rectangle(processed['original'],
                            (x, y - label_size[1] - 20),
                            (x + label_size[0] + 10, y - 5),
                            draw_color, -1)

                text_color = (0, 0, 0) if color in ['amarillo'] else (255, 255, 255)
                cv2.putText(processed['original'], label, (x + 5, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, text_color, 2)

                detected_objects.append(detection)

            # Actualizar interfaz
            frame_with_ui = self.draw_adaptive_interface(processed['original'],
                                                         detected_objects, show_help)

            # Mostrar
            cv2.imshow("Sistema de Aprendizaje Inclusivo", frame_with_ui)

            if show_help:
                thresh_display = cv2.resize(processed['thresh'], (200, 150))
                cv2.imshow("Procesamiento (para el docente)", thresh_display)

            # Procesar teclas
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("\n📊 Finalizando sesión...")
                break

            elif key == ord(' '):  # Espaciobarra
                if detected_objects:
                    # Identificar el objeto más grande
                    largest = max(detected_objects, key=lambda x: x.area)

                    announcement = self.feedback_service.get_detection_announcement(largest)
                    print(f"\n🎯 {announcement}")
                    self.speak(announcement)

                    # Refuerzo positivo
                    time.sleep(1)
                    feedback = self.feedback_service.get_positive_feedback()
                    print(f"   {feedback}")
                    self.speak(feedback)

                    # Registrar progreso
                    self.session.registrar_acierto(largest)

                else:
                    msg = "No veo ningún objeto. Por favor, muestra un objeto de color."
                    self.speak(msg)
                    print(f"\n⚠️  {msg}")

            elif key == ord('h'):
                show_help = not show_help
                if not show_help:
                    cv2.destroyWindow("Procesamiento (para el docente)")

        # Finalizar
        self.video.release()
        cv2.destroyAllWindows()

        # Guardar progreso
        self.save_progress_uc.execute(self.session)

        # Resumen final
        print("\n" + "="*70)
        print("📊 RESUMEN DE LA SESIÓN")
        print("="*70)
        print(f"   Estudiante: {self.student.nombre}")
        print(f"   Duración: {int(self.session.duracion_minutos)} minutos")
        print(f"   Objetos identificados: {self.session.aciertos}")
        print(f"   Intentos totales: {self.session.intentos}")

        if self.session.intentos > 0:
            print(f"   Porcentaje de éxito: {self.session.porcentaje_aciertos:.1f}%")

        print("="*70)

        # Mensaje de despedida
        summary = self.feedback_service.get_session_summary(
            self.session.intentos,
            self.session.aciertos,
            self.session.duracion_minutos
        )
        despedida = f"{self.student.nombre}, {summary} Hasta la próxima sesión."
        self.speak(despedida)
        print(f"\n👋 {despedida}\n")


def collect_student_info() -> Student:
    """Recopila información del estudiante"""
    print("\n" + "="*70)
    print("   SISTEMA DE APRENDIZAJE INCLUSIVO CON VISIÓN ARTIFICIAL")
    print("="*70)
    print("\n📝 CONFIGURACIÓN DEL ESTUDIANTE\n")

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

    return Student(
        nombre=nombre,
        edad=edad,
        discapacidad=discapacidad,
        nivel=nivel
    )


def main():
    """Función principal"""
    try:
        # Recopilar información del estudiante
        student = collect_student_info()

        # Crear y ejecutar interfaz
        interface = LearningInterface(student)
        interface.run()

    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
