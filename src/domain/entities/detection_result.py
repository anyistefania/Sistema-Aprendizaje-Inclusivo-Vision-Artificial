"""
Entidad DetectionResult - Capa de Dominio
Representa el resultado de una detección de forma y color
"""

from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class DetectionResult:
    """
    Entidad que representa el resultado de una detección.

    Attributes:
        forma: Tipo de forma detectada
        color: Color detectado
        centro: Coordenadas (x, y) del centro
        area: Área del objeto en píxeles
        confianza: Nivel de confianza de la detección (0.0-1.0)
    """
    forma: str
    color: str
    centro: Tuple[int, int]
    area: float
    confianza: float = 1.0

    def __post_init__(self):
        """Validación de datos"""
        if not isinstance(self.forma, str):
            raise ValueError("Forma debe ser una cadena")

        if not isinstance(self.color, str):
            raise ValueError("Color debe ser una cadena")

        if not isinstance(self.centro, tuple) or len(self.centro) != 2:
            raise ValueError("Centro debe ser una tupla (x, y)")

        if not isinstance(self.area, (int, float)) or self.area < 0:
            raise ValueError("Área debe ser un número positivo")

        if not 0.0 <= self.confianza <= 1.0:
            raise ValueError("Confianza debe estar entre 0.0 y 1.0")

    def es_valido(self) -> bool:
        """Verifica si la detección es válida"""
        return (self.forma != 'desconocido' and
                self.color not in ['desconocido', 'sin color', None] and
                self.area > 0)

    def descripcion_educativa(self) -> str:
        """Genera una descripción educativa del objeto"""
        descripciones_formas = {
            'circulo': 'círculo, como una pelota',
            'triangulo': 'triángulo, como un tejado',
            'cuadrado': 'cuadrado, como una ventana',
            'rectangulo': 'rectángulo, como una puerta',
            'pentagono': 'pentágono, tiene cinco lados',
            'hexagono': 'hexágono, tiene seis lados'
        }

        descripciones_colores = {
            'rojo': 'rojo como una manzana',
            'azul': 'azul como el cielo',
            'verde': 'verde como las plantas',
            'amarillo': 'amarillo como el sol',
            'naranja': 'naranja como la fruta',
            'morado': 'morado como las uvas'
        }

        forma_desc = descripciones_formas.get(self.forma, self.forma)
        color_desc = descripciones_colores.get(self.color, self.color)

        return f"un {forma_desc} de color {color_desc}"

    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario"""
        return {
            'forma': self.forma,
            'color': self.color,
            'centro': self.centro,
            'area': self.area,
            'confianza': self.confianza
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'DetectionResult':
        """Crea una entidad DetectionResult desde un diccionario"""
        return cls(
            forma=data['forma'],
            color=data['color'],
            centro=tuple(data['centro']),
            area=data['area'],
            confianza=data.get('confianza', 1.0)
        )
