"""Strongly connected components.

For a directed graph, a strongly connected component is a set of
nodes in which every node is reachable from other nodes inside
the component.

Algorithm:

1. Reverse every edge's direction in the graph, call this G'
2. Do DSF on G', which give each node an order by which the nodes
   are visited.
3. Do DSF on original graph G, in the reverse order assigned in step 2.
   Nodes that can be reached by on DSF belong to the same SCC.

"""
import random


def scc(g, dsf_func_to_use='stack'):
    """Strongly connected components."""

    def _dsf_stack(g, i):
        """Do dsf for node i, using manually managed stack"""
        stack = []
        stack.append((i, True))

        while len(stack) > 0:
            cur_node, to_process = stack.pop(-1)
            if to_process:
                explored[cur_node] = True
                leader[leader_s].append(cur_node)

            next_node = None
            if cur_node in g:
                for j in g[cur_node]:
                    if j not in explored:
                        next_node = j
                        break
            if next_node is not None:
                stack.append((cur_node, False))
                stack.append((next_node, True))
            else:
                ordered_nodes.append(cur_node)

    def _dsf_rec(g, i):
        """Do dsf for node i, using simple recursion."""
        explored[i] = True
        leader[leader_s].append(i)
        if i in g:
            for j in g[i]:
                if j not in explored:
                    _dsf_rec(g, j)
        ordered_nodes.append(i)

    if dsf_func_to_use == 'stack':
        dsf_func = _dsf_stack
    else:
        dsf_func = _dsf_rec

    # santize graph, remove paralla edges
    for k in g:
        g[k] = list(set(g[k]))

    # step 1, reverse g
    gr = {}
    for i in g:
        for j in g[i]:
            if j not in gr:
                gr[j] = [i]
            else:
                if i not in gr[j]:
                    gr[j].append(i)
    # step 2, run dsf on gr
    explored = {}

    leader = {}
    ordered_nodes = []
    for i in gr:
        if i not in explored:
            leader_s = i
            leader[leader_s] = []
            dsf_func(gr, i)

    # step 3, run dsf on g in order calculated above
    explored = {}
    leader = {}
    reverse_ordered_nodes = reversed(ordered_nodes)
    for i in reverse_ordered_nodes:
        if i not in explored:
            leader_s = i
            leader[leader_s] = []
            dsf_func(g, i)

    return leader

def count_len(groups):
    grp_lens = [len(grp) for grp in groups.values()]
    grp_lens.sort(reverse=True)
    return grp_lens


def _assert_dict_equal(d1, d2):
    if sorted(d1.keys()) != sorted(d2.keys()): return False
    for k in d1:
        if sorted(d1[k]) != sorted(d2[k]):
            return False
    return True

def _assert_test(g, expected_counts, expected_groups = None):

    groups = scc(g)

    if expected_groups:
        assert _assert_dict_equal(groups, expected_groups), '%s -- %s' % (expected_groups, groups)

    assert count_len(groups) == expected_counts, '%s -- %s' % (expected_counts,
                                                               count_len(groups))
    nodes = set()
    for s in g:
        nodes.add(s)
        for t in g[s]:
            nodes.add(t)

    assert sum(count_len(groups)) == len(nodes), '%s -- %s' % (sum(count_len(groups)), len(nodes))

    def _same_group(groups, s, t):
        """Return true if s and t are in the same group."""
        for group in groups.values():
            if s in group and t in group:
                return True
        return False

    def _is_connected(g, s, t):
        explored = {}
        def _dsf(g, i):
            explored[i] = True
            if i in g:
                for j in g[i]:
                    if j not in explored:
                        _dsf(g, j)
        _dsf(g, s)
        return t in explored

    for s in nodes:
        for t in nodes:
            s_to_t = _is_connected(g, s, t)
            t_to_s = _is_connected(g, t, s)
            # print '%s -> %s: %s, %s -> %s: %s' % (s, t, s_to_t, s, t, t_to_s)
            # print 'is same group: %s' % (_same_group(groups, s, t))
            if _same_group(groups, s, t):
                assert s_to_t and t_to_s, '%s and %s should be in same group. %s' % (s, t, groups)
            else:
                assert not s_to_t or not t_to_s, '%s and %s should not be in the same group. %s' % (s, t, groups)


def test1():
    g ={1: [7],
        7: [4, 9],
        4: [1],
        9: [6],
        6: [3, 8],
        3: [9],
        8: [2],
        2: [5],
        5: [8],
        }
    _assert_test(g,
                 [3, 3, 3],
                 {1: [1, 4, 7],
                  2: [2, 5, 8],
                  6: [6, 3, 9]})

    g = {1: [2],
         2: [3],
         3: [1, 4]}
    _assert_test(g,
                 [3, 1],
                 {1: [3, 2, 1], 4: [4]})

    g = {1: [2, 2],
         2: [3, 1],
         3: [4, 2, 2]}
    _assert_test(g,
                 [3, 1],
                 {1: [1, 2, 3], 4: [4]})

    g = {2: [46, 15],
         46: [15, 9],
         15: [9],
         }
    _assert_test(g,
                 [1, 1, 1, 1])


def tests():
    g = read_input('test1.txt')
    expected = {1: [6, 3, 5, 1],
                2: [10, 4, 2],
                11: [11],
                9: [8, 7, 9]}
    _assert_test(g,
                 [4, 3, 3, 1],
                 expected)

    g = read_input('test2.txt')
    expected = {1: [5, 2, 1],
                3: [8, 4, 3],
                6: [7, 6]}
    _assert_test(g,
                 [3, 3, 2],
                 expected)

    g = read_input('test3.txt')
    _assert_test(g,
                 [6, 3, 2, 1])

    g = read_input('test4.txt')
    _assert_test(g,
                 [35, 7, 1, 1, 1, 1, 1, 1, 1, 1])

    g = read_input('test5.txt')
    _assert_test(g,[36, 7, 1, 1, 1, 1, 1, 1, 1])

    g = read_input('test6.txt')
    _assert_test(g, [8, 5, 2, 1])

    g = read_input('test7.txt')
    _assert_test(g, [3, 3, 3, 1])

    g = read_input('test8.txt')
    _assert_test(g, [3, 3, 3, 1])

def random_tests(test_cnt=300):
    for _ in xrange(test_cnt):
        problem_size = random.randint(2, 500)
        g = {}
        for s in range(1, problem_size+1):
            g[s] = []
            for t in range(1, problem_size + 1):
                if s == t: continue
                if random.randint(1, 300) < 100:
                    g[s].append(t)
        groups1 = scc(g, 'stack')
        groups2 = scc(g, 'rec')
        assert _assert_dict_equal(groups1, groups2), '%s \n%s\n%s' % (g, groups1, groups2)


def read_input(filename):
    g = {}
    with open(filename) as f:
        for line in f:
            n1, n2 = line.split()
            n1 = int(n1)
            n2 = int(n2)
            if n1 not in g:
                g[n1] = []
            g[n1].append(n2)
    return g


if __name__ == '__main__':
    print "Running small manual tests."
    test1()

    print "Running small text based tests."
    tests()

    print "Running random tests."
    random_tests(400)
