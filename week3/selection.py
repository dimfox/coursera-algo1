"""Return kth order statistics.

Given an unordered array, return kth smallest item.

Algorithm:
def selection(a, k, start_ind, end_ind):
   pivot = randomly choose a pivot point between [start_ind, end_ind)
   partition a[start_ind:end_ind) to move items <= pivot to left of the pivot
       and move items >= pivot to right of the pivot
   After partiton
   p_ind_aft = index of pivot after the partition
   if p_ind_aft == k:
     return a[p_ind_aft]
   elif p_ind_aft > k:
     return selection(a, k, start_ind, p_ind_aft)
   else
     return selection(a, k, p_ind_aft, end_ind)
"""

import doctest
import random

def selection(a, k):
    """Return kth order statisitics (zero based).

    >>> selection([1, 2, 0, 3, 4], 1)
    1
    >>> selection([1, 2, 3, 0, 4], 2)
    2
    >>> selection([1, 2, 3, 4, 0], 3)
    3
    >>> selection([1, 4, 3, 0, 2], 1)
    1
    >>> selection([1, 4, 6, 2, 0], 4)
    6
    """

    return _selection(a, k, 0, len(a), _choose_pivot_first_element)

def _choose_pivot_first_element(a, start_ind, end_ind):
    return a[start_ind], start_ind

def _selection(a, k, start_ind, end_ind, choose_pivot_func):
    """Return kth order statistic for a between start_ind and end_ind."""
    # choose a pivot
    pivot, pivot_ind = choose_pivot_func(a, start_ind, end_ind)

    # move pivot to begining of the section
    a[start_ind], a[pivot_ind] = pivot, a[start_ind]

    # move items <= pivot to left of the pivot, >= pivot to right of the pivot
    right_to_pivot_pos = start_ind + 1
    for i in range(start_ind + 1, end_ind):
	if a[i] < pivot:
	    a[i], a[right_to_pivot_pos] = a[right_to_pivot_pos], a[i]
	    right_to_pivot_pos += 1
    # swap pivot item to its location
    pivot_pos = right_to_pivot_pos - 1
    a[pivot_pos], a[start_ind] = a[start_ind], a[pivot_pos]

    if pivot_pos == k:
	return a[k]
    elif pivot_pos > k:
	return _selection(a, k, start_ind, pivot_pos, choose_pivot_func)
    else:
	return _selection(a, k, pivot_pos + 1, end_ind, choose_pivot_func)

def test_selection(test_cnt=3000):
    for _ in xrange(test_cnt):
	problem_size = random.randint(1, 2000)
	problem = range(problem_size)
	random.shuffle(problem)
	k = random.randint(0, problem_size)
	if k >= problem_size: continue
	assert selection(problem, k) == k

if __name__ == '__main__':
    doctest.testmod()
    test_selection()
