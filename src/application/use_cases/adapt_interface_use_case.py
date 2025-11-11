"""
Caso de Uso: Adaptar Interfaz - Capa de Aplicación
Encapsula la lógica para adaptar la interfaz según el tipo de discapacidad
"""

from typing import Dict, Tuple
from ...domain.entities.student import Student


class AdaptInterfaceUseCase:
    """
    Caso de uso para adaptar la interfaz según las necesidades del estudiante.

    Este caso de uso encapsula la lógica de negocio para
    personalizar la interfaz visual y auditiva según el tipo de discapacidad.
    """

    def execute(self, student: Student) -> Dict[str, any]:
        """
        Ejecuta la adaptación de la interfaz.

        Args:
            student: Entidad Student con información del estudiante

        Returns:
            dict: Configuración de interfaz adaptada
        """
        config = self._get_base_config()

        if student.discapacidad == 'visual':
            config.update(self._adapt_for_visual())
        elif student.discapacidad == 'auditiva':
            config.update(self._adapt_for_auditory())
        elif student.discapacidad == 'cognitiva':
            config.update(self._adapt_for_cognitive())
        elif student.discapacidad == 'lenguaje':
            config.update(self._adapt_for_language())
        elif student.discapacidad == 'multiple':
            config.update(self._adapt_for_multiple())

        return config

    def _get_base_config(self) -> Dict[str, any]:
        """Configuración base de la interfaz"""
        return {
            'font_scale': 0.9,
            'thickness': 2,
            'text_color': (255, 255, 255),
            'use_voice': True,
            'voice_rate': 150,
            'simplified_ui': False,
            'high_contrast': False
        }

    def _adapt_for_visual(self) -> Dict[str, any]:
        """Adaptaciones para baja visión"""
        return {
            'font_scale': 1.2,  # Texto 33% más grande
            'thickness': 3,     # Líneas más gruesas
            'text_color': (0, 255, 255),  # Amarillo brillante
            'high_contrast': True,
            'voice_rate': 130   # Voz más lenta
        }

    def _adapt_for_auditory(self) -> Dict[str, any]:
        """Adaptaciones para discapacidad auditiva"""
        return {
            'use_voice': False,  # Sin retroalimentación de voz
            'font_scale': 1.1,   # Texto ligeramente más grande
            'thickness': 2,
            'visual_feedback_enhanced': True
        }

    def _adapt_for_cognitive(self) -> Dict[str, any]:
        """Adaptaciones para discapacidad cognitiva"""
        return {
            'font_scale': 1.0,
            'thickness': 2,
            'simplified_ui': True,  # Interfaz más simple
            'voice_rate': 120,      # Voz más lenta
            'clear_icons': True
        }

    def _adapt_for_language(self) -> Dict[str, any]:
        """Adaptaciones para trastornos del lenguaje"""
        return {
            'font_scale': 1.0,
            'thickness': 2,
            'voice_rate': 120,           # Voz más lenta
            'detailed_descriptions': True # Descripciones más detalladas
        }

    def _adapt_for_multiple(self) -> Dict[str, any]:
        """Adaptaciones para discapacidad múltiple"""
        return {
            'font_scale': 1.2,
            'thickness': 3,
            'text_color': (0, 255, 255),
            'simplified_ui': True,
            'high_contrast': True,
            'voice_rate': 120
        }

    def should_use_voice(self, student: Student) -> bool:
        """Determina si se debe usar retroalimentación por voz"""
        return student.requiere_voz

    def get_text_size(self, student: Student) -> float:
        """Obtiene el tamaño de texto apropiado"""
        config = self.execute(student)
        return config['font_scale']
