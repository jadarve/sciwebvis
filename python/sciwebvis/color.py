"""
    sciwebvis.color
    ---------------

    :copyright: 2015, Juan David Adarve. See AUTHORS for more details
    :license: 3-clause BSD, see LICENSE for more details
"""

import collections
import numpy as np
from jinja2 import Environment, PackageLoader

from .JSRenderable import JSRenderable

__all__ = ['Color']

# template Environment object
_templateEnv = Environment(loader=PackageLoader('sciwebvis', 'templates'))


class Color(JSRenderable):

    def __init__(self, c=None):
        
        if c == None:
            # random color with alpha = 1.0
            self.__color = np.random.rand(4).astype(np.float32)
            self.__color[3] = 1.0
        else:

            if isinstance(c, str):
                # TODO
                # decode from string in format #XXXXXX or #XXXXXXXX
                pass

            elif isinstance(c, collections.Iterable):

                n = -1

                #  count color components
                for n, _ in enumerate(c):
                    if n > 3:
                        raise ValueError('Expecting iterable with 1, 3, or 4 elements, got more than 4')

                # in case c is empty, n is equal -1
                n += 1

                # creates color according to number of components
                if n == 0:
                    # random color
                    self.__color = np.random.rand(4).astype(np.float32)
                    self.__color[3] = 1.0
                elif n == 1:
                    # gray scale
                    self.__color = np.array([c[0], c[0], c[0], 1.0], dtype=np.float32)
                elif n == 2:
                    # incorrect number of color components
                    raise ValueError('Expecting iterable with 1, 3, or 4 elements, got: 2')
                elif n == 3:
                    # RGB, alpha = 1
                    self.__color = np.array([c[0], c[1], c[2], 1.0], dtype=np.float32)
                elif n == 4:
                    # RGBA
                    self.__color = np.array([c[0], c[1], c[2], c[3]], dtype=np.float32)

        
    def render(self):
        
        colorTemplate = _templateEnv.get_template('js/color.js')
        return colorTemplate.render(R=self.__color[0],
            G=self.__color[1], B=self.__color[2], A=self.__color[3])