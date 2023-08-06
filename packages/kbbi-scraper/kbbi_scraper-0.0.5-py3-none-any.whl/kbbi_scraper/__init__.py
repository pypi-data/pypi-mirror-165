import os
from kbbi_scraper.constants import *
from kbbi_scraper.word import *
from kbbi_scraper.utils import *

__version__ = "alpha"

from pathlib import Path

if not Path(Path(__file__).parent/'bowl.json').is_file():
    Path(Path(__file__).parent/'bowl.json').touch()