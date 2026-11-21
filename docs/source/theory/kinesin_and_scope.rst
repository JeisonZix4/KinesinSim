Kinesina-1 y alcance del modelo
===============================

Kinesina-1 es un motor molecular que se desplaza predominantemente hacia el
extremo positivo de los microtúbulos. El motor convencional es un dímero con
dos dominios motores, neck linkers, un tallo y regiones de unión a carga. Su
marcha se suele describir mediante un mecanismo *hand-over-hand*, con un paso
característico cercano a 8 nm bajo condiciones habituales.

KineSIM 0.1.2 no modela de forma independiente todos esos elementos. La red
cinética incluida es un modelo efectivo y reducido con tres estados activos
(``bound_apo``, ``atp_bound`` y ``post_hydrolysis``) y un estado terminal de
desprendimiento. La posición cambia mediante desplazamientos discretos
asociados a las transiciones.

.. important::

   La animación de dos cabezas es una reconstrucción gráfica esquemática basada
en la trayectoria del centro del motor. No se integran coordenadas individuales
   de las cabezas, ni las deformaciones reales de los neck linkers.

La carga puede representarse mediante una clase auxiliar y la fuerza externa
puede modificar tasas mediante una ley tipo Bell. Sin embargo, la carga no está
acoplada dinámicamente a la trayectoria de Gillespie en esta versión.

Variables representativas
-------------------------

Para un modelo de pasos discretos, una coordenada longitudinal simplificada
puede escribirse como:

.. math::

   x(t) = x_0 + n(t) d,

con :math:`n(t)` como número neto de pasos y :math:`d` como tamaño de paso
configurado en el modelo. En KineSIM, los retrocesos se contabilizan con
incrementos negativos.
