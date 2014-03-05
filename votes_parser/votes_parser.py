#!/usr/bin/env python
"""Module for parsing game votings.

Example of parsing:
    >>> parse("1,2 7-10 4")
    [1, 2, 4, 7, 8, 9, 10]
    >>> parse(0)
    []
    >>> parse(None)
    []
    >>> parse("1,2 4;  ")
    [1, 2, 4]
"""

import re

def parse(votestr):
    if isinstance(votestr, int) and votestr != 0:
        votestr = str(votestr)

    if not isinstance(votestr, str):
        return []

    votestr = votestr.strip()
    if votestr[-1] == ';':
        votestr = votestr[:-1]

    votes = (v.split(',') for v in (v for v in votestr.split()))

    dash_vote = re.compile(r'^(\d+)-(\d+)$')
    votes = (range(int(dash_vote.match(v[0]).groups()[0]),
                   int(dash_vote.match(v[0]).groups()[1]) + 1) \
             if dash_vote.match(v[0]) else v for v in votes)
    try:
        votes = (int(v) for sub in votes for v in sub if v)
        votes = [v for v in set(votes)]
    except ValueError as ve:
        from StringIO import StringIO
        buf = StringIO()
        print >> buf, "Can't parse next voting:"
        print >> buf, ' '*8 + votestr
        print >> buf, "Parser error:", ve
        raise SyntaxError(buf.getvalue())
    votes.sort()
    return votes

if __name__ == '__main__':
    import doctest
    doctest.testmod()
