
uniform vec4 color;
uniform float pointSize;

/* output color to fragment shader */
varying vec4 vertexColor;

void main() {

    gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0);
    gl_PointSize = pointSize; /* pixels */
    vertexColor = color;
}