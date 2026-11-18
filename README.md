# ProteinMotorSim

**ProteinMotorSim** es una librería de Python en desarrollo para construir, ejecutar, analizar y visualizar modelos computacionales de motores proteicos. Su primer modelo es una representación cinética, estocástica y simplificada de **kinesina-1** que se desplaza sobre una pista molecular unidimensional.

El objetivo del proyecto es proporcionar una arquitectura extensible para estudiar la conversión de energía química en movimiento mecánico. La librería separa las definiciones moleculares, las redes de estados y transiciones, las leyes cinéticas, los algoritmos de simulación, los componentes mecánicos, el análisis de resultados y la visualización.

> **Estado científico del proyecto:** ProteinMotorSim es actualmente un prototipo de investigación y aprendizaje. El modelo de kinesina incluido es fenomenológico y reducido; sus parámetros predeterminados son ilustrativos y no constituyen un conjunto calibrado experimentalmente. Las animaciones y los paisajes energéticos son representaciones esquemáticas o fenomenológicas, no simulaciones atomísticas ni superficies de energía libre medidas.

---

## Tabla de contenido

1. [Objetivos y alcance](#1-objetivos-y-alcance)
2. [Capacidades actuales](#2-capacidades-actuales)
3. [Arquitectura del proyecto](#3-arquitectura-del-proyecto)
4. [Instalación](#4-instalación)
5. [Inicio rápido](#5-inicio-rápido)
6. [Conceptos científicos y matemáticos](#6-conceptos-científicos-y-matemáticos)
7. [Referencia de la API](#7-referencia-de-la-api)
   - [Core](#71-core)
   - [Kinetics](#72-kinetics)
   - [Modelos de motores](#73-modelos-de-motores)
   - [Simulation](#74-simulation)
   - [Mechanics](#75-mechanics)
   - [Analysis](#76-analysis)
   - [Visualization](#77-visualization)
   - [I/O](#78-io)
8. [Notebooks de Jupyter](#8-notebooks-de-jupyter)
9. [Unidades y convenciones](#9-unidades-y-convenciones)
10. [Pruebas y calidad del código](#10-pruebas-y-calidad-del-código)
11. [Limitaciones actuales](#11-limitaciones-actuales)
12. [Hoja de ruta](#12-hoja-de-ruta)
13. [Contribuir al proyecto](#13-contribuir-al-proyecto)
14. [Licencia](#14-licencia)

---

## 1. Objetivos y alcance

### Metadatos del paquete

- Nombre del proyecto para instalación: `protein-motor-sim`.
- Nombre del paquete para importación en Python: `protein_motor_sim`.
- Versión indicada en `pyproject.toml`: `0.1.1`.
- Requiere Python 3.10 o superior.


Los motores proteicos son máquinas moleculares que utilizan energía química —por ejemplo, la liberada durante la unión e hidrólisis de ATP— para producir movimiento, ejercer fuerzas o transportar cargas. Su comportamiento combina procesos bioquímicos discretos, fluctuaciones térmicas y respuestas mecánicas.

ProteinMotorSim busca ofrecer componentes reutilizables para representar esos procesos en distintos niveles de descripción.

### Preguntas que se pueden explorar con la versión actual

- ¿Cómo cambia la actividad simulada al variar la concentración de ATP?
- ¿Cómo modifica una fuerza externa las tasas de transición definidas por el modelo?
- ¿Qué secuencia de estados y eventos puede recorrer una kinesina durante una simulación?
- ¿Cómo varían la velocidad y el desplazamiento entre realizaciones estocásticas?
- ¿Cuántas moléculas de ATP contabiliza el modelo como consumidas?
- ¿Cómo representar una trayectoria discreta mediante una animación esquemática?
- ¿Cómo cambia un paisaje energético fenomenológico al modificar barreras, acoplamientos o carga externa?

### Motores contemplados

| Motor | Estado en el proyecto | Pista biológica asociada |
|---|---|---|
| Kinesina-1 | Modelo cinético mínimo implementado | Microtúbulos |
| Miosina | Espacio reservado; modelo no implementado | Filamentos de actina |
| Dineína | Espacio reservado; modelo no implementado | Microtúbulos |

La arquitectura está pensada para incorporar otros motores, pero la existencia de los paquetes `myosin` y `dynein` no significa que esos motores ya puedan simularse.

---

## 2. Capacidades actuales

### 2.1. Núcleo y redes cinéticas

- Representación de estados bioquímicos o mecánicos mediante `State`.
- Representación de eventos entre estados mediante `Transition`.
- Construcción de redes dirigidas mediante `ReactionNetwork`.
- Definición de condiciones experimentales con ATP, fuerza y temperatura mediante `Environment`.
- Definición geométrica de una pista molecular unidimensional mediante `Track`.
- Registro de estados, eventos, tiempos y posiciones mediante `Trajectory`.

### 2.2. Leyes cinéticas

- Tasa constante de primer orden.
- Asociación de ATP mediante una ley pseudo-primer orden, `k_on [ATP]`.
- Dependencia fenomenológica de tasas con fuerza mediante una expresión de tipo Bell.

### 2.3. Simulación

- Algoritmo estocástico directo de Gillespie (SSA).
- Reproducción de corridas mediante semillas aleatorias.
- Ejecución de conjuntos de trayectorias independientes (*ensembles*).
- Barrido de concentraciones de ATP.

### 2.4. Mecánica auxiliar

- Suma de fuerzas escalares colineales.
- Resorte lineal de Hooke.
- Incrementos brownianos unidimensionales.
- Modelo elemental de arrastre lineal para una carga.
- Paisaje energético fenomenológico de dos coordenadas.

Estos componentes mecánicos son herramientas independientes en esta versión. No están acoplados todavía a una ecuación de Langevin que evolucione junto con los eventos de Gillespie.

### 2.5. Análisis y visualización

- Velocidad media, desplazamiento neto, longitud de trayectoria y consumo de ATP.
- Estadísticas descriptivas de conjuntos de simulaciones.
- Gráficas posición-tiempo y velocidad-concentración de ATP.
- Animación esquemática de dos cabezas de kinesina.
- Mapas de energía bidimensionales y superficies tridimensionales.
- Perfiles de energía para distintas conformaciones y fuerzas.
- Superposición y animación de una trayectoria sobre un mapa energético.
- Diagramas de energías de estados y barreras introducidas explícitamente.
- Exportación de animaciones a GIF o MP4.

---

## 3. Arquitectura del proyecto

El proyecto utiliza una estructura `src/` para separar el paquete instalable del material de desarrollo.

```text
ProteinMotorSim/
│
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── LICENSE
├── .gitignore
│
├── src/
│   └── protein_motor_sim/
│       ├── __init__.py
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── motor.py
│       │   ├── state.py
│       │   ├── transition.py
│       │   ├── environment.py
│       │   ├── track.py
│       │   └── trajectory.py
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── kinesin/
│       │   │   ├── __init__.py
│       │   │   ├── kinesin1.py
│       │   │   ├── parameters.py
│       │   │   └── kinetic_network.py
│       │   ├── myosin/
│       │   └── dynein/
│       │
│       ├── kinetics/
│       │   ├── __init__.py
│       │   ├── rate_laws.py
│       │   ├── force_dependence.py
│       │   └── reaction_network.py
│       │
│       ├── simulation/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── gillespie.py
│       │   └── ensemble.py
│       │
│       ├── mechanics/
│       │   ├── __init__.py
│       │   ├── forces.py
│       │   ├── elasticity.py
│       │   ├── brownian.py
│       │   ├── cargo.py
│       │   └── energy_landscape.py
│       │
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── observables.py
│       │   ├── statistics.py
│       │   └── parameter_sweep.py
│       │
│       ├── visualization/
│       │   ├── __init__.py
│       │   ├── plots.py
│       │   ├── animation.py
│       │   ├── molecular_view.py
│       │   ├── energy_landscape.py
│       │   └── energy_maps.py
│       │
│       └── io/
│           ├── __init__.py
│           └── serialization.py
│
├── notebooks/
│   ├── 01_...ipynb
│   ├── ...
│   └── 24_...ipynb
│
├── tests/
│   ├── test_core.py
│   ├── test_kinetics.py
│   ├── test_gillespie.py
│   ├── test_kinesin.py
│   ├── test_mechanics.py
│   └── test_energy_landscape.py
│
└── examples/
    ├── 01_basic_kinesin.py
    ├── 02_atp_concentration.py
    ├── 03_external_force.py
    └── 04_motor_animation.py
```

### Responsabilidad de cada paquete

| Paquete | Responsabilidad |
|---|---|
| `core` | Objetos fundamentales compartidos: motor, estado, transición, entorno, pista y trayectoria. |
| `models` | Parámetros y redes particulares de cada familia de motores. |
| `kinetics` | Leyes que calculan tasas y estructura de las redes de reacción. |
| `simulation` | Interfaces y algoritmos que generan trayectorias. |
| `mechanics` | Fuerzas, elasticidad, ruido browniano, cargas y paisajes energéticos. |
| `analysis` | Observables y estadísticas derivados de las trayectorias. |
| `visualization` | Gráficas, animaciones y visualización de energía. |
| `io` | Guardado y recuperación de trayectorias. |
| `notebooks` | Laboratorio interactivo para experimentos y análisis. |
| `tests` | Pruebas automatizadas del comportamiento del software. |

### Principio de diseño

El modelo molecular no debe depender de Matplotlib ni de Jupyter. El núcleo (`core`, `kinetics`, `models` y `simulation`) puede ejecutarse sin abrir una interfaz gráfica. Los paquetes `visualization` y `notebooks` consumen los resultados y los presentan.

La arquitectura utiliza clases y contratos comunes. `Motor` define una interfaz abstracta para los motores; `SimulationStrategy` define una interfaz para algoritmos de simulación. Esto permite ampliar el proyecto sin mezclar la definición de una proteína con el algoritmo numérico que la simula.

---

## 4. Instalación

### Requisitos

- Python 3.10 o superior.
- `pip`.
- Git (recomendado para desarrollo).
- Matplotlib para gráficas y animaciones.
- JupyterLab e IPykernel para trabajar con los notebooks.
- FFmpeg para exportar animaciones MP4.

### Clonar el repositorio

Cuando el proyecto esté alojado en un repositorio Git, se podrá clonar con:

```bash
git clone <URL_DEL_REPOSITORIO>
cd ProteinMotorSim
```

Si ya tienes la carpeta del proyecto, entra directamente en ella:

```bash
cd ProteinMotorSim
```

### Crear y activar el entorno virtual

En Ubuntu/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### Instalar la librería

Para instalar el paquete en modo editable con herramientas de desarrollo y visualización:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev,viz]"
```

El modo editable permite modificar los archivos de `src/protein_motor_sim/` y utilizar esos cambios sin reinstalar el paquete después de cada edición.

### Extras disponibles

| Extra | Dependencias | Uso |
|---|---|---|
| `viz` | Matplotlib | Gráficas, esquemas y animaciones. |
| `science` | SciPy | Herramientas científicas adicionales para futuras extensiones; no es requisito del núcleo actual. |
| `dev` | Pytest, Ruff, Build | Pruebas, estilo y construcción de distribuciones. |

### Instalar JupyterLab

JupyterLab no forma parte de los extras definidos en `pyproject.toml`; se instala por separado:

```bash
python -m pip install jupyterlab ipykernel
python -m ipykernel install --user \
    --name proteinmotorsim \
    --display-name "Python (ProteinMotorSim)"
```

Inicia JupyterLab desde la raíz del proyecto:

```bash
jupyter lab
```

En cada notebook selecciona el kernel **Python (ProteinMotorSim)**.

### Exportar animaciones

Para GIF se utiliza el escritor Pillow de Matplotlib. Si Pillow no está disponible:

```bash
python -m pip install pillow
```

Para MP4 instala FFmpeg en Ubuntu:

```bash
sudo apt install ffmpeg
```

---

## 5. Inicio rápido

El siguiente ejemplo construye una kinesina-1, especifica las condiciones experimentales, ejecuta una trayectoria con Gillespie y calcula observables.

```python
from protein_motor_sim import Environment, GillespieSimulator, Kinesin1
from protein_motor_sim.analysis import analyze_trajectory

# 1. Crear el modelo de motor.
motor = Kinesin1()

# 2. Especificar las condiciones experimentales.
environment = Environment(
    atp_concentration=1.0e-3,  # mol/L
    external_force_N=0.0,      # N; positiva si se opone al avance +x
    temperature_K=310.0,       # K
)

# 3. Crear el simulador y ejecutar una realización.
simulator = GillespieSimulator()
trajectory = simulator.run(
    motor=motor,
    environment=environment,
    t_max=2.0,  # s
    seed=42,
)

# 4. Analizar los resultados.
results = analyze_trajectory(trajectory)
print(results)
print("Velocidad (nm/s):", results.velocity_nm_s)
print("Recorrido neto absoluto (nm):", results.run_length_nm)
print("ATP contabilizado:", results.atp_consumed)
```

### Graficar la trayectoria

```python
import matplotlib.pyplot as plt
from protein_motor_sim.visualization import plot_trajectory

ax = plot_trajectory(trajectory)
plt.show()
```

### Animar el ciclo de marcha esquemático

```python
from IPython.display import HTML, display
from protein_motor_sim.visualization import (
    AnimationStyle,
    animate_kinesin_walk,
)

style = AnimationStyle(
    step_size_nm=8.2,
    frames_per_step=16,
    arc_height=3.2,
    interval_ms=50,
    trail_length=15,
    show_trail=True,
    show_time=True,
)

animation = animate_kinesin_walk(trajectory, style=style)
display(HTML(animation.to_jshtml()))
```

### Construir y visualizar un paisaje de energía

```python
import matplotlib.pyplot as plt
from protein_motor_sim.mechanics import EnergyLandscape
from protein_motor_sim.visualization import (
    plot_energy_landscape_2d,
    plot_energy_landscape_3d,
)

landscape = EnergyLandscape(
    period_nm=8.2,
    spatial_barrier_kBT=2.5,
    conformational_barrier_kBT=3.0,
    conformational_bias_kBT=0.2,
    phase_shift=0.5,
    coupling_kBT=0.4,
    opposing_force_pN=1.0,
    temperature_K=310.0,
)

ax, contour = plot_energy_landscape_2d(
    landscape,
    x_range_nm=(-8.2, 32.8),
)
plt.show()

ax3d, surface = plot_energy_landscape_3d(
    landscape,
    x_range_nm=(-8.2, 32.8),
)
plt.show()
```

Este paisaje es fenomenológico e independiente de la red de Gillespie. No se debe interpretar como una energía libre real de kinesina sin calibración y justificación termodinámica.

---

## 6. Conceptos científicos y matemáticos

### 6.1. Red de estados y transiciones

El motor se representa como una red dirigida:

\[
S_i \xrightarrow{k_{ij}} S_j,
\]

donde `State` representa una configuración efectiva y `Transition` representa un evento que conecta dos estados. La tasa \(k_{ij}\) tiene unidades de \(s^{-1}\) y puede depender del ambiente.

### 6.2. Asociación de ATP

La ley de asociación actual es pseudo-primer orden:

\[
a_{ATP}=k_{on}[ATP],
\]

donde \(k_{on}\) se expresa en \(M^{-1}s^{-1}\) y \([ATP]\) en \(M\). Por tanto, la tasa efectiva se expresa en \(s^{-1}\).

### 6.3. Dependencia de fuerza tipo Bell

La implementación usa una forma fenomenológica:

\[
k(F)=k_0\exp\left(
-\frac{s\,\theta F\delta}{k_B T}
\right),
\]

donde `force_direction` determina el signo de la sensibilidad, `load_fraction` representa la fracción efectiva de carga, \(F\) es la fuerza en newtons y \(\delta\) es la distancia característica en metros. Esta relación es una aproximación; no es una ley universal para todas las transiciones.

### 6.4. Algoritmo directo de Gillespie

Para un estado actual se evalúan las tasas de las transiciones salientes \(a_1,\ldots,a_M\) y se calcula:

\[
a_0=\sum_{\mu=1}^{M}a_\mu.
\]

El tiempo de espera se obtiene mediante:

\[
\tau=-\frac{\ln r_1}{a_0},
\]

y se selecciona el evento \(\mu\) según las probabilidades \(a_\mu/a_0\). Después de cada evento, se actualiza el estado, la posición y el consumo de ATP, y se vuelven a evaluar las tasas.

El algoritmo implementado supone que las tasas se mantienen constantes entre dos eventos para el estado y el ambiente actuales. No integra simultáneamente coordenadas mecánicas continuas.

### 6.5. Paisaje de energía `EnergyLandscape`

La clase `EnergyLandscape` representa un potencial fenomenológico bidimensional:

\[
U=U(x,q),
\]

donde \(x\) es la coordenada longitudinal en nm y \(q\in[0,1]\) es una coordenada conformacional adimensional. El resultado se expresa en unidades de \(k_BT\).

La implementación suma cinco contribuciones:

\[
\frac{U(x,q)}{k_BT}=
U_{espacial}+U_{conformacional}+U_{sesgo}+U_{acoplamiento}+U_{carga}.
\]

- **Espacial:** potencial periódico cuya fase puede desplazarse con `q`.
- **Conformacional:** barrera de doble pozo entre los extremos de `q`.
- **Sesgo:** diferencia energética lineal entre conformaciones.
- **Acoplamiento:** término periódico que depende simultáneamente de `x` y `q`.
- **Carga:** inclinación lineal del paisaje para una fuerza que se opone al movimiento en +x.

La energía térmica se convierte entre joules y pN·nm para mantener coherencia dimensional. `EnergyLandscape` es una superficie de exploración y visualización; sus parámetros no se estiman a partir de las tasas del modelo cinético.

### 6.6. Otra formulación conformacional

El módulo `visualization.energy_landscape` contiene una segunda formulación independiente con coordenada \(q\in[-1,1]\), donde \(q=-1\) representa visualmente una conformación no acoplada y \(q=+1\) una conformación acoplada. Esta convención no es la misma que la coordenada \([0,1]\) de `EnergyLandscape`. No se deben mezclar sin convertir los valores explícitamente.

---

## 7. Referencia de la API

Esta sección describe las clases y funciones públicas incluidas en el código actual. Los métodos que comienzan con guion bajo (`_`) son auxiliares internos y no forman parte de la API pública estable.

### 7.1. `core`

#### `State`

**Importación:**

```python
from protein_motor_sim.core import State
```

Representa un estado efectivo del motor.

**Atributos:**

| Atributo | Tipo | Descripción |
|---|---|---|
| `name` | `str` | Identificador del estado dentro de la red. |
| `description` | `str` | Descripción legible. |
| `is_terminal` | `bool` | Indica si entrar a este estado termina la simulación. |

**Métodos:**

- `__post_init__()`: valida el nombre, la descripción y el indicador terminal al crear la instancia.

Ejemplo:

```python
from protein_motor_sim.core import State

bound = State("bound_apo", "Motor unido sin ATP")
detached = State("detached", "Motor desprendido", is_terminal=True)
```

#### `Environment`

**Importación:** `from protein_motor_sim.core import Environment`

Contiene las condiciones experimentales que se suministran a las leyes de tasa.

**Atributos:**

| Atributo | Unidad | Descripción |
|---|---|---|
| `atp_concentration` | mol/L (M) | Concentración de ATP. |
| `external_force_N` | N | Fuerza firmada; positiva si se opone al avance +x. |
| `temperature_K` | K | Temperatura absoluta. |

**Métodos:**

- `__post_init__()`: valida que los valores sean números reales finitos, que ATP no sea negativo y que la temperatura sea positiva.

Es una clase inmutable (`frozen=True`), adecuada para describir una condición experimental fija durante una corrida. Las dependencias temporales o cambios de ambiente durante una trayectoria requieren una extensión del simulador.

#### `Transition`

**Importación:** `from protein_motor_sim.core import Transition`

Representa un evento estocástico de un estado de origen a uno de destino.

**Atributos:**

| Atributo | Tipo/unidad | Descripción |
|---|---|---|
| `source` | `str` | Nombre del estado de origen. |
| `target` | `str` | Nombre del estado de destino. |
| `rate_law` | callable | Objeto o función que recibe `Environment` y devuelve una tasa. |
| `event_name` | `str` | Nombre del evento registrado en la trayectoria. |
| `displacement_nm` | nm | Cambio de posición asociado al evento; puede ser negativo. |
| `atp_consumed` | entero | Moléculas de ATP contabilizadas como consumidas. |

**Métodos:**

- `__post_init__()`: valida nombres, ley invocable, desplazamiento finito y consumo no negativo.
- `rate(environment)`: evalúa la ley de tasa en el ambiente suministrado y devuelve `s⁻¹`. Lanza `ValueError` si la tasa es negativa o no finita.

#### `Track`

Representa una pista periódica unidimensional, como aproximación geométrica de un microtúbulo o un filamento.

**Atributos:**

| Atributo | Unidad | Descripción |
|---|---|---|
| `name` | — | Nombre de la pista. |
| `lattice_spacing_nm` | nm | Separación entre sitios. |
| `polarity` | — | Orientación +1 o -1 del eje. |
| `origin_nm` | nm | Coordenada del sitio índice cero. |

**Métodos:**

- `__post_init__()`: valida nombre, espaciamiento, polaridad y origen.
- `site_position_nm(site_index)`: convierte un índice entero de sitio a posición en nm.
- `nearest_site_index(position_nm)`: devuelve el índice del sitio más cercano a una posición en nm.

`Track` define la geometría de la pista, pero en la simulación cinética actual la posición se actualiza con `Transition.displacement_nm`; no se utiliza todavía como restricción dinámica automática.

#### `Trajectory`

Almacena los registros de una realización estocástica. Sus listas están alineadas por índice: el registro `i` tiene tiempo, posición, estado y evento correspondientes.

**Atributos:**

| Atributo | Unidad | Descripción |
|---|---|---|
| `times_s` | s | Tiempos registrados. |
| `positions_nm` | nm | Posiciones longitudinales. |
| `states` | — | Estados después de cada registro. |
| `events` | — | Eventos asociados a cada registro. |
| `atp_consumed_total` | moléculas | Consumo acumulado contabilizado. |

**Métodos y propiedades:**

- `__post_init__()`: comprueba que las listas tengan la misma longitud, que los tiempos no retrocedan y que los valores sean válidos.
- `record(time_s, position_nm, state, event, atp_delta=0)`: agrega un registro y suma `atp_delta` al consumo total.
- `duration_s`: duración entre el primer y último registro; vale cero si hay menos de dos.
- `displacement_nm`: desplazamiento neto final menos inicial.
- `path_length_nm`: suma de los módulos de los cambios de posición entre registros; incluye retrocesos.
- `mean_velocity_nm_s`: desplazamiento neto dividido por duración.
- `final_state`: último estado o `None` si no hay registros.
- `number_of_events`: número de registros cuyo evento no es `initial`. Por tanto, también puede contar `observation_end`.
- `to_dict()`: devuelve una copia de los datos en un diccionario serializable.

**Distinción importante:** `displacement_nm` es desplazamiento neto; `path_length_nm` es distancia total recorrida. No son la misma magnitud.

#### `Motor`

Clase abstracta que define el contrato que debe cumplir cada modelo de motor.

**Propiedades y métodos abstractos:**

- `name`: nombre del modelo.
- `step_size_nm`: tamaño de paso nominal en nm.
- `build_network()`: construye y devuelve la `ReactionNetwork` del motor.

**Método concreto:**

- `validate()`: verifica nombre, tamaño de paso finito y positivo, y que se pueda construir la red.

Para añadir un nuevo motor se debe heredar de `Motor` e implementar las propiedades y el método abstractos.

### 7.2. `kinetics`

#### `RateLaw`

Es un `Protocol` que especifica el contrato de una ley de tasa: debe poder llamarse como `rate_law(environment)` y devolver una tasa en `s⁻¹`.

#### `ConstantRate`

Representa una tasa independiente del ambiente.

- `rate_s`: tasa constante en `s⁻¹`.
- `__post_init__()`: comprueba que la tasa sea no negativa y finita.
- `__call__(environment)`: devuelve la tasa; el ambiente se ignora.

#### `ATPBindingRate`

Representa una asociación bimolecular de ATP convertida a tasa pseudo-primer orden.

- `association_rate_M_s`: constante de asociación en `M⁻¹ s⁻¹`.
- `__post_init__()`: valida la constante.
- `__call__(environment)`: devuelve `association_rate_M_s * environment.atp_concentration`, en `s⁻¹`.

#### `BellRate`

Envuelve otra ley de tasa y añade dependencia con la fuerza externa.

**Atributos:**

- `base_rate`: ley de tasa sin la corrección de fuerza.
- `distance_m`: distancia característica en metros.
- `force_direction`: debe ser +1 o -1; define el signo de la sensibilidad.
- `load_fraction`: fracción efectiva entre 0 y 1.

**Métodos:**

- `__post_init__()`: valida distancia, dirección y fracción.
- `__call__(environment)`: calcula la tasa modificada usando fuerza y temperatura del ambiente.

La convención de `Environment` considera positiva la carga opuesta al avance +x. Con `force_direction=+1`, esa carga reduce la tasa; con `force_direction=-1`, la aumenta. La interpretación concreta depende del evento al que se aplique la ley.

#### `ReactionNetwork`

Almacena estados y transiciones, y organiza las transiciones salientes de cada estado.

**Constructor:**

```python
ReactionNetwork(states, transitions, initial_state)
```

- `states`: iterable de objetos `State`.
- `transitions`: iterable de objetos `Transition`.
- `initial_state`: nombre del estado inicial.

**Métodos:**

- `outgoing(state_name)`: devuelve una tupla con las transiciones salientes del estado indicado.
- `rates(state_name, environment)`: devuelve pares `(transition, rate)` para todas las transiciones salientes, evaluadas en el ambiente actual.

El constructor verifica que los nombres sean únicos, que exista el estado inicial y que los estados de origen y destino de cada transición pertenezcan a la red.

### 7.3. Modelos de motores

#### `KinesinParameters`

Contenedor inmutable de parámetros del modelo efectivo de kinesina-1.

| Parámetro | Valor predeterminado | Unidad |
|---|---:|---|
| `atp_association_rate_M_s` | `1.0e6` | M⁻¹ s⁻¹ |
| `hydrolysis_rate_s` | `80.0` | s⁻¹ |
| `forward_step_rate_s` | `100.0` | s⁻¹ |
| `backward_step_rate_s` | `0.05` | s⁻¹ |
| `detachment_rate_s` | `0.2` | s⁻¹ |
| `step_size_nm` | `8.2` | nm |
| `force_distance_m` | `1.0e-9` | m |

`__post_init__()` valida las tasas y parámetros geométricos. Estos valores son ilustrativos, no valores experimentales certificados.

#### `Kinesin1`

Implementa la interfaz `Motor` para la red efectiva de kinesina-1.

- `parameters`: objeto `KinesinParameters`; se crea uno predeterminado si no se suministra.
- `name`: propiedad que devuelve `"Kinesin-1"`.
- `step_size_nm`: propiedad que devuelve el tamaño de paso de los parámetros.
- `build_network()`: construye y devuelve la red cinética efectiva llamando a `build_kinesin1_network(parameters)`.

#### `build_kinesin1_network(parameters)`

Construye la red cinética reducida que actualmente utiliza el simulador. Incluye los estados:

- `bound_apo`: motor unido al microtúbulo sin ATP unido.
- `atp_bound`: estado efectivo con ATP unido.
- `post_hydrolysis`: estado efectivo posterior a la hidrólisis.
- `detached`: estado terminal de desprendimiento.

Incluye eventos de unión de ATP, hidrólisis, paso hacia adelante, paso hacia atrás y desprendimiento. La transición de hidrólisis contabiliza una molécula de ATP. Los pasos modifican la posición mediante `displacement_nm`.

La red no resuelve las dos cabezas por separado, la unión explícita de ADP/Pi ni todos los intermediarios mecanoquímicos.

### 7.4. `simulation`

#### `SimulationStrategy`

Interfaz abstracta para los algoritmos de simulación.

- `run(motor, environment, t_max, seed=None)`: contrato que deben implementar las estrategias concretas.
- Entradas: motor, ambiente, tiempo máximo en segundos y semilla opcional.
- Salida: objeto `Trajectory`.

#### `GillespieSimulator`

Implementa el algoritmo directo de Gillespie para redes de transiciones con tasas constantes entre eventos.

**Método:**

```python
run(motor, environment, t_max, seed=None, max_events=1_000_000)
```

- `motor`: instancia de una clase derivada de `Motor`.
- `environment`: condiciones experimentales.
- `t_max`: tiempo máximo en segundos.
- `seed`: semilla opcional para reproducibilidad.
- `max_events`: límite de seguridad de eventos.
- **Devuelve:** `Trajectory`.

La simulación empieza en `network.initial_state` y posición cero. Se detiene cuando alcanza `t_max`, entra a un estado terminal o no quedan tasas positivas. Si llega al límite `max_events`, lanza `RuntimeError`.

#### `EnsembleResult`

Contenedor de una lista de trayectorias.

- `trajectories`: lista de `Trajectory`.
- `size`: propiedad con el número de trayectorias almacenadas.

#### `run_ensemble(...)`

Ejecuta varias realizaciones independientes:

```python
run_ensemble(simulator, motor, environment, t_max, n_runs, seed=None)
```

Crea semillas hijas a partir de una semilla maestra y devuelve `EnsembleResult`. `n_runs` debe ser positivo.

Ejemplo:

```python
from protein_motor_sim.simulation.ensemble import run_ensemble

ensemble = run_ensemble(
    simulator=GillespieSimulator(),
    motor=Kinesin1(),
    environment=Environment(atp_concentration=1e-3),
    t_max=1.0,
    n_runs=100,
    seed=1234,
)
print(ensemble.size)
```

### 7.5. `mechanics`

#### `Force` y `net_force`

`Force(value_N, label="external")` representa una fuerza escalar firmada en newtons.

- `value_N`: fuerza en N.
- `label`: etiqueta descriptiva.
- `__post_init__()`: comprueba que la fuerza sea finita.

`net_force(*forces)` suma los valores de las fuerzas suministradas y devuelve otra instancia de `Force` con etiqueta `net`. Esta operación supone que todas las fuerzas son colineales y utilizan el mismo eje y convención de signo.

#### `HookeanSpring`

Representa un resorte lineal.

- `stiffness_N_m`: rigidez en N/m.
- `rest_length_m`: longitud natural en m.
- `__post_init__()`: valida que rigidez y longitud natural no sean negativas.
- `force_N(length_m)`: devuelve la fuerza restauradora según `F = -k (length - rest_length)`.

#### `brownian_displacement`

Genera un desplazamiento browniano unidimensional:

```python
brownian_displacement(diffusion_coefficient_m2_s, delta_time_s, rng=None)
```

El incremento se extrae de una distribución normal de media cero y varianza `2 * D * dt`.

- `diffusion_coefficient_m2_s`: coeficiente de difusión en m²/s.
- `delta_time_s`: intervalo temporal en s.
- `rng`: generador `numpy.random.Generator` opcional.
- **Devuelve:** desplazamiento en metros.

Es una función auxiliar independiente; el resultado no se integra automáticamente en `GillespieSimulator`.

#### `Cargo`

Modelo de una carga puntual simplificada.

- `position_m`: posición en m.
- `drag_coefficient_N_s_m`: coeficiente de arrastre lineal en N·s/m.
- `mass_kg`: masa efectiva en kg, reservada para extensiones inerciales.
- `__post_init__()`: valida que el coeficiente de arrastre y la masa no sean negativos.
- `drag_force_N(velocity_m_s)`: calcula `-gamma * velocity`, en N.

#### `EnergyLandscape`

Modelo fenomenológico de energía `U(x, q)`.

**Parámetros del constructor:**

| Parámetro | Unidad / dominio | Función |
|---|---|---|
| `period_nm` | nm, positivo | Periodicidad espacial. |
| `spatial_barrier_kBT` | kBT, no negativo | Amplitud de barrera espacial. |
| `conformational_barrier_kBT` | kBT, no negativo | Barrera de la coordenada conformacional. |
| `conformational_bias_kBT` | kBT | Sesgo energético lineal entre conformaciones. |
| `phase_shift` | fracción entre 0 y 1 | Desplazamiento relativo de fase con `q`. |
| `coupling_kBT` | kBT | Amplitud del acoplamiento espacial-conformacional. |
| `opposing_force_pN` | pN | Carga que se opone al avance +x. |
| `temperature_K` | K, positivo | Temperatura para calcular `kBT`. |

**Propiedades y métodos:**

- `thermal_energy_J`: devuelve `k_B T` en joules.
- `thermal_energy_pN_nm`: devuelve `k_B T` en pN·nm.
- `energy_kBT(x_nm, q, opposing_force_pN=None)`: evalúa `U/(kBT)`. Acepta escalares o arreglos NumPy compatibles por *broadcasting*. `q` debe estar en [0, 1]. Si no se especifica una fuerza, se utiliza la almacenada en el objeto.
- `grid(x_range_nm, q_range=(0,1), nx=240, nq=120, opposing_force_pN=None)`: genera las mallas `X`, `Q` y la energía `U`, todas como arreglos 2D.
- `energy_profile_kBT(x_nm, q, opposing_force_pN=None)`: evalúa el perfil longitudinal manteniendo fija la coordenada `q`.

Ejemplo:

```python
import numpy as np
from protein_motor_sim.mechanics import EnergyLandscape

landscape = EnergyLandscape(temperature_K=310.0, opposing_force_pN=1.5)
x = np.linspace(0, 32.8, 300)
profile = landscape.energy_profile_kBT(x, q=0.5)
X, Q, U = landscape.grid((0, 32.8), nx=200, nq=100)
```

### 7.6. `analysis`

#### `TrajectoryAnalysis`

Contenedor inmutable de observables calculados para una trayectoria:

- `velocity_nm_s`: velocidad media neta en nm/s.
- `run_length_nm`: valor absoluto del desplazamiento neto en nm.
- `path_length_nm`: distancia total recorrida incluyendo retrocesos, en nm.
- `duration_s`: duración en s.
- `atp_consumed`: consumo acumulado contabilizado.
- `forward_steps`: número de eventos `forward_step`.
- `backward_steps`: número de eventos `backward_step`.
- `detached`: indica si la trayectoria incluye un evento de desprendimiento.

#### `analyze_trajectory(trajectory)`

Calcula y devuelve `TrajectoryAnalysis`. La longitud de recorrido de este resumen es `abs(trajectory.displacement_nm)`; para la distancia acumulada se debe consultar `path_length_nm`.

#### `EnsembleStatistics`

Contenedor de estadísticas descriptivas:

- `mean_velocity_nm_s` y `std_velocity_nm_s`.
- `mean_run_length_nm` y `std_run_length_nm`.
- `number_of_trajectories`.

#### `summarize_trajectories(trajectories)`

Calcula media y desviación estándar muestral de velocidad y longitud neta absoluta para un iterable de trayectorias. Si solo hay una trayectoria, fija las desviaciones estándar en cero. Lanza `ValueError` si el iterable está vacío.

#### `sweep_atp_concentration(...)`

Ejecuta conjuntos de simulaciones para varias concentraciones de ATP:

```python
sweep_atp_concentration(
    simulator,
    motor,
    environment,
    concentrations_M,
    t_max,
    n_runs=20,
    seed=None,
)
```

Para cada concentración crea un nuevo `Environment` cambiando solo `atp_concentration`, ejecuta `n_runs` trayectorias y calcula estadísticas de velocidad. Devuelve una lista de diccionarios con:

- `atp_concentration_M`
- `mean_velocity_nm_s`
- `std_velocity_nm_s`

### 7.7. `visualization`

Las funciones de visualización importan Matplotlib cuando se ejecutan. La mayoría devuelve los ejes (`Axes`) o el objeto de animación para que el usuario pueda personalizarlo.

#### Gráficas de trayectorias

- `plot_trajectory(trajectory, ax=None)`: gráfica escalonada de posición (nm) frente a tiempo (s). Puede dibujar sobre ejes existentes.
- `plot_atp_sweep(results, ax=None)`: representa velocidad media frente a concentración de ATP y utiliza la desviación estándar como barras de error.
- `plot_kinesin_schematic(position_nm=0.0, ax=None)`: dibujo conceptual estático de kinesina sobre una pista. No es una estructura molecular a escala.

#### Animaciones

##### `AnimationStyle`

Objeto inmutable que configura el aspecto de `animate_kinesin_walk`.

| Atributo | Función |
|---|---|
| `step_size_nm` | Separación nominal entre sitios; valor predeterminado 8.2 nm. |
| `frames_per_step` | Fotogramas usados para interpolar cada paso. |
| `arc_height` | Altura gráfica del arco de la cabeza móvil; no es una altura molecular calibrada. |
| `interval_ms` | Tiempo entre fotogramas en ms. |
| `trail_length` | Cantidad aproximada de posiciones recientes que se muestran en el rastro. |
| `show_trail` | Activa/desactiva el rastro. |
| `show_time` | Activa/desactiva el indicador de tiempo. |

##### Funciones

- `animate_kinesin_walk(trajectory, style=None, figsize=(12.5, 7.0), repeat=False)`: crea una animación esquemática de dos cabezas, cuello, tallo, carga y pista de tubulina. Los avances y retrocesos se interpolan mediante arcos.
- `animate_trajectory(trajectory, interval_ms=50)`: interfaz de compatibilidad que llama a `animate_kinesin_walk` con un `AnimationStyle` básico.
- `save_animation(animation, filepath, fps=20, dpi=120)`: guarda una animación como `.gif` o `.mp4`. MP4 requiere FFmpeg disponible.

**Limitación de la animación:** la trayectoria actual almacena una posición longitudinal del motor, no las coordenadas independientes de las dos cabezas. La ubicación de cada cabeza y la forma del movimiento *hand-over-hand* se reconstruyen gráficamente a partir de los eventos; no proceden de una dinámica estructural simulada.

#### Paisajes de energía: funciones alternativas

El módulo `visualization.energy_landscape` ofrece otra formulación fenomenológica, con coordenada conformacional `q` entre -1 y +1.

- `thermal_energy_pN_nm(temperature_K=310.0)`: calcula `k_B T` en pN·nm.
- `periodic_potential_kbt(x_nm, lattice_spacing_nm=8.2, barrier_kbt=4.0, opposing_force_pN=0.0, temperature_K=310.0, reference_position_nm=0.0)`: evalúa un potencial periódico unidimensional inclinado por una carga opuesta.
- `conformational_energy_surface_kbt(x_nm, q, ...)`: genera mallas `X`, `Q`, `U` de una superficie con `q` entre -1 y +1.
- `plot_periodic_energy_landscape(...)`: compara perfiles periódicos para varias fuerzas.
- `plot_conformational_energy_surface(...)`: representa una superficie conformacional 2D mediante contornos.
- `plot_state_energy_diagram(state_energies_kbt, barriers_kbt=None, ax=None)`: dibuja energías relativas de estados y barreras esquemáticas introducidas por el usuario.

`plot_state_energy_diagram` conserva el orden de inserción de `state_energies_kbt`. Si no se proporciona una barrera para una transición consecutiva, usa una altura predeterminada igual a la energía mayor de los dos estados más 1.5 kBT. Las barreras deben ser mayores o iguales que las energías de los estados adyacentes.

#### Mapas y trayectorias sobre paisajes

El módulo `visualization.energy_maps` utiliza la clase `mechanics.EnergyLandscape`, cuya coordenada `q` está definida en [0, 1].

- `plot_energy_landscape_2d(landscape, x_range_nm, q_range=(0,1), resolution=(260,150), opposing_force_pN=None, levels=28, ax=None)`: crea un mapa de contornos 2D y devuelve `(ax, contour)`.
- `plot_energy_landscape_3d(landscape, x_range_nm, q_range=(0,1), resolution=(180,90), opposing_force_pN=None, ax=None)`: crea una superficie 3D y devuelve `(ax, surface)`.
- `plot_energy_profiles(landscape, x_range_nm, conformations, n_points=500, opposing_force_pN=None, ax=None)`: compara perfiles 1D para distintas etiquetas y valores de `q`. `conformations` es un diccionario ordenado del tipo `{"undocked": 0.1, "intermediate": 0.5, "docked": 0.9}`.
- `plot_trajectory_on_energy_landscape(trajectory, landscape, state_coordinates, x_range_nm=None, opposing_force_pN=None, ax=None)`: dibuja la trayectoria sobre el mapa. `state_coordinates` debe asociar explícitamente cada nombre de estado de la trayectoria con una coordenada `q` entre 0 y 1.
- `animate_trajectory_on_energy_landscape(trajectory, landscape, state_coordinates, x_range_nm=None, interval_ms=70, opposing_force_pN=None)`: anima un marcador que recorre el mapa. Devuelve un objeto `FuncAnimation`.

El mapeo estado-`q` lo debe proporcionar el usuario. La red cinética no contiene actualmente una coordenada conformacional calibrada; asignar valores de `q` es una hipótesis de visualización y debe documentarse.

El módulo `visualization.energy_maps` también contiene `plot_state_energy_diagram(state_energies_kbt, barriers_kbt=None, ax=None)`, una segunda implementación del diagrama discreto. Esta variante describe explícitamente los valores de barrera como energías absolutas de estado de transición. No se reexporta desde `visualization.__init__`; se importa directamente desde `protein_motor_sim.visualization.energy_maps` si se necesita esa variante.

### 7.8. `io`

#### `save_trajectory(trajectory, filepath)`

Serializa una trayectoria como JSON. Crea los directorios padre si no existen. Guarda tiempos, posiciones, estados, eventos y consumo total de ATP.

#### `load_trajectory(filepath)`

Lee un JSON y reconstruye un objeto `Trajectory`. Comprueba que los cuatro arreglos tengan la misma longitud. El consumo total de ATP se restaura como metadato global.

Ejemplo:

```python
from protein_motor_sim.io.serialization import save_trajectory, load_trajectory

save_trajectory(trajectory, "results/run_001.json")
restored = load_trajectory("results/run_001.json")
```

---

## 8. Notebooks de Jupyter

Los notebooks son el laboratorio interactivo recomendado para explorar el simulador. Los primeros catorce desarrollan el uso general y el análisis de simulaciones. Los notebooks 15–24 se enfocan en animaciones y energía.

| N.º | Archivo | Contenido |
|---:|---|---|
| 01 | `01_simulacion_basica.ipynb` | Primera simulación de kinesina-1. |
| 02 | `02_explorar_red_cinetica.ipynb` | Estados, transiciones y tasas de la red. |
| 03 | `03_inspeccion_trayectoria_eventos.ipynb` | Inspección de eventos, estados y posiciones. |
| 04 | `04_dependencia_concentracion_atp.ipynb` | Barrido de concentración de ATP. |
| 05 | `05_dependencia_fuerza_externa.ipynb` | Efecto de la carga externa. |
| 06 | `06_ensamble_estadistico.ipynb` | Comparación de realizaciones independientes. |
| 07 | `07_tiempos_espera.ipynb` | Tiempos de espera y distribución exponencial. |
| 08 | `08_consumo_atp_acoplamiento.ipynb` | Contabilización de hidrólisis y eventos mecánicos. |
| 09 | `09_mecanica_auxiliar.ipynb` | Resortes, fuerzas y desplazamiento browniano. |
| 10 | `10_geometria_microtubulo.ipynb` | Índices de sitio, espaciamiento y polaridad. |
| 11 | `11_guardar_cargar_resultados.ipynb` | Serialización de trayectorias. |
| 12 | `12_animacion_trayectoria.ipynb` | Animación esquemática de una trayectoria. |
| 13 | `13_sensibilidad_parametros.ipynb` | Variación de parámetros del modelo. |
| 14 | `14_reproducibilidad_semillas.ipynb` | Semillas aleatorias y reproducibilidad. |
| 15 | `15_animacion_kinesina_esquematica.ipynb` | Animación detallada de dos cabezas esquemáticas. |
| 16 | `16_mapa_energia_2d.ipynb` | Mapa de contornos de energía. |
| 17 | `17_superficie_energia_3d.ipynb` | Superficie energética tridimensional. |
| 18 | `18_perfiles_energia_y_fuerza.ipynb` | Perfiles energéticos bajo distintas cargas. |
| 19 | `19_trayectoria_sobre_paisaje_energia.ipynb` | Superposición de trayectoria sobre paisaje energético. |
| 20 | `20_animacion_trayectoria_sobre_mapa_energia.ipynb` | Animación de una trayectoria sobre el mapa. |
| 21 | `21_explorar_parametros_del_paisaje.ipynb` | Sensibilidad a parámetros del paisaje. |
| 22 | `22_diagrama_energias_estados_y_barreras.ipynb` | Diagrama de energías y barreras discretas. |
| 23 | `23_mapa_conformacional_acoplamiento.ipynb` | Coordenada conformacional y acoplamiento. |
| 24 | `24_exportar_animaciones.ipynb` | Exportación de animaciones GIF/MP4. |

### Abrir JupyterLab

Desde la raíz del proyecto y con el entorno virtual activado:

```bash
source .venv/bin/activate
jupyter lab
```

Los notebooks esperan que el paquete esté instalado en modo editable (`pip install -e .`) o que se ejecute Jupyter desde un entorno donde `protein_motor_sim` sea importable.

---

## 9. Unidades y convenciones

Las unidades deben mantenerse explícitas al definir parámetros o comparar resultados.

| Magnitud | Unidad interna / esperada |
|---|---|
| Tiempo | segundo (s) |
| Posición longitudinal | nanómetro (nm) |
| Tamaño de paso | nanómetro (nm) |
| Fuerza del entorno | newton (N) |
| Fuerza en paisajes energéticos | piconewton (pN) |
| Temperatura | kelvin (K) |
| Concentración de ATP | mol/L (M) |
| Tasa pseudo-primer orden | s⁻¹ |
| Constante de asociación de ATP | M⁻¹ s⁻¹ |
| Constante elástica | N/m |
| Coeficiente de difusión | m²/s |
| Longitud de resorte | m |
| Coeficiente de arrastre | N·s/m |
| Energía en los paisajes | kBT |

### Convención de fuerza

En `Environment.external_force_N`, una fuerza positiva se interpreta como una carga opuesta al movimiento hacia +x. En los paisajes energéticos, `opposing_force_pN` utiliza la misma convención, pero se expresa en pN. Recuerda convertir unidades al pasar de una representación a otra:

\[
1\;\mathrm{pN}=10^{-12}\;\mathrm{N}.
\]

### Coordenadas conformacionales

Hay dos formulaciones en la librería:

- `mechanics.EnergyLandscape`: `q` está en [0, 1].
- `visualization.energy_landscape.conformational_energy_surface_kbt`: `q` está en [-1, 1].

No intercambies directamente valores de `q` entre ambas formulaciones.

---

## 10. Pruebas y calidad del código

Las pruebas se ejecutan desde la raíz del repositorio:

```bash
pytest -v
```

Para comprobar estilo y errores básicos con Ruff:

```bash
ruff check src tests
```

La suite comprueba, entre otros aspectos:

- Validación de estados, condiciones y pistas.
- Evaluación de leyes de tasa.
- Respuesta de las tasas a la concentración de ATP y la carga.
- Reproducibilidad del algoritmo estocástico para una semilla fija.
- Registro de eventos y magnitudes de trayectoria.
- Comportamiento de componentes mecánicos auxiliares.
- Evaluación y visualización de paisajes energéticos.

Las pruebas de software verifican la implementación y los contratos computacionales. **No constituyen por sí mismas una validación biológica o experimental del modelo.**

---

## 11. Limitaciones actuales

Las siguientes limitaciones deben considerarse antes de interpretar los resultados como predicciones físicas o biológicas.

1. **Red cinética reducida.** La kinesina se representa mediante estados efectivos `bound_apo`, `atp_bound`, `post_hydrolysis` y `detached`. No están explícitos todos los estados de ambas cabezas, los intermediarios de ADP/Pi ni los mecanismos detallados de coordinación.
2. **Parámetros ilustrativos.** Los valores predeterminados de `KinesinParameters` sirven para ejecutar y probar el software. Deben sustituirse por parámetros procedentes de experimentos o de modelos publicados, con sus condiciones y unidades.
3. **Fuerza fenomenológica.** La dependencia de fuerza utiliza una relación tipo Bell. No describe necesariamente la respuesta correcta de todas las transiciones y no incluye por sí sola un modelo mecánico completo del cuello.
4. **Mecánica desacoplada.** Los componentes de resorte, arrastre y ruido browniano se pueden utilizar de forma independiente, pero no están integrados en un solver de Langevin acoplado a Gillespie.
5. **Paisajes ilustrativos.** Los potenciales `EnergyLandscape` y `visualization.energy_landscape` no son superficies de energía libre experimentales ni potenciales atomísticos. Sus parámetros no se infieren automáticamente de la red cinética.
6. **No hay balance detallado impuesto.** No se impone todavía una relación de balance detallado local entre tasas, diferencias de energía libre y potencial químico de ATP. Por ello, no se debe inferir un diagrama termodinámico únicamente a partir de las tasas.
7. **Animación esquemática.** La animación reconstruye visualmente dos cabezas a partir de una coordenada longitudinal y etiquetas de eventos. La trayectoria no contiene posiciones individuales de ambas cabezas y la escena vertical no está a escala.
8. **Sin simulación colectiva implementada.** No hay todavía un modelo de varios motores compartiendo una carga, compitiendo por una pista o distribuyendo fuerza.
9. **Miosina y dineína pendientes.** Sus carpetas son puntos de extensión, no implementaciones funcionales.

### Uso responsable de resultados

Para una comparación cuantitativa con experimentos se debe documentar la fuente de cada parámetro, las condiciones experimentales, la estructura de la red de estados, las hipótesis de fuerza y la incertidumbre. Es recomendable comparar múltiples observables —velocidad, distribución de tiempos de espera, longitud de recorrido, probabilidad de desprendimiento y consumo de ATP— en lugar de ajustar el modelo a una sola curva.

---

## 12. Hoja de ruta

La hoja de ruta propuesta es:

### v0.1 — Núcleo estocástico

- Objetos fundamentales y redes de reacción.
- Modelo efectivo inicial de kinesina-1.
- Simulador Gillespie.
- Registro de trayectorias y análisis básico.

### Extensión de visualización y energía

- Animación esquemática tipo *hand-over-hand*.
- Mapas energéticos 2D y superficies 3D fenomenológicas.
- Perfiles energéticos bajo distintas cargas.
- Superposición de trayectorias y paisajes.

### Próximos desarrollos científicos

- Red mecanística de kinesina con estados explícitos de las dos cabezas.
- Tratamiento explícito de unión de ATP, hidrólisis, liberación de Pi y ADP, según el modelo elegido.
- Calibración de tasas con datos publicados y estimación de incertidumbres.
- Consistencia termodinámica y balance detallado local.
- Dinámica mecánica continua (por ejemplo, Langevin sobreamortiguado) acoplada a eventos discretos.
- Coordenadas individuales de las cabezas y modelo elástico del cuello.
- Interacción con cargas transportadas.
- Simulación de múltiples motores.
- Implementación de miosina y dineína.
- Documentación API automatizada y publicación de versiones estables.

Las versiones se deben etiquetar cuando el código, las pruebas y la documentación correspondientes estén consolidados; la hoja de ruta no implica que todas estas funcionalidades estén disponibles hoy.

---

## 13. Contribuir al proyecto

Para contribuir con un modelo, una ley cinética o un algoritmo nuevo:

1. Mantén las responsabilidades separadas por paquete.
2. Documenta clases, métodos y funciones con **Google-style docstrings**.
3. Añade anotaciones de tipo a la API pública.
4. Declara las unidades físicas en nombres, argumentos y documentación.
5. Añade pruebas unitarias para entradas válidas, inválidas y límites físicos.
6. Incluye un notebook que explique la hipótesis científica y cómo reproducir el resultado.
7. Distingue claramente parámetros medidos, parámetros ajustados y parámetros ilustrativos.
8. Evita que el núcleo científico dependa de herramientas de visualización.

Flujo sugerido para desarrollo:

```bash
git checkout -b feature/nombre-de-la-funcionalidad
# Editar src/, añadir tests/ y actualizar documentación.
pytest -v
ruff check src tests
git status
```

---

## 14. Licencia

Este proyecto se distribuye bajo la licencia indicada en el archivo [`LICENSE`](LICENSE). Consulta ese archivo para conocer los términos completos de uso, modificación y redistribución.

---

## Nota final

ProteinMotorSim pretende evolucionar desde un prototipo didáctico de cinética estocástica hacia una plataforma modular de modelado mecanoquímico de motores proteicos. La prioridad es mantener trazabilidad entre las hipótesis físicas, las ecuaciones, la implementación numérica y las visualizaciones. Una animación atractiva no sustituye la validación del modelo; cada representación debe indicar qué variables se simulan, cuáles se reconstruyen y cuáles son supuestos ilustrativos.
