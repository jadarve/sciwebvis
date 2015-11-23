# color = require('./color')

# pointMaterial_vertex = """
# uniform float pointSize;
# varying vec4 color;

# void main() {
#     gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0);
#     gl_PointSize = pointSize; // pixels
#     color = vec4(0.0, 1.0, 0.0, 0.5);
# }
# """

pointMaterial_vertex = """

uniform vec4 color;
uniform float pointSize;

/* output color to fragment shader */
varying vec4 vertexColor;

void main() {

    gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0);
    gl_PointSize = pointSize; /* pixels */
    vertexColor = color;
}
"""

pointMaterial_fragment = """
varying vec4 vertexColor;
void main() {
    float r = length(gl_PointCoord - vec2(0.5, 0.5)); // radius
    gl_FragColor = vertexColor;
    if(r > 0.5) { discard; }
}
"""

PointMaterial_ = new THREE.ShaderMaterial({
    vertexShader : pointMaterial_vertex
    fragmentShader : pointMaterial_fragment
    # transparent : true
    defines :
        version : 110
  })

# material properties
# matprop =
#     color : 0x01BA23
#     size : 0.05
#     sizeAttenuation : true
#     fog : true
#     vertexColors : THREE.NoColors
#     transparent : true
#     opacity : 0.5

# PointMaterial = new THREE.PointsMaterial(matprop);


class Material

    constructor: () ->
        return


class PointMaterial

    constructor: (prop) ->

        # unroll properties
        @properties = new Array()
        @properties['pointSize'] = if prop['pointSize'] then prop['pointSize'] else 5
        @properties['color'] = if prop['color']? then SCIWIZ.color2vec4(prop['color']) else SCIWIZ.color2vec4(SCIWIZ.randomColor())
        @properties['transparent'] = if prop['transparent']? then prop['transparent'] else true

        @material = new THREE.ShaderMaterial({
            vertexShader : pointMaterial_vertex
            fragmentShader : pointMaterial_fragment
            transparent : @properties['transparent']
            uniforms:
                pointSize : {type : 'f', value : @properties['pointSize']}
                color : {type : 'v4', value : @properties['color']}
            })


module.exports =

    Material : Material
    PointMaterial : PointMaterial