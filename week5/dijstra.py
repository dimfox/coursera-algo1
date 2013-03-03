"""Dijstra's Algorithm for Shortest Path.

Given a directed graph find the shortest path from
vertex S to all other vertecies.

V is the set of all vertices in graph
Init X = {S}, A[S] = 0
while X != V:
  among all edges (u, v) where u in X and v in V
  fine the edge that minimize:
    A[u] + l(u, v)
  Add v to X, A[v] = A[u] + l(u, v)
"""

import collections
import doctest
import heapq
import random


_INF = float('inf')

class _Node(object):
    def __init__(self, label, dist, explored):
        self.dist = dist
        self.explored = explored
        self.label = label

    def __str__(self):
        return str(self.label)

    def __repr__(self):
        return str((self.label, self.dist, self.explored))


def _create_node_dict(graph):
    """Create a dictionary of nodes with vertex of graph as key and
       instance of _Node as value."""
    nodes = {}
    # Build dictionary of nodes."""
    for n1 in graph:
        if n1 not in nodes:
            nodes[n1] = _Node(n1, _INF, False)
        for n2 in graph[n1]:
            if n2 not in nodes:
                nodes[n2] = _Node(n2, _INF, False)
    return nodes

def dijstra(graph, s):
    """Return shortest path from s to all other nodes in g.

    >>> g = {'a': {'b': 10}, 'b': {'c': 20}}
    >>> dijstra(g, 'a')
    {'a': 0, 'c': 30, 'b': 10}
    >>> g = {'a': {'b': 10, 'c': 20}, 'b': {'c': 20}}
    >>> dijstra(g, 'a')
    {'a': 0, 'c': 20, 'b': 10}
    """
    nodes = _create_node_dict(graph)

    # node has been explored
    nodes[s].dist = 0
    nodes[s].explored = True

    # unexplored
    unexplored = []
    for t in nodes:
        if t is s: continue
        if t in graph[s]:
            # has direct link from explored set to unexplored set
            dist = graph[s][t]
        else:
            dist = float('inf')
        heapq.heappush(unexplored, (dist, t))
        nodes[t].dist = dist
    while len(unexplored) > 0:
        dist, t = heapq.heappop(unexplored)
        node_t = nodes[t]
        if node_t.explored: continue
        node_t.dist = dist
        node_t.explored = True

        if t not in graph: continue

        for nt in graph[t]:
            node_nt = nodes[nt]
            if node_nt.explored: continue
            if node_t.dist + graph[t][nt] < node_nt.dist:
                node_nt.dist = node_t.dist + graph[t][nt]
                heapq.heappush(unexplored, (node_nt.dist, nt))
    dist = {}
    for n in nodes:
        dist[n] = nodes[n].dist
    return dist


def read_input(file_name):
    g = {}
    with open(file_name) as f:
        for line in f:
            row = line.split()
            node = int(row[0])
            if node not in g: g[node] = {}
            for edge in row[1:]:
                t, cost = edge.split(',')
                t, cost = int(t), int(cost)
                g[node][t] = cost
    return g


if __name__ == '__main__':
    doctest.testmod()
    g = {'a': {'b': 10}, 'b': {'c': 20}}
    print dijstra(g, 'a')
