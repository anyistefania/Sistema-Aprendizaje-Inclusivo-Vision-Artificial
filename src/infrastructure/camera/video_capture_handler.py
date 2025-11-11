"""
Manejador de Captura de Video - Capa de Infraestructura
Implementación concreta para captura de video desde cámara
"""

import cv2
import numpy as np
from typing import Tuple, Optional


class VideoCaptureHandler:
    """
    Manejador para la captura de video desde cámara web.

    Encapsula la funcionalidad de OpenCV para captura de video
    y preprocesamiento de frames.
    """

    def __init__(self, camera_index: int = 0, width: int = 800, height: int = 600):
        """
        Inicializa el manejador de captura.

        Args:
            camera_index: Índice de la cámara (0 por defecto)
            width: Ancho del frame
            height: Alto del frame
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap = None
        self.is_opened = False

    def open(self) -> bool:
        """
        Abre la cámara.

        Returns:
            bool: True si se abrió exitosamente
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_index)

            if not self.cap.isOpened():
                print(f"❌ Error: No se pudo abrir la cámara {self.camera_index}")
                return False

            # Configurar resolución
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

            self.is_opened = True
            return True

        except Exception as e:
            print(f"❌ Error al abrir cámara: {e}")
            return False

    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Lee un frame de la cámara.

        Returns:
            tuple: (éxito, frame) - éxito es bool, frame es numpy array o None
        """
        if not self.is_opened or not self.cap:
            return False, None

        try:
            ret, frame = self.cap.read()

            if ret:
                # Voltear horizontalmente para efecto espejo
                frame = cv2.flip(frame, 1)

            return ret, frame

        except Exception as e:
            print(f"❌ Error al leer frame: {e}")
            return False, None

    def preprocess_frame(self, frame: np.ndarray) -> dict:
        """
        Preprocesa un frame para detección.

        Args:
            frame: Frame BGR de OpenCV

        Returns:
            dict: Diccionario con frame original y versiones procesadas
        """
        if frame is None:
            return {}

        try:
            # Aplicar desenfoque para reducir ruido
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)

            # Convertir a diferentes espacios de color
            gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            # Umbralización adaptativa
            thresh = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY_INV,
                11, 2
            )

            # Operaciones morfológicas para limpiar
            kernel = np.ones((5, 5), np.uint8)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

            return {
                'original': frame,
                'blurred': blurred,
                'gray': gray,
                'hsv': hsv,
                'thresh': thresh
            }

        except Exception as e:
            print(f"❌ Error al preprocesar frame: {e}")
            return {'original': frame}

    def find_contours(self, thresh: np.ndarray) -> list:
        """
        Encuentra contornos en una imagen umbralizada.

        Args:
            thresh: Imagen umbralizada

        Returns:
            list: Lista de contornos
        """
        try:
            contours, _ = cv2.findContours(
                thresh,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            return contours

        except Exception as e:
            print(f"❌ Error al encontrar contornos: {e}")
            return []

    def release(self):
        """Libera los recursos de la cámara"""
        if self.cap:
            try:
                self.cap.release()
                self.is_opened = False
            except Exception as e:
                print(f"⚠️  Error al liberar cámara: {e}")

    def __enter__(self):
        """Soporte para context manager"""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Soporte para context manager"""
        self.release()

    def __del__(self):
        """Limpia recursos al destruir el objeto"""
        self.release()
