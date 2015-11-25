

class Surface

    constructor: (prop) ->

        if not prop?
            throw new SCIWIZ.SciwizException('expecting properties object')

        if not prop.vertex?
            throw new SCIWIZ.SciwizException('vertex property not found')

        @vertex = prop.vertex
        @faces = if prop['faces']? then prop['faces'] else SCIWIZ.surfaceFaces(@vertex)
        @uv = if prop['uv']? then prop['uv'] else SCIWIZ.surfaceUV(@vertex)
        @material = if prop['material'] then prop['material'] else new SCIWIZ.WireframeMaterial()


    update: (axes) ->

        # geometry
        geometry = new THREE.BufferGeometry()
        geometry.addAttribute('position', new THREE.BufferAttribute(@vertex.data, 3));
        geometry.addAttribute('uv', new THREE.BufferAttribute(@uv.data, 2))
        geometry.setIndex(new THREE.BufferAttribute(@faces.data, 1))

        # create and add mesh to axes' scene
        mesh = new THREE.Mesh(geometry, @material.get())
        axes.scene.add(mesh)


module.exports =
    Surface : Surface