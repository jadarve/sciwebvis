

class Scatter

    constructor: (prop) ->

        # @axes = axes
        @properties = prop

        # numjis array
        vertex = @properties.vertex

        geometry = new THREE.BufferGeometry()
        geometry.addAttribute( 'position', new THREE.BufferAttribute(vertex.data, 3));
        @properties.geometry = geometry



    update: (axes) ->

        mesh = new THREE.Points(@properties.geometry,
            @properties.material.material)

        axes.scene.add(mesh)


module.exports = 
    Scatter : Scatter
