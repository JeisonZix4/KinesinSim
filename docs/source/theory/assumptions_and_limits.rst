Hipótesis y limitaciones científicas
====================================

KineSIM 0.1.2 es una plataforma de prototipado y aprendizaje. Las siguientes
limitaciones deben acompañar cualquier interpretación de sus resultados:

* El modelo de kinesina-1 es una red cinética efectiva con estados agregados.
  No simula por separado los nucleótidos y las posiciones de las dos cabezas.
* La animación representa dos cabezas de forma esquemática; sus coordenadas se
  reconstruyen gráficamente desde la posición del motor.
* Los parámetros predeterminados son ilustrativos y no están calibrados con
  un conjunto de datos experimentales.
* La ley de Bell se aplica como dependencia fenomenológica de tasas, no como
  un modelo completo de todas las transiciones mecanoquímicas.
* Los modelos de fuerza, elasticidad, carga y Browniano se ofrecen como
  componentes auxiliares. No se acoplan todavía a la dinámica cinética.
* Los paisajes energéticos son funciones fenomenológicas. No son campos de
  fuerza atomísticos ni potenciales de energía libre experimentales.
* No se impone actualmente balance detallado local entre las tasas, el
  consumo químico y el trabajo mecánico.
* Los paquetes de miosina y dineína son espacios reservados, no modelos
  implementados.

Una futura validación debería contrastar velocidades, tiempos de espera,
longitudes de recorrido, fuerza de parada y tasas de desprendimiento con datos
experimentales bajo condiciones comparables. También debería relacionar las
tasas y los paisajes mediante restricciones termodinámicas coherentes.
