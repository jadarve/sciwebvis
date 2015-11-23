
###
Convert from NJ.NDArray to THREE.Vector4 color representation

@param [NJ.NDArray] c color array with 1, 3, or 4 components
  if c.length == 1, c represents a gray scal color, alpha = 1.0
  if c.length == 3, c represents a RGB color, alpha = 1.0
  if c.length == 4, c represents a RGBA color

@return [THREE.Vector4] RBGA color
###
color2vec4 = (c) ->
    
    if !c instanceof NJ.NDArray
        throw new SCIWIZ.SciwizException('Expecting NJ.NDArray object')

    [R, G, B, A] = [1.0, 1.0, 1.0, 1.0]
    switch c.length
        when 1 then [R, G, B] = [c.data[0], c.data[0], c.data[0]]
        when 3 then [R, G, B] = [c.data[0], c.data[1], c.data[2]]
        when 4 then [R, G, B, A] = [c.data[0], c.data[1], c.data[2], c.data[3]]
        else throw new SCIWIZ.SciwizException('Unexpected color length: got: ' + c.length)

    return new THREE.Vector4(R, G, B, A)

###
Return a random RGB color with given alpha

@param [float] alpha alpha value [0, 1]

@return [NJ.NDArrray] 4 element array with RGBA value
###
randomColor = (alpha=1.0) ->
    return NJ.array([Math.random(), Math.random(), Math.random(), alpha], dtype=NJ.float32)

module.exports =
    color2vec4 : color2vec4
    randomColor : randomColor
