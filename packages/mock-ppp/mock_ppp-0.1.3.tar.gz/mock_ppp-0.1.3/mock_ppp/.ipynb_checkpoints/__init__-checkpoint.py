__version__ = '0.1.2'

from .utils import hello_world
from .module1.module1 import Module1_class
from .module2.module2 import Module2_class

__all__ = [
    'hello_world',
    'Module1_class',
    'Module2_class'
]
