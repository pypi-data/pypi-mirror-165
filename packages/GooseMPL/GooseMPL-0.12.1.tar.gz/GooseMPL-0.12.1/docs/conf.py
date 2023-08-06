import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "GooseMPL"
copyright = "2017, Tom de Geus"
author = "Tom de Geus"

autodoc_type_aliases = {
    "Iterable": "Iterable",
    "ArrayLike": "ArrayLike",
    "DTypeLike": "DTypeLike",
}

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
]

html_theme = "furo"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_static_path = ["_static"]
