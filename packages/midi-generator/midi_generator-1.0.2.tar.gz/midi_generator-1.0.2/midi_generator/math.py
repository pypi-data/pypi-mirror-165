from itertools import chain, combinations


def powerset(iterable):
    return list(map(lambda x: set(x), chain.from_iterable(combinations(iterable, r) for r in range(len(iterable)+1))))
