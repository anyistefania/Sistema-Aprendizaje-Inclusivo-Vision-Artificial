"""
Interfaz SessionRepository - Capa de Dominio
Define el contrato para la persistencia de sesiones
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.learning_session import LearningSession


class SessionRepository(ABC):
    """
    Interfaz para el repositorio de sesiones de aprendizaje.

    Define los métodos que debe implementar cualquier
    repositorio concreto de sesiones.
    """

    @abstractmethod
    def save(self, session: LearningSession) -> bool:
        """
        Guarda una sesión de aprendizaje.

        Args:
            session: Sesión a guardar

        Returns:
            bool: True si se guardó exitosamente
        """
        pass

    @abstractmethod
    def find_by_student(self, student_name: str) -> List[LearningSession]:
        """
        Busca todas las sesiones de un estudiante.

        Args:
            student_name: Nombre del estudiante

        Returns:
            Lista de sesiones del estudiante
        """
        pass

    @abstractmethod
    def find_latest(self, student_name: str) -> Optional[LearningSession]:
        """
        Busca la sesión más reciente de un estudiante.

        Args:
            student_name: Nombre del estudiante

        Returns:
            Sesión más reciente o None
        """
        pass

    @abstractmethod
    def get_all(self) -> List[LearningSession]:
        """
        Obtiene todas las sesiones guardadas.

        Returns:
            Lista de todas las sesiones
        """
        pass
