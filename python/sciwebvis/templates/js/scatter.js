    var vertex = dataDict['{{vertex}}'];    // retrieve data
    var material = materialDict['{{material}}'] // retrieve material
    var scatter = new SCIWIS.Scatter({vertex : vertex, material : material});  // scatter object
    axes.addObject(scatter);  // add to axes
