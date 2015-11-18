
var vertex = dataDict['{{vertex}}'];
var scatter = new SCIWIZ.Scatter({vertex : vertex});

// material properties
var matprop = {
    color : 0x01BA23,
    size : 0.05,
    sizeAttenuation : true,
    fog : true,
    vertexColors : THREE.NoColors
};
var material = new THREE.PointsMaterial(matprop);

// add material to scatter
scatter.properties.material = material;

axes.addObject(scatter);