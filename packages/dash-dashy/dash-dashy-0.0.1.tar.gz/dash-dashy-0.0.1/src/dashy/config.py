from pathlib import Path

import dash_bootstrap_components as dbc


DASHY_DIR = Path(__file__).parent
ASSETS_PATH = DASHY_DIR / 'assets'

EXTERNAL_STYLESHEETS = [
    dbc.themes.FLATLY
]

EXTERNAL_SCRIPTS = []
