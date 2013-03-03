"""Provided with a stream of numbers, at any point, return the meadian of the
numbers seen so far with in O(log(i)) time. Where i is the number have seen
so far.
"""

import doctest
import heapq
import random


class Heap:
    def __init__(self):
        self.queue = []

    def push(self, i):
        raise NotImplementedError("Must be implemented by sub class of Heap")

    def pop(self):
        raise NotImplementedError("Must be implemented by sub class of Heap")

    def len(self):
        return len(self.queue)


class MinHeap(Heap):

    def push(self, i):
        heapq.heappush(self.queue, i)

    def pop(self):
        return heapq.heappop(self.queue)

    def top(self):
        return self.queue[0]


class MaxHeap(Heap):

    def push(self, i):
        heapq.heappush(self.queue, -i)

    def pop(self):
        return -heapq.heappop(self.queue)

    def top(self):
        return -self.queue[0]


def meadian(stream):
    """Return meadian of the stream up to k elements.

    >>> meadian([1, 2, 3, 4])
    [1, 1.5, 2, 2.5]
    """
    lower_half = MaxHeap()
    upper_half = MinHeap()

    result = []
    for i in stream:
        if lower_half.len() == 0:
            lower_half.push(i)
        elif i < lower_half.top():
            lower_half.push(i)
        else:
            upper_half.push(i)

        if lower_half.len() > upper_half.len() + 1:
            k = lower_half.pop()
            upper_half.push(k)
        elif upper_half.len() > lower_half.len() + 1:
            k = upper_half.pop()
            lower_half.push(k)

        if lower_half.len() > upper_half.len():
            result.append(lower_half.top())
        elif upper_half.len() > lower_half.len():
            result.append(upper_half.top())
        else:
            result.append(float(lower_half.top() + upper_half.top())/2)
    return result

def _brute_force(stream):
    """Brute force solver for the meadian problem.

    >>> _brute_force([1, 2, 3, 4])
    [1, 1.5, 2, 2.5]
    """
    result = []
    cur_nums = []
    for i in stream:
        cur_nums.append(i)
        sorted_nums = sorted(cur_nums)
        half = len(cur_nums)/2
        if len(cur_nums) % 2 != 0:
            m = sorted_nums[half]
        else:
            m = float(sorted_nums[half - 1] + sorted_nums[half])/2
        result.append(m)
    return result

def random_tests(test_cnt=3000):
    """Test the solver with random inputs."""
    for _ in xrange(test_cnt):
        problem_size = random.randint(1, 3000)
        problem = []
        for _ in xrange(problem_size):
            problem.append(random.randint(-300, 300))
        sol1 = meadian(problem)
        sol2 = _brute_force(problem)
        assert sol1 == sol2, '%s\n%s\n%s\n' % (problem, sol1, sol2)


if __name__ == '__main__':
    doctest.testmod()
    random_tests(300)
