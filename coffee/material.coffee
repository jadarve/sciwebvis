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

# PointMaterial_ = new THREE.ShaderMaterial({
#     vertexShader : pointMaterial_vertex
#     fragmentShader : pointMaterial_fragment
#     # transparent : true
#     defines :
#         version : 110
#   })

TextureMaterial_vertex = """

varying vec2 vertexUV;

void main() {
    vertexUV = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0);
}
"""

TextureMaterial_fragment = """
uniform sampler2D textureSampler;

varying vec2 vertexUV;

void main() {
    float lum = texture2D(textureSampler, vertexUV).x;
    //gl_FragColor = vec4(lum.x, lum.x, lum.x, 1.0);

    //gl_FragColor = texture2D(textureSampler, vertexUV);
    gl_FragColor = lum*vec4(1.0, 0.0, 0.0, 0.0);
}
"""

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

        #  test for undefined prop
        prop = if prop? then prop else new Array()

        # unroll properties
        @pointSize = if prop['pointSize'] then prop['pointSize'] else 5
        @color = if prop['color']? then prop['color'] else new SCIWIS.Color()
        @transparent = if prop['transparent']? then prop['transparent'] else true

    get: () ->
        return new THREE.ShaderMaterial({
            vertexShader : pointMaterial_vertex
            fragmentShader : pointMaterial_fragment
            transparent : @transparent
            uniforms:
                pointSize : {type : 'f', value : @pointSize}
                color : {type : 'v4', value : @color.vec4()}
            })


class WireframeMaterial

    constructor: (prop) ->

        # test for undefined prop
        prop = if prop? then prop else new Array()

        # unroll properties
        @color = if prop['color']? then prop['color'] else new SCIWIS.Color()
        @transparent = if prop['transparent']? then prop['transparent'] else true
        @lineWidth = if prop['lineWidth']? then prop['lineWidth'] else 1
    

    get: () ->

        return new THREE.MeshBasicMaterial({
                wireframe : true
                wireframeLinewidth : @lineWidth
                color : @color.intRGB()
                transparent : @transparent
                opacity : @color.A
            })        


class TextureMaterial

    constructor: (prop) ->

        # test for undefined prop
        prop = if prop? then prop else new Array()

        # unroll properties
        if prop['texture']
            # numjis array
            @texture = prop['texture']
        else
            throw new SCIWIS.SciwisException('texture property not set')

    get: () ->

        # console.log('TextureMaterial.get(): shape: ' + @texture.shape)
        # console.log('texture dtype: ' + @texture.dtype.name)

        # THIS WORKS!
        # tex = new THREE.DataTexture(@texture.data, @texture.shape[1],
        #     @texture.shape[0],
        #     THREE.LuminanceFormat,
        #     THREE.UnsignedByteType,
        #     THREE.UVMapping)
        # tex.unpackAlignment = 1
        # tex.needsUpdate = true

        # creates texture object from numjis array
        tex = SCIWIS.textureFromNumjis(@texture)

        return new THREE.ShaderMaterial({
            vertexShader : TextureMaterial_vertex
            fragmentShader : TextureMaterial_fragment
            transparent : false
            uniforms:
                textureSampler : {type : 't', value : tex}
            })


module.exports =

    Material : Material
    PointMaterial : PointMaterial
    WireframeMaterial : WireframeMaterial
    TextureMaterial : TextureMaterial