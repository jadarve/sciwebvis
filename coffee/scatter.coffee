

class Scatter

    constructor: (prop) ->

        if not prop?
            throw new SCIWIZ.SciwizException('expecting properties object')

        if not prop.vertex?
            throw new SCIWIZ.SciwizException('vertex property not found')

        # unroll properties
        @vertex = prop['vertex']
        @material = if prop['material']? then prop['material'] else new SCIWIZ.PointMaterial()


    update: (axes) ->

        # geometry
        geometry = new THREE.BufferGeometry()
        geometry.addAttribute('position', new THREE.BufferAttribute(@vertex.data, 3));

        # create and add mesh to axes' scene
        mesh = new THREE.Points(geometry, @material.get())
        axes.scene.add(mesh)


module.exports = 
    Scatter : Scatter
