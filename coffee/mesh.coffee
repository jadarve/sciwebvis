
surfaceUV = (arr) ->

    if !arr instanceof NJ.NDArray
        throw new error.NumjisException('argument is not a NDArray object')

    if !(arr.ndim == 2 || arr.ndim == 3)
        throw new error.NumjisException('Array dimensions should be 2 or 3, got: ' + arr.ndim)
    
    height = arr.shape[0]
    width = arr.shape[1]

    UV = new NJ.NDArray([height, width, 2], NJ.float32)

    for r in [0...height]
        for c in [0...width]

            UV.data[UV.flat([r, c, 0])] = r / (height-1)
            UV.data[UV.flat([r, c, 1])] = c / (width-1)

    return UV