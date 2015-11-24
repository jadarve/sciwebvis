
if '__RELOAD_SCIWIZ__' in globals():
    __RELOAD_SCIWIZ__ = True
else:
    __RELOAD_SCIWIZ__ = False


from . import figure as __figure
from . import material as __material
from . import color as __color
from . import JSRenderable as __JSRenderable


if __RELOAD_SCIWIZ__:

    print('reloading sciwiz')

    __figure = reload(__figure)
    __material = reload(__material)
    __color = reload(__color)
    __JSRenderable = reload(__JSRenderable)


from .figure import *
from .material import *
from .color import *
from .JSRenderable import *

__all__ = []
__all__.extend(__figure.__all__)
__all__.extend(__material.__all__)
__all__.extend(__color.__all__)
__all__.extend(__JSRenderable.__all__)