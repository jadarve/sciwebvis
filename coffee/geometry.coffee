
###
Base geometry class.
###
class Geometry

    ###
    @property [Array] attributes hashmap.
      Each attribute is identified by a string name and contains
      a Numjis ndarray holding data.
    ###
    attributes : null


    ###
    @property [THREE.BufferGeometry] geometry BufferGeometry object.
      This object makes the link between SCIWIS Geometry and the
      renderer.
    ###
    geometry : null


    constructor: (attributes) ->

        # dictionary containing geometry attributes
        @attributes = new Array()
        @geometry = new THREE.BufferGeometry()

        # unroll attributes
        for name, arr of attributes
            console.log('Geometry.constructor. Adding attribute: ' + name)
            @addAttribute(name, arr)


    ###
    Add a new attribute to the geometry

    @param [string] name Attribute name.
    @param [NJ.NDarray] arr Attribute array.
    ###
    addAttribute: (name, arr) ->

        if not typeof name == 'string'
            throw new SCIWIS.SciwisException('attribute name should be string')

        if !arr instanceof NJ.NDArray
                throw new SCIWIS.SciwisException('attribute array should be instante of NDArray')

        # add attribute
        @attributes[name] = arr


        # create attribute
        # attrbSize = arr.shape[arr.ndim-1]
        attrbSize = switch name
            when 'index' then 1
            else arr.shape[arr.ndim-1]

        attrb = new THREE.BufferAttribute(arr.data, attrbSize)

        if name == 'index'
            # index needs to be set using setIndex method
            @geometry.setIndex(attrb)
        else
            # add attribute to geometry
            @geometry.addAttribute(name, attrb)


    ###
    return true if the given attribute name is present in the geometry.
    ###
    hasAttribute: (name) ->

        return @attributes[name]?


    ###
    return THREE.BufferGeometry object representing the geometry.
    ###
    getBufferGeometry: () ->

        return @geometry


module.exports =
    Geometry : Geometry
