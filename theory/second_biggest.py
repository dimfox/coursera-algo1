"""You are given as input an unsorted array of n distinct numbers, where
n is a power of 2. Give an algorithm that identifies the second-largest
number in the array, and that uses at most n+log2n-2 comparisons.
"""

import doctest
import random
import math


def _get_swaped_indices(S):
    """Swap the array so that S[2**k] is the largest between S[2**(k)]
    and S[2**(k+1)-1] (inclusive). We will swap indices instead of array itself.

    >>> _get_swaped_indices(['a', 'c', 'd', 'b'])  # Should swap to ['d', 'a', 'c', 'b']
    [2, 0, 1, 3]
    >>> _get_swaped_indices(['c', 'd', 'a', 'b'])  # Should swap to ['d', 'c', 'b', 'a']
    [1, 0, 3, 2]
    >>> _get_swaped_indices(['f', 'c', 'e', 'd', 'a', 'g', 'h', 'b'])
    [6, 1, 2, 3, 0, 4, 5, 7]
    """
    inds = range(len(S))
    step = 2
    while step <= len(S):
	for i in range(0, len(S), step):
	    j = i + step/2
	    if S[inds[j]] > S[inds[i]]:
		inds[i], inds[j] = inds[j], inds[i]
	step *= 2
    return inds


def _get_second_largest(S, inds):
    """For array S, its indices 'inds' has S's elements' indices arranged in such way
    that inds[2**k] contains the index for largest elements between inds[2**k] and
    inds[2**(k+1) - 1]. Which means that inds[0] is the index for the largest element
    Find the index for second largest.

    The second largest can only be one of the elements that were compared against the
    biggest element and lost during the swapping round.

    The swapping round moves winners to begining of the section, 0, 2, 4, ... for
    first round, 0, 4, 8, ... for second round, etc. Since we know the original index
    of the largest element, we can deduce the path it was promoted. And therefore find out
    all the elements it has been compared against.

    For example, for first round we compared S[0] with S[1], S[2] with S[3] etc. For second
    round we compared S[0] with S[2], S[4] with S[6] etc. Say the biggest element was on
    position 5, then it was compared with S[4] and promoted to S[4], on second round, it was
    compared with S[6] and stayed at S[4]. 


    >>> _get_second_largest(['a', 'c', 'd', 'b'], [2, 0, 1, 3])
    'c'
    >>> _get_second_largest(['c', 'd', 'a', 'b'], [1, 0, 3, 2])
    'c'
    >>> _get_second_largest(['f', 'c', 'e', 'd', 'a', 'g', 'h', 'b'], [6, 1, 2, 3, 0, 4, 5, 7])
    'g'
    """
    # Element in middle of the array is the one that was compared against largest
    # element in last round
    largest2 = S[inds[len(S)/2]]

    tree_height = int(math.log(len(S), 2))
    for k in range(1, tree_height):
        # length of current range to search for
	cur_range = len(S) >> k
        group = int(inds[0]/cur_range)
        compared_ind = inds[group * cur_range + cur_range/2]

	if S[compared_ind] > largest2:
	    largest2 = S[compared_ind]
    return largest2

def second_biggest(S):
    """find the second largest element of S

    >>> second_biggest([0, 2, 3, 1])
    2
    >>> second_biggest([0, 2, 5, 4])
    4
    >>> second_biggest([0, 6, 5, 4])
    5
    """
    inds = _get_swaped_indices(S)
    return _get_second_largest(S, inds)


def test(test_cnt=2000):
    for _ in xrange(test_cnt):
	problem_size = random.randint(1, 10)
	problem = range(2**problem_size)
	random.shuffle(problem)
	s = second_biggest(problem)
	assert s == 2**problem_size - 2, '%s, %s' % (s, problem)

if __name__ == '__main__':
    doctest.testmod()
    test()
