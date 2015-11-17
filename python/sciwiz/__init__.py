
if '__RELOAD_SCIWIZ__' in globals():
    __RELOAD_SCIWIZ__ = True
else:
    __RELOAD_SCIWIZ__ = False


from . import figure as __figure

if __RELOAD_SCIWIZ__:

    print('reloading sciwiz')

    __figure = reload(__figure)


from .figure import *

__all__ = []
__all__.extend(__figure.__all__)