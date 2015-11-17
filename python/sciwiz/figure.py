
import uuid

import IPython.display as display

from jinja2 import Environment, PackageLoader

import numpy as np
import numjis as nj


__all__ = ['Figure', 'Axes3D']

# template Environment object
_templateEnv = Environment(loader=PackageLoader('sciwiz', 'templates'))


class Figure(object):
    """
    Figure class

    A Figure contains global properties such as layout and Axes.
    """

    def __init__(self):

        # figure ID
        self.__ID = str(uuid.uuid4())

        # axes list
        self.__axes = list()

        # data source dictionary
        self.__dataDict = dict()

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

        # if code reach this point, new data source
        # need to be created

        # create a new UUID
        dataUUID = str(uuid.uuid4())

        # prevents duplicate keys, although unlikely
        while self.__dataDict.has_key(dataUUID):
            dataUUID = str(uuid.uuid4())

        # insert new data source
        self.__dataDict[dataUUID] = data

        return dataUUID

    def addAxes(self, **kwargs):
        """
        Add a new axes to the figure.
        """
        ax = Axes3D(self, **kwargs)
        self.__axes.append(ax)
        return ax

    def show(self):
        """
        Shows figure.
        """

        figPanelTemp = _templateEnv.get_template('html/figure.html')
        figPanel = figPanelTemp.render(ID=self.__ID)

        HTML = display.HTML(data=figPanel)
        display.display(HTML)

        renderJSlist = []

        # render data sources
        # creates a dictionary with JSON code for each data source
        dataDictJson = dict()
        for d in self.__dataDict.viewitems():
            dataDictJson[d[0]] = nj.toJson(d[1])

        dataSourceTemplate = _templateEnv.get_template('js/datasource.js')
        dataJS = dataSourceTemplate.render(DATA=dataDictJson)
        renderJSlist.append(dataJS)

        # render each axes
        for ax in self.__axes:
            renderJSlist.append(ax.render())

        JScode = ''.join(renderJSlist)

        # print(JScode)


        libs = ['http://threejs.org/build/three.min.js',
                'js/numjis_bundle.js',
                'js/OrbitControls.js']
        JS = display.Javascript(data = JScode, lib = libs)
        display.display(JS)



class Axes3D(object):
    """
    An Axes3D object contains the different objects that make the
    scene such as axis, data points, etc.
    """

    def __init__(self, fig, **kwargs):

        self.__fig = fig
        self.__renderObjects = list()

        # unroll kwargs
        self.__bgcolor = kwargs.get('bgcolor', '0xFFFFFF')
        self.__width = int(kwargs.get('width', 800))
        self.__height = int(kwargs.get('height', 800))
        

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


    def render(self):

        renderCodeList=list()

        # Append the render codes for each object
        for obj in self.__renderObjects:
            renderCodeList.append(obj.renderCode())


        jsTemp = _templateEnv.get_template('js/axes3D.js')
        js = jsTemp.render(id = self.__fig.ID,
            width = self.__width,
            height = self.__height,
            bgcolor = self.__bgcolor,
            objects = renderCodeList)

        return js



    def scatter(self, vertex, **kwargs):

        if type(vertex) != np.ndarray:
            raise TypeError('Expecting a Numpy NDArray object')

        # add vertex to data sources
        vertexID = self.__fig.addData(vertex)

        # adds a Scatter3D render object
        self.__renderObjects.append(Scatter3D(self, vertexID, **kwargs))



    def surface(self, vertex, **kwargs):

        if type(vertex) != np.ndarray:
            raise TypeError('Expecting a Numpy NDArray object')

        # add vertex to data sources
        vertexID = self.__fig.addData(vertex)

        # adds a Surface3D render object
        self.__renderObjects.append(Surface3D(self, vertexID, **kwargs))




class RenderObject(object):
    """
    Base class for render classes
    """

    def __init__(self):
        pass

    def renderCode(self):
        pass



class Scatter3D(RenderObject):

    def __init__(self, axes, dataID, **kwargs):

        self.__axes = axes
        self.__dataID = dataID

        # unroll kwargs

        # TODO: add color management
        self.__color = kwargs.get('color', '0x000000')
        self.__size = kwargs.get('size', 0.01)
        self.__sizeAttenuation = str(kwargs.get('sizeAttenuation', True)).lower()
        self.__fog = str(kwargs.get('fog', True)).lower()


    def renderCode(self):

        renderTemplate = _templateEnv.get_template('js/scatter3D.js')
        JScode = renderTemplate.render(
            vertex = self.__dataID,
            color = self.__color,
            size = self.__size,
            size_attenuation = self.__sizeAttenuation,
            fog = self.__fog
            )

        return JScode



class Surface3D(RenderObject):

    def __init__(self, axes, dataID, **kwargs):

        self.__axes = axes
        self.__dataID = dataID

        # unroll kwargs

        # TODO: add color management
        self.__color = kwargs.get('color', '0x01BA23')
        self.__wireframe = str(kwargs.get('wireframe', False)).lower()
        self.__wirewidth = kwargs.get('wirewidth', 0.01)

        self.__hasTexture = True if 'texture' in  kwargs.keys() else False

        ###############################
        # TEXTURE VALIDATION
        ###############################
        self.__textureID = None

        if self.__hasTexture:
            
            # validate texture and create data source
            texData = kwargs['texture']
            if self.__validateTexture(texData):

                # create data source for texture
                self.__textureID = self.__axes.addData(texData)
                

    def renderCode(self):

        renderTemplate = _templateEnv.get_template('js/surface3D.js')
        JScode = renderTemplate.render(
            vertex = self.__dataID,
            color = self.__color,
            wireframe = self.__wireframe,
            wirewidth = self.__wirewidth,
            hasTexture = self.__hasTexture,
            textureID = self.__textureID
            )

        return JScode


    def __validateTexture(self, texData):

        # check texture object type
        if type(texData) != np.ndarray:
            raise TypeError('Texture data should be a Numpy ndarray object')

        # check texture dimensions
        if not texData.ndim in [2, 3]:
            raise ValueError('Expecting 2 or three dimentional nd array')

        # check texture channels
        if texData.ndim == 3:
            channels = texData.shape[2]
            if not channels in [1, 3, 4]:
                raise ValueError('Texture channels musht be [1, 3, 4], got: ' + depth)

        return True