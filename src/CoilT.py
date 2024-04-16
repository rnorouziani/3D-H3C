import math


class CoilT:
    def __init__(self, r, l, n, max_i):

        if not (0 < r):
            raise ValueError("Error: Radius must be bigger than 0.")
        if not (0 < l):
            raise ValueError("Distance between the coils must be bigger than 0.")
        if not (isinstance(n, int) and n >= 1):
            raise ValueError("Error: The number of turns must be elements of the set of natural numbers.")
        if not (0 < max_i):
            raise ValueError("Error: maximum current must be bigger than 0.")

        self.r = r
        self.l = l
        self.n = n
        self.max_i = max_i
