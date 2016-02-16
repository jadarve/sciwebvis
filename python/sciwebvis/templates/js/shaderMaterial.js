SCIWIS.ShaderMaterial({
    vertex: 'uniform vec4 color;uniform float pointSize;/* output color to fragment shader */varying vec4 vertexColor;void main() {    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);    gl_PointSize = pointSize; /* pixels */    vertexColor = color;}',
    fragment: 'varying vec4 vertexColor;void main() {    /* point radius */    float r = length(gl_PointCoord - vec2(0.5, 0.5));    gl_FragColor = vertexColor;    if(r > 0.5) { discard; }}',
    transparent: true,
    uniforms: {pointSize : {type : 'f', value : 10}, color : {type : 'v4', value : new THREE.Vector4(1.0, 0.0, 0.0, 1.0)}}
})