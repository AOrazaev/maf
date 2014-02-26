#!/usr/bin/env python

def euqlidean(x, y):
    result = list(x)
    for num, e in enumerate(y):
        result[num] = (result[num] - e) ** 2
    return sum(result)


def calc_distance(state, metric=euqlidean):
    distances = []
    for pos in state.position:
        cur = [euqlidean(pos, x) for x in state.position]
        distances.append(cur)

    return distances


def max_distance(distances):
    max_distance = list(set((y, tuple(sorted([p + 1, x + 1]))) \
                            for p, row in enumerate(distances) \
                            for x, y in enumerate(row)
                           ))
    max_distance.sort(reverse=True)
    return max_distance
