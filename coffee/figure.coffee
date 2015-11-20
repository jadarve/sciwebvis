

class Figure

    constructor: (prop) ->

        console.log('Figure constructor')

        @properties = prop

        # axes
        @axes = new Array()

        # figure container element, a <div>
        @container = $('#'+@properties.ID)
        @container.append('<h2>SciWiz Figure</h2')


    addAxes: (prop) ->

        # generate axes container
        axesID = @properties.ID + '_axes_' + @axes.length
        console.log('axes ID: ' + axesID)

        axContainer = @container.append('<div></div>')
        axContainer.attr('id', axesID)
        axContainer.append(axesID)

        ax = new Axes(axesID, prop)
        
        @axes.push(ax)
        return ax



class Axes

    constructor: (containerID, prop) ->

        @container = $('#'+containerID)

        @properties = prop

        # render objects
        @objects = new Array()

        # renderer
        @renderer = new THREE.WebGLRenderer()
        @renderer.setSize(@properties.width, @properties.height)
        @renderer.setClearColor(@properties.bgcolor)
        @container.append(@renderer.domElement)

        # scene
        @scene = new THREE.Scene();

        # camera
        # aspect ratio
        ar = @properties.width / @properties.height

        @camera = new THREE.PerspectiveCamera( 75, ar, 0.1, 1000 );
        @camera.position.z = 2;

        # render objects
        @renderObjects = new Array()

        # camera controls
        @controls = new THREE.OrbitControls( @camera, @renderer.domElement )
        @controls.addEventListener( 'change', @.render ) # add this only if there is no animation loop (requestAnimationFrame)
        @controls.enableDamping = true
        @controls.dampingFactor = 0.25
        @controls.enableZoom = true


        # the axes needs to be updated after creation
        @needsUpdate = true


    addObject: (obj) ->

        console.log('adding new object')
        @renderObjects.push(obj)


    # notice the use of fat arrow!
    render: () =>


        # enable alpha blending
        # TODO: make optional
        GL = @renderer.context
        GL.enable(GL.BLEND)
        GL.blendFunc(GL.SRC_ALPHA, GL.ONE_MINUS_SRC_ALPHA)

        if @needsUpdate

            console.log('calling update')

            # call update to all render objects
            for obj in @renderObjects
                obj.update(@)

            @needsUpdate = false

        @renderer.render(@scene, @camera)


module.exports = 

    Figure : Figure
    Axes : Axes