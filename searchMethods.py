from __future__ import print_function
from __future__ import generators
from utils import PriorityQueue, infinity, memoize
from waterPump import *
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
        """display depth, f, action, path_cost and state"""
        if hasattr(self, 'f'):
            return "\n<Node: depth=%d, action=%s, path_cost=%d, h=%d\n\n%s\n>" % (
                                                              self.depth,
                                                              self.action,
                                                              self.path_cost,
                                                              self.h,
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


def graph_search(problem, frontier):
    """Search through the successors of a problem to find a goal.
    The argument fringe should be an empty queue.
    If two paths reach a state, only use the best one."""
    closed = {}
    frontier.append(Node(problem.initial, problem.i, problem.j))
    max_depth = 0
    counter = 0
    while frontier:
        node = frontier.pop()
        # Print some information about search progress
        if node.depth > max_depth:
            max_depth = node.depth
            if max_depth < 50 or max_depth % 1000 == 0:
                pid = os.getpid()
                py = psutil.Process(pid)
                memory_use = py.memory_info()[0] / 1024 / 1024
                print('Reached depth', max_depth,
                      'Open len', len(frontier),
                      'Memory used (MBytes)', memory_use)

        if problem.goal_test(node.state):
            print('\n**************** Stats:\nTotal nodes expanded :', counter)
            print('Solution depth :', node.depth)
            print('Penetrance :', float(node.depth)/counter)
            print('Effective branching factor ~ ', effective_branchingf(counter, node.depth))
            print('Path cost :', node.path_cost, '\n\n**************** Solution:\n')
            return node
        serial = node.state.__str__()
        if serial not in closed:
            closed[serial] = True
            counter += 1
            frontier.extend(node.expand(problem))
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

# ______________________________________________________________________________
# Peter Norvig - With small changes/additions


def effective_branchingf(exp, depth):
    """Function to calculate effective branching factor b*."""
    return bisect(exp, depth)


def truncate(f, n):
    """Truncates/pads a float f to n decimal places without rounding;
    added because float overflow."""
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


def exp(value, e):
    """exponential reformulation that uses truncate function."""
    i = 0
    val = 1

    while i < e:
        val *= value
        val = float(truncate(val, 2))
        i += 1
    return val


def bisect(nodes, depth, lo=0, hi=3):
    """Bisect method to find a reasonable approximation."""
    error = float(nodes)/100
    while lo < hi:
        mid = (float(lo+hi)/2)
        i = 0
        x = mid
        counter = 0
        while i <= depth:
            e = exp(x, i)
            counter += e
            i += 1
        if abs(counter - (nodes + 1)) < error:
            return mid
        elif counter > nodes + 1:
            hi = mid
        else:
            lo = mid

    return -1


def trace():
    """User-friendly function to analyze search methods and problem instances."""
    input = raw_input("Type the number corresponding to the type of problem you want to analize:\n"
                       "1) basicProblem\n"
                       "2) standardProblem\n"
                       "3) standardProblem2\n"
                       "4) standardProblem3\n")
    input2 = raw_input("Type the number corresponding to the searching method:\n"
                       "1) UniformCostSearch\n"
                       "2) A* with distance inadmissible heuristic\n"
                       "3) A* with widely inadmissible heuristic\n"
                       "4) A* with admissible heuristic\n"
                       "5) A* with improved admissible heuristic\n")

    if input == "1" :
        problem = basicProblem()
    elif input == "2":
        problem = standardProblem()
    elif input == "3":
        problem = standardProblem2()
    elif input == "4":
        problem = standardProblem3()

    else:
        return print ("Error: invalid number")

    if input2 == "1":
        type = WaterPump(8, 8, 0, 7, problem)
    elif input2 == "2":
        type = WaterPumpDistance(8, 8, 0, 7, problem)
    elif input2 == "3":
        type = WaterPumpInadmissible(8, 8, 0, 7, problem)
    elif input2 == "4":
        type = WaterPumpAdmissible(8, 8, 0, 7, problem)
    elif input2 == "5":
        type = WaterPumpAdmissible2(8, 8, 0, 7, problem)

    else:
        return print("Error: invalid number")
    searcher = astar_search
    solution = searcher(type)
    path = solution.path()
    path.reverse()
    print(path)
