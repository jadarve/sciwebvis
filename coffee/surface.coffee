

class Surface

    constructor: (prop) ->

        if not prop?
            throw new SCIWIS.SciwisException('expecting properties object')

        if not prop.vertex?
            throw new SCIWIS.SciwisException('vertex property not found')

        @vertex = prop.vertex
        @faces = if prop['faces']? then prop['faces'] else SCIWIS.surfaceFaces(@vertex)
        @uv = if prop['uv']? then prop['uv'] else SCIWIS.surfaceUV(@vertex)
        @material = if prop['material'] then prop['material'] else new SCIWIS.WireframeMaterial()


    update: (axes) ->

        # TODO: replace by SCIWIS.Geometry

        # geometry
        geometry = new THREE.BufferGeometry()
        geometry.addAttribute('position', new THREE.BufferAttribute(@vertex.data, 3));
        geometry.addAttribute('uv', new THREE.BufferAttribute(@uv.data, 2))
        geometry.setIndex(new THREE.BufferAttribute(@faces.data, 1))

        # NJ.print(@uv)

        # create and add mesh to axes' scene
        mesh = new THREE.Mesh(geometry, @material.get())
        axes.scene.add(mesh)


module.exports =
    Surface : Surface
