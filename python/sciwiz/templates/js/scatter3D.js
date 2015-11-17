    // retrieve vertex array from dictionary
    var vertices = dataDict['{{vertex}}']
    
    var geometry = new THREE.BufferGeometry();
    geometry.addAttribute( 'position', new THREE.BufferAttribute(vertices.data, 3));

    // TODO: vertex colors [optional]

    // material properties
    var matprop = {
        color : {{color}},
        size : {{size}},
        sizeAttenuation : {{size_attenuation}},
        fog : {{fog}},

        // TODO: change value when vertex color is supported
        vertexColors : THREE.NoColors
    };

    // material
    var material = new THREE.PointsMaterial(matprop);

    // create mesh object
    var mesh = new THREE.Points( geometry, material );
    scene.add(mesh);
