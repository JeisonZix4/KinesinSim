"""Configuración de Sphinx para la documentación de KineSIM."""

from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE_NOTEBOOKS = ROOT / "notebooks"
DOC_NOTEBOOKS = Path(__file__).resolve().parent / "tutoriales"

# Los notebooks de la raíz son la fuente canónica. Se copian al árbol de
# documentación para que nbsphinx pueda renderizarlos sin duplicar su edición.
DOC_NOTEBOOKS.mkdir(parents=True, exist_ok=True)
if SOURCE_NOTEBOOKS.exists():
    for old_notebook in DOC_NOTEBOOKS.glob("*.ipynb"):
        old_notebook.unlink()
    for notebook in SOURCE_NOTEBOOKS.glob("*.ipynb"):
        shutil.copy2(notebook, DOC_NOTEBOOKS / notebook.name)

sys.path.insert(0, str(ROOT / "src"))

project = "KineSIM"
author = "KineSIM contributors"
release = "0.1.2"
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "nbsphinx",
]

autosummary_generate = True
autodoc_typehints = "description"
autodoc_typehints_format = "short"
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "show-inheritance": True,
}

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True

# Los notebooks se muestran como material didáctico, pero no se ejecutan al
# construir la documentación. Así Sphinx no instala paquetes ni corre
# simulaciones largas durante el build.
nbsphinx_execute = "never"
nbsphinx_allow_errors = False
nbsphinx_kernel_name = "python3"
nbsphinx_timeout = 300

exclude_patterns = [
    "_build",
    "build",
    "Thumbs.db",
    ".DS_Store",
    "**/.ipynb_checkpoints",
]
master_doc = "index"
html_theme = "furo"
html_title = "KineSIM — Documentación"
html_static_path = []
html_show_sourcelink = True

nitpicky = False
