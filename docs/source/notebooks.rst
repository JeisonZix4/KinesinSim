Laboratorios Jupyter
===================

Los seis notebooks son laboratorios científicos guiados. Cada uno incluye
objetivos, fundamento matemático, unidades, configuración experimental,
código, interpretación de resultados, limitaciones y referencias.

Los archivos originales y editables se mantienen en ``notebooks/`` en la raíz
del repositorio. Durante la construcción de Sphinx, ``conf.py`` los copia a
``docs/source/tutoriales/`` y ``nbsphinx`` los incorpora a esta documentación.
Así se conserva una sola fuente de edición.

.. important::

   Sphinx renderiza las celdas Markdown y el código de los notebooks, pero no
   ejecuta las celdas durante la construcción. Para reproducir los experimentos,
   instala KineSIM y sus dependencias, abre el notebook en JupyterLab y ejecuta
   sus celdas en orden.

.. toctree::
   :maxdepth: 1
   :caption: Laboratorios disponibles

   tutoriales/index

Preparar el entorno
-------------------

Desde PyPI:

.. code-block:: bash

   python -m pip install "kinesim[notebooks]==0.1.2"
   python -m pip install jupyterlab
   jupyter lab

Para ejecutar los notebooks desde el repositorio en modo editable, consulta la
guía de :doc:`installation`.
