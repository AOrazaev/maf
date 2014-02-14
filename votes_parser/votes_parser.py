#!/usr/bin/env python

import re

def parse(votestr):
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

