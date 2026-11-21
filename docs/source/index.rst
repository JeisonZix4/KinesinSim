KineSIM: documentación científica y técnica
============================================

KineSIM es una librería de Python para construir, ejecutar, analizar y
visualizar modelos computacionales de motores proteicos. La primera versión
incluye un modelo cinético, estocástico y simplificado de kinesina-1.

Los seis notebooks se documentan como laboratorios guiados y se renderizan
dentro de Sphinx mediante nbsphinx. Los archivos editables se mantienen en
``notebooks/``.

Esta documentación separa tres niveles:

* **Fundamento científico:** fenómenos físicos, ecuaciones e hipótesis.
* **Referencia de la API:** clases, funciones, argumentos y resultados
  documentados en el código fuente mediante Google-style docstrings.
* **Uso del software:** instalación, notebooks, pruebas y construcción de
  la documentación.

.. important::

   KineSIM es un prototipo de investigación y aprendizaje. El modelo de
   kinesina es reducido y fenomenológico; los parámetros predeterminados son
   ilustrativos, no calibrados experimentalmente. Las animaciones son
   esquemáticas y los paisajes de energía son fenomenológicos. Los componentes
   mecánicos auxiliares todavía no están acoplados al algoritmo de Gillespie.

.. toctree::
   :maxdepth: 2
   :caption: Guía de uso

   installation
   notebooks
   development

.. toctree::
   :maxdepth: 2
   :caption: Fundamentos físicos

   theory/index

.. toctree::
   :maxdepth: 2
   :caption: Referencia de la API

   api/index

Índice y búsqueda
-----------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
