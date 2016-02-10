
###
Creates a THREE.DataTexture object from a Numjis array

@param [arr, NDArray] array containing texture data. It can be
  2D or 3D, where the third component represents the color channels.

@return THREE.DataTexture object.
###
textureFromNumjis = (arr) ->

    if !arr instanceof NJ.NDArray
        throw new SCIWIS.SciwisException('array is not an instance of Numjis NDArray')

    console.log('arr.ndim: ' + arr.ndim)

    if !(arr.ndim == 2 || arr.ndim == 3)
        throw new SCIWIS.SciwisException('array should have 2 or 3 dimensions, got: ' + arr.ndim)

    format = null

    if arr.ndim == 2
        format = THREE.LuminanceFormat
    else
        format = switch arr.shape[2]
            when 1 then THREE.LuminanceFormat
            when 3 then THREE.RGBFormat
            when 4 then THREE.RGBAFormat
            else throw new SCIWIS.SciwisException('invalid number of color channels, expecting {1, 3, 4}, got: ' + arr.shape[2])

    dtype = arr.dtype

    type = switch dtype.name
        when 'uint8'   then THREE.UnsignedByteType
        when 'int8'    then THREE.ByteType
        when 'uint16'  then THREE.UnsignedShortType
        when 'int16'   then THREE.ShortType
        when 'uint32'  then THREE.UnsignedIntType
        when 'int32'   then THREE.IntType
        when 'float32' then THREE.FloatType
        else throw new SCIWIS.SciwisException('invalid array dtype: ' + dtype.name)

    tex = new THREE.DataTexture(arr.data, arr.shape[1],
        arr.shape[0],
        format,
        type,
        THREE.UVMapping)

    # FIXME: if arr.shape[2] == 3, I need to create an array with
    # depth = 4 to make proper alignment of RGB (uint8) data
    tex.unpackAlignment = dtype.size
    tex.needsUpdate = true

    return tex


module.exports =

    # functions
    textureFromNumjis : textureFromNumjis
