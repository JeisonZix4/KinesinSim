Termodinámica: ATP y trabajo mecánico
====================================

La hidrólisis del ATP se representa mediante la reacción global:

.. math::

   \mathrm{ATP} + \mathrm{H_2O}
   \longrightarrow \mathrm{ADP} + P_i.

El cambio de energía libre de Gibbs depende de las concentraciones químicas:

.. math::

   \Delta G = \Delta G^{\circ'} + RT
   \ln\left(\frac{[\mathrm{ADP}][P_i]}{[\mathrm{ATP}] }\right).

Aquí :math:`R` es la constante de los gases, :math:`T` la temperatura absoluta
y las concentraciones se expresan en unidades compatibles. Un valor negativo
de :math:`\Delta G` indica que la reacción directa es favorable en esas
condiciones.

El trabajo mecánico para una fuerza constante paralela al desplazamiento es:

.. math::

   W = Fd.

A escala molecular suele ser útil comparar las energías con la escala térmica:

.. math::

   k_B T,

que en KineSIM se convierte, cuando corresponde, a pN nm. La energía química
disponible no se convierte íntegramente en trabajo: hay disipación y
fluctuaciones térmicas.

.. note::

   La versión actual de KineSIM no calcula el potencial químico del ATP a
   partir de concentraciones de ATP, ADP y fosfato, ni impone un balance
   termodinámico completo entre consumo de ATP, trabajo y tasas. La
   concentración de ATP se utiliza en la ley de asociación definida en el
   modelo cinético.
