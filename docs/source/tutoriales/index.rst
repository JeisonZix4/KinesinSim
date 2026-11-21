Colección de laboratorios
=========================

Los notebooks se presentan en un orden que va desde la simulación cinética
básica hasta los componentes mecánicos auxiliares y el registro reproducible
de resultados.

.. list-table:: Resumen de los laboratorios
   :header-rows: 1
   :widths: 8 35 57

   * - N.º
     - Laboratorio
     - Pregunta principal
   * - 01
     - Fundamentos y simulación
     - ¿Cómo se construye una red cinética y cómo Gillespie genera una trayectoria individual?
   * - 02
     - Experimentos con ATP y fuerza
     - ¿Cómo modifican ATP y la carga las tasas y los observables del modelo?
   * - 03
     - Estadística y reproducibilidad
     - ¿Qué variabilidad aparece entre trayectorias y cómo se distribuyen los tiempos de espera?
   * - 04
     - Mecánica y paisajes de energía
     - ¿Cómo se representan mínimos, barreras, coordenadas y cargas en potenciales fenomenológicos?
   * - 05
     - Animaciones y trayectorias energéticas
     - ¿Cómo se visualiza la trayectoria y qué parte de la animación es reconstrucción esquemática?
   * - 06
     - Mecánica, datos y reproducibilidad
     - ¿Cómo se representan la geometría, elasticidad, arrastre, difusión y almacenamiento de datos?

.. toctree::
   :maxdepth: 1

   01_fundamentos_y_simulacion
   02_experimentos_atp_y_fuerza
   03_estadistica_tiempos_y_reproducibilidad
   04_mecanica_y_paisajes_de_energia
   05_animaciones_y_trayectorias_energeticas
   06_mecanica_datos_y_reproducibilidad

Convenciones comunes
--------------------

* Concentración de ATP: mol/L, salvo que el eje indique mM.
* Tiempo: s.
* Posición: nm.
* Fuerza: N en ``Environment`` y pN en los parámetros de los paisajes energéticos.
* Energía de los mapas: unidades de :math:`k_B T`.
* Las semillas permiten repetir realizaciones pseudoaleatorias bajo la misma
  versión, parámetros y entorno computacional.

Alcance científico
------------------

Los experimentos usan el modelo cinético fenomenológico disponible en KineSIM
0.1.2. Las animaciones no son atomísticas; las coordenadas individuales de las
dos cabezas se reconstruyen gráficamente. Los paisajes energéticos son
ilustrativos y no se derivan de las tasas de Gillespie. Los componentes de
elasticidad, arrastre y difusión se presentan como utilidades auxiliares y aún
no están acoplados al integrador cinético.
