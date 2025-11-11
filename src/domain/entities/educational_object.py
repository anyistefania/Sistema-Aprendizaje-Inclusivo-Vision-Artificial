"""
Entidad EducationalObject - Capa de Dominio
Representa un objeto didáctico para educación especial
"""

from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


class ObjectCategory(Enum):
    """Categorías de objetos didácticos"""
    JUGUETE = "juguete"
    ALIMENTO = "alimento"
    ANIMAL = "animal"
    VEHICULO = "vehiculo"
    NUMERO = "numero"
    LETRA = "letra"
    FORMA = "forma"
    COLOR = "color"
    EMOCION = "emocion"
    OBJETO_COTIDIANO = "objeto_cotidiano"
    HERRAMIENTA = "herramienta"


class DifficultyLevel(Enum):
    """Niveles de dificultad pedagógica"""
    BASICO = 1      # 3-5 años
    INTERMEDIO = 2  # 6-8 años
    AVANZADO = 3    # 9+ años


@dataclass
class EducationalObject:
    """
    Entidad que representa un objeto didáctico.

    Attributes:
        nombre: Nombre del objeto (ej: "manzana", "perro", "número_5")
        categoria: Categoría del objeto
        descripcion_educativa: Descripción pedagógica del objeto
        nivel_dificultad: Nivel de complejidad
        palabras_clave: Palabras relacionadas para aprendizaje
        valor_pedagogico: Información educativa adicional
    """
    nombre: str
    categoria: ObjectCategory
    descripcion_educativa: str
    nivel_dificultad: DifficultyLevel = DifficultyLevel.BASICO
    palabras_clave: List[str] = None
    valor_pedagogico: Optional[str] = None

    def __post_init__(self):
        """Validación y valores por defecto"""
        if not self.nombre:
            raise ValueError("El nombre del objeto es requerido")

        if self.palabras_clave is None:
            self.palabras_clave = []

    def descripcion_completa(self) -> str:
        """Genera descripción completa para el estudiante"""
        desc = f"Este es {self._articulo()} {self.nombre}"

        if self.valor_pedagogico:
            desc += f". {self.valor_pedagogico}"

        if self.descripcion_educativa:
            desc += f". {self.descripcion_educativa}"

        return desc

    def _articulo(self) -> str:
        """Determina el artículo apropiado"""
        vocales = 'aeiou'
        if self.nombre[0].lower() in vocales:
            return "un" if self._es_masculino() else "una"
        return "un" if self._es_masculino() else "una"

    def _es_masculino(self) -> bool:
        """Determina el género gramatical"""
        # Simplificación - en un sistema real usarías un diccionario
        terminaciones_femeninas = ['a', 'ión', 'dad', 'tad', 'tud']
        for term in terminaciones_femeninas:
            if self.nombre.endswith(term):
                return False
        return True

    def es_apropiado_para_nivel(self, nivel: int) -> bool:
        """Verifica si el objeto es apropiado para el nivel del estudiante"""
        return self.nivel_dificultad.value <= nivel

    def to_dict(self) -> dict:
        """Convierte a diccionario"""
        return {
            'nombre': self.nombre,
            'categoria': self.categoria.value,
            'descripcion_educativa': self.descripcion_educativa,
            'nivel_dificultad': self.nivel_dificultad.value,
            'palabras_clave': self.palabras_clave,
            'valor_pedagogico': self.valor_pedagogico
        }


# Catálogo de objetos didácticos predefinidos
CATALOGO_OBJETOS_DIDACTICOS = {
    # Alimentos
    'manzana': EducationalObject(
        nombre='manzana',
        categoria=ObjectCategory.ALIMENTO,
        descripcion_educativa='una fruta roja, dulce y nutritiva',
        nivel_dificultad=DifficultyLevel.BASICO,
        palabras_clave=['fruta', 'rojo', 'redonda', 'comida'],
        valor_pedagogico='Las manzanas son saludables y nos dan energía'
    ),
    'platano': EducationalObject(
        nombre='plátano',
        categoria=ObjectCategory.ALIMENTO,
        descripcion_educativa='una fruta amarilla, dulce y alargada',
        nivel_dificultad=DifficultyLevel.BASICO,
        palabras_clave=['fruta', 'amarillo', 'alargado', 'comida'],
        valor_pedagogico='Los plátanos tienen potasio que fortalece nuestros músculos'
    ),

    # Animales
    'perro': EducationalObject(
        nombre='perro',
        categoria=ObjectCategory.ANIMAL,
        descripcion_educativa='un animal doméstico que ladra y es muy amigable',
        nivel_dificultad=DifficultyLevel.BASICO,
        palabras_clave=['animal', 'mascota', 'ladra', 'amigo'],
        valor_pedagogico='Los perros son leales y nos hacen compañía'
    ),
    'gato': EducationalObject(
        nombre='gato',
        categoria=ObjectCategory.ANIMAL,
        descripcion_educativa='un animal doméstico que maúlla y es muy suave',
        nivel_dificultad=DifficultyLevel.BASICO,
        palabras_clave=['animal', 'mascota', 'maúlla', 'suave'],
        valor_pedagogico='Los gatos son independientes y cariñosos'
    ),

    # Vehículos
    'carro': EducationalObject(
        nombre='carro',
        categoria=ObjectCategory.VEHICULO,
        descripcion_educativa='un vehículo con cuatro ruedas para transportarse',
        nivel_dificultad=DifficultyLevel.BASICO,
        palabras_clave=['vehículo', 'transporte', 'ruedas', 'conducir'],
        valor_pedagogico='Los carros nos ayudan a viajar a lugares lejanos'
    ),
    'autobus': EducationalObject(
        nombre='autobús',
        categoria=ObjectCategory.VEHICULO,
        descripcion_educativa='un vehículo grande que transporta muchas personas',
        nivel_dificultad=DifficultyLevel.INTERMEDIO,
        palabras_clave=['vehículo', 'transporte', 'público', 'grande'],
        valor_pedagogico='Los autobuses transportan a muchas personas al mismo tiempo'
    ),

    # Números (0-9)
    **{f'numero_{i}': EducationalObject(
        nombre=f'número {i}',
        categoria=ObjectCategory.NUMERO,
        descripcion_educativa=f'el número {i}',
        nivel_dificultad=DifficultyLevel.BASICO if i <= 5 else DifficultyLevel.INTERMEDIO,
        palabras_clave=['número', 'matemáticas', 'contar'],
        valor_pedagogico=f'El {i} se usa para contar y hacer matemáticas'
    ) for i in range(10)},

    # Letras vocales
    **{f'letra_{letra}': EducationalObject(
        nombre=f'letra {letra.upper()}',
        categoria=ObjectCategory.LETRA,
        descripcion_educativa=f'la vocal {letra.upper()}',
        nivel_dificultad=DifficultyLevel.BASICO,
        palabras_clave=['letra', 'vocal', 'alfabeto', 'leer'],
        valor_pedagogico=f'La {letra.upper()} es una vocal del abecedario'
    ) for letra in 'aeiou'},

    # Formas geométricas (mantener compatibilidad)
    'circulo': EducationalObject(
        nombre='círculo',
        categoria=ObjectCategory.FORMA,
        descripcion_educativa='una forma redonda sin esquinas',
        nivel_dificultad=DifficultyLevel.BASICO,
        palabras_clave=['forma', 'redondo', 'geometría'],
        valor_pedagogico='Los círculos son formas perfectamente redondas'
    ),
    'triangulo': EducationalObject(
        nombre='triángulo',
        categoria=ObjectCategory.FORMA,
        descripcion_educativa='una forma con tres lados y tres esquinas',
        nivel_dificultad=DifficultyLevel.BASICO,
        palabras_clave=['forma', 'tres', 'geometría'],
        valor_pedagogico='Los triángulos tienen tres lados iguales o diferentes'
    ),
    'cuadrado': EducationalObject(
        nombre='cuadrado',
        categoria=ObjectCategory.FORMA,
        descripcion_educativa='una forma con cuatro lados iguales',
        nivel_dificultad=DifficultyLevel.BASICO,
        palabras_clave=['forma', 'cuatro', 'geometría'],
        valor_pedagogico='Los cuadrados tienen todos sus lados del mismo tamaño'
    ),
}


def get_educational_object(nombre: str) -> Optional[EducationalObject]:
    """
    Obtiene un objeto educativo del catálogo.

    Args:
        nombre: Nombre del objeto

    Returns:
        EducationalObject o None si no existe
    """
    return CATALOGO_OBJETOS_DIDACTICOS.get(nombre.lower())


def get_objects_by_category(categoria: ObjectCategory) -> List[EducationalObject]:
    """
    Obtiene objetos por categoría.

    Args:
        categoria: Categoría a filtrar

    Returns:
        Lista de objetos de esa categoría
    """
    return [obj for obj in CATALOGO_OBJETOS_DIDACTICOS.values()
            if obj.categoria == categoria]


def get_objects_for_level(nivel: int) -> List[EducationalObject]:
    """
    Obtiene objetos apropiados para un nivel.

    Args:
        nivel: Nivel del estudiante (1-3)

    Returns:
        Lista de objetos apropiados
    """
    return [obj for obj in CATALOGO_OBJETOS_DIDACTICOS.values()
            if obj.es_apropiado_para_nivel(nivel)]
