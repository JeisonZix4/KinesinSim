"""Registro temporal de la evolución de un motor molecular."""

from dataclasses import dataclass, field
from math import isfinite
from typing import Any


@dataclass
class Trajectory:
    """Almacena los eventos observados durante una simulación estocástica.

    Cada índice de las listas corresponde al mismo evento y al mismo instante.
    Los tiempos se expresan en segundos y las posiciones en nanómetros.

    El registro inicial se guarda como un evento llamado ``initial``. Los
    siguientes registros representan transiciones o el final de la ventana de
    observación.

    Attributes:
        times_s: Tiempos de cada registro, en segundos.
        positions_nm: Posiciones del motor, en nanómetros.
        states: Nombres de los estados después de cada registro.
        events: Nombres de los eventos registrados.
        atp_consumed_total: Número acumulado de moléculas de ATP consumidas.
    """

    times_s: list[float] = field(default_factory=list)
    positions_nm: list[float] = field(default_factory=list)
    states: list[str] = field(default_factory=list)
    events: list[str] = field(default_factory=list)
    atp_consumed_total: int = 0

    def __post_init__(self) -> None:
        """Comprueba que los datos iniciales de la trayectoria sean coherentes.

        Raises:
            ValueError: Si las listas no tienen igual longitud, si contienen
                valores inválidos o si el consumo total de ATP es negativo.
        """
        lengths = {
            len(self.times_s),
            len(self.positions_nm),
            len(self.states),
            len(self.events),
        }
        if len(lengths) != 1:
            raise ValueError("Todos los registros de la trayectoria deben alinearse.")
        if isinstance(self.atp_consumed_total, bool) or not isinstance(
            self.atp_consumed_total, int
        ):
            raise ValueError("atp_consumed_total debe ser un entero.")
        if self.atp_consumed_total < 0:
            raise ValueError("El consumo total de ATP no puede ser negativo.")

        previous_time = float("-inf")
        for time_s, position_nm, state, event in zip(
            self.times_s, self.positions_nm, self.states, self.events
        ):
            if not isfinite(float(time_s)) or time_s < previous_time:
                raise ValueError("Los tiempos deben ser finitos y no decrecientes.")
            if not isfinite(float(position_nm)):
                raise ValueError("Las posiciones deben ser números finitos.")
            if not isinstance(state, str) or not state.strip():
                raise ValueError("Cada registro debe incluir un estado no vacío.")
            if not isinstance(event, str) or not event.strip():
                raise ValueError("Cada registro debe incluir un evento no vacío.")
            previous_time = time_s

    def record(
        self,
        time_s: float,
        position_nm: float,
        state: str,
        event: str,
        atp_delta: int = 0,
    ) -> None:
        """Añade un registro y actualiza el consumo acumulado de ATP.

        Args:
            time_s: Tiempo del evento, en segundos.
            position_nm: Posición después del evento, en nanómetros.
            state: Nombre del estado después del evento.
            event: Identificador del evento que produjo el registro.
            atp_delta: Moléculas de ATP consumidas durante este evento.

        Raises:
            ValueError: Si el registro no es finito, el tiempo retrocede o el
                consumo incremental de ATP es inválido.
        """
        try:
            time_value = float(time_s)
            position_value = float(position_nm)
        except (TypeError, ValueError) as error:
            raise ValueError("Tiempo y posición deben ser valores numéricos.") from error

        if not isfinite(time_value) or not isfinite(position_value):
            raise ValueError("Tiempo y posición deben ser finitos.")
        if self.times_s and time_value < self.times_s[-1]:
            raise ValueError("Los tiempos de la trayectoria no pueden retroceder.")
        if not isinstance(state, str) or not state.strip():
            raise ValueError("El estado registrado no puede estar vacío.")
        if not isinstance(event, str) or not event.strip():
            raise ValueError("El evento registrado no puede estar vacío.")
        if isinstance(atp_delta, bool) or not isinstance(atp_delta, int):
            raise ValueError("atp_delta debe ser un entero.")
        if atp_delta < 0:
            raise ValueError("El consumo incremental de ATP no puede ser negativo.")

        self.atp_consumed_total += atp_delta
        self.times_s.append(time_value)
        self.positions_nm.append(position_value)
        self.states.append(state)
        self.events.append(event)

    @property
    def duration_s(self) -> float:
        """Duración entre el primer y el último registro, en segundos."""
        if len(self.times_s) < 2:
            return 0.0
        return self.times_s[-1] - self.times_s[0]

    @property
    def displacement_nm(self) -> float:
        """Desplazamiento neto entre la posición inicial y final, en nm."""
        if len(self.positions_nm) < 2:
            return 0.0
        return self.positions_nm[-1] - self.positions_nm[0]

    @property
    def path_length_nm(self) -> float:
        """Distancia total recorrida, incluyendo avances y retrocesos, en nm."""
        return sum(
            abs(next_position - position)
            for position, next_position in zip(
                self.positions_nm[:-1], self.positions_nm[1:]
            )
        )

    @property
    def mean_velocity_nm_s(self) -> float:
        """Velocidad media neta durante la trayectoria, en nm/s."""
        if self.duration_s == 0:
            return 0.0
        return self.displacement_nm / self.duration_s

    @property
    def final_state(self) -> str | None:
        """Nombre del último estado registrado, o ``None`` si está vacía."""
        return self.states[-1] if self.states else None

    @property
    def number_of_events(self) -> int:
        """Cantidad de eventos registrados, sin contar el evento inicial."""
        return sum(event != "initial" for event in self.events)

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una copia de los datos en un diccionario serializable."""
        return {
            "times_s": list(self.times_s),
            "positions_nm": list(self.positions_nm),
            "states": list(self.states),
            "events": list(self.events),
            "atp_consumed_total": self.atp_consumed_total,
        }
