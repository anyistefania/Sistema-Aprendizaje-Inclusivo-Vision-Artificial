"""
Caso de Uso: Detectar Color - Capa de Aplicación
Encapsula la lógica para detectar colores en imágenes
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple


class DetectColorUseCase:
    """
    Caso de uso para detectar colores en regiones de imagen.

    Este caso de uso encapsula la lógica de negocio para
    identificar colores usando el espacio HSV.
    """

    def __init__(self):
        """Inicializa el caso de uso con rangos de colores"""
        self.color_ranges = {
            'rojo': {
                'ranges': [
                    {'lower': np.array([0, 120, 70]), 'upper': np.array([10, 255, 255])},
                    {'lower': np.array([170, 120, 70]), 'upper': np.array([180, 255, 255])}
                ]
            },
            'azul': {
                'ranges': [{'lower': np.array([100, 150, 50]), 'upper': np.array([130, 255, 255])}]
            },
            'verde': {
                'ranges': [{'lower': np.array([40, 40, 40]), 'upper': np.array([80, 255, 255])}]
            },
            'amarillo': {
                'ranges': [{'lower': np.array([20, 100, 100]), 'upper': np.array([35, 255, 255])}]
            },
            'naranja': {
                'ranges': [{'lower': np.array([10, 100, 100]), 'upper': np.array([20, 255, 255])}]
            },
            'morado': {
                'ranges': [{'lower': np.array([130, 50, 50]), 'upper': np.array([160, 255, 255])}]
            }
        }

    def execute(self, hsv_roi: np.ndarray, umbral_minimo: float = 0.15) -> str:
        """
        Ejecuta la detección de color.

        Args:
            hsv_roi: Región de interés en espacio HSV
            umbral_minimo: Porcentaje mínimo de píxeles para considerar un color

        Returns:
            str: Nombre del color detectado o None si no se detecta ninguno
        """
        if hsv_roi is None or hsv_roi.size == 0:
            return None

        max_pixels = 0
        detected_color = None
        total_pixels = hsv_roi.shape[0] * hsv_roi.shape[1]

        for color_name, color_data in self.color_ranges.items():
            color_pixels = 0

            # Procesar cada rango del color (algunos colores tienen múltiples rangos)
            for range_data in color_data['ranges']:
                mask = cv2.inRange(hsv_roi, range_data['lower'], range_data['upper'])
                color_pixels += cv2.countNonZero(mask)

            if color_pixels > max_pixels:
                max_pixels = color_pixels
                detected_color = color_name

        # Verificar que cumple con el umbral mínimo
        if max_pixels < total_pixels * umbral_minimo:
            return None

        return detected_color

    def get_color_bgr(self, color_name: str) -> Tuple[int, int, int]:
        """
        Obtiene el valor BGR representativo de un color.

        Args:
            color_name: Nombre del color

        Returns:
            tuple: Valor BGR
        """
        colors_bgr = {
            'rojo': (0, 0, 255),
            'azul': (255, 0, 0),
            'verde': (0, 255, 0),
            'amarillo': (0, 255, 255),
            'naranja': (0, 165, 255),
            'morado': (255, 0, 255)
        }
        return colors_bgr.get(color_name, (128, 128, 128))
