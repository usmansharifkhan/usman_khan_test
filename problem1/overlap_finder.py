

def find_overlap(tup1, tup2):
    if not isinstance(tup1, tuple) or not isinstance(tup2, tuple):
        raise TypeError("Supplied arguments needs to be tuple")
    if len(tup1) != 2 or len(tup2) != 2:
        raise AttributeError("Tuple arguments needs to be the size of 2")
    return _check_middle(tup1, tup2[0]) or _check_middle(tup1, tup2[1])


def _check_middle(tup1, num):
    if tup1[0] < tup1[1]:
        return tup1[0] <= num <= tup1[1]
    else:
        return tup1[1] <= num <= tup1[0]


