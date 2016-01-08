
import uuid
import numpy as np

from jinja2 import Environment, PackageLoader

from .JSRenderable import JSRenderable
from .color import Color


__all__ = ['Material', 'PointMaterial', 'WireframeMaterial']

# template Environment object
_templateEnv = Environment(loader=PackageLoader('sciwebvis', 'templates'))

class Material(JSRenderable):

    def __init__(self):
        self.__ID = uuid.uuid4()


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



class TexturedSurfaceMaterial(Material):

    def addToFigure(self, fig):
        pass

    def render(self):
        pass