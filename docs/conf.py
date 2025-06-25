# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(".."))

project = "Evolution LangChain"
copyright = "2024, Evolution ML Inference Team"
author = "Evolution ML Inference Team"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx_rtd_theme",
    "sphinx_autodoc_typehints",
    "myst_parser",  # Keep for any remaining .md files
]

# Исключаем проблемные builders для Python 3.13+
if sys.version_info >= (3, 13):
    # В Python 3.13+ модуль imghdr был удален, поэтому исключаем epub3 builder
    exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
else:
    exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

templates_path = ["_templates"]

language = "en"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Extension configuration -------------------------------------------------

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# Type hints
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# MyST Parser settings (for any remaining .md files)
myst_enable_extensions = [
    "deflist",
    "tasklist",
    "colon_fence",
]

# Custom CSS
html_css_files = [
    "custom.css",
]

# Theme options
html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",
    "logo_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "vcs_pageview_mode": "",
    "style_nav_header_background": "#2980B9",
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# HTML context
html_context = {
    "display_github": True,
    "github_user": "cloud-ru-tech",
    "github_repo": "evolution-langchain-python",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

# Custom sidebar
html_sidebars = {
    "**": [
        "navigation.html",
        "relations.html",
        "searchbox.html",
    ]
}

# -- Options for LaTeX output ------------------------------------------------
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "11pt",
    "figure_align": "htbp",
}

# -- Options for manual page output ------------------------------------------
man_pages = [
    (
        "index",
        "evolution-langchain",
        "Evolution LangChain Documentation",
        [author],
        1,
    )
]

# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    (
        "index",
        "evolution-langchain",
        "Evolution LangChain Documentation",
        author,
        "evolution-langchain",
        "Modern integration of Evolution Inference API with LangChain ecosystem",
        "Miscellaneous",
    ),
]

# -- Options for Epub output -------------------------------------------------
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# -- Options for PDF output --------------------------------------------------
# pdf_documents = [
#     ("index", "evolution-langchain", "Evolution LangChain Documentation", author),
# ]

# -- Options for linkcheck ---------------------------------------------------
linkcheck_ignore = [
    r"http://localhost",
    r"http://127.0.0.1",
]

# -- Options for todo extension ----------------------------------------------
todo_include_todos = True
