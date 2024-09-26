# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# from sphinx_astropy.conf import *

project = 'MYRaf'
copyright = '2024, Mohammad Niaei, Yücel Kılıç'
author = 'Mohammad Niaei, Yücel Kılıç'
release = '0.0.2 Beta'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Optional: For Google and NumPy-style docstrings
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
# html_theme = 'sphinx_astropy'
html_static_path = ['_static']

html_logo = "_static/myraf.png"

# html_theme_options = {
#     'collapse_navigation': False,
#     'navigation_depth': 3,
#     'titles_only': False,
# }

