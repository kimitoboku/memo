from recommonmark.parser import CommonMarkParser
project = 'memo.techack.net'
copyright = '2020, kimitoboku'
author = 'Kento Kawakami'
master_doc = 'index'
source_suffix = ['.rst','.md']
source_parsers = { '.md': CommonMarkParser, }
extensions = [ ]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.md']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

