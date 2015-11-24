
# library object
SCIWIZ = {}

# append library to window, if it is being used in a web browser
window.SCIWIZ = SCIWIZ if window?


appendModule = (root, module) ->
    """
    Append module objects to root object
    """
    for m in Object.keys(module)
        root[m] = module[m]


# append modules
appendModule(SCIWIZ, require('./error'))
appendModule(SCIWIZ, require('./figure'))
appendModule(SCIWIZ, require('./material'))
appendModule(SCIWIZ, require('./color'))
appendModule(SCIWIZ, require('./mesh'))
appendModule(SCIWIZ, require('./scatter'))
appendModule(SCIWIZ, require('./surface'))

module.exports = SCIWIZ