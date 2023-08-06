# coding: utf-8
import sys
from io import StringIO

if sys.version_info == (3, 6):
    from .unparser36 import Unparser
if sys.version_info == (3, 7):
    from .unparser37 import Unparser
else:
    from .unparser import Unparser
from .printer import Printer


__version__ = '1.6.2'


def unparse(tree):
    v = StringIO()
    Unparser(tree, file=v)
    return v.getvalue()


def dump(tree):
    v = StringIO()
    Printer(file=v).visit(tree)
    return v.getvalue()
