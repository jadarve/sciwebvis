
    // retrieve vertex array from dictionary
    var vertices = dataDict['{{vertex}}']

    // var normals = NJ.surfaceVertexNormals(vertices);
    var faces = NJ.surfaceFaces(vertices);
    var UV = NJ.surfaceUVs(vertices);

    // creates geometry
    var geometry = new THREE.BufferGeometry();
    geometry.addAttribute( 'position', new THREE.BufferAttribute(vertices.data, 3));
    // geometry.addAttribute( 'normal', new THREE.BufferAttribute(normals.data, 3));
    geometry.addAttribute( 'uv', new THREE.BufferAttribute(UV.data, 2));
    geometry.setIndex(new THREE.BufferAttribute(faces.data, 1));

    
    var texture = undefined;

    {% if hasTexture %}
        console.log('hasTexture!');

        var texArr = dataDict['{{textureID}}'];
        var texHeight = texArr.shape[0];
        var texWidth = texArr.shape[0];

        console.log('tex dtype: ' + texArr.dtype.name);
        console.log('tex height: ' + texHeight);
        console.log('tex width: ' + texWidth);
        console.log(texArr.data[texArr.flat([500, 512])]);

        // TODO: figure out format and type from texArr
        texture = new THREE.DataTexture(texArr.data,
            texHeight, texWidth,
            THREE.LuminanceFormat, THREE.UnsignedByteType,
            THREE.UVMapping,
            THREE.ClampToEdgeWrapping, THREE.ClampToEdgeWrapping, 
            THREE.NearestFilter, THREE.NearestFilter, 1);

        // TODO: handle alignment
        texture.unpackAlignment = 1;
        texture.needsUpdate = true;

    {% endif %}

    // material properties
    var matprop = {
        color : {{color}},
        map : texture,
        side : THREE.DoubleSide,
        wireframe : {{wireframe}},
        wireframeLinewidth : {{wirewidth}}
    };

    // material
    var material = new THREE.MeshBasicMaterial(matprop);

    // mesh object
    var mesh = new THREE.Mesh(geometry, material);

    // add mesh to scene
    scene.add(mesh);