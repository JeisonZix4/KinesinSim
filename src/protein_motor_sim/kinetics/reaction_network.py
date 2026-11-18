"""Red dirigida de transiciones bioquímicas y mecánicas."""

from collections import defaultdict
from collections.abc import Iterable

from protein_motor_sim.core.environment import Environment
from protein_motor_sim.core.state import State
from protein_motor_sim.core.transition import Transition


class ReactionNetwork:
    """Almacena estados y transiciones de un modelo de motor proteico."""

    def __init__(
        self,
        states: Iterable[State],
        transitions: Iterable[Transition],
        initial_state: str,
    ) -> None:
        """Crea y valida una red de reacciones.

        Args:
            states: Estados que componen la red.
            transitions: Transiciones permitidas.
            initial_state: Nombre del estado inicial.

        Raises:
            ValueError: Si la red contiene referencias inválidas.
        """
        state_list = list(states)
        self.states = {state.name: state for state in state_list}
        self.transitions = list(transitions)
        self.initial_state = initial_state

        if len(self.states) != len(state_list):
            raise ValueError("La red contiene nombres de estado duplicados.")
        if initial_state not in self.states:
            raise ValueError("El estado inicial no pertenece a la red.")

        self._outgoing: dict[str, list[Transition]] = defaultdict(list)
        for transition in self.transitions:
            if transition.source not in self.states:
                raise ValueError(f"Estado de origen desconocido: {transition.source}")
            if transition.target not in self.states:
                raise ValueError(f"Estado de destino desconocido: {transition.target}")
            self._outgoing[transition.source].append(transition)

    def outgoing(self, state_name: str) -> tuple[Transition, ...]:
        """Devuelve las transiciones salientes de un estado.

        Args:
            state_name: Estado del que se buscan transiciones.

        Returns:
            Tupla de transiciones salientes.
        """
        if state_name not in self.states:
            raise KeyError(f"Estado desconocido: {state_name}")
        return tuple(self._outgoing.get(state_name, ()))

    def rates(
        self, state_name: str, environment: Environment
    ) -> tuple[tuple[Transition, float], ...]:
        """Evalúa las tasas de todas las transiciones salientes.

        Args:
            state_name: Estado actual.
            environment: Condiciones de simulación.

        Returns:
            Pares (transición, tasa) con tasas expresadas en s^-1.
        """
        return tuple(
            (transition, transition.rate(environment))
            for transition in self.outgoing(state_name)
        )
