from .dto import *
from .svc import *
from .dmo import *
from .bp import *

from .bp.finder import Finder

finder = Finder()


def entity_exists(input_text: str) -> bool:
    return finder.exists(input_text)
