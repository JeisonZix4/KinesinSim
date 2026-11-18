"""Animaciones esquemáticas de motores proteicos sobre pistas moleculares.

Las animaciones de este módulo convierten una trayectoria unidimensional en
una representación visual de dos cabezas. La reconstrucción de las cabezas es
cinemática e ilustrativa: la trayectoria actual no contiene coordenadas
individuales de cada cabeza ni información estructural atomística.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from protein_motor_sim.core.trajectory import Trajectory


@dataclass(frozen=True, slots=True)
class AnimationStyle:
    """Parámetros visuales de la animación de kinesina.

    Attributes:
        step_size_nm: Separación nominal entre sitios consecutivos, en nm.
        frames_per_step: Número de fotogramas usados para interpolar un paso.
        arc_height: Altura máxima del arco de la cabeza móvil, en coordenadas
            gráficas. No representa una distancia estructural calibrada.
        interval_ms: Duración de cada fotograma en milisegundos.
        trail_length: Número máximo de posiciones recientes que se muestran.
        show_trail: Indica si se muestra la estela del centro del motor.
        show_time: Indica si se muestra el tiempo de la trayectoria.
    """

    step_size_nm: float = 8.2
    frames_per_step: int = 12
    arc_height: float = 3.2
    interval_ms: int = 45
    trail_length: int = 12
    show_trail: bool = True
    show_time: bool = True

    def __post_init__(self) -> None:
        """Valida los parámetros de presentación."""
        if self.step_size_nm <= 0:
            raise ValueError("step_size_nm debe ser positivo.")
        if self.frames_per_step < 2:
            raise ValueError("frames_per_step debe ser al menos 2.")
        if self.arc_height < 0:
            raise ValueError("arc_height no puede ser negativo.")
        if self.interval_ms <= 0:
            raise ValueError("interval_ms debe ser positivo.")
        if self.trail_length < 0:
            raise ValueError("trail_length no puede ser negativo.")


def _state_docking_fraction(state_name: str) -> float:
    """Devuelve una fracción visual ilustrativa de acoplamiento del cuello."""
    normalized = state_name.lower()
    if "atp" in normalized:
        return 0.95
    if "hydrolysis" in normalized or "post" in normalized:
        return 0.65
    if "detached" in normalized:
        return 0.0
    return 0.15


def _build_animation_frames(
    trajectory: Trajectory,
    style: AnimationStyle,
) -> list[dict[str, Any]]:
    """Reconstruye fotogramas esquemáticos a partir de eventos discretos.

    La trayectoria aporta la posición del centro del motor y el nombre de cada
    evento. En los eventos ``forward_step`` y ``backward_step`` se infiere qué
    cabeza se desplaza, manteniendo la otra fija y dibujando una trayectoria
    arqueada entre sitios. Esta reconstrucción no es una simulación de las
    coordenadas moleculares de las dos cabezas.

    Args:
        trajectory: Trayectoria estocástica registrada por ProteinMotorSim.
        style: Parámetros visuales de la animación.

    Returns:
        Lista de diccionarios, uno por fotograma.
    """
    if not trajectory.times_s:
        raise ValueError("No se puede animar una trayectoria vacía.")

    center = float(trajectory.positions_nm[0])
    head_x = np.array(
        [center - style.step_size_nm / 2, center + style.step_size_nm / 2],
        dtype=float,
    )
    head_y = np.array([0.0, 0.0], dtype=float)
    state = trajectory.states[0]
    event = trajectory.events[0]
    current_time = float(trajectory.times_s[0])
    atp_count = 0
    detached = "detached" in state.lower()
    frames: list[dict[str, Any]] = []

    def append_frame(
        x_values: np.ndarray,
        y_values: np.ndarray,
        frame_time: float,
        frame_state: str,
        frame_event: str,
        progress: float,
        frame_detached: bool,
        frame_atp: int,
    ) -> None:
        """Añade una copia independiente del estado gráfico."""
        frames.append(
            {
                "head_x": x_values.copy(),
                "head_y": y_values.copy(),
                "center_x": float(np.mean(x_values)),
                "time_s": frame_time,
                "state": frame_state,
                "event": frame_event,
                "progress": progress,
                "detached": frame_detached,
                "atp": frame_atp,
            }
        )

    append_frame(head_x, head_y, current_time, state, event, 0.0, detached, atp_count)

    for index in range(1, len(trajectory.times_s)):
        next_time = float(trajectory.times_s[index])
        next_state = trajectory.states[index]
        next_event = trajectory.events[index]
        next_center = float(trajectory.positions_nm[index])
        previous_center = float(np.mean(head_x))
        delta_center = next_center - previous_center
        atp_count = atp_count + (1 if next_event == "atp_hydrolysis" else 0)

        if next_event == "forward_step":
            moving_index = int(np.argmin(head_x))
            fixed_index = 1 - moving_index
            target_x = 2.0 * next_center - head_x[fixed_index]
            start_x = float(head_x[moving_index])
            fixed_x = float(head_x[fixed_index])
            for fraction in np.linspace(0.0, 1.0, style.frames_per_step)[1:]:
                frame_x = head_x.copy()
                frame_y = head_y.copy()
                frame_x[moving_index] = start_x + fraction * (target_x - start_x)
                frame_y[moving_index] = style.arc_height * np.sin(np.pi * fraction)
                append_frame(
                    frame_x, frame_y, next_time, next_state, next_event,
                    float(fraction), detached, atp_count,
                )
            head_x[moving_index] = target_x
            head_x[fixed_index] = fixed_x
            head_y[:] = 0.0
        elif next_event == "backward_step":
            moving_index = int(np.argmax(head_x))
            fixed_index = 1 - moving_index
            target_x = 2.0 * next_center - head_x[fixed_index]
            start_x = float(head_x[moving_index])
            fixed_x = float(head_x[fixed_index])
            for fraction in np.linspace(0.0, 1.0, style.frames_per_step)[1:]:
                frame_x = head_x.copy()
                frame_y = head_y.copy()
                frame_x[moving_index] = start_x + fraction * (target_x - start_x)
                frame_y[moving_index] = style.arc_height * np.sin(np.pi * fraction)
                append_frame(
                    frame_x, frame_y, next_time, next_state, next_event,
                    float(fraction), detached, atp_count,
                )
            head_x[moving_index] = target_x
            head_x[fixed_index] = fixed_x
            head_y[:] = 0.0
        else:
            # Los eventos químicos modifican el estado indicado en pantalla,
            # pero no desplazan las cabezas en este modelo cinemático mínimo.
            if abs(delta_center) > 1e-9:
                head_x += delta_center
            detached = "detached" in next_state.lower() or next_event == "detachment"
            append_frame(
                head_x, head_y, next_time, next_state, next_event,
                1.0, detached, atp_count,
            )

        state = next_state
        event = next_event
        current_time = next_time
        detached = detached or "detached" in next_state.lower()

    return frames


def animate_kinesin_walk(
    trajectory: Trajectory,
    style: AnimationStyle | None = None,
    figsize: tuple[float, float] = (12.5, 7.0),
    repeat: bool = False,
):
    """Crea una animación 2D detallada y esquemática de kinesina-1.

    La escena incluye dos cabezas, cuello conector, tallo, carga y una pista
    con subunidades de tubulina. Los pasos se interpolan mediante arcos para
    comunicar el mecanismo ``hand-over-hand``. Las posiciones individuales de
    las cabezas se reconstruyen visualmente a partir del desplazamiento del
    centro del motor; no proceden de coordenadas moleculares simuladas.

    Args:
        trajectory: Trayectoria generada por un simulador de ProteinMotorSim.
        style: Configuración de estilo; si es None se utiliza la configuración
            predeterminada de :class:`AnimationStyle`.
        figsize: Tamaño de la figura en pulgadas.
        repeat: Indica si la animación se repite al terminar.

    Returns:
        Objeto ``matplotlib.animation.FuncAnimation``.

    Raises:
        ImportError: Si Matplotlib no está instalado.
        ValueError: Si la trayectoria está vacía o el estilo es inválido.

    Note:
        El eje vertical es diagramático y no está a escala estructural.
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
        from matplotlib.patches import Circle, Ellipse, FancyBboxPatch
    except ImportError as exc:
        raise ImportError("Instala Matplotlib para crear animaciones.") from exc

    visual_style = style or AnimationStyle()
    frames = _build_animation_frames(trajectory, visual_style)
    positions = np.asarray(trajectory.positions_nm, dtype=float)
    span = max(float(np.ptp(positions)), visual_style.step_size_nm * 3)
    padding = max(visual_style.step_size_nm * 2, span * 0.12)
    x_min = float(np.min(positions) - padding)
    x_max = float(np.max(positions) + padding)

    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(top=0.84, bottom=0.13, left=0.06, right=0.97)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-4.0, 10.5)
    ax.set_xlabel("Posición a lo largo del microtúbulo (nm)", fontsize=11)
    ax.set_ylabel("Altura esquemática (no a escala)", fontsize=10)
    ax.set_title("Ciclo de marcha de kinesina-1 · esquema hand-over-hand", pad=18)
    ax.grid(axis="x", alpha=0.15)
    ax.set_yticks([])

    # Pista: dos hileras esquemáticas de dímeros de tubulina.
    site_spacing = visual_style.step_size_nm
    first_site = int(np.floor(x_min / site_spacing)) - 1
    last_site = int(np.ceil(x_max / site_spacing)) + 1
    for site in range(first_site, last_site + 1):
        site_x = site * site_spacing
        ax.add_patch(
            Ellipse((site_x, -1.5), site_spacing * 0.88, 1.15,
                    alpha=0.32, linewidth=0.8, zorder=1)
        )
        ax.add_patch(
            Ellipse((site_x + site_spacing / 2, -2.65), site_spacing * 0.88,
                    1.05, alpha=0.18, linewidth=0.8, zorder=1)
        )
    ax.plot([x_min, x_max], [-2.1, -2.1], linewidth=1.0, alpha=0.3, zorder=0)
    ax.text(x_min + 0.3, -3.55, "−", fontsize=16, weight="bold")
    ax.text(x_max - 0.5, -3.55, "+", fontsize=16, weight="bold")
    ax.text((x_min + x_max) / 2, -3.55, "Microtúbulo · protofilamento esquemático",
            ha="center", fontsize=9)

    # Elementos dinámicos del motor.
    head_a = Circle((0.0, 0.0), 1.05, zorder=6, linewidth=1.5)
    head_b = Circle((0.0, 0.0), 1.05, zorder=6, linewidth=1.5)
    ax.add_patch(head_a)
    ax.add_patch(head_b)
    label_a = ax.text(0.0, 0.0, "A", ha="center", va="center",
                      weight="bold", fontsize=10, zorder=7)
    label_b = ax.text(0.0, 0.0, "B", ha="center", va="center",
                      weight="bold", fontsize=10, zorder=7)
    neck_line, = ax.plot([], [], linewidth=3.0, zorder=5)
    stalk_line, = ax.plot([], [], linewidth=4.0, zorder=4)
    cargo = FancyBboxPatch((0.0, 0.0), 3.0, 1.5,
                           boxstyle="round,pad=0.15,rounding_size=0.3",
                           zorder=4, linewidth=1.2)
    ax.add_patch(cargo)
    cargo_label = ax.text(0.0, 0.0, "Carga", ha="center", va="center",
                          fontsize=8, zorder=5)
    trail_line, = ax.plot([], [], linestyle="--", linewidth=1.5,
                          alpha=0.65, zorder=2)
    info = ax.text(0.01, 1.04, "", transform=ax.transAxes,
                   ha="left", va="bottom", fontsize=9,
                   bbox={"boxstyle": "round,pad=0.45", "alpha": 0.12})
    state_text = ax.text(0.99, 1.04, "", transform=ax.transAxes,
                         ha="right", va="bottom", fontsize=9)

    head_colors = ("#277DA1", "#F9844A")

    def update(frame_index: int):
        """Actualiza la geometría y los indicadores del fotograma actual."""
        frame = frames[frame_index]
        x_values = frame["head_x"]
        y_values = frame["head_y"]
        docking = _state_docking_fraction(frame["state"])
        detached_now = frame["detached"]
        hub_x = float(np.mean(x_values))
        hub_y = 4.35 + 0.4 * docking

        for index, patch in enumerate((head_a, head_b)):
            patch.center = (float(x_values[index]), float(y_values[index]))
            patch.set_facecolor("#9E9E9E" if detached_now else head_colors[index])
            patch.set_alpha(0.65 if detached_now else 0.96)
        label_a.set_position((float(x_values[0]), float(y_values[0])))
        label_b.set_position((float(x_values[1]), float(y_values[1])))
        label_a.set_color("white")
        label_b.set_color("white")

        # El acoplamiento del cuello se indica con una longitud/ángulo gráficos.
        linker_target_x = hub_x + (docking - 0.5) * visual_style.step_size_nm * 0.45
        neck_line.set_data(
            [x_values[0], linker_target_x, x_values[1]],
            [y_values[0], hub_y - 0.35, y_values[1]],
        )
        stalk_line.set_data([hub_x, hub_x], [hub_y, 7.45])
        cargo.set_bounds(hub_x - 1.7, 7.45, 3.4, 1.5)
        cargo_label.set_position((hub_x, 8.2))

        if visual_style.show_trail:
            start = max(0, frame_index - visual_style.trail_length * visual_style.frames_per_step)
            trail_frames = frames[start:frame_index + 1]
            trail_line.set_data(
                [item["center_x"] for item in trail_frames],
                [-0.15 for _ in trail_frames],
            )
        else:
            trail_line.set_data([], [])

        if visual_style.show_time:
            info.set_text(
                f"t = {frame['time_s']:.4g} s    ATP hidrolizados = {frame['atp']}"
            )
        else:
            info.set_text(f"ATP hidrolizados = {frame['atp']}")
        state_text.set_text(
            f"Estado: {frame['state']}\nEvento: {frame['event']}"
        )
        ax.set_title(
            "Kinesina desprendida" if detached_now
            else "Ciclo de marcha de kinesina-1 · esquema hand-over-hand",
            pad=18,
        )
        return (head_a, head_b, label_a, label_b, neck_line, stalk_line,
                cargo, cargo_label, trail_line, info, state_text)

    animation = FuncAnimation(
        fig,
        update,
        frames=len(frames),
        interval=visual_style.interval_ms,
        blit=False,
        repeat=repeat,
    )
    # Facilita inspección desde Jupyter y conserva la figura asociada.
    animation._protein_motor_sim_frames = frames  # type: ignore[attr-defined]
    return animation


def animate_trajectory(
    trajectory: Trajectory,
    interval_ms: int = 50,
):
    """Mantiene compatibilidad con la API de animación anterior.

    Args:
        trajectory: Trayectoria que se desea animar.
        interval_ms: Intervalo entre fotogramas en milisegundos.

    Returns:
        Animación esquemática de dos cabezas.
    """
    return animate_kinesin_walk(
        trajectory,
        style=AnimationStyle(interval_ms=interval_ms),
    )


def save_animation(
    animation: Any,
    filepath: str | Path,
    fps: int = 20,
    dpi: int = 120,
) -> Path:
    """Guarda una animación como GIF o MP4.

    Args:
        animation: Instancia de ``FuncAnimation``.
        filepath: Ruta de destino; la extensión debe ser ``.gif`` o ``.mp4``.
        fps: Fotogramas por segundo.
        dpi: Resolución de salida en puntos por pulgada.

    Returns:
        Ruta absoluta del archivo guardado.

    Raises:
        ValueError: Si la extensión o los parámetros no son válidos.
        RuntimeError: Si falta el escritor necesario para el formato elegido.
    """
    from matplotlib.animation import FFMpegWriter, PillowWriter

    path = Path(filepath).expanduser().resolve()
    if fps <= 0 or dpi <= 0:
        raise ValueError("fps y dpi deben ser positivos.")
    path.parent.mkdir(parents=True, exist_ok=True)
    suffix = path.suffix.lower()
    if suffix == ".gif":
        writer = PillowWriter(fps=fps)
    elif suffix == ".mp4":
        if not FFMpegWriter.isAvailable():
            raise RuntimeError("FFmpeg no está disponible; instala ffmpeg.")
        writer = FFMpegWriter(fps=fps)
    else:
        raise ValueError("El formato debe ser .gif o .mp4.")
    animation.save(str(path), writer=writer, dpi=dpi)
    return path

