    var vertex = dataDict['{{vertex}}'];    // retrieve data
    // var material = materialDict['{{material}}'] // retrieve material

    // TODO: faces and UVs

    var surface = new SCIWIZ.Surface({vertex : vertex});  // surface object
    axes.addObject(surface);  // add to axes

