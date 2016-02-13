"""
    sciwebvis.material
    ------------------

    :copyright: 2015, Juan David Adarve. See AUTHORS for more details
    :license: 3-clause BSD, see LICENSE for more details
"""

import numpy as np

from jinja2 import Environment, PackageLoader

from .JSRenderable import JSRenderable
from .color import Color
# from .util import generateID

__all__ = ['Material', 'PointMaterial',
    'WireframeMaterial', 'TextureMaterial', 'ShaderMaterial']

# template Environment object
_templateEnv = Environment(loader=PackageLoader('sciwebvis', 'templates'))

class Material(JSRenderable):

    def __init__(self):
        self.__ID = None


    def render(self):
        pass


    def addToFigure(self, fig):
        pass


    @property
    def ID(self):
        return self.__ID
    
    @ID.setter
    def ID(self, value):
        self.__ID = value



class PointMaterial(Material):
    """
    Material used to render points.
    """

    def __init__(self, fig=None, **kwargs):
        """Creates a new point material.

        Parameters
        ----------
        fig : Figure, optional.
            Figure object to which this material is attached. Defaults to None.

        Kwargs
        ------
        pointSize : int, optional.
            Point size

        color : Color, optional.
            Point color.
        """

        super(PointMaterial, self).__init__()

        self.__properties = dict()
        self.__properties['pointSize'] = kwargs.pop('pointSize', 5)
        self.__properties['color'] = kwargs.pop('color', Color())


        if fig != None:
            fig.addMaterial(self)

    def addToFigure(self, fig):
        # nothing to do for this material
        pass


    def render(self):

        materialTemplate = _templateEnv.get_template('js/pointMaterial.js')
        return materialTemplate.render(pointSize = self.__properties['pointSize'],
            color = self.__properties['color'].render())



class WireframeMaterial(Material):

    def __init__(self, fig=None, **kwargs):
        """Creates a new wireframe material

        Parameters
        ----------
        fig : Figure, optional.
            Figure object to which this material is attached. Defaults to None.

        Kwargs
        ------
        color : Color, optional.

        lineWidth : int, optional.

        transparent : bool, optional.
        """

        super(WireframeMaterial, self).__init__()

        self.__properties = dict()
        self.__properties['color'] = kwargs.pop('color', Color())
        self.__properties['lineWidth'] = kwargs.pop('lineWidth', 1)
        self.__properties['transparent'] = str(kwargs.pop('transparent', True)).lower()


        if fig != None:
            fig.addMaterial(self)


    def addToFigure(self, fig):
        # nothing to do
        pass


    def render(self):
        
        materialTemplate = _templateEnv.get_template('js/wireframeMaterial.js')
        return materialTemplate.render(lineWidth=self.__properties['lineWidth'],
            color=self.__properties['color'].render(),
            transparent=self.__properties['transparent'])



class TextureMaterial(Material):

    def __init__(self, fig=None, **kwargs):
        """Creates a new texture material.

        Parameters
        ----------
        fig : Figure, optional.
            Figure object to which this material is attached. Defaults to None.

        Kwargs
        ------
        texture : ndarray.
            Image texture to use by the material

        Raises
        ------
        KeyError: if texture kwarg is not present.
        """

        super(TextureMaterial, self).__init__()


        self.__properties = dict()

        if not 'texture' in kwargs.keys():
            raise KeyError('texture argument not set')

        try:
            tex = kwargs.pop('texture')

            if type(tex) != np.ndarray:
                raise TypeError('texture parameter should be numpy ndarray')

            self.__properties['texture_data'] = tex

        except KeyError as ke:
            raise KeyError('texture argument not set')


        # add material to figure
        if fig != None:
            self.addToFigure(fig)


    def addToFigure(self, fig):
        
        # add texture data to figure
        self.__properties['texture'] = fig.addData(self.__properties['texture_data'])


    def render(self):
        
        materialTemplate = _templateEnv.get_template('js/textureMaterial.js')
        return materialTemplate.render(texture=self.__properties['texture'])



class ShaderMaterial(Material):

    def __init__(self, fig=None, **kwargs):
        """Creates a new shader material.

        Parameters
        ----------
        fig : Figure, optional.
            Figure object to which this material is attached. Defaults to None.

        Kwargs
        ------
        vertex : string
            Vertex shader code.

        fragment : string
            Fragment shader code.
        """

        super(ShaderMaterial, self).__init__()


    def render(self):
        pass


    def addToFigure(self, fig):
        pass