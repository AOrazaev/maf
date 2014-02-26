#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
Utils for maf module.

`str_pmatrix`
    Make human readble str representation of player matrix.
    >>> str_pmatrix([[1., 0.199996], [0.8, 1.]])
    '[  1: [1.000, 0.200] \n   2: [0.800, 1.000] ]\n'
"""

from StringIO import StringIO

def str_pmatrix(mat):
    buf = StringIO()
    for num, row in enumerate(mat):
        print >>buf, "[" if num == 0 else "\n ",
        print >>buf, "%2d:" % (num + 1, ),
        for n, r in enumerate(row):
            print >>buf, "[%.3f," % (r,) if n == 0 else \
                        ("%.3f," % (r,) if n + 1 != len(row) else \
                         "%.3f]"% (r)),
    print >>buf, ']'
    return buf.getvalue()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
