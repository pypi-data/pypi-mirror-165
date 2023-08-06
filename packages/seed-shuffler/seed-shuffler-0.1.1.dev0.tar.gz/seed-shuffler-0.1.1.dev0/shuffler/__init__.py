# -*- coding: utf-8 -*-
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("seed-shuffler")

except:
    pass
