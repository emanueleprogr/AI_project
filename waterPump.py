from __future__ import print_function
from __future__ import generators

from copy import deepcopy
import math


# ______________________________________________________________________________


class Problem:
    """The abstract class for a formal problem.  You should subclass this and
    implement the method successor, and possibly __init__, goal_test, and
    path_cost. Then you will create instances of your subclass and solve them
    with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def successor(self, state):
        """Given a state, return a sequence of (action, state) pairs reachable
        from this state. If there are many successors, consider an iterator
        that yields the successors one at a time, rather than building them
        all at once. Iterators will work fine within the framework."""
        pass  # abstract

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Implement this
        method if checking against a single self.goal is not enough."""
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1


# ______________________________________________________________________________

class Vase:
    def __init__(self, posX, posY, goal=0, cap=0, value=0):
        self.posX = posX
        self.posY = posY
        self.value = value
        self.cap = cap
        self.goal = goal


class WaterDistributionState:

    def __init__(self, vases, n, r, c, cost=0):
        self.n = n
        self.vases = vases
        self.r = r
        self.c = c
        self.cost = cost

    def __getitem__(self, i):
        return self.vases[i]

    def __setitem__(self, i, val, cap, posX, posY):
        self.vases[i].value = val
        self.vases[i].cap = cap
        self.vases[i].posX = posX
        self.vases[i].posY = posY

    def act(self, action, i, y=0):
        ch = deepcopy(self)

        if action == 'empty' and self.vases[i].value != 0:
            ch.vases[i].value = 0

        elif action == 'pump':

            dist = math.hypot(self.r - self.vases[i].posX, self.c - self.vases[i].posY)
            ch.cost = 1 * dist * self.vases[i].value
            ch.vases[i].value = self.vases[i].cap
            ch.cost = ch.cost + (1 * dist * ch.vases[i].value)

        elif action == 'takeFromI' and self.vases[y].value >= self.vases[i].cap - self.vases[i].value and self.vases[i].value != self.vases[i].cap and self.vases[y].value != 0:

            dist = math.hypot(self.vases[y].posX - self.vases[i].posX, self.vases[y].posY - self.vases[i].posY)
            ch.cost = 1 * dist * self.vases[i].value
            ch.vases[y].value = self.vases[y].value - (self.vases[i].cap - self.vases[i].value)
            ch.vases[i].value = self.vases[i].cap
            ch.cost = ch.cost + (1 * dist * ch.vases[i].value)

        elif action == 'transferFromI' and self.vases[i].value <= self.vases[y].cap - self.vases[y].value and self.vases[y].value != self.vases[y].cap and self.vases[i].value != 0:

            dist = math.hypot(self.vases[y].posX - self.vases[i].posX, self.vases[y].posY - self.vases[i].posY)
            ch.cost = 1 * dist * self.vases[i].value

            ch.vases[y].value = self.vases[y].value + self.vases[i].value
            ch.vases[i].value = 0
        else:
            return None

        return ch

    def heuristic(self):
        i = 0
        goal_difference = 0
        while i < len(self.vases):
            goal_difference = goal_difference + abs(self.vases[i].goal - self.vases[i]. value)
            i = i + 1
        return goal_difference

    def __str__(self):
        """Serialize the state in a human-readable form"""
        s = ''
        empty = True
        for r in xrange(self.n):
            for c in xrange(self.n):
                if r == self.r and c == self.c:
                    s += '(P,P)'
                    empty = False
                for i in xrange(len(self.vases)):
                    if r == self.vases[i].posX and c == self.vases[i].posY:
                        s += '(%d' % self.vases[i].value
                        s += ',%d)' % self.vases[i].goal
                        empty = False

                if empty is True:
                    s += '(- -)'
                empty = True
            s += '\n'
        return s
    def __repr__(self):
        return self.__str__()


class WaterPump(Problem):
    def __init__(self, n, i, j, r, c):
        self.actions = ['empty', 'pump', 'takeFromI', 'transferFromI']
        self.n = n
        self.i = i
        self.j = j
        self.make_initial_state(i, r, c)

    def make_initial_state(self, n, r, c):
        vases = []
        vases.append(Vase(1, 3, 2, 4))
        vases.append(Vase(n-1, n-1, 1, 1))
        vases.append(Vase(1, 1, 3, 4))

        self.initial = WaterDistributionState(vases, self.i, r, c)

        print('Problem:', self.__doc__, 'Initial state:')
        print(self.initial)
        print('==============')

    def goal_test(self, state):
        for i in range(self.n):
            if state.vases[i].value != state.vases[i].goal:
                return False

        return True

    def path_cost(self, c, state1, action, state2):
        if action == 'empty':
            return c

        elif action == 'pump' or action == 'takeFromI' or action == 'transferFromI':
            return c + state2.cost

    def h(self, node):
        """No heuristic. A* becomes uniform cost in this case"""
        return 0

    def successor(self, state):
        """Legal moves (empty, pump, takeFromI, transferFromI). Implemented as a generator"""
        list = range(self.n)
        for action in self.actions:
            if action == 'empty' or action == 'pump':
                y = 0
                for i in list:
                    nexts = state.act(action, i)
                    if nexts is not None:
                        yield (action, nexts, i, y)
            else:
                for x in list:
                    for y in list:
                        if x != y:
                            nexts = state.act(action, x, y)
                            if nexts is not None:
                                yield (action, nexts, x, y)


class WaterPumpRelaxed(WaterPump):
    """Admissible heuristic"""
    def h(self, node):
        return node.state.heuristic()
