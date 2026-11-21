Paisajes de energía
===================

Coordenadas
-----------

La clase ``EnergyLandscape`` define un potencial fenomenológico
:math:`U(x,q)`, donde :math:`x` es la coordenada longitudinal en nm y
:math:`q\in[0,1]` es una coordenada conformacional adimensional. La energía se
expresa en unidades de :math:`k_B T`.

La función implementada suma cinco contribuciones:

.. math::

   \frac{U(x,q)}{k_B T} = U_{\mathrm{spatial}}
   + U_{\mathrm{conformational}} + U_{\mathrm{bias}}
   + U_{\mathrm{coupling}} + U_{\mathrm{load}}.

Potencial espacial periódico
----------------------------

.. math::

   U_{\mathrm{spatial}} = \frac{A_x}{2}
   \left[1-\cos\left(2\pi\left(\frac{x}{d}-\phi q\right)\right)\right].

Aquí :math:`A_x` es la amplitud de barrera en :math:`k_BT`, :math:`d` el
período espacial y :math:`\phi` el desplazamiento de fase entre conformaciones.

Potencial conformacional de doble pozo
--------------------------------------

.. math::

   U_{\mathrm{conformational}} = 16 A_q q^2(1-q)^2.

Este término presenta mínimos en :math:`q=0` y :math:`q=1` y una barrera en
:math:`q=1/2`.

Sesgo y acoplamiento
--------------------

.. math::

   U_{\mathrm{bias}} = \Delta g\,q,

.. math::

   U_{\mathrm{coupling}} = J\sin\left(\frac{2\pi x}{d}\right)q(1-q).

El sesgo modifica la energía relativa de las conformaciones y el acoplamiento
hace que el potencial espacial dependa también de :math:`q`.

Carga externa
-------------

.. math::

   U_{\mathrm{load}} = \frac{F x}{k_B T},

con :math:`F` positiva para una carga que se opone al movimiento en la dirección
positiva de :math:`x`. En esta expresión deben utilizarse unidades coherentes;
la implementación convierte pN nm y :math:`k_BT`.

La fuerza derivada de un potencial respecto a una coordenada espacial es:

.. math::

   F_x = -\frac{\partial U}{\partial x}.

Interpretación y límites
------------------------

Los mínimos representan configuraciones relativamente favorables dentro de
este potencial elegido; las barreras representan regiones energéticamente
más altas. Sin calibración, no deben interpretarse como estados estructurales
medidos o como barreras reales de kinesina.

KineSIM también contiene utilidades alternativas de visualización energética
con una coordenada conformacional :math:`q\in[-1,1]`. Esa convención es distinta
de la coordenada :math:`[0,1]` de ``EnergyLandscape`` y no se deben mezclar
ambas formulaciones sin transformar explícitamente la coordenada.

.. important::

   Los paisajes actuales no se infieren de la red cinética ni se acoplan a las
   tasas de Gillespie. Un diagrama de energías de estados necesita información
   termodinámica adicional; las tasas por sí solas no determinan de forma
   general los niveles de energía y las barreras.
