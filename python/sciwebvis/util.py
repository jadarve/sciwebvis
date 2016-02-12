"""
    sciwebvis.figure
    ----------------

    :copyright: 2015, Juan David Adarve. See AUTHORS for more details
    :license: 3-clause BSD, see LICENSE for more details
"""

import uuid


__all__ = ['generateID']


def generateID(keys=None):
    """Generates a new unique identifier.

    Parameters
    ----------
    keys : iterable, optional.
        List of other keys in which the new generated ID will be used.
        The returned key is guaranteed to not be equal to any key in
        the list.

    Returns
    -------
    ID : str.
        New generated ID
    """
    

    # create a new UUID
    ID = str(uuid.uuid4()).split('-')[-1]

    if keys == None:
        return ID

    # prevents duplicate keys, although unlikely
    while ID in keys:
        ID = str(uuid.uuid4()).split('-')[-1]

    return ID