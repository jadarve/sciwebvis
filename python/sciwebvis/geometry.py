"""
    sciwebvis.geometry
    ------------------

    :copyright: 2015, Juan David Adarve. See AUTHORS for more details
    :license: 3-clause BSD, see LICENSE for more details
"""

import numpy as np

from jinja2 import Environment, PackageLoader

from .JSRenderable import JSRenderable

__all__ = ['Geometry']


# template Environment object
_templateEnv = Environment(loader=PackageLoader('sciwebvis', 'templates'))


"""
Base geometry class
"""
class Geometry(JSRenderable):

    def __init__(self):

        self.__ID = None
        
        # attributes dictionary
        self.__attributes = dict()

        # IDs of attributes in the figure
        # this dictionary is populated by
        # addToFigure() method and then used
        # by render()
        self.__attributesFigDict = dict()


    @property
    def ID(self):
        return self.__ID
    
    @ID.setter
    def ID(self, value):
        self.__ID = value


    ###################################
    # ACCESS TO ATTRIBUTES
    ###################################

    def __getitem__(self, name):
        
        if type(name) != str:
            raise TypeError('attribute name should be string')

        return self.__attributes[name]


    def __setitem__(self, name, arr):
        
        if type(name) != str:
            raise TypeError('attribute name should be string')

        if type(arr) != np.ndarray:
            raise TypeError('attribute value should be numpy ndarray')

        self.__attributes[name] = arr



    def addToFigure(self, fig):
        """Configure this Geometry object for this figure.

        The method add all relevant attribute buffers to the
        data dictionary of the figure.

        Parameters
        ----------
        fig : Figure.
            Figure to which this geometry will be added.


        Raises
        ------
        TypeError : if type(fig) != Figure
        """

        # if type(fig) != Figure:
        #     raise TypeError('fig parameter should be of type Figure')

        
        for name, arr in self.__attributes.viewitems():
            self.__attributesFigDict[name] = fig.addData(arr)


    def render(self):

        # TODO: create geometry object and set attributes
        """
        var attrb = {
            'position': dataDict['u83459asf'],
            'uv': dataDict['asf1238'],
            ...
        };

        geom = new SCIWIS.Geometry(attrb);
        geometryDict['oiuasd7912'] = geom;
        """

        geometryTemplate = _templateEnv.get_template('js/geometry.js')
        return geometryTemplate.render(ATTRIBUTES=self.__attributesFigDict)




