from __future__ import print_function
from __future__ import generators
from utils import PriorityQueue, infinity, memoize, name, print_table, update
import sys
import time
import os
import psutil


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.  Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, i, j, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.i = i
        self.j = j
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        """display depth, f, action and state"""
        if hasattr(self, 'f'):
            return "<Node: f=%d, depth=%d, action=%s\n%s>" % (self.f,
                                                              self.depth,
                                                              self.action,
                                                              self.state)
        else:
            return "<Node: depth=%d\n%s>" % (self.depth, self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """Return a list of nodes reachable from this node."""
        return [Node(next_state, i, j, self, action,
                     problem.path_cost(self.path_cost, self.state, action, next_state))
                for (action, next_state, i, j) in problem.successor(self.state)]

    def path(self):
        """ Create a list of nodes from the root to this node."""
        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
        return result

    # We want for a queue of nodes in breadth_first_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)


def graph_search(problem, fringe):
    """Search through the successors of a problem to find a goal.
    The argument fringe should be an empty queue.
    If two paths reach a state, only use the best one."""
    closed = {}
    fringe.append(Node(problem.initial, problem.i, problem.j))
    max_depth = 0
    while fringe:
        node = fringe.pop()
        # Print some information about search progress
        if node.depth > max_depth:
            max_depth = node.depth
            if max_depth < 50 or max_depth % 1000 == 0:
                pid = os.getpid()
                py = psutil.Process(pid)
                memory_use = py.memory_info()[0] / 1024 / 1024
                print('Reached depth', max_depth,
                      'Open len', len(fringe),
                      'Memory used (MBytes)', memory_use)

        if problem.goal_test(node.state):
            return node
        serial = node.state.__str__()
        if serial not in closed:
            closed[serial] = True
            fringe.extend(node.expand(problem))
    return None

# ______________________________________________________________________________
# Informed (Heuristic) Search


def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have depth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    return graph_search(problem, PriorityQueue(min, f))


def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search.
    Uses the pathmax trick: f(n) = max(f(n), g(n)+h(n))."""
    h = h or problem.h
    h = memoize(h, 'h')

    def f(n):
        return max(getattr(n, 'f', -infinity), n.path_cost + h(n))

    return best_first_graph_search(problem, f)
