"""Definición de los estados discretos de un motor molecular."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class State:
    """Representa un estado bioquímico o mecánico del motor proteico.

    Un estado es una descripción discreta del motor en un instante dado. Por
    ejemplo, puede representar una cabeza unida al microtúbulo con ATP unido,
    un estado posterior a la hidrólisis o un motor desprendido.

    Attributes:
        name: Identificador único dentro de una red de reacción.
        description: Descripción legible del estado.
        is_terminal: Indica si la simulación debe detenerse al entrar al estado.
    """

    name: str
    description: str = ""
    is_terminal: bool = False

    def __post_init__(self) -> None:
        """Comprueba la validez del identificador y de los campos descriptivos.

        Raises:
            ValueError: Si el nombre está vacío o los campos tienen tipos
                incorrectos.
        """
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("El nombre de un estado debe ser una cadena no vacía.")
        if not isinstance(self.description, str):
            raise ValueError("La descripción del estado debe ser una cadena.")
        if not isinstance(self.is_terminal, bool):
            raise ValueError("is_terminal debe ser un valor booleano.")
