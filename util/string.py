#!/usr/bin/env python
"""Helper functions for work with strings.

Helpers:
    `ci_equals` -- case insensative equal for str and other objects.
    >>> ci_equals(1, 'both')
    False
    >>> ci_equals('BoTh', 'both')
    True
    >>> ci_equals(1, 1)
    True
"""

def ci_equals(left, right):
    """Check is @left string is case-insensative equal to @right string.

    :returns: left.lower() == right.lower() if @left and @right is str. Or
    left == right in other case.
    """
    if isinstance(left, str) and isinstance(right, str):
        return left.lower() == right.lower()

    return left == right
