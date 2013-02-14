"""Quicksort.

Algorithm:

def quicksort(a):

   pivot = pick a pivot, and put it at beginning of the array
   left, right = partition a by pivot, where all elements left to pivot is <= pivot
                 and all elements right to pivot is >= pivot
   quicksort(left)
   quicksort(right)

def partition(a):
    Assume that pivot is at position a[0]
    i = 1
    for j = 1 to last element of a:
      if a[j] > pivot:
        swap a[j] and a[i]
        i ++
    swap a[0] and a[i-1]
    i-1 is where the pivot is after partition.
"""

import doctest
import random

cmp_cnt = 0

def choose_pivot_first_element(a, start_ind, end_ind):
    pass  # just use first element as pivot

def choose_pivot_last_element(a, start_ind, end_ind):
    # use last element as pivot
    a[start_ind], a[end_ind-1] = a[end_ind - 1], a[start_ind]

def choose_pivot_median_of_three(a, start_ind, end_ind):
    """Use median of first, last and middle element."""
    first = a[start_ind]
    last = a[end_ind - 1]
    if (end_ind - start_ind) % 2 == 0:
        middle_ind = start_ind + (end_ind - start_ind)/2 - 1
    else:
        middle_ind = start_ind + (end_ind - start_ind)/2
    middle = a[middle_ind]
    if first >= middle >= last or first <= middle <= last:
        # middle element is the median
        a[start_ind], a[middle_ind] = a[middle_ind], a[start_ind]
    elif middle >= first >= last or middle <= first <= last:
        pass # first element is the median
    else:
        # last elment is median
        a[start_ind], a[end_ind-1] = a[end_ind - 1], a[start_ind]


def quicksort(a, pivot_func=choose_pivot_first_element):
    """Quick sort

    >>> a = [1, 2, 3, 4, 5]; quicksort(a); print a
    [1, 2, 3, 4, 5]
    >>> a = [1, 1, 3, 3, 2, 2, 5]; quicksort(a); print a
    [1, 1, 2, 2, 3, 3, 5]
    >>> a = [1]; quicksort(a); print a
    [1]
    >>> a = []; quicksort(a); print a
    []

    """
    global cmp_cnt
    cmp_cnt = 0  # number of comparisions made

    def _quicksort(start_ind, end_ind):
        """Sort the part of a from start_ind (inclusive) to end_ind (exclusive)."""
        if end_ind - start_ind <= 1:
            return
        #if end_ind - start_ind == 2:
        #    if a[start_ind] > a[start_ind + 1]:
        #        a[start_ind], a[start_ind + 1] = a[start_ind + 1], a[start_ind]
        #    return

        # partition
        split_ind = _partition(start_ind, end_ind)
        # sort left and right of the pivot
        _quicksort(start_ind, split_ind)
        _quicksort(split_ind + 1, end_ind)

    def _partition(start_ind, end_ind):
        global cmp_cnt
        cmp_cnt += end_ind - start_ind - 1

        # choose a pivot and swap it to start_ind
        pivot_func(a, start_ind, end_ind)
        pivot = a[start_ind]

        # boundary between < pivot and > pivot, this points at the first element
        # that is >= pivot
        i = start_ind + 1
        # j is boundary between partitioned elements and not partitioned elements
        # This points at last partitioned element

        for j in range(start_ind + 1, end_ind):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        # swap pivot to middle
        a[i - 1], a[start_ind] = a[start_ind], a[i - 1]
        return i - 1

    _quicksort(0, len(a))


def test_quicksort(test_cnt=30):
    for _ in xrange(test_cnt):
        for pivot_func in (choose_pivot_first_element,
                           choose_pivot_last_element,
                           choose_pivot_median_of_three):
            problem_size = random.randint(0, 2000)
            problem = range(problem_size)
            random.shuffle(problem)
            quicksort(problem, pivot_func)
            assert range(problem_size) == problem

def test_pivot_count():
    """test pivot count."""
    f1 = choose_pivot_first_element
    f2 = choose_pivot_last_element
    f3 = choose_pivot_median_of_three

    for a, f, cnt in [(range(10), f1, 45),
                      (range(10), f2, 45),
                      (range(10), f3, 19),
                      (range(10, 0, -1), f1, 45),
                      (range(10, 0, -1), f2, 45),
                      (range(10, 0, -1), f3, 19),
                      (range(100), f1, 4950),
                      (range(100), f2, 4950),
                      (range(100), f3, 480),
                      (range(100, 0, -1), f1, 4950),
                      (range(100, 0, -1), f2, 4950),
                      (range(100, 0, -1), f3, 1302),
                      ([2, 8, 9, 3, 7, 5, 10, 1, 6, 4], f1, 25),
                      ([2, 8, 9, 3, 7, 5, 10, 1, 6, 4], f2, 20),
                      ([2, 8, 9, 3, 7, 5, 10, 1, 6, 4], f3, 19),
                      ]:
        quicksort(a, f)
        assert cmp_cnt == cnt, '%s, %s, %s' % (f, cnt, cmp_cnt)


def read_input(file_name):
    a = []
    with open(file_name) as f:
        for line in f:
            i = int(line)
            a.append(i)
    return a

def solve_homework():
    for f in (choose_pivot_first_element,
              choose_pivot_last_element,
              choose_pivot_median_of_three):
        a = read_input('QuickSort.txt')
        sorted_a = sorted(a)
        quicksort(a, f)
        assert a == sorted_a
        print f, cmp_cnt
        

if __name__ == '__main__':
    doctest.testmod()
    test_quicksort()
    test_pivot_count()

    solve_homework()
