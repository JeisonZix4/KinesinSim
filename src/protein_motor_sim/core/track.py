"""Representación unidimensional de una pista molecular."""

from dataclasses import dataclass
from math import isfinite
from numbers import Real


@dataclass(frozen=True, slots=True)
class Track:
    """Describe una pista molecular periódica, como un microtúbulo o actina.

    La pista se representa como una sucesión unidimensional de sitios de unión.
    La coordenada positiva sigue la orientación indicada por ``polarity``.

    Attributes:
        name: Nombre de la pista molecular.
        lattice_spacing_nm: Separación entre sitios consecutivos, en nm.
        polarity: Orientación del eje de la pista; debe ser +1 o -1.
        origin_nm: Coordenada del sitio con índice cero, en nm.
    """

    name: str = "microtubule"
    lattice_spacing_nm: float = 8.2
    polarity: int = 1
    origin_nm: float = 0.0

    def __post_init__(self) -> None:
        """Valida los parámetros geométricos de la pista.

        Raises:
            ValueError: Si la pista tiene un nombre, espaciamiento o polaridad
                inválidos.
        """
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("El nombre de la pista no puede estar vacío.")
        if isinstance(self.lattice_spacing_nm, bool) or not isinstance(
            self.lattice_spacing_nm, Real
        ):
            raise ValueError("El espaciamiento debe ser un número real.")
        if not isfinite(float(self.lattice_spacing_nm)):
            raise ValueError("El espaciamiento debe ser finito.")
        if self.lattice_spacing_nm <= 0:
            raise ValueError("El espaciamiento de la pista debe ser positivo.")
        if isinstance(self.polarity, bool) or self.polarity not in (-1, 1):
            raise ValueError("La polaridad debe ser +1 o -1.")
        if isinstance(self.origin_nm, bool) or not isinstance(self.origin_nm, Real):
            raise ValueError("El origen debe ser un número real.")
        if not isfinite(float(self.origin_nm)):
            raise ValueError("El origen de la pista debe ser finito.")

    def site_position_nm(self, site_index: int) -> float:
        """Calcula la coordenada de un sitio de la pista.

        Args:
            site_index: Índice entero del sitio. Puede ser negativo.

        Returns:
            Posición del sitio en nanómetros.

        Raises:
            TypeError: Si ``site_index`` no es un entero.
        """
        if isinstance(site_index, bool) or not isinstance(site_index, int):
            raise TypeError("site_index debe ser un número entero.")
        return self.origin_nm + self.polarity * self.lattice_spacing_nm * site_index

    def nearest_site_index(self, position_nm: float) -> int:
        """Encuentra el índice del sitio más cercano a una posición.

        Args:
            position_nm: Posición sobre la pista, en nanómetros.

        Returns:
            Índice entero del sitio más cercano.
        """
        if not isfinite(float(position_nm)):
            raise ValueError("La posición debe ser un número finito.")
        coordinate = (position_nm - self.origin_nm) / (
            self.polarity * self.lattice_spacing_nm
        )
        return int(round(coordinate))
