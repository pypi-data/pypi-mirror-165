import os
from pathlib import Path

import pkg_resources

__version__ = pkg_resources.get_distribution("bobifi").version

DATADIR = Path(os.path.abspath(os.path.dirname(__file__))) / "data"
