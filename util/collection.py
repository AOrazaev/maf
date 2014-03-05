#!/usr/bin/env python
# -*- coding: utf-8 -*-
ur"""Helper functions for work with collections.

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

`strlist` -- convert list to readable string.
    >>> print strlist([u'Строки', 'Юникод', 123])
    [Строки, Юникод, 123]
    >>> print strlist(['Строки'])
    [Строки]

    Feel difference:
    >>> print ['Строки']
    ['\xd0\xa1\xd1\x82\xd1\x80\xd0\xbe\xd0\xba\xd0\xb8']

`join` -- join list of iterable to list.
    >>> join([[1, 2], "Sasha", xrange(4)])
    [1, 2, 'S', 'a', 's', 'h', 'a', 0, 1, 2, 3]
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


def strlist(li):
    """:returns: str represintation of list. But elements are represented
    by str(elem), insead of repr(elem).

    Not [u'Строка'], but [Строка]
    """
    result = u'['
    for num, elem in enumerate(li):
        result += elem if isinstance(elem, str) or isinstance(elem, unicode) \
                  else str(elem)
        if num + 1 != len(li):
            result += ', '
    result += ']'
    return result.encode('utf-8')


def join(li):
    """:returns: list of objs joined from list of iterable with objs.

    >>> join([[1,2], [3], [4,5]])
    [1, 2, 3, 4, 5]
    """
    result = []
    for iterable in li:
        for obj in iterable:
            result.append(obj)
    return result


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    import doctest
    doctest.testmod()
