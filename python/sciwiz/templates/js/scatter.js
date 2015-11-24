    var vertex = dataDict['{{vertex}}'];    // retrieve data
    var material = materialDict['{{material}}'] // retrieve material

    // var matProp = {
    //     pointSize : 20.0
    // };
    // var material = new SCIWIZ.PointMaterial(matProp)
    var scatter = new SCIWIZ.Scatter({vertex : vertex, material : material});  // scatter object
    axes.addObject(scatter);  // add to axes

