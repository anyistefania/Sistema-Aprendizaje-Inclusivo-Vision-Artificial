"""
Caso de Uso: Guardar Progreso - Capa de Aplicación
Encapsula la lógica para guardar el progreso del estudiante
"""

from ...domain.entities.learning_session import LearningSession
from ...domain.repositories.session_repository import SessionRepository


class SaveProgressUseCase:
    """
    Caso de uso para guardar el progreso de una sesión de aprendizaje.

    Este caso de uso encapsula la lógica de negocio para
    persistir el progreso del estudiante.
    """

    def __init__(self, repository: SessionRepository):
        """
        Inicializa el caso de uso.

        Args:
            repository: Repositorio de sesiones
        """
        self.repository = repository

    def execute(self, session: LearningSession) -> bool:
        """
        Ejecuta el guardado de progreso.

        Args:
            session: Sesión de aprendizaje a guardar

        Returns:
            bool: True si se guardó exitosamente
        """
        # Validar que la sesión tenga datos
        if not session.estudiante_nombre:
            raise ValueError("La sesión debe tener un nombre de estudiante")

        # Finalizar la sesión si no está finalizada
        if session.esta_activa:
            session.finalizar_sesion()

        # Guardar en el repositorio
        try:
            return self.repository.save(session)
        except Exception as e:
            print(f"Error al guardar sesión: {e}")
            return False

    def get_student_history(self, student_name: str) -> list:
        """
        Obtiene el historial de sesiones de un estudiante.

        Args:
            student_name: Nombre del estudiante

        Returns:
            list: Lista de sesiones del estudiante
        """
        try:
            return self.repository.find_by_student(student_name)
        except Exception as e:
            print(f"Error al obtener historial: {e}")
            return []

    def get_latest_session(self, student_name: str):
        """
        Obtiene la sesión más reciente de un estudiante.

        Args:
            student_name: Nombre del estudiante

        Returns:
            LearningSession o None
        """
        try:
            return self.repository.find_latest(student_name)
        except Exception as e:
            print(f"Error al obtener última sesión: {e}")
            return None
