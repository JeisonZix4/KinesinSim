Desarrollo y construcción de la documentación
==============================================

Instalación del entorno de desarrollo
-------------------------------------

Desde la raíz del repositorio:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -e ".[notebooks,dev,docs]"

Pruebas y estilo
----------------

.. code-block:: bash

   pytest -v
   ruff check src tests

Construir Sphinx
----------------

.. code-block:: bash

   python -m sphinx -b html docs/source docs/build/html

Abre ``docs/build/html/index.html`` en el navegador. Para reconstruir la
página, vuelve a ejecutar el comando después de modificar los archivos
``.rst`` o los docstrings del código.

La referencia de la API se genera mediante ``sphinx.ext.autodoc`` y
``sphinx.ext.napoleon``. Los notebooks de la carpeta raíz se renderizan con
``nbsphinx``; ``conf.py`` genera copias dentro de ``docs/source/tutoriales/``
antes de leer el árbol de documentación. Por tanto, los docstrings Google-style del código son
la fuente de las descripciones de clases, métodos, argumentos y resultados.

Contribuir
----------

Al añadir una funcionalidad:

1. Documenta clases y funciones públicas con Google-style docstrings.
2. Especifica las unidades físicas en nombres de argumentos y docstrings.
3. Añade pruebas automatizadas.
4. Actualiza la documentación de teoría si cambia una hipótesis o ecuación.
5. Comprueba que Sphinx construye sin advertencias relevantes.


Documentar los notebooks
------------------------

Cada notebook debe incluir objetivos de aprendizaje, fundamento físico y
matemático, ecuaciones con unidades, parámetros de simulación, interpretación
de gráficas, límites del modelo y referencias. Mantén los archivos editables
en ``notebooks/``. Las copias de ``docs/source/tutoriales/`` se generan
automáticamente y no deben editarse a mano.
