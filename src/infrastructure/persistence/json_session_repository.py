"""
Repositorio JSON de Sesiones - Capa de Infraestructura
Implementación concreta de persistencia en archivos JSON
"""

import json
import os
from typing import List, Optional
from datetime import datetime
from ...domain.entities.learning_session import LearningSession
from ...domain.repositories.session_repository import SessionRepository


class JsonSessionRepository(SessionRepository):
    """
    Implementación del repositorio de sesiones usando archivos JSON.

    Guarda las sesiones en archivos JSON en un directorio específico.
    """

    def __init__(self, storage_dir: str = "sessions"):
        """
        Inicializa el repositorio.

        Args:
            storage_dir: Directorio donde se guardarán las sesiones
        """
        self.storage_dir = storage_dir
        self._ensure_storage_dir()

    def _ensure_storage_dir(self):
        """Asegura que el directorio de almacenamiento existe"""
        if not os.path.exists(self.storage_dir):
            try:
                os.makedirs(self.storage_dir)
            except Exception as e:
                print(f"⚠️  Error al crear directorio de sesiones: {e}")

    def _get_filename(self, session: LearningSession) -> str:
        """
        Genera el nombre del archivo para una sesión.

        Args:
            session: Sesión de aprendizaje

        Returns:
            str: Nombre del archivo
        """
        timestamp = session.fecha_inicio.strftime('%Y%m%d_%H%M%S')
        filename = f"progreso_{session.estudiante_nombre}_{timestamp}.json"
        return os.path.join(self.storage_dir, filename)

    def save(self, session: LearningSession) -> bool:
        """
        Guarda una sesión en un archivo JSON.

        Args:
            session: Sesión a guardar

        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            filename = self._get_filename(session)
            data = session.to_dict()

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            print(f"✅ Progreso guardado en: {filename}")
            return True

        except Exception as e:
            print(f"❌ Error al guardar sesión: {e}")
            return False

    def find_by_student(self, student_name: str) -> List[LearningSession]:
        """
        Busca todas las sesiones de un estudiante.

        Args:
            student_name: Nombre del estudiante

        Returns:
            Lista de sesiones del estudiante
        """
        sessions = []

        try:
            if not os.path.exists(self.storage_dir):
                return sessions

            # Buscar archivos que coincidan con el nombre del estudiante
            for filename in os.listdir(self.storage_dir):
                if filename.startswith(f"progreso_{student_name}_") and filename.endswith('.json'):
                    filepath = os.path.join(self.storage_dir, filename)

                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            session = LearningSession.from_dict(data)
                            sessions.append(session)
                    except Exception as e:
                        print(f"⚠️  Error al leer archivo {filename}: {e}")

            # Ordenar por fecha
            sessions.sort(key=lambda s: s.fecha_inicio, reverse=True)

        except Exception as e:
            print(f"❌ Error al buscar sesiones: {e}")

        return sessions

    def find_latest(self, student_name: str) -> Optional[LearningSession]:
        """
        Busca la sesión más reciente de un estudiante.

        Args:
            student_name: Nombre del estudiante

        Returns:
            Sesión más reciente o None
        """
        sessions = self.find_by_student(student_name)

        if sessions:
            return sessions[0]  # Ya está ordenado por fecha descendente

        return None

    def get_all(self) -> List[LearningSession]:
        """
        Obtiene todas las sesiones guardadas.

        Returns:
            Lista de todas las sesiones
        """
        sessions = []

        try:
            if not os.path.exists(self.storage_dir):
                return sessions

            for filename in os.listdir(self.storage_dir):
                if filename.startswith('progreso_') and filename.endswith('.json'):
                    filepath = os.path.join(self.storage_dir, filename)

                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            session = LearningSession.from_dict(data)
                            sessions.append(session)
                    except Exception as e:
                        print(f"⚠️  Error al leer archivo {filename}: {e}")

            # Ordenar por fecha
            sessions.sort(key=lambda s: s.fecha_inicio, reverse=True)

        except Exception as e:
            print(f"❌ Error al obtener todas las sesiones: {e}")

        return sessions

    def delete_old_sessions(self, days: int = 90) -> int:
        """
        Elimina sesiones más antiguas que el número de días especificado.

        Args:
            days: Número de días a mantener

        Returns:
            int: Número de sesiones eliminadas
        """
        deleted_count = 0

        try:
            if not os.path.exists(self.storage_dir):
                return 0

            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)

            for filename in os.listdir(self.storage_dir):
                if filename.startswith('progreso_') and filename.endswith('.json'):
                    filepath = os.path.join(self.storage_dir, filename)

                    # Verificar fecha de modificación del archivo
                    file_time = os.path.getmtime(filepath)

                    if file_time < cutoff_date:
                        try:
                            os.remove(filepath)
                            deleted_count += 1
                        except Exception as e:
                            print(f"⚠️  Error al eliminar {filename}: {e}")

            if deleted_count > 0:
                print(f"✅ Se eliminaron {deleted_count} sesiones antiguas")

        except Exception as e:
            print(f"❌ Error al eliminar sesiones antiguas: {e}")

        return deleted_count
