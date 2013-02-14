"""Implement merge sort.

   def merge_sort(a)
      return merge(merge_sort(left_half_of_a),
                   merge_sort(right_half_of_a))
   def merge(a, b):
     for k in 1, n:
         if i not overflow or j over flow or a[i] < b[j]:
            c[k] = a[i]
            i += 1
         else:
            c[k] = b[j]
            j += 1
"""

def _merge(a, b):
    """Merge a and b in sorting order.

    >>> _merge([1, 2], [])
    [1, 2]
    >>> _merge([1, 2], [3, 4])
    [1, 2, 3, 4]
    >>> _merge([1, 3], [2, 4])
    [1, 2, 3, 4]
    >>> _merge([], [1, 2])
    [1, 2]
    >>> _merge([1, 2, 4], [3])
    [1, 2, 3, 4]
    """
    size = len(a) + len(b)
    c = []
    i, j = 0, 0
    for k in range(size):
        if j >= len(b) or (i < len(a) and a[i] < b[j]):
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
    return c


def merge_sort(a):
    """Merge sort.

    >>> merge_sort([1, 3, 2, 4])
    [1, 2, 3, 4]
    >>> merge_sort([4, 3, 2, 1])
    [1, 2, 3, 4]
    """
    if len(a) <= 1:
        return a
    half_point = len(a)/2
    return _merge(merge_sort(a[:half_point]), merge_sort(a[half_point:]))


def test_merge_sort(test_cnt):
    import random
    for _ in range(test_cnt):
        problem_size = random.randint(10, 3000)
        problem = range(problem_size)
        random.shuffle(problem)
        assert merge_sort(problem) == sorted(problem)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    test_merge_sort(100)
