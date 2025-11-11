"""
Servicio de Feedback - Capa de Aplicación
Proporciona retroalimentación educativa al estudiante
"""

import random
from typing import List
from ...domain.entities.detection_result import DetectionResult
from ...domain.entities.student import Student


class FeedbackService:
    """
    Servicio para proporcionar retroalimentación educativa.

    Este servicio encapsula la lógica de generar mensajes
    de refuerzo positivo y descripciones educativas.
    """

    def __init__(self):
        """Inicializa el servicio de feedback"""
        self._positive_messages = [
            "¡Muy bien!",
            "¡Excelente!",
            "¡Lo estás haciendo genial!",
            "¡Perfecto!",
            "¡Sigue así!",
            "¡Eres increíble!",
            "¡Qué bien lo haces!",
            "¡Fantástico!",
            "¡Increíble trabajo!",
            "¡Lo lograste!"
        ]

    def get_positive_feedback(self) -> str:
        """
        Genera un mensaje de refuerzo positivo aleatorio.

        Returns:
            str: Mensaje de refuerzo positivo
        """
        return random.choice(self._positive_messages)

    def get_detection_announcement(self, detection: DetectionResult) -> str:
        """
        Genera un anuncio educativo de la detección.

        Args:
            detection: Resultado de la detección

        Returns:
            str: Anuncio educativo
        """
        if not detection.es_valido():
            return "No puedo identificar bien el objeto. Intenta mostrarlo más cerca."

        descripcion = detection.descripcion_educativa()
        return f"Veo {descripcion}"

    def get_encouragement_message(self, intentos: int, aciertos: int) -> str:
        """
        Genera un mensaje de ánimo basado en el progreso.

        Args:
            intentos: Número de intentos
            aciertos: Número de aciertos

        Returns:
            str: Mensaje de ánimo
        """
        if intentos == 0:
            return "¡Vamos a empezar! Muéstrame objetos de colores."

        porcentaje = (aciertos / intentos) * 100 if intentos > 0 else 0

        if porcentaje >= 90:
            return "¡Eres un experto! Sigue así."
        elif porcentaje >= 70:
            return "¡Muy bien! Estás aprendiendo rápido."
        elif porcentaje >= 50:
            return "¡Buen trabajo! Continúa practicando."
        else:
            return "¡No te rindas! Cada intento te hace mejorar."

    def get_session_summary(self, intentos: int, aciertos: int, duracion_minutos: float) -> str:
        """
        Genera un resumen de la sesión.

        Args:
            intentos: Número de intentos
            aciertos: Número de aciertos
            duracion_minutos: Duración en minutos

        Returns:
            str: Resumen de la sesión
        """
        porcentaje = (aciertos / intentos) * 100 if intentos > 0 else 0

        summary = f"Has identificado {aciertos} objetos correctamente "
        summary += f"de {intentos} intentos "
        summary += f"({porcentaje:.1f}% de éxito) "
        summary += f"en {duracion_minutos:.1f} minutos. "

        if porcentaje >= 80:
            summary += "¡Excelente sesión!"
        elif porcentaje >= 60:
            summary += "¡Buen trabajo!"
        else:
            summary += "¡Sigue practicando!"

        return summary

    def get_adapted_feedback(self, student: Student, detection: DetectionResult) -> str:
        """
        Genera retroalimentación adaptada al tipo de discapacidad.

        Args:
            student: Entidad Student
            detection: Resultado de la detección

        Returns:
            str: Retroalimentación adaptada
        """
        base_announcement = self.get_detection_announcement(detection)

        if student.discapacidad == 'cognitiva':
            # Feedback más simple y directo
            return f"{detection.forma.capitalize()} {detection.color}"

        elif student.discapacidad == 'lenguaje':
            # Feedback más detallado con descripciones
            return base_announcement + ". " + self.get_positive_feedback()

        else:
            # Feedback estándar
            return base_announcement
