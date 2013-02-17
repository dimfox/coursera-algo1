
import math
import random
import datetime

class Node:
  """A node in the graph."""
  def __init__(self, label):
    if not isinstance(label, tuple):
      label = (label,)

    self.label = label
    self.dest_nodes = []

  def add_dest_node(self, node):
    self.dest_nodes.append(node)


class Graph:
  """A graph."""
  def __init__(self):
    self.nodes = {}

  def add_node(self, node):
    self.nodes[node.label] = node

  def add_edge(self, s_label, t_label, dual_dir=True):
    if not isinstance(s_label, tuple):
      s_label = (s_label,)
    if not isinstance(t_label, tuple):
      t_label = (t_label,)

    if s_label not in self.nodes:
      self.nodes[s_label] = Node(s_label)
    if t_label not in self.nodes:
      self.nodes[t_label] = Node(t_label)

    s = self.nodes[s_label]
    t = self.nodes[t_label]

    s.add_dest_node(t)
    if dual_dir:
      t.add_dest_node(s)

  def combine_nodes(self, n1, n2):
    """combine n1 and n2 to one node."""
    new_dests = [s for s in n1.dest_nodes + n2.dest_nodes
                 if s not in (n1, n2)]  # this will remove self loop
    new_label = n1.label + n2.label

    new_node = Node(new_label)
    new_node.dest_nodes = new_dests

    # Remove the old nodes from graph
    self.nodes.pop(n1.label)
    self.nodes.pop(n2.label)

    # Replace old nodes with combined nodes
    for s_label, s in self.nodes.items():
      s_dest_nodes = []
      for dest in s.dest_nodes:
        if dest not in (n1, n2):
          s_dest_nodes.append(dest)
        else:
          s_dest_nodes.append(new_node)
      s.dest_nodes = s_dest_nodes

    self.nodes[new_label] = new_node

  def pick_random_edge(self):
    u = random.choice(self.nodes.values())
    v = random.choice(list(u.dest_nodes))
    return (u, v)

  @property
  def edge_cnt(self):
    return sum(len(s.dest_nodes) for s in self.nodes.values())/2

  @property
  def node_cnt(self):
    return len(self.nodes)

  def __str__(self):
    result = ''
    for s in self.nodes.values():
      for t in s.dest_nodes:
        result += '%s --> %s\n' % (s.label, t.label)
    return result

  def deep_copy(self):
    """create a deep copy of self."""
    gc = Graph()
    # create nodes
    for s_l, s in self.nodes.items():
      for t in s.dest_nodes:
        gc.add_edge(s_l, t.label, dual_dir=False)
    return gc


def min_cut(g):

  best_cut = g.edge_cnt
  best_cut_iter = -1
  run_cnt = g.node_cnt**2*int(math.log(g.node_cnt))
  run_cnt = max(run_cnt, 1)

  for i in xrange(run_cnt):
    gc = g.deep_copy()
    while gc.node_cnt > 2:
      u, v = gc.pick_random_edge()
      gc.combine_nodes(u, v)

    cut = gc.edge_cnt
    print (datetime.datetime.now(),
           'best_cut: %s at iteration %s (last best '
           'cut %s at iteration %s)' % (cut, i, best_cut, best_cut_iter))
    if cut < best_cut:
      best_cut = cut
      best_cut_iter = i
      print 'find best cut %s at iteration %s' % (cut, i)
  return best_cut


def _brute_force(g):
  best_cut = g.edge_cnt

  node_cnt = g.node_cnt
  for pattern in xrange(1, 2**node_cnt - 1):
    pattern = bin(pattern)[2:]
    pattern = ''.join(['0'] * (node_cnt - len(pattern))) + pattern
    cross_edge_cnt = 0
    for group1, node1 in zip(pattern, g.nodes.values()):
      for group2, node2 in zip(pattern, g.nodes.values()):
        if group1 != group2 and node2 in node1.dest_nodes:
          cross_edge_cnt += 1
    if cross_edge_cnt/2 < best_cut:
      best_cut = cross_edge_cnt/2

  return best_cut

def test():
  g1 = Graph()
  g1.add_edge('a', 'b')
  g1.add_edge('b', 'c')
  g1.add_edge('c', 'a')
  cut = min_cut(g1)
  assert cut == 2, cut
  cut = _brute_force(g1)
  assert cut == 2, cut

  g2 = Graph()
  g2.add_edge('a', 'b')
  g2.add_edge('b', 'c')
  g2.add_edge('c', 'd')
  g2.add_edge('d', 'a')
  cut = min_cut(g2)
  assert cut == 2
  cut = _brute_force(g2)
  assert cut == 2, cut

  g3 = Graph()
  g3.add_edge('a', 'b')
  g3.add_edge('b', 'c')
  cut = min_cut(g3)
  assert cut == 1, cut
  cut = _brute_force(g3)
  assert cut == 1, cut

  g4 = Graph()
  g4.add_edge('a', 'b')
  g4.add_edge('a', 'c')
  g4.add_edge('a', 'd')
  g4.add_edge('b', 'c')
  g4.add_edge('b', 'd')
  g4.add_edge('c', 'd')
  cut = min_cut(g4)
  assert cut == 3, cut
  cut = _brute_force(g4)
  assert cut == 3, cut

  test_result = {1:2, 2:2, 3:1, 4:3, 5:4}
  for testcase in (1, 2, 3, 4, 5):
    test_file = 'min_cut_test%s.txt' % testcase
    g = read_input(test_file)
    cut = min_cut(g)
    assert cut == test_result[testcase], '%s: exepcted: %s, got: %s' % (
        test_file, test_result[testcase], cut)


def test_random(test_cnt=200):
  for _ in xrange(test_cnt):
    problem_size = random.randint(3, 15)
    g = Graph()
    for n1 in range(problem_size):
      for n2 in range(n1 + 1, problem_size):
        if random.choice([True, False]):
          g.add_edge(n1, n2)
    if g.node_cnt == 0: continue
    cut1 = min_cut(g)
    cut2 = _brute_force(g)
    assert cut1 == cut2, 'min_cut: %s, brute_force: %s' % (cut1, cut2)


def read_input(filename):
  g = Graph()
  with open(filename) as f:
    for line in f:
      nodes = line.strip().split()
      nodes = [int(n) for n in nodes]
      s = nodes[0]
      for t in nodes[1:]:
        g.add_edge(s, t, dual_dir=False)
  print g
  return g

if __name__ == '__main__':
  test()
  test_random()


