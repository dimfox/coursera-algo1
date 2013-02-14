import doctest
import random
import sys

"""Counting inversions.
Count number of pairs in an array that are in reverse order. E.g
[1, 2, 3, 5, 4] has one pair of inversion (4, 5), [1, 4, 2, 3, 5]
has 2 pairs of inversions (2, 4) and (3, 4)

def count_inversion(a):
  return count_inversion(left_half_of_a) +
         count_inversion(right_half_of_a) +
         count_split_inversion(sorted_left_half_of_a, sorted_right_half_of_a)

def count_split_inversion(a, b):
  inversion_cnt = 0
  for k in 1, n:
    if j over flow or (i not overflow and a[i] < b[j]):
      c[k] = a[i]
      i += 1
    else:
      c[k] = b[j]
      j += 1
      inversion_cnt += len(a) - i
"""

def inversion_cnt(a):
    """Count inversions in array a.

    >>> inversion_cnt([1, 2, 3, 5, 4])
    (1, [1, 2, 3, 4, 5])

    >>> inversion_cnt([1, 2, 3, 4, 5])
    (0, [1, 2, 3, 4, 5])

    >>> inversion_cnt([1, 4, 2, 3, 5])
    (2, [1, 2, 3, 4, 5])

    >>> inversion_cnt([5, 4, 3, 2, 1])
    (10, [1, 2, 3, 4, 5])

    >>> inversion_cnt([6, 5, 4, 3, 2, 1])
    (15, [1, 2, 3, 4, 5, 6])
    """
    if len(a) <= 1:
        return (0, a)
    half_point = len(a)/2
    left_inversion, left_sorted = inversion_cnt(a[:half_point])
    right_inversion, right_sorted = inversion_cnt(a[half_point:])
    split_inversion, all_sorted = _split_inversion(left_sorted, right_sorted)
    return (left_inversion + right_inversion + split_inversion, all_sorted)

def _split_inversion(a, b):
    """Count inversions between two sorted array a and b.

    >>> _split_inversion([1, 2], [3, 4])
    (0, [1, 2, 3, 4])

    >>> _split_inversion([1, 3], [2, 4])
    (1, [1, 2, 3, 4])

    >>> _split_inversion([3], [2, 4])
    (1, [2, 3, 4])

    >>> _split_inversion([1], [])
    (0, [1])
    """
    inversion_cnt = 0
    c = []
    i, j = 0, 0
    for k in range(len(a) + len(b)):
        if j >= len(b) or (i < len(a) and a[i] < b[j]):
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
            inversion_cnt += len(a) - i
    return (inversion_cnt, c)

def _brute_force(a):
    """Brute force to solve inversion count.
    >>> _brute_force([1, 2, 3, 5, 4])
    1

    >>> _brute_force([1, 2, 3, 4, 5])
    0

    >>> _brute_force([1, 4, 2, 3, 5])
    2

    >>> _brute_force([5, 4, 3, 2, 1])
    10

    >>> _brute_force([6, 5, 4, 3, 2, 1])
    15
    """
    cnt = 0
    for i, x in enumerate(a):
        for j in range(i+1, len(a)):
            y = a[j]
            if x > y:
                cnt += 1
    return cnt


def test_inversions(test_cnt=200):


    for _ in range(test_cnt):
        problem_size = random.randint(1, 10)
        problem = range(problem_size)
        random.shuffle(problem)
        inversion_cnt1, _ = inversion_cnt(problem)
        inversion_cnt2 = _brute_force(problem)
        assert inversion_cnt1 == inversion_cnt2

def read_input(filename):
    a = []
    with open(filename) as f:
        for line in f:
            n = int(line)
            a.append(n)
    return a

if __name__ == "__main__":

    if len(sys.argv) == 1:
        # run test
        doctest.testmod()
        test_inversions(200)
    else:
        cnt, _ = inversion_cnt(read_input(sys.argv[1]))
        print cnt
