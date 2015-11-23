
import uuid

from .figure import JSRenderable, Axes


__all__ = ['Material']

class Material(JSRenderable):

    def __init__(self):
        self.__ID = uuid.uuid4()


    def render(self):
        pass


    def addToAxes(self, fig):
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

    def __init__(self, **kwargs):
        super(PointMaterial).__init__(self)

        self.__properties = dict()
        self.__properties['pointSize'] = 20


    def addToAxes(self, ax):

        if type(ax) != Axes:
            raise TypeError('Expecting Axes object')

        # TODO


    def render(self):

        pass