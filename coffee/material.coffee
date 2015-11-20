
pointMaterial_vertex = """
varying vec4 color;

void main() {
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0);
    gl_PointSize = 10.0; // pixels
    color = vec4(0.0, 1.0, 0.0, 0.5);
}
"""

pointMaterial_fragment = """
varying vec4 color;
void main() {
    float r = length(gl_PointCoord - vec2(0.5, 0.5)); // radius
    float s = step(r, 0.5);
    gl_FragColor = (1.0-s)*vec4(1.0, 1.0, 1.0, 0.0) + s*color;
}
"""

PointMaterial = new THREE.ShaderMaterial({
    vertexShader : pointMaterial_vertex
    fragmentShader : pointMaterial_fragment
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



module.exports =

    Material : Material

    PointMaterial : PointMaterial