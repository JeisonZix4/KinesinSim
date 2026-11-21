# Laboratorios de KineSIM

Los seis notebooks de esta carpeta son la fuente original de los laboratorios
científicos. Cada notebook incluye objetivos, fundamento físico y matemático,
unidades, configuración experimental, código, interpretación, limitaciones y
referencias.

## Preparar el entorno desde PyPI

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
python -m pip install --upgrade pip
python -m pip install "kinesim[notebooks]==0.1.2"
python -m pip install jupyterlab
jupyter lab
```

Selecciona el kernel del entorno virtual. Cada notebook incluye además una
celda de instalación fijada a la versión 0.1.2 para poder ejecutarse de forma
independiente.

La distribución se llama `kinesim`; el namespace de importación se conserva
como `protein_motor_sim`.

## Documentación web con Sphinx

La documentación Sphinx incorpora los notebooks mediante `nbsphinx`. Los
archivos de esta carpeta son la fuente canónica: durante la construcción,
`docs/source/conf.py` los copia a `docs/source/tutoriales/` para renderizarlos.
No edites las copias generadas dentro de `docs/source/tutoriales/`.

Instala y construye la documentación desde la raíz del repositorio:

```bash
python -m pip install -e ".[notebooks,dev,docs]"
python -m sphinx -b html docs/source docs/build/html
```

Sphinx muestra las celdas Markdown y de código, pero no ejecuta los notebooks
durante la construcción. Para reproducir los experimentos, ejecútalos desde
JupyterLab.
