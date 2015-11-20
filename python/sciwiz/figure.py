

import uuid

import IPython.display as display

from jinja2 import Environment, PackageLoader

import numpy as np
import numjis as nj


__all__ = ['Figure', 'Axes', 'RenderObject', 'Scatter']

# template Environment object
_templateEnv = Environment(loader=PackageLoader('sciwiz', 'templates'))


class Figure(object):

    def __init__(self):

        # figure ID
        self.__ID = str(uuid.uuid4())

        # axes list
        self.__axes = list()

        self.__dataDict = dict()      # data source dictionary
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
        dataUUID : UUID string
        """

        if type(data) != np.ndarray:
            raise TypeError('Expecting Numpy ndarray object')

        # check if date is already in dataDict
        for d in self.__dataDict.viewitems():

            # compare pointers
            if d[1] is data:
                return d[0]

        # if code reached this point, new data source needs to be created

        # create a new UUID
        dataUUID = str(uuid.uuid4())

        # prevents duplicate keys, although unlikely
        while self.__dataDict.has_key(dataUUID):
            dataUUID = str(uuid.uuid4())

        # insert new data source
        self.__dataDict[dataUUID] = data

        return dataUUID


    def addMaterial(self, material):
        """
        Add a new material to figure.
        """

        # TODO: add material to material dictionary
        pass


    def addAxes(self, **kwargs):
        """
        Add a new axes to the figure.
        """
        ax = Axes(self, **kwargs)
        self.__axes.append(ax)
        return ax


    def show(self):

        figPanelTemp = _templateEnv.get_template('html/figure.html')
        figPanel = figPanelTemp.render(id=self.__ID)

        HTML = display.HTML(data=figPanel)
        display.display(HTML)

        ##########################
        # Javascript rendering
        ##########################
        JScode = list()

        # data sources
        # creates a dictionary with JSON code for each data source
        dataDictJson = dict()
        for d in self.__dataDict.viewitems():
            dataDictJson[d[0]] = nj.toJson(d[1])

        dataSourceTemplate = _templateEnv.get_template('js/datasource.js')
        dataJS = dataSourceTemplate.render(DATA=dataDictJson)
        JScode.append(dataJS)

        # Figure creation
        jsTemp = _templateEnv.get_template('js/figure.js')
        JScode.append(jsTemp.render(id=self.__ID))

        # Axes
        for axes in self.__axes:
            JScode.append(axes.render())

        JSsrc = ''.join(JScode)

        print(JSsrc)

        libs = ['http://threejs.org/build/three.min.js',
                'js/numjis_bundle.js',
                'js/OrbitControls.js',
                'js/sciwiz_bundle.js']
        JS = display.Javascript(data = JSsrc, lib = libs)
        display.display(JS)



class JSRenderable(object):
    """
    Base class for render classes
    """

    def __init__(self):
        pass

    def render(self):
        """
        returns Javascript code for rendering the object.
        """
        pass


class Axes(JSRenderable):

    def __init__(self, fig, **kwargs):
        
        self.__fig = fig
        self.__renderObjects = list()


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
        JScode.append(axesTemp.render(objects = JSrenderObj))

        return ''.join(JScode)


    def scatter(self, vertex, **kwargs):

        if type(vertex) != np.ndarray:
            raise TypeError('Expecting a Numpy NDArray object')

        # adds a Scatter render object
        self.__renderObjects.append(Scatter(self, vertex, **kwargs))



class Scatter(JSRenderable):

    def __init__(self, axes, vertex, **kwargs):

        self.__axes = axes

        # add vertex array to data sources
        self.__dataID = self.__axes.addData(vertex)

        # unroll kwargs
        # TODO: add material management


    def render(self):

        renderTemplate = _templateEnv.get_template('js/scatter.js')
        JSsrc = renderTemplate.render(vertex = self.__dataID)

        return JSsrc


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