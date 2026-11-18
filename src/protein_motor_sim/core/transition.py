"""Transiciones permitidas entre estados de una red cinética."""

from dataclasses import dataclass
from math import isfinite
from numbers import Real
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from protein_motor_sim.core.environment import Environment


RateFunction = Callable[["Environment"], float]


@dataclass(frozen=True, slots=True)
class Transition:
    """Describe un evento estocástico entre dos estados del motor.

    ``rate_law`` debe ser una función u objeto invocable que reciba un
    :class:`Environment` y devuelva una tasa en s⁻¹. La ley puede depender,
    por ejemplo, de la concentración de ATP o de la fuerza externa.

    Attributes:
        source: Nombre del estado de origen.
        target: Nombre del estado de destino.
        rate_law: Función que calcula la tasa de transición en s⁻¹.
        event_name: Identificador del evento que se guardará en la trayectoria.
        displacement_nm: Cambio de posición asociado al evento, en nanómetros.
        atp_consumed: Número de moléculas de ATP consumidas durante el evento.
    """

    source: str
    target: str
    rate_law: RateFunction
    event_name: str
    displacement_nm: float = 0.0
    atp_consumed: int = 0

    def __post_init__(self) -> None:
        """Valida los datos estáticos de la transición.

        Raises:
            ValueError: Si los nombres, la tasa o los cambios asociados son
                inválidos.
        """
        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError("El estado de origen debe ser una cadena no vacía.")
        if not isinstance(self.target, str) or not self.target.strip():
            raise ValueError("El estado de destino debe ser una cadena no vacía.")
        if not isinstance(self.event_name, str) or not self.event_name.strip():
            raise ValueError("Toda transición debe tener un nombre de evento.")
        if not callable(self.rate_law):
            raise ValueError("rate_law debe ser una función u objeto invocable.")
        if isinstance(self.displacement_nm, bool) or not isinstance(
            self.displacement_nm, Real
        ):
            raise ValueError("El desplazamiento debe ser un número real.")
        if not isfinite(float(self.displacement_nm)):
            raise ValueError("El desplazamiento debe ser un número finito.")
        if isinstance(self.atp_consumed, bool) or not isinstance(
            self.atp_consumed, int
        ):
            raise ValueError("atp_consumed debe ser un número entero.")
        if self.atp_consumed < 0:
            raise ValueError("El consumo de ATP no puede ser negativo.")

    def rate(self, environment: "Environment") -> float:
        """Evalúa la tasa de esta transición para un entorno dado.

        Args:
            environment: Condiciones experimentales de la simulación.

        Returns:
            Tasa de transición en s⁻¹.

        Raises:
            ValueError: Si la ley devuelve una tasa negativa o no finita.
        """
        value = float(self.rate_law(environment))
        if not isfinite(value) or value < 0:
            raise ValueError(
                f"La tasa de '{self.event_name}' debe ser finita y no negativa; "
                f"se recibió {value!r}."
            )
        return value
