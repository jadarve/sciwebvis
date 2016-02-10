
varying vec4 vertexColor;

void main() {

    /* point radius */
    float r = length(gl_PointCoord - vec2(0.5, 0.5));
    gl_FragColor = vertexColor;

    if(r > 0.5) { discard; }
}
