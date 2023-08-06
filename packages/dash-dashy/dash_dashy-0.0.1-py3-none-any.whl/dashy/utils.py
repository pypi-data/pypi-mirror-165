import os
from pathlib import Path

ROOT = os.path.join(os.sep, *__file__.split(os.sep)[1:-1])
PROJECT_ROOT = Path(__file__).parent
