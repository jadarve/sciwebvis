
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

    constructor: () ->

        # dictionary containing geometry attributes
        @attritubutes = new Array()



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
        @attritubutes[name] = arr


    ###
    return THREE.BufferGeometry object representing the geometry.
    ###
    getBufferGeometry: () ->

        geom = new THREE.BufferGeometry()

        for name, arr of @attritubutes

            # check if arr is instance of NJ.NDarray
            if !arr instanceof NJ.NDArray
                throw new SCIWIS.SciwisException('attribute should be instante of NDArray, attribute: ' + name)

            # attribute item size is equal to the size of
            # last dimension of arr
            attrbSize = arr.shape[arr.ndim -1]

            # create attribute
            attrb = new THREE.BufferAttribute(arr.data, attrbSize)

            if name == 'index'
                # index needs to be set using setIndex method
                geom.setIndex(attrb)
            else
                # add attribute to geometry
                geom.addAttribute(name, attrb)


        return geom


module.exports =
    Geometry : Geometry
