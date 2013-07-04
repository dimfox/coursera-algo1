"""You are given a sorted (from smallest to largest) array A of n distinct
integers which can be positive, negative, or zero. You want to decide whether or
not there is an index i such that A[i] = i. Design the fastest algorithm that
you can for solving this problem.

Alogrithm:

index    0 1 2 3 4 5 6
element -1 0 2 3 5 6 9
             ^ ^

If a section of the array has the property that A[i] = i, then anything before
that section have A[i] < i, and anything after the section have A[i] > i

"""

import doctest
import random

def match_index(A):
    """Return True if there is an index i in A with A[i] = i

    >>> match_index([0, 1, 2])
    True
    >>> match_index([1, 2, 3])
    False
    >>> match_index([-1, 1, 4, 5])
    True
    >>> match_index([-1, 2, 3, 4])
    False
    """
    mid = len(A) / 2
    lb, ub = 0, len(A) - 1

    # Trivial case
    if len(A) == 0:
        return False

    if A[mid] == mid or A[lb] == lb or A[ub] == ub:
        return True

    while ub - lb > 1:
        if A[mid] == mid or A[lb] == lb or A[ub] == ub:
            return True
        elif A[mid] < mid:
            lb = mid
        elif A[mid] > mid:
            ub = mid
        mid = lb + (ub - lb) / 2
    return False


def random_test(test_cnt=20000):
    def _brute_force(A):
        for i in range(len(A)):
            if i == A[i]:
                return True
        return False

    for _ in xrange(test_cnt):
        problem_size = random.randint(0, 100)
        problem = [x - 50 for x in range(100)]
        random.shuffle(problem)
        problem1 = problem[:problem_size]
        problem1.sort()
        has_match1 = match_index(problem1)
        has_match2 = _brute_force(problem1)
        assert has_match1 == has_match2, 'Brute force: %s, problem: %s' % (
                has_match2, problem1)

if __name__ == '__main__':
    doctest.testmod()
    random_test()
