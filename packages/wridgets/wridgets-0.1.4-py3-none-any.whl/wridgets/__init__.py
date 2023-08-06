from .utils import GridBox2
from .version import __version__
from .wridgets import *
import logging
from ipywidgets import __version__ as ipywidgets_version
if int(ipywidgets_version.split('.')[0]) < 8:
    logging.warning(f'you have ipywidgets version {ipywidgets_version} which is incompatible with some features of wridgets version {__version__}.')