project = "enstat"
copyright = "2021, Tom de Geus"
author = "Tom de Geus"
autodoc_type_aliases = {"Iterable": "Iterable", "ArrayLike": "ArrayLike"}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_theme = "furo"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]
