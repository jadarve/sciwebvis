
###
Computes surface UV for a grid of points
###
meshUV = (arr) ->

    if !arr instanceof NJ.NDArray
        throw new error.NumjisException('argument is not a NDArray object')

    if !(arr.ndim == 2 || arr.ndim == 3)
        throw new error.NumjisException('Array dimensions should be 2 or 3, got: ' + arr.ndim)
    
    height = arr.shape[0]
    width = arr.shape[1]

    UV = new NJ.NDArray([height, width, 2], NJ.float32)

    for r in [0...height]
        for c in [0...width]

            UV.data[UV.flat([r, c, 0])] = r / (height-1)
            UV.data[UV.flat([r, c, 1])] = c / (width-1)

    return UV


###
Computes vertex indices for each triangle in a surface
###
meshFaces = (arr) ->
    
    if !arr instanceof NJ.NDArray
        throw new NJ.NumjisException('argument is not a NDArray object')

    if !(arr.ndim == 2 || arr.ndim == 3)
        throw new NJ.NumjisException('Array dimensions should be 2 or 3, got: ' + arr.ndim)

    
    height = arr.shape[0]
    width = arr.shape[1]

    faces = new NJ.NDArray([height-1, width-1, 6], NJ.uint32)

    for r in [0...height-1]
        for c in [0...width-1]

            # first triangle
            faces.data[faces.flat([r,c,0])] = r*width + c
            faces.data[faces.flat([r,c,1])] = (r+1)*width + c + 1
            faces.data[faces.flat([r,c,2])] = (r+1)*width + c

            # second triangle
            faces.data[faces.flat([r,c,3])] = r*width + c
            faces.data[faces.flat([r,c,4])] = r*width + c + 1
            faces.data[faces.flat([r,c,5])] = (r+1)*width + c + 1
    
    return faces


class Mesh

    constructor: (prop) ->

        if not prop?
            throw new SCIWIS.SciwisException('expecting properties object')

        if not prop.geometry?
            throw new SCIWIS.SciwisException('geometry property not found')

        @geometry = prop.geometry

        # texture UV coordinates
        if not @geometry.hasAttribute('uv')
            console.log('Mesh.constructor. Creating UV coordinates')
            @geometry.addAttribute('uv', SCIWIS.meshUV(@geometry.attributes['position']))

        # Triangle face indices
        if not @geometry.hasAttribute('index')
            console.log('Mesh.constructor. Creating face index.')
            @geometry.addAttribute('index', SCIWIS.meshFaces(@geometry.attributes['position']))

        # @vertex = prop.vertex
        # @faces = if prop['faces']? then prop['faces'] else SCIWIS.meshFaces(@vertex)
        # @uv = if prop['uv']? then prop['uv'] else SCIWIS.meshUV(@vertex)

        @material = if prop['material'] then prop['material'] else new SCIWIS.WireframeMaterial()


    update: (axes) ->

        # TODO: replace by SCIWIS.Geometry

        # geometry
        # geometry = new THREE.BufferGeometry()
        # geometry.addAttribute('position', new THREE.BufferAttribute(@vertex.data, 3));
        # geometry.addAttribute('uv', new THREE.BufferAttribute(@uv.data, 2))
        # geometry.setIndex(new THREE.BufferAttribute(@faces.data, 1))

        # NJ.print(@uv)

        # create and add mesh to axes' scene
        mesh = new THREE.Mesh(@geometry.getBufferGeometry(), @material.get())
        axes.scene.add(mesh)

# class Mesh

#     constructor: (prop) ->

#         if not prop?
#             throw new SCIWIS.SciwisException('expecting properties object')

#         if not prop.vertex?
#             throw new SCIWIS.SciwisException('vertex property not found')

#         @vertex = prop.vertex
#         @faces = if prop['faces']? then prop['faces'] else SCIWIS.meshFaces(@vertex)
#         @uv = if prop['uv']? then prop['uv'] else SCIWIS.meshUV(@vertex)
#         @material = if prop['material'] then prop['material'] else new SCIWIS.WireframeMaterial()


#     update: (axes) ->

#         # TODO: replace by SCIWIS.Geometry

#         # geometry
#         geometry = new THREE.BufferGeometry()
#         geometry.addAttribute('position', new THREE.BufferAttribute(@vertex.data, 3));
#         geometry.addAttribute('uv', new THREE.BufferAttribute(@uv.data, 2))
#         geometry.setIndex(new THREE.BufferAttribute(@faces.data, 1))

#         # NJ.print(@uv)

#         # create and add mesh to axes' scene
#         mesh = new THREE.Mesh(geometry, @material.get())
#         axes.scene.add(mesh)


module.exports =
    meshUV : meshUV
    meshFaces : meshFaces
    Mesh : Mesh