
# library object
SCIWIS = {}

# append library to window, if it is being used in a web browser
window.SCIWIS = SCIWIS if window?


appendModule = (root, module) ->
    """
    Append module objects to root object
    """
    for m in Object.keys(module)
        root[m] = module[m]


# append modules
appendModule(SCIWIS, require('./error'))
appendModule(SCIWIS, require('./figure'))
appendModule(SCIWIS, require('./material'))
appendModule(SCIWIS, require('./geometry'))
appendModule(SCIWIS, require('./color'))
appendModule(SCIWIS, require('./mesh'))
appendModule(SCIWIS, require('./scatter'))
# appendModule(SCIWIS, require('./surface'))
appendModule(SCIWIS, require('./texture'))

module.exports = SCIWIS