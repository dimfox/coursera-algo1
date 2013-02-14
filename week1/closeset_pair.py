"""
Closest pair

For a set of points P = {p1, p2, ....pn} on a 2D plane, d(pi, pj) is
the Eulidean distance between pi and pi. 
  d(pi, pj) = sqrt[(pi_x - pj_x)**2 + (pi_y - pj_y)**2]
Find a pair of p*, q* so that d(p*, q*) is the smallest among all pairs
in P.

Algorithm:
Px = sort P by x cord
Py = sort P by y cord
def closest_pair(Px, Py):
  Lx, Ly = left half of P by x cord
  Rx, Ry = right half of P by x cord
  (p1, q1, d1) = closest_pair(Lx, Ly)
  (p2, q2, d2) = closest_pair(Rx, Ry)
  (p3, q3, d3) = closest_split_pair(Px, Py, min(d1, d2))
  return min(d1, d2, d3) and the coresponding pair

def closest_split_pair(Px, Py, delta):
  Sy = middle of P by x cord that at most delta away from the
      middle point, sorted by y cord.
  for p in Sy:
    for q in Sy that is at most 7 places away from p:
      if d(p, q) < best:
        update best
"""

import collections
import itertools
import math
import random

Inf = 10000000

Point = collections.namedtuple('Point', 'x, y')


def closest_pair(P):
    """Return a pair of points in P with least Eulidean distance.

    >>> closest_pair([(0, 0), (0, 3), (0, 4), (0, 6)])
    (1, (0, 3), (0, 4))
    """
    sort_by_x = sorted(P, key=lambda p: p.x)
    d, pair =  _closest_pair(sort_by_x)
    return (d, pair)


def _dist(p, q):
    """Return Eulidean distance between p and q."""
    return math.sqrt((p.x - q.x)**2 + (p.y - q.y)**2)

def _closest_pair(Px):
    """Return the closest pair for given points.

    Px is sorted by their x cord
    """
    if len(Px) <= 1:
        return (Inf, None)
    if len(Px) == 2:
        p = Px[0]
        q = Px[1]
        return (_dist(p, q), (p, q))

    half = len(Px) / 2
    left_Px = Px[:half]
    right_Px = Px[half:]

    d1, pair1 = _closest_pair(left_Px)
    d2, pair2 = _closest_pair(right_Px)
    d3, pair3 = _closest_split_pair(Px, half, min(d1, d2))

    if d1 <= d2 and d1 <= d3:
        return (d1, pair1)
    elif d2 <= d1 and d2 <= d3:
        return (d2, pair2)
    else:
        return (d3, pair3)

def _closest_split_pair(Px, half, delta):
    """Find the closest pair in Px that is at most delta away from the
    half point on x coord."""
    
    # find out points that are at most delta away from half point
    Sy = [Px[half]]
    i = 1
    while (half + i) < len(Px) and abs(Px[half].x - Px[half + i].x) <= delta:
        Sy.append(Px[half + i])
        i += 1
    i = 1
    while (half - i) >= 0 and abs(Px[half].x - Px[half - i].x) <= delta:
        Sy.append(Px[half - i])
        i += 1
    # sort by y coord
    Sy.sort(key=lambda p: p.y)

    best_dist = delta
    best_pair = None
    for i, p in enumerate(Sy):
        for j in range(1, 8):
            if i + j >= len(Sy): break
            d = _dist(p, Sy[i+j])
            if d < best_dist:
                best_dist = d
                best_pair = (p, Sy[i+j])
    if best_pair is None:
        best_dist = Inf
    return (best_dist, best_pair)


def _brute_force(P):
    """Solve closest pair by brute force."""
    best_dist = Inf
    best_pair = None
    for p, q in itertools.combinations(P, 2):
        dist = _dist(p, q)
        if dist < best_dist:
            best_dist = dist
            best_pair = (p, q)

    return (best_dist, best_pair)


def _gen_problem(size):
    """randomly generate a problem with input size (number of points)."""
    P = []
    for _ in xrange(size):
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        P.append(Point(x, y))

    return P

def main():
    # test
    for _ in xrange(200):
        problem_size = random.randint(2, 250)
        problem = _gen_problem(problem_size)
        dist1, pair1 = closest_pair(problem)
        dist2, pair2 = _brute_force(problem)
        print dist1, pair1
        print dist2, pair2
        assert dist1 == dist2


if __name__ == '__main__':
    main()
