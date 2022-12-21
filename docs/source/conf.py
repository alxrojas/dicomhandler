# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import pathlib
import sys

# ----- Agrego la ruta para importar el paquete -------------------------------

# add the skcriteria source to the build path
CURRENT_PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
DICOMHANDLER_PATH = CURRENT_PATH.parent.parent

sys.path.insert(0, str(DICOMHANDLER_PATH))

# sys.path.insert(0, os.path.abspath("../.."))
# esta línea es alternativa a las 3 anteriores
# la ventaja de las otras es que uso el path más
# abajo para generar el README.rst

import dicomhandler

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "dicomhandler"
copyright = "2022, Jerónimo Fotinós, Alejandro Rojas, Nicola Maddalozzo"
author = "Jerónimo Fotinós, Alejandro Rojas, Nicola Maddalozzo"
release = dicomhandler.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = [
#     "sphinx.ext.autodoc",
#     "nbsphinx",
#     "sphinxcontrib.bibtex",
# ]

extensions = [
    # "sphinx.ext.napoleon", # me tira error de descripción duplicada
    "sphinx.ext.autodoc",
    # "sphinx.ext.coverage",
    # "sphinx.ext.mathjax",
    # "sphinx.ext.intersphinx",
    # "sphinx.ext.viewcode",
    # "sphinx.ext.autosummary",
    "nbsphinx",
    "sphinxcontrib.bibtex",
    # "sphinx_copybutton",
]

# =============================================================================
# BIB TEX
# =============================================================================

bibtex_default_style = "apa"  # pybtex-apa-style

bibtex_bibfiles = ["refs.bib"]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
# html_static_path = ["_static"]

# =============================================================================
# INJECT README INTO THE RESTRUCTURED TEXT
# =============================================================================

import m2r2

DYNAMIC_RST = {
    "README.md": "README.rst",
}

for md_name, rst_name in DYNAMIC_RST.items():
    md_path = DICOMHANDLER_PATH / md_name
    with open(md_path) as fp:
        readme_md = fp.read().split("<!-- BODY -->")[-1]

    rst_path = CURRENT_PATH / "_dynamic" / rst_name

    with open(rst_path, "w") as fp:
        fp.write(".. FILE AUTO GENERATED !! \n")
        fp.write(m2r2.convert(readme_md))
        print(f"{md_path} -> {rst_path} regenerated!")

# =============================================================================
# INDICATING READ THE DOCS HOW TO FIND index.rst 
# =============================================================================

# master_doc = 'index'