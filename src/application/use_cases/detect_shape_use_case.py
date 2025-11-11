"""
Caso de Uso: Detectar Forma - Capa de Aplicación
Encapsula la lógica para detectar formas geométricas
"""

import cv2
import numpy as np
from typing import Optional


class DetectShapeUseCase:
    """
    Caso de uso para detectar formas geométricas en contornos.

    Este caso de uso encapsula la lógica de negocio para
    identificar formas geométricas básicas.
    """

    def execute(self, contour: np.ndarray) -> str:
        """
        Ejecuta la detección de forma.

        Args:
            contour: Contorno de OpenCV

        Returns:
            str: Nombre de la forma detectada
        """
        if contour is None or len(contour) == 0:
            return 'desconocido'

        # Calcular el perímetro del contorno
        perimeter = cv2.arcLength(contour, True)

        if perimeter == 0:
            return 'desconocido'

        # Aproximar el contorno con un polígono
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        vertices = len(approx)

        # Clasificar según el número de vértices
        if vertices == 3:
            return 'triangulo'

        elif vertices == 4:
            # Distinguir entre cuadrado y rectángulo
            (x, y, w, h) = cv2.boundingRect(approx)
            aspect_ratio = w / float(h) if h != 0 else 0

            if 0.85 <= aspect_ratio <= 1.15:
                return 'cuadrado'
            else:
                return 'rectangulo'

        elif vertices == 5:
            return 'pentagono'

        elif vertices == 6:
            return 'hexagono'

        else:
            # Verificar si es un círculo
            area = cv2.contourArea(contour)
            circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0

            if circularity > 0.7:
                return 'circulo'

        return 'desconocido'

    def get_center(self, contour: np.ndarray) -> tuple:
        """
        Calcula el centro del contorno.

        Args:
            contour: Contorno de OpenCV

        Returns:
            tuple: Coordenadas (x, y) del centro
        """
        M = cv2.moments(contour)

        if M["m00"] == 0:
            return (0, 0)

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        return (cX, cY)

    def get_area(self, contour: np.ndarray) -> float:
        """
        Calcula el área del contorno.

        Args:
            contour: Contorno de OpenCV

        Returns:
            float: Área en píxeles
        """
        return cv2.contourArea(contour)
