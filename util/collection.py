#!/usr/bin/env python
"""Helper functions for work with collections.

Utils:

`unlist` -- extracts element from one-element collections:
    >>> unlist([]) is None
    True
    >>> unlist(['hello'])
    'hello'
    >>> unlist(['hello', 'world'])
    Traceback (most recent call last):
    ...
    TypeError: Cannot unlist collection: ['hello', 'world']
    Collection size is greater than 1.

`undict` -- extracts element from one-element dict:
    >>> undict({}) is None
    True
    >>> undict({'fruits': ['apple', 'banana']})
    ('fruits', ['apple', 'banana'])
    >>> undict({'fruit_0': 'apple', 'fruit_1': 'banana'})
    Traceback (most recent call last):
    ...
    TypeError: Cannot undict dictionary: {'fruit_0': 'apple', 'fruit_1': 'banana'}
    Dictionary size is greater than 1.
"""


def unlist(collection):
    """Extracts element from @collection if len(collection) 1.

    :returns: element in collection or None.
    :raises: TypeError if len(collection) > 1
    """
    if len(collection) > 1:
        raise TypeError("Cannot unlist collection: {0}\n".format(collection) +
                        "Collection size is greater than 1.")

    return collection[0] if len(collection) == 1 else None


def undict(dictionary):
    """Extracts tuple (key, value) from one-element dict.

    :returns: (key, value) tuple or None.
    :raises: TypeError if len(dictionary) > 1
    """
    if len(dictionary) > 1:
        raise TypeError("Cannot undict dictionary: {0}\n".format(dictionary) +
                        "Dictionary size is greater than 1.")
    return dictionary.items()[0] if len(dictionary) == 1 else None

if __name__ == '__main__':
    import doctest
    doctest.testmod()
