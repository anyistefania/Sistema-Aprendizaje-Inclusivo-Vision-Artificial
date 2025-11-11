"""
Entidad Student - Capa de Dominio
Representa un estudiante del sistema de aprendizaje inclusivo
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    """
    Entidad que representa un estudiante con necesidades educativas especiales.

    Attributes:
        nombre: Nombre del estudiante
        edad: Edad del estudiante
        discapacidad: Tipo de discapacidad ('visual', 'auditiva', 'cognitiva', 'lenguaje', 'multiple')
        nivel: Nivel de dificultad (1-5)
    """
    nombre: str
    edad: int
    discapacidad: str
    nivel: int = 1

    def __post_init__(self):
        """Validación de datos"""
        if not self.nombre or not isinstance(self.nombre, str):
            raise ValueError("El nombre debe ser una cadena no vacía")

        if not isinstance(self.edad, int) or self.edad < 0:
            raise ValueError("La edad debe ser un número positivo")

        valid_disabilities = ['visual', 'auditiva', 'cognitiva', 'lenguaje', 'multiple']
        if self.discapacidad not in valid_disabilities:
            raise ValueError(f"Discapacidad debe ser una de: {valid_disabilities}")

        if not isinstance(self.nivel, int) or not 1 <= self.nivel <= 5:
            raise ValueError("El nivel debe estar entre 1 y 5")

    @property
    def requiere_voz(self) -> bool:
        """Determina si el estudiante requiere retroalimentación por voz"""
        return self.discapacidad != 'auditiva'

    @property
    def requiere_texto_grande(self) -> bool:
        """Determina si requiere texto más grande"""
        return self.discapacidad == 'visual'

    @property
    def requiere_interfaz_simplificada(self) -> bool:
        """Determina si requiere interfaz simplificada"""
        return self.discapacidad in ['cognitiva', 'multiple']

    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario"""
        return {
            'nombre': self.nombre,
            'edad': self.edad,
            'discapacidad': self.discapacidad,
            'nivel': self.nivel
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        """Crea una entidad Student desde un diccionario"""
        return cls(
            nombre=data['nombre'],
            edad=data['edad'],
            discapacidad=data['discapacidad'],
            nivel=data.get('nivel', 1)
        )
