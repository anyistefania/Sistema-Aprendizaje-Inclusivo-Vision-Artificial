"""
Entidad LearningSession - Capa de Dominio
Representa una sesión de aprendizaje de un estudiante
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from .detection_result import DetectionResult


@dataclass
class LearningSession:
    """
    Entidad que representa una sesión de aprendizaje.

    Attributes:
        estudiante_nombre: Nombre del estudiante
        fecha_inicio: Timestamp del inicio de la sesión
        aciertos: Número de aciertos
        intentos: Número de intentos totales
        objetos_reconocidos: Lista de objetos reconocidos
        fecha_fin: Timestamp del fin de la sesión (opcional)
    """
    estudiante_nombre: str
    fecha_inicio: datetime = field(default_factory=datetime.now)
    aciertos: int = 0
    intentos: int = 0
    objetos_reconocidos: List[str] = field(default_factory=list)
    fecha_fin: Optional[datetime] = None

    def __post_init__(self):
        """Validación de datos"""
        if not self.estudiante_nombre:
            raise ValueError("El nombre del estudiante es requerido")

        if self.aciertos < 0 or self.intentos < 0:
            raise ValueError("Aciertos e intentos deben ser números positivos")

        if self.aciertos > self.intentos:
            raise ValueError("Los aciertos no pueden ser mayores que los intentos")

    def registrar_acierto(self, detection: DetectionResult):
        """Registra un acierto en la sesión"""
        self.aciertos += 1
        self.intentos += 1
        objeto = f"{detection.forma}_{detection.color}"
        self.objetos_reconocidos.append(objeto)

    def registrar_intento(self):
        """Registra un intento sin éxito"""
        self.intentos += 1

    def finalizar_sesion(self):
        """Marca la sesión como finalizada"""
        self.fecha_fin = datetime.now()

    @property
    def duracion_minutos(self) -> float:
        """Calcula la duración de la sesión en minutos"""
        if self.fecha_fin:
            delta = self.fecha_fin - self.fecha_inicio
        else:
            delta = datetime.now() - self.fecha_inicio
        return delta.total_seconds() / 60.0

    @property
    def porcentaje_aciertos(self) -> float:
        """Calcula el porcentaje de aciertos"""
        if self.intentos == 0:
            return 0.0
        return (self.aciertos / self.intentos) * 100.0

    @property
    def esta_activa(self) -> bool:
        """Verifica si la sesión está activa"""
        return self.fecha_fin is None

    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario"""
        return {
            'estudiante': self.estudiante_nombre,
            'fecha': self.fecha_inicio.isoformat(),
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'duracion_minutos': self.duracion_minutos,
            'estadisticas': {
                'aciertos': self.aciertos,
                'intentos': self.intentos,
                'porcentaje': round(self.porcentaje_aciertos, 2),
                'objetos_reconocidos': self.objetos_reconocidos
            }
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'LearningSession':
        """Crea una entidad LearningSession desde un diccionario"""
        return cls(
            estudiante_nombre=data['estudiante'],
            fecha_inicio=datetime.fromisoformat(data['fecha']),
            aciertos=data['estadisticas']['aciertos'],
            intentos=data['estadisticas']['intentos'],
            objetos_reconocidos=data['estadisticas']['objetos_reconocidos'],
            fecha_fin=datetime.fromisoformat(data['fecha_fin']) if data.get('fecha_fin') else None
        )
