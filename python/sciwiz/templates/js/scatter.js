    // retrieve data
    var vertex = dataDict['{{vertex}}'];

    // create scatter object and set material
    var scatter = new SCIWIZ.Scatter({vertex : vertex});
    scatter.properties.material = SCIWIZ.PointMaterial;

    // add to axes
    axes.addObject(scatter);