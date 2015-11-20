    var vertex = dataDict['{{vertex}}'];    // retrieve data
    var scatter = new SCIWIZ.Scatter({vertex : vertex, material : SCIWIZ.PointMaterial});  // scatter object
    axes.addObject(scatter);  // add to axes