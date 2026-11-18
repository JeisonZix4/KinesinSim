"""Esquema 2D conceptual de kinesina y microtúbulo."""

def plot_kinesin_schematic(position_nm: float = 0.0, ax=None):
    """Dibuja un esquema conceptual de un motor sobre un microtúbulo.

    Args:
        position_nm: Posición longitudinal del motor en nanómetros.
        ax: Ejes Matplotlib existentes o None.

    Returns:
        Ejes Matplotlib utilizados.

    Note:
        Es una ilustración esquemática, no una estructura molecular a escala.
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle
    except ImportError as exc:
        raise ImportError("Matplotlib es necesario para el esquema.") from exc

    if ax is None:
        _, ax = plt.subplots()

    ax.plot([-20, 20], [0, 0], linewidth=12, alpha=0.18, solid_capstyle="round")
    ax.plot(
        [position_nm - 2.5, position_nm + 2.5],
        [0.9, 0.9],
        linewidth=3,
    )
    ax.add_patch(Circle((position_nm - 2.5, 0.9), 0.8))
    ax.add_patch(Circle((position_nm + 2.5, 0.9), 0.8))
    ax.set_xlim(-20, 20)
    ax.set_ylim(-1.5, 3)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Posición (nm)")
    ax.set_title("Esquema conceptual de kinesina")
    ax.set_yticks([])
    return ax
