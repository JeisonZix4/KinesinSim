# KineSIM

[![PyPI version](https://img.shields.io/pypi/v/kinesim)](https://pypi.org/project/kinesim/)
[![Python versions](https://img.shields.io/pypi/pyversions/kinesim)](https://pypi.org/project/kinesim/)

**KineSIM** es una librería de Python para construir, ejecutar, analizar y visualizar modelos computacionales de motores proteicos. Su primera implementación incluye un modelo cinético estocástico simplificado de kinesina-1.

> **Estado del proyecto:** KineSIM es un prototipo de investigación y aprendizaje. Los parámetros predeterminados son ilustrativos, no están calibrados experimentalmente. Las animaciones y los paisajes energéticos son representaciones esquemáticas o fenomenológicas; no son simulaciones atomísticas ni superficies de energía libre medidas.

## Instalación desde PyPI

Requiere Python 3.10 o superior.

```bash
python -m pip install --upgrade pip
python -m pip install kinesim
```

Para trabajar con los notebooks, gráficas y animaciones:

```bash
python -m pip install "kinesim[notebooks]"
```

El nombre de la distribución es `kinesim`, mientras que el namespace de importación se conserva como `protein_motor_sim`.

## Descargar el proyecto desde GitHub

Clona el repositorio para obtener el código fuente, las pruebas y los seis notebooks. Sustituye la URL de ejemplo por la dirección pública del repositorio KineSIM:

```bash
git clone https://github.com/<USUARIO>/<REPOSITORIO>.git
cd <REPOSITORIO>
```

Crea un entorno virtual e instala el proyecto en modo editable:

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\Activate.ps1    # Windows PowerShell
python -m pip install --upgrade pip
python -m pip install -e ".[notebooks,dev,docs]"
```

Registra el kernel y abre JupyterLab:

```bash
python -m ipykernel install --user --name kinesim --display-name "Python (KineSIM)"
jupyter lab
```

Selecciona el kernel **Python (KineSIM)** al abrir los notebooks.

## Uso básico

Este ejemplo crea el modelo de kinesina-1, define las condiciones experimentales, ejecuta una trayectoria con el algoritmo de Gillespie y calcula algunos observables:

```python
from protein_motor_sim import Environment, GillespieSimulator, Kinesin1
from protein_motor_sim.analysis import analyze_trajectory

motor = Kinesin1()
environment = Environment(
    atp_concentration=1.0e-3,  # mol/L
    external_force_N=0.0,      # N; positiva si se opone al avance +x
    temperature_K=310.0,       # K
)

simulator = GillespieSimulator()
trajectory = simulator.run(
    motor=motor,
    environment=environment,
    t_max=2.0,  # s
    seed=42,
)

results = analyze_trajectory(trajectory)
print("Velocidad (nm/s):", results.velocity_nm_s)
print("Desplazamiento neto (nm):", trajectory.displacement_nm)
print("ATP contabilizado:", results.atp_consumed)
```

## Notebooks

El repositorio incluye seis notebooks que presentan los experimentos y flujos de trabajo principales:

1. **Fundamentos y simulación:** red cinética, Gillespie y análisis de una trayectoria.
2. **Experimentos con ATP y fuerza:** influencia de las condiciones experimentales.
3. **Estadística y reproducibilidad:** conjuntos de simulaciones y tiempos de espera.
4. **Mecánica y paisajes de energía:** modelos auxiliares y superficies fenomenológicas.
5. **Animaciones y trayectorias energéticas:** visualización esquemática del movimiento.
6. **Mecánica, datos y reproducibilidad:** geometría, elasticidad, difusión y almacenamiento.

## Docker

KineSIM dispone de un `Dockerfile` preparado para ejecutar JupyterLab y los notebooks en un contenedor. Para descargar la imagen publicada, sustituye los marcadores por el usuario y el nombre exacto del repositorio de Docker Hub:

```bash
docker pull <DOCKERHUB_USER>/<IMAGE_NAME>:0.1.2
docker run --rm -it -p 8888:8888 \
  -v "$(pwd)/notebooks:/workspace/notebooks" \
  -v "$(pwd)/results:/workspace/results" \
  <DOCKERHUB_USER>/<IMAGE_NAME>:0.1.2
```

JupyterLab estará disponible en `http://localhost:8888`. El token de acceso se muestra en los registros del contenedor. No desactives la autenticación al exponer el servicio.

También puedes construir la imagen localmente desde la raíz del repositorio:

```bash
docker build -t kinesim:0.1.2 .
```

> **Enlace pendiente:** añade aquí la URL pública de la imagen de Docker Hub cuando confirmes el namespace y el nombre del repositorio.

## Documentación completa

La documentación técnica se genera con **Sphinx** e incluye:

- Fundamentos físicos y matemáticos del modelo.
- Hipótesis, unidades y limitaciones científicas.
- Descripción detallada de clases, funciones, argumentos y valores de retorno.
- Referencia automática de la API a partir de los docstrings del código.
- Guía de instalación, notebooks y desarrollo.

Consulta el índice de fuentes en [`docs/source/index.rst`](docs/source/index.rst). La página completa se genera localmente con:

```bash
python -m pip install -e ".[docs]"
python -m sphinx -b html docs/source docs/build/html
```

Abre `docs/build/html/index.html` en el navegador. La página de inicio de la documentación es `docs/source/index.rst`.

## Desarrollo y pruebas

Desde el repositorio clonado y con el entorno virtual activo:

```bash
python -m pip install -e ".[dev,notebooks,docs]"
pytest -v
ruff check src tests
```

## Distribución y enlaces

- **PyPI:** [pypi.org/project/kinesim](https://pypi.org/project/kinesim/)
- **GitHub:** sustituir por la URL pública del repositorio.
- **Docker Hub:** sustituir por la URL pública de la imagen.
- **Documentación Sphinx:** generar localmente con los comandos anteriores; se podrá enlazar aquí cuando se publique en un sitio web.

## Licencia

KineSIM se distribuye bajo los términos de la licencia MIT. Consulta el archivo [`LICENSE`](LICENSE).
