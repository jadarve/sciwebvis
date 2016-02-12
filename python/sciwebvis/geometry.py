"""
    sciwebvis.geometry
    ------------------

    :copyright: 2015, Juan David Adarve. See AUTHORS for more details
    :license: 3-clause BSD, see LICENSE for more details
"""

import numpy as np

__all__ = ['Geometry']


"""
Base geometry class
"""
class Geometry:

    def __init__(self):
        
        # attributes dictionary
        self.__atributes = dict()



    def __getitem__(self, name):
        
        if type(name) != str:
            raise TypeError('attribute name should be string')

        return self.__atributes[name]


    def __setitem__(self, name, val):
        
        if type(name) != str:
            raise TypeError('attribute name should be string')

        if type(val) != np.ndarray:
            raise TypeError('attribute value should be numpy ndarray')

        self.__atributes[name] = val

