from scc import scc
from scc import read_input
from scc import count_len
import datetime

def main():
    print '%s: reading input' % (datetime.datetime.now())
    g = read_input('SCC.txt')
    nodes = set()
    for s in sorted(g.keys()):
        nodes.add(s)
        for t in g[s]:
            nodes.add(t)
    print '%s: Sloving' % (datetime.datetime.now())
    groups = scc(g)
    print '%s: Done Sloving' % (datetime.datetime.now())
    print 'total_nodes in groups: %s' % sum(count_len(groups))
    print 'total_nodes in graph: %s' % len(list(nodes))
    print '%s: sorting to get output' % (datetime.datetime.now())
    print count_len(groups)[:20]

import sys
import threading

if __name__ == '__main__':
    #threading.stack_size(128*1024*1024)
    #sys.setrecursionlimit(2 ** 15)
    #thread = threading.Thread(target=main)
    #thread.start()

    main()
