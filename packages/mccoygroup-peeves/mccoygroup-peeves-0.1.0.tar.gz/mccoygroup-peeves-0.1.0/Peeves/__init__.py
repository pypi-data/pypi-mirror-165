"""
Peeves began life as a minor extension to the `unittest` framework.
These days it's primarily used as a documentation generator, through its `Doc` subpackage.
The documentation for Peeves itself is generated with `Peeves.Doc`
"""

from .TestUtils import *
from .Timer import *
from .Profiler import *

__all__ = []
from .TestUtils import __all__ as exposed
__all__ += exposed
from .Timer import __all__ as exposed
__all__ += exposed
from .Profiler import __all__ as exposed
__all__ += exposed
import Peeves.Doc as Doc
exposed = [ "Doc" ]
__all__ += exposed