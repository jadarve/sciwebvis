

class Scatter

    constructor: (prop) ->

        if not prop?
            throw new SCIWIS.SciwisException('expecting properties object')

        if not prop.geometry?
            throw new SCIWIS.SciwisException('geometry property not found')

        # unroll properties
        @geometry = prop['geometry']

        if not @geometry.hasAttribute('position')
            throw new SCIWIS.SciwisException('geometry object does not have position attribute')

        @material = if prop['material']? then prop['material'] else new SCIWIS.PointMaterial()


    update: (axes) ->

        # geometry
        # geometry = new THREE.BufferGeometry()
        # geometry.addAttribute('position', new THREE.BufferAttribute(@vertex.data, 3));

        # create and add mesh to axes' scene
        mesh = new THREE.Points(@geometry.getBufferGeometry(), @material.get())
        axes.scene.add(mesh)


# class Scatter

#     constructor: (prop) ->

#         if not prop?
#             throw new SCIWIS.SciwisException('expecting properties object')

#         if not prop.vertex?
#             throw new SCIWIS.SciwisException('vertex property not found')

#         # unroll properties
#         @vertex = prop['vertex']
#         @material = if prop['material']? then prop['material'] else new SCIWIS.PointMaterial()


#     update: (axes) ->

#         # geometry
#         geometry = new THREE.BufferGeometry()
#         geometry.addAttribute('position', new THREE.BufferAttribute(@vertex.data, 3));

#         # create and add mesh to axes' scene
#         mesh = new THREE.Points(geometry, @material.get())
#         axes.scene.add(mesh)


module.exports = 
    Scatter : Scatter
