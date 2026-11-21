# Changelog

## Documentation update — 2026-11-20

### Added
- Expanded all six Jupyter notebooks with learning objectives, scientific
  background, equations, units, parameter explanations, result interpretation,
  limitations, and references.
- Integrated notebooks into the Sphinx site using nbsphinx.
- Added a tutorials index and automatic synchronization from the canonical
  ``notebooks/`` directory.

### Changed
- Configured Sphinx not to execute notebooks during documentation builds.
- Updated documentation and development dependencies to include nbsphinx.


## 0.1.2

- Se prepara el cambio del nombre de distribución de `protein-motor-sim` a `KineSIM` para la publicación en PyPI. El namespace de importación Python `protein_motor_sim` se conserva para mantener compatibilidad con el código y los notebooks existentes.

- Se incorporan visualizaciones avanzadas de la marcha esquemática de kinesina.
- Se añaden mapas energéticos 2D, superficies 3D y perfiles de energía fenomenológicos.
- Se incorporan herramientas para superponer y animar trayectorias sobre paisajes energéticos.
- Se consolida la colección de experimentos en seis notebooks de Jupyter.
- Se añade configuración de instalación para JupyterLab, Docker y distribución en PyPI.

## 0.1.1

- Fortalecimiento de las validaciones de Environment, State y Transition.
- Geometría de pista con conversión entre índices de sitio y posiciones.
- Contrato explícito para modelos de motores y validación de su red.
- Validación de coherencia de datos en las trayectorias.
- Pruebas unitarias adicionales para el módulo core.

## 0.1.0

- Estructura modular inicial.
- Modelo cinético efectivo de kinesina-1.
- Simulador estocástico directo de Gillespie.
- Registro y análisis de trayectorias.
- Primeras herramientas de visualización y pruebas.

## [Unreleased]

### Added
- Documentación científica y referencia de la API con Sphinx.

### Changed
- README reducido a instalación, descarga, uso básico y distribución.
- Fundamentos físicos y descripciones detalladas de la API trasladados a `docs/source/`.
