"""Binary Search Tree."""

class _Node(object):
    """A node in binary search tree."""
    def __init__(self, key, element):
        self.key = key
        self.element = element
        
        self.left = None
        self.right = None


class BST(object):
    """A binary search tree."""
    def __init__(self):
        self.root = None

    def find(self, key):
        """Find the element in tree for the given key."""

    def select(self, i):
        """Find the ith smallest element in tree."""

    def min(self):
        """Find the smallest element in tree."""

    def max(self):
        """Find the largest element in tree."""

    def predecessor(self, key):
        """Find previous element. """

    def successor(self, key):
        """Find next element."""

    def rank(self, key):
        """Return the index in tree of element of the given key."""

    def insert(self, key, element):
        """Insert an element into tree."""
        def _inner(cur_node):
            if cur_node.key == key:
                return cur_node
            elif cur_node.key > key:
                pass
        if self.root is None:
            self.root = _Node(roo

    def delete(self, key):
        """Delete an element from tree."""
