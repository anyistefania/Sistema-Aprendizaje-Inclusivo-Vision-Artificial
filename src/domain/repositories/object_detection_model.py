"""
Interfaz ObjectDetectionModel - Capa de Dominio
Define el contrato para modelos de detección de objetos
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
import numpy as np
from ..entities.educational_object import EducationalObject


class ObjectDetectionResult:
    """Resultado de detección con bounding box"""

    def __init__(self, objeto: EducationalObject, bbox: Tuple[int, int, int, int],
                 confianza: float):
        """
        Args:
            objeto: Objeto educativo detectado
            bbox: Bounding box (x, y, width, height)
            confianza: Nivel de confianza (0.0-1.0)
        """
        self.objeto = objeto
        self.bbox = bbox
        self.confianza = confianza

    def __repr__(self):
        return f"DetectionResult({self.objeto.nombre}, conf={self.confianza:.2f})"


class ObjectDetectionModel(ABC):
    """
    Interfaz para modelos de detección de objetos didácticos.

    Esta interfaz permite usar diferentes implementaciones:
    - Detectores basados en reglas (OpenCV actual)
    - Modelos pre-entrenados (YOLO, MobileNet, etc.)
    - Modelos custom entrenados específicamente
    """

    @abstractmethod
    def detect(self, image: np.ndarray, confidence_threshold: float = 0.5) -> List[ObjectDetectionResult]:
        """
        Detecta objetos didácticos en una imagen.

        Args:
            image: Imagen BGR de OpenCV
            confidence_threshold: Umbral mínimo de confianza

        Returns:
            Lista de objetos detectados con sus bounding boxes
        """
        pass

    @abstractmethod
    def get_supported_objects(self) -> List[str]:
        """
        Obtiene la lista de objetos que el modelo puede detectar.

        Returns:
            Lista de nombres de objetos
        """
        pass

    @abstractmethod
    def is_ready(self) -> bool:
        """
        Verifica si el modelo está listo para usar.

        Returns:
            True si el modelo está cargado y listo
        """
        pass

    @abstractmethod
    def get_model_info(self) -> dict:
        """
        Obtiene información sobre el modelo.

        Returns:
            Diccionario con información del modelo (nombre, versión, precisión, etc.)
        """
        pass
