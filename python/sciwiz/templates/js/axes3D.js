

// Before is the creation of dataDict containing
var scene, camera, renderer, controls;

initScene();
animate();

// render for the first time
render();

function initScene() {
    scene = new THREE.Scene();

    var width = {{width}};
    var height = {{height}};

    // Renderer
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(width, height);
    renderer.setClearColor({{bgcolor}})
    $('div#{{id}}').append(renderer.domElement);


    // Camera
    var aspectRatio = width / height;
    camera = new THREE.PerspectiveCamera( 75, aspectRatio, 0.1, 1000 );
    camera.position.z = 2;

    controls = new THREE.OrbitControls( camera, renderer.domElement );
    controls.addEventListener( 'change', render ); // add this only if there is no animation loop (requestAnimationFrame)
    controls.enableDamping = true;
    controls.dampingFactor = 0.25;
    controls.enableZoom = true;

    // Render objects
    {% for obj in objects %}
    {
        {{obj}}
    };
    {% endfor %}
}


function animate() {

    // requestAnimationFrame( animate );
    // controls.update(); // required if controls.enableDamping = true, or if controls.autoRotate = true
    // render();
}

// var render = function () {
//     requestAnimationFrame(render);
//     camera.rotation.z += 0.01;
//     renderer.render(scene, camera);
// };

// render();

function render() {
    renderer.render( scene, camera );
}


