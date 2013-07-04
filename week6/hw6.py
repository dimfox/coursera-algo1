"""The goal of this problem is to implement a variant of the 2-SUM algorithm
(covered in the Week 6 lecture on hash table applications).
The file contains 500,000 positive integers (there might be some repetitions!).
This is your array of integers, with the ith row of the file specifying the ith
entry of the array.

Your task is to compute the number of target values t in the interval
[2500,4000] (inclusive) such that there are distinct numbers x,y in the input
file that satisfy x+y=t. (NOTE: ensuring distinctness requires a one-line
addition to the algorithm from lecture.)
"""

def two_sum(int_array, lb, ub):
    """return number of pairs in int_array whose sum is between lb and ub.

    >>> two_sum([1, 2, 3, 4, 5], 3, 4)
    2
    >>> two_sum([1, 2, 3, 4, 5], 3, 3)
    1
    >>> two_sum([0, 1, 2, 3, 4], 3, 3)
    1
    >>> two_sum([-1, 1, 2, 3, 4], 2, 4)
    3
    """
    hash_int = {}
    sum_hash = {}
    for x in int_array:
        if x >= ub: continue
        hash_int[x] = True

    for x in int_array:
        if x >= ub: continue
        for sum_x_y in range(lb, ub + 1):
            y = sum_x_y - x
            if x < y and y in hash_int:
                # print '%s + %s = %s' % (x, y, sum_x_y)
                sum_hash[sum_x_y] = True
    return len(sum_hash)

def read_input(file_name):
    int_array = []
    with open(file_name) as f:
        for line in f:
            x = int(line)
            int_array.append(x)
    return int_array


def test_two_sum():
    int_array = read_input('test1.txt')
    sum_cnt = two_sum(int_array, 30, 60)
    assert sum_cnt == 9, '%s != 9' % sum_cnt

    int_array = read_input('test2.txt')
    sum_cnt = two_sum(int_array, 30, 60)
    assert sum_cnt == 20, '%s != 20' % sum_cnt


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    test_two_sum()

    int_array = read_input('/Users/weliu/Downloads/HashInt.txt')
    print two_sum(int_array, 2500, 4000)
