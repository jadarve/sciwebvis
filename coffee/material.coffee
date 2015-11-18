
pointMaterial_vertex = """
void main() {
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0);
    gl_PointSize = 5.0; // pixels
}
"""

pointMaterial_fragment = """
void main() {
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0); // RGBA
}
"""

PointMaterial = new THREE.ShaderMaterial({
    vertexShader : pointMaterial_vertex,
    fragmentShader : pointMaterial_fragment
  })

# # material properties
# matprop =
#     color : 0x01BA23
#     size : 0.05
#     sizeAttenuation : true
#     fog : true
#     vertexColors : THREE.NoColors

# PointMaterial = new THREE.PointsMaterial(matprop);

class Material

    constructor: () ->
        return



module.exports =

    Material : Material

    PointMaterial : PointMaterial