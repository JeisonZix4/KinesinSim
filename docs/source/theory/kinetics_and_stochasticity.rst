Cinética química y simulación estocástica
=========================================

Estados y transiciones
---------------------

El modelo representa configuraciones efectivas mediante estados discretos:

.. math::

   S_i \xrightarrow{k_{ij}} S_j.

La tasa :math:`k_{ij}` tiene unidades de :math:`\mathrm{s}^{-1}` para una
transición de primer orden. Las tasas determinan probabilidades por unidad de
tiempo; no especifican un instante determinista de transición.

Asociación de ATP
-----------------

La asociación bimolecular se aproxima como una tasa pseudo-primer orden cuando
la concentración de ATP permanece constante:

.. math::

   k_{\mathrm{ATP}} = k_{\mathrm{on}}[\mathrm{ATP}],

con :math:`k_{\mathrm{on}}` en :math:`\mathrm{M}^{-1}\mathrm{s}^{-1}` y ATP en
:math:`\mathrm{M}`.

Dependencia de fuerza tipo Bell
-------------------------------

KineSIM implementa una dependencia fenomenológica de la forma:

.. math::

   k(F) = k_0 \exp\left(
   -\frac{s\,\theta F\delta}{k_B T}\right),

según la convención de signos del objeto ``BellRate``. :math:`s` representa la
dirección de sensibilidad configurada, :math:`\theta` la fracción de carga,
:math:`F` la fuerza y :math:`\delta` la distancia característica. Esta ley es
una aproximación para una transición particular; no determina por sí sola la
curva fuerza-velocidad completa de kinesina.

Algoritmo directo de Gillespie
------------------------------

Para las transiciones disponibles desde el estado actual, se evalúan las tasas
:math:`a_1,\ldots,a_M` y se calcula:

.. math::

   a_0 = \sum_{\mu=1}^{M} a_\mu.

El tiempo hasta el próximo evento se extrae mediante:

.. math::

   \tau = -\frac{\ln r_1}{a_0}, \qquad 0 < r_1 < 1,

mientras que la probabilidad de seleccionar el evento :math:`\mu` es:

.. math::

   P(\mu) = \frac{a_\mu}{a_0}.

Después del evento se actualizan el estado, la posición y el contador de ATP;
las tasas se vuelven a evaluar. La implementación supone que las tasas se
mantienen constantes entre eventos para el estado y ambiente actuales.

.. warning::

   El algoritmo actual no integra variables mecánicas continuas dentro del
   mismo paso temporal. Los incrementos brownianos y los componentes
   elásticos están implementados como utilidades independientes.
