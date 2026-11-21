Instalación y primeros pasos
============================

Requisitos
----------

* Python 3.10 o superior.
* ``pip``.
* JupyterLab e IPykernel para ejecutar los notebooks (incluidos en el extra
  ``notebooks``).
* Docker, si se desea ejecutar la imagen de contenedor.

Instalar desde PyPI
-------------------

Para utilizar el núcleo de la librería:

.. code-block:: bash

   python -m pip install --upgrade pip
   python -m pip install kinesim

Para instalar también las dependencias de notebooks, gráficas y animaciones:

.. code-block:: bash

   python -m pip install "kinesim[notebooks]"

El nombre de distribución es ``kinesim``. El namespace de importación se
conserva por compatibilidad como ``protein_motor_sim``.

Primer ejemplo
--------------

.. code-block:: python

   from protein_motor_sim import Environment, GillespieSimulator, Kinesin1
   from protein_motor_sim.analysis import analyze_trajectory

   motor = Kinesin1()
   environment = Environment(
       atp_concentration=1.0e-3,
       external_force_N=0.0,
       temperature_K=310.0,
   )

   trajectory = GillespieSimulator().run(
       motor=motor,
       environment=environment,
       t_max=2.0,
       seed=42,
   )
   observables = analyze_trajectory(trajectory)
   print(observables)

Descargar desde GitHub
----------------------

La URL depende del propietario del repositorio. Sustituye los marcadores por
la dirección pública real:

.. code-block:: bash

   git clone https://github.com/<USUARIO>/<REPOSITORIO>.git
   cd <REPOSITORIO>
   python -m venv .venv
   source .venv/bin/activate
   python -m pip install -e ".[notebooks,dev,docs]"

En Windows PowerShell, activa el entorno con:

.. code-block:: powershell

   .venv\Scripts\Activate.ps1

JupyterLab
----------

.. code-block:: bash

   python -m ipykernel install --user --name kinesim \
       --display-name "Python (KineSIM)"
   jupyter lab

Abre la carpeta ``notebooks/`` y selecciona el kernel ``Python (KineSIM)``.

Docker
------

El repositorio incluye un ``Dockerfile`` para construir localmente una imagen
con KineSIM y JupyterLab:

.. code-block:: bash

   docker build -t kinesim:0.1.2 .
   mkdir -p results
   docker run --rm -it -p 8888:8888 \
       -v "$(pwd)/notebooks:/workspace/notebooks" \
       -v "$(pwd)/results:/workspace/results" \
       kinesim:0.1.2

Para descargar desde Docker Hub se necesita el namespace exacto del repositorio
publicado por el mantenedor:

.. code-block:: bash

   docker pull <DOCKERHUB_USER>/<IMAGE_NAME>:0.1.2

.. warning::

   ``<DOCKERHUB_USER>/<IMAGE_NAME>`` es un marcador, no una dirección pública
   verificada. Debe sustituirse por la referencia real de Docker Hub. JupyterLab
   conserva la autenticación por token; consulta los logs del contenedor para
   obtenerlo. No desactives la autenticación al exponer el puerto.

Extras disponibles
------------------

.. list-table:: Extras definidos en ``pyproject.toml``
   :header-rows: 1
   :widths: 20 80

   * - Extra
     - Uso
   * - ``viz``
     - Matplotlib para gráficas y animaciones.
   * - ``notebooks``
     - Matplotlib, Pandas, Pillow, JupyterLab e IPykernel.
   * - ``science``
     - SciPy para extensiones científicas.
   * - ``dev``
     - Pytest, Ruff, Build y Twine.
   * - ``docs``
     - Sphinx, Furo y nbsphinx para generar esta documentación e integrar los notebooks.
