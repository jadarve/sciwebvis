"""
    sciwebvis.figure
    ----------------

    :copyright: 2015, Juan David Adarve. See AUTHORS for more details
    :license: 3-clause BSD, see LICENSE for more details
"""

import IPython.display as display

from jinja2 import Environment, PackageLoader

import numpy as np
import numjis as nj

from .JSRenderable import JSRenderable
from . import material
from . import geometry
from .color import Color
from .util import generateID

__all__ = ['Figure', 'Axes', 'Scatter', 'Surface']

# template Environment object
_templateEnv = Environment(loader=PackageLoader('sciwebvis', 'templates'))


class Figure(JSRenderable):

    def __init__(self):
        """Creates a new figure.
        """
        
        self.__ID = generateID() # figure ID
        self.__axes = list()          # axes list
        self.__dataDict = dict()      # data source dictionary
        self.__geometryDict = dict()  # geometry dictionary
        self.__materialDict = dict()  # material dictionary

    ###################################
    # PROPERTIES
    ###################################

    @property
    def ID(self):
        """
        Figure ID
        """
        return self.__ID

    @ID.setter
    def ID(self, value):
        self.__ID = value

    @property
    def data(self):
        """
        Data source dictionary
        """
        return self.__dataDict

    @data.setter
    def data(self, value):
        raise Exception('data source dictionary cannot be set')


    ###################################
    # METHODS
    ###################################

    def addData(self, data):
        """
        Add a new data source for the figure and return its UUID.

        In case data array is already contained, the insertion
        does not take place and the data UUID is returned.

        Parameters
        ----------
        data : Numpy ndarray object

        Returns
        -------
        dataID : str
            Unique string identifier of data in this figure.

        Raises
        ------
        TypeError : if data is not an instance of np.ndarray.

        """

        if type(data) != np.ndarray:
            raise TypeError('Expecting Numpy ndarray object')

        # check if data is already in dataDict
        for d in self.__dataDict.viewitems():

            # compare pointers
            if d[1] is data:
                return d[0]

        # if code reaches this point, a new data source needs to be created

        dataID = generateID(self.__dataDict.keys())

        # insert new data source
        self.__dataDict[dataID] = data

        return dataID


    def addGeometry(self, geom):
        """Adds a new Geometry object to the figure.

        Parameters
        ----------
        geom : Geometry.
            Geometry object.

        Returns
        -------
        geom : Geometry.
            Same geometry parameter.

        Raises
        ------
        TypeError : if type(geom) != Geometry
        """

        if type(geom) != geometry.Geometry:
            raise TypeError('geom parameter should be of type Geometry')

        # check if geom already exists
        for g in self.__geometryDict.viewitems():
            if g[1] is geom:
                return g[1]


        # configure geometry to this figure
        geom.addToFigure(self)

        # generate a new ID
        geomID = generateID(self.__geometryDict.keys())
        self.__geometryDict[geomID] = geom
        return geom


    def addMaterial(self, m):
        """Add a new material to axes.

        Parameters
        ----------
        m : Material.
            Material instance

        Returns
        -------
        m : Material.
            Same material parameter.

        Raises
        ------
        TypeError : if m is not a Material object.
        """

        if not isinstance(m, material.Material):
            raise TypeError('Expecting Material object')


        # check if material already exists
        for mat in self.__materialDict.viewitems():
            if mat[1] is m:
                return mat[1]

        # if code reaches this point, a new material needs to be added

        m.ID = generateID(self.__materialDict.keys())
        

        # add material to dictionary
        self.__materialDict[m.ID] = m

        return m


    def addAxes(self, **kwargs):
        """Add a new axes to the figure.

        Kwargs
        ------
        See Axes.__init__() for a list of admisible kwargs.
        """
        ax = Axes(self, **kwargs)
        self.__axes.append(ax)
        return ax


    def render(self):

        #####################
        # GEOMETRY
        #####################
        geomJS = dict()
        for g in self.__geometryDict.viewitems():

            geom = g[1]

            # add geom to this figure and then render JS code
            geom.addToFigure(self)
            geomJS[g[0]] = geom.render()

        #####################
        # MATERIALS
        #####################
        materialsJS = dict()
        for m in self.__materialDict.viewitems():

            mat = m[1]

            # add material to this figure and then render JS code
            mat.addToFigure(self)
            materialsJS[m[0]] = mat.render()


        #####################
        # DATA
        #####################
        dataJS = dict()
        for d in self.__dataDict.viewitems():
            dataJS[d[0]] = nj.toJson(d[1])

        #####################
        # AXES
        #####################
        axesJS = list()
        for axes in self.__axes:
            axesJS.append(axes.render())


        figTemp = _templateEnv.get_template('js/figure.js')

        jsCode = figTemp.render(
            ID=self.ID,
            DATA=dataJS,
            GEOMETRY=geomJS,
            MATERIALS=materialsJS,
            AXES=axesJS)

        return jsCode


    def show(self):

        figPanelTemp = _templateEnv.get_template('html/figure.html')
        figPanel = figPanelTemp.render(id=self.__ID)

        HTML = display.HTML(data=figPanel)
        display.display(HTML)

        # JavaScript code
        JScode = self.render()

        # NOTE: r69 in Google CDN does not work creating Three.Points objects.
        #   No idea of why.

        libs = [#'https://ajax.googleapis.com/ajax/libs/threejs/r69/three.min.js',
                'http://threejs.org/build/three.min.js',
                'http://threejs.org/examples/js/controls/OrbitControls.js',
                './js/numjis_bundle.js',
                './js/sciwis_bundle.js']
        JS = display.Javascript(data = JScode, lib = libs)
        display.display(JS)


class Axes(JSRenderable):

    def __init__(self, fig, **kwargs):
        """Creates a new Axes instance.

        Parameters
        ----------
        fig : Figure.
            Figure to which the axes is attaced.

        Kwargs
        ------
        size : int tuple, optional.
            Figure size (width, height) in pixels. Defaults to (800, 800).

        bgcolor : Color, optional.
            Background color. Defaults to light gray Color(0.9375).
        """
        
        self.__fig = fig
        self.__renderObjects = list()

        # unroll kwargs
        self.__properties = dict()
        self.__properties['size'] = kwargs.pop('size', (800, 800))  # (width, height)
        self.__properties['bgcolor'] = kwargs.pop('bgcolor', Color(0.9375))


    ###################################
    # PROPERTIES
    ###################################

    @property
    def data(self):
        """
        Data source dictionary
        """
        return self.__fig.data

    @data.setter
    def data(self, value):
        raise Exception('data source dictionary cannot be set')


    ###################################
    # METHODS
    ###################################

    def addData(self, data):
        """
        Add a new data source for the figure and return its UUID.

        In case data array is already contained, the insertion
        does not take place and the data UUID is returned.

        Parameters
        ----------
        data : Numpy ndarray object

        Returns
        -------
        dataUUID : UUID string
        """

        return self.__fig.addData(data)


    def addMaterial(self, material):
        """
        Add a new material to axes.

        This method calls parent figure.addMaterial(). The
        added material will be available to all axes of the
        figure.
        """

        return self.__fig.addMaterial(material)


    def addRenderObject(self, obj):

        # TODO: add validation
        self.__renderObjects.append(obj)


    def render(self):
        
        ##########################
        # Javascript rendering
        ##########################
        JScode = list()


        # render each render object
        JSrenderObj = list()
        for obj in self.__renderObjects:
            JSrenderObj.append(obj.render())
            # print(obj.render())

        # axes rendering
        axesTemp = _templateEnv.get_template('js/axes.js')
        JScode.append(axesTemp.render(objects = JSrenderObj,
            prop = self.__properties))

        return ''.join(JScode)


    def scatter(self, vertex, **kwargs):

        if type(vertex) != np.ndarray:
            raise TypeError('Expecting a Numpy NDArray object')

        # adds a Scatter render object
        self.__renderObjects.append(Scatter(self, vertex, **kwargs))


    def surface(self, vertex, **kwargs):
        
        if type(vertex) != np.ndarray:
            raise TypeError('Expecting a Numpy NDArray object')

        # adds a Surface render object
        self.__renderObjects.append(Surface(self, vertex, **kwargs))


class Scatter(JSRenderable):

    def __init__(self, axes, vertex, **kwargs):

        self.__axes = axes

        # add vertex array to data sources
        self.__dataID = self.__axes.addData(vertex)

        # unroll kwargs
        self.__properties = dict()
        self.__properties['material'] = kwargs.pop('material', material.PointMaterial())


        # add material to axes
        axes.addMaterial(self.__properties['material'])


    def render(self):

        renderTemplate = _templateEnv.get_template('js/scatter.js')
        JScode = renderTemplate.render(vertex = self.__dataID,
            material=self.__properties['material'].ID)

        return JScode


class Surface(JSRenderable):

    def __init__(self, axes, vertex, **kwargs):
        
        self.__axes = axes

        # add vertex array to data sources
        self.__dataID = self.__axes.addData(vertex)

        # unroll kwargs
        self.__properties = dict()
        self.__properties['material'] = kwargs.pop('material', material.WireframeMaterial())


        # add material to axes
        axes.addMaterial(self.__properties['material'])

    def render(self):

        renderTemplate = _templateEnv.get_template('js/surface.js')
        JScode = renderTemplate.render(vertex = self.__dataID,
            material = self.__properties['material'].ID)

        return JScode
    

# class Surface(JSRenderable):

#     def __init__(self, axes, dataID, **kwargs):

#         self.__axes = axes
#         self.__dataID = dataID

#         # unroll kwargs

#         # TODO: add color management
#         self.__color = kwargs.get('color', '0x01BA23')
#         self.__wireframe = str(kwargs.get('wireframe', False)).lower()
#         self.__wirewidth = kwargs.get('wirewidth', 0.01)

#         self.__hasTexture = True if 'texture' in  kwargs.keys() else False

#         ###############################
#         # TEXTURE VALIDATION
#         ###############################
#         self.__textureID = None

#         if self.__hasTexture:
            
#             # validate texture and create data source
#             texData = kwargs['texture']
#             if self.__validateTexture(texData):

#                 # create data source for texture
#                 self.__textureID = self.__axes.addData(texData)
                

#     def render(self):

#         renderTemplate = _templateEnv.get_template('js/surface3D.js')
#         JScode = renderTemplate.render(
#             vertex = self.__dataID,
#             color = self.__color,
#             wireframe = self.__wireframe,
#             wirewidth = self.__wirewidth,
#             hasTexture = self.__hasTexture,
#             textureID = self.__textureID
#             )

#         return JScode


#     def __validateTexture(self, texData):

#         # check texture object type
#         if type(texData) != np.ndarray:
#             raise TypeError('Texture data should be a Numpy ndarray object')

#         # check texture dimensions
#         if not texData.ndim in [2, 3]:
#             raise ValueError('Expecting 2 or three dimentional nd array')

#         # check texture channels
#         if texData.ndim == 3:
#             channels = texData.shape[2]
#             if not channels in [1, 3, 4]:
#                 raise ValueError('Texture channels musht be [1, 3, 4], got: ' + depth)

#         return True