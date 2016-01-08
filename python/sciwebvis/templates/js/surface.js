    var vertex = dataDict['{{vertex}}'];    // retrieve data
    var material = materialDict['{{material}}'] // retrieve material

    // TODO: faces and UVs

    var surface = new SCIWIS.Surface({vertex : vertex, material : material});  // surface object
    axes.addObject(surface);  // add to axes

