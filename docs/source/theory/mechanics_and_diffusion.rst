Mecánica auxiliar y difusión browniana
======================================

Elasticidad lineal
------------------

El modelo de resorte de Hooke utiliza:

.. math::

   F_{\mathrm{spring}} = -k(x-x_0),

con constante elástica :math:`k` en N/m y longitud natural :math:`x_0` en m.
La energía potencial del resorte correspondiente es:

.. math::

   U_{\mathrm{spring}} = \frac{1}{2}k(x-x_0)^2.

Arrastre lineal
---------------

La clase ``Cargo`` utiliza una aproximación lineal:

.. math::

   F_{\mathrm{drag}} = -\gamma v,

con coeficiente de arrastre :math:`\gamma` en N s/m. Es un modelo auxiliar y
no representa por sí solo la hidrodinámica compleja del citoplasma.

Desplazamiento browniano
-----------------------

Para difusión libre unidimensional, el incremento durante un intervalo
:math:`\Delta t` se modela como:

.. math::

   \Delta x = \sqrt{2D\Delta t}\,\xi,
   \qquad \xi \sim \mathcal{N}(0,1),

por lo que:

.. math::

   \mathbb{E}[\Delta x]=0,
   \qquad \operatorname{Var}(\Delta x)=2D\Delta t.

La utilidad ``brownian_displacement`` genera ese incremento. No resuelve la
ecuación de Langevin completa ni incorpora automáticamente fuerzas,
condiciones de frontera o un potencial.

Una posible extensión sobreamortiguada
--------------------------------------

Una dinámica futura podría formularse como:

.. math::

   \gamma\dot{x} = -\frac{\partial U}{\partial x}
   + F_{\mathrm{ext}} + \sqrt{2\gamma k_B T}\,\eta(t),

con una convención apropiada para el ruido blanco :math:`\eta(t)`. Esta
ecuación es una propuesta de extensión y no está acoplada a Gillespie en la
versión actual.
