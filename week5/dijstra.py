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

import doctest
import heapq
import random


_INF = float('inf')


class Node(object):
    """A vertex in graph."""
    def __init__(self, n):
        """Convert the orignal node to an instance of Node class."""
        self.n = n
        self._outedges = []
        self._inedges = []
        self.dist = float('inf')
        self.explored = False

    def out_edges(self):
        """yield outgoing edges of this node."""
        for t in self._outedges:
            yield t

    def in_edges(self):
        """yield incoming edges to this node."""
        for s in self._inedges:
            yield s

    @classmethod
    def convert_graph(cls, g):
        """Convert the input graph to use Node class."""
        graph = {}
        nodes = {}
        def _get_node(n):
            if n not in nodes:
                nodes[n] = Node(n)
            return nodes[n]

        for s in g:
            node_s = _get_node(s)
            if node_s not in graph:
                graph[node_s] = {}
            for t in g[s]:
                node_t = _get_node(t)
                node_s._outedges.append(node_t)
                node_t._inedges.append(node_s)
                graph[node_s][node_t] = g[s][t]

        return graph, nodes


def dijstra(g, s):
    """Return shortest path from s to all other nodes in g.

    >>> g = {'a': {'b': 10}, 'b': {'c': 20}}
    >>> dijstra(g, 'a')
    {'a': 0, 'c': 30, 'b': 10}
    >>> g = {'a': {'b': 10, 'c': 20}, 'b': {'c': 20}}
    >>> dijstra(g, 'a')
    {'a': 0, 'c': 20, 'b': 10}
    """
    graph, nodes = Node.convert_graph(g)
    s = nodes[s]

    # node has been explored
    s.dist = 0
    s.explored = True

    # unexplored
    unexplored = []
    for label, t in nodes.items():
        if t is s: continue
        if t in graph[s]:
            # has direct link from explored set to unexplored set
            dist = graph[s][t]
        else:
            dist = float('inf')
        heapq.heappush(unexplored, (dist, t))
        t.dist = dist

    while len(unexplored) > 0:
        dist, t = heapq.heappop(unexplored)
        if t.explored: continue
        t.dist = dist
        t.explored = True

        if t not in graph: continue

        for nt in graph[t]:
            if nt.explored: continue
            if t.dist + graph[t][nt] < nt.dist:
                nt.dist = t.dist + graph[t][nt]
                heapq.heappush(unexplored, (nt.dist, nt))

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
