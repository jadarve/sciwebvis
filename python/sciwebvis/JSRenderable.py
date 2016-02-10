"""
    sciwebvis.JSRenderable
    ----------------------

    :copyright: 2015, Juan David Adarve. See AUTHORS for more details
    :license: 3-clause BSD, see LICENSE for more details
"""

__all__ = ['JSRenderable']

class JSRenderable(object):
    """
    Base class for Javascript render classes
    """

    def __init__(self):
        pass

    def render(self):
        """
        returns Javascript code for rendering the object.
        """
        pass