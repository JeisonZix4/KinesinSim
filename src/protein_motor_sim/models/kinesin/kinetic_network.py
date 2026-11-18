"""Construcción de la red cinética simplificada de kinesina-1."""

from protein_motor_sim.core.state import State
from protein_motor_sim.core.transition import Transition
from protein_motor_sim.kinetics.force_dependence import BellRate
from protein_motor_sim.kinetics.rate_laws import ATPBindingRate, ConstantRate
from protein_motor_sim.kinetics.reaction_network import ReactionNetwork
from protein_motor_sim.models.kinesin.parameters import KinesinParameters


def build_kinesin1_network(parameters: KinesinParameters) -> ReactionNetwork:
    """Construye una red fenomenológica mínima de kinesina-1.

    La red agrupa varios intermediarios moleculares en tres estados efectivos:
    unido sin ATP, ATP unido y posterior a hidrólisis. El cierre del ciclo
    produce un paso forward o backward. Es un prototipo computacional y no
    representa todos los intermediarios estructurales del ciclo mecanoquímico.

    Args:
        parameters: Parámetros cinéticos configurables.

    Returns:
        Red de reacciones con desprendimiento como estado terminal.
    """
    states = [
        State("bound_apo", "Motor unido al microtúbulo, sin ATP unido."),
        State("atp_bound", "Estado efectivo con ATP unido."),
        State("post_hydrolysis", "Estado efectivo posterior a hidrólisis."),
        State("detached", "Motor desprendido del microtúbulo.", is_terminal=True),
    ]

    forward = BellRate(
        ConstantRate(parameters.forward_step_rate_s),
        distance_m=parameters.force_distance_m,
        force_direction=1,
    )
    backward = BellRate(
        ConstantRate(parameters.backward_step_rate_s),
        distance_m=parameters.force_distance_m,
        force_direction=-1,
    )
    detachment = BellRate(
        ConstantRate(parameters.detachment_rate_s),
        distance_m=parameters.force_distance_m,
        force_direction=-1,
    )

    transitions = [
        Transition(
            source="bound_apo",
            target="atp_bound",
            rate_law=ATPBindingRate(parameters.atp_association_rate_M_s),
            event_name="atp_binding",
        ),
        Transition(
            source="atp_bound",
            target="post_hydrolysis",
            rate_law=ConstantRate(parameters.hydrolysis_rate_s),
            event_name="atp_hydrolysis",
            atp_consumed=1,
        ),
        Transition(
            source="post_hydrolysis",
            target="bound_apo",
            rate_law=forward,
            event_name="forward_step",
            displacement_nm=parameters.step_size_nm,
        ),
        Transition(
            source="post_hydrolysis",
            target="bound_apo",
            rate_law=backward,
            event_name="backward_step",
            displacement_nm=-parameters.step_size_nm,
        ),
        Transition(
            source="bound_apo",
            target="detached",
            rate_law=detachment,
            event_name="detachment",
        ),
        Transition(
            source="atp_bound",
            target="detached",
            rate_law=detachment,
            event_name="detachment",
        ),
        Transition(
            source="post_hydrolysis",
            target="detached",
            rate_law=detachment,
            event_name="detachment",
        ),
    ]
    return ReactionNetwork(states, transitions, initial_state="bound_apo")
