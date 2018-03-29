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


    def NAheuristic2(self):
        i = 0
        goal_difference = [0] * (len(self.vases))
        while i < len(self.vases):
            goal_difference[i] = self.vases[i].goal - self.vases[i].value
            dist = math.hypot(self.r - self.vases[i].posX, self.c - self.vases[i].posY)
            goal_difference[i] = goal_difference[i] * dist
            i = i + 1
        return sum(goal_difference) * 5


    def NAheuristic(self):
        i = 0
        goal_difference = [0] * (len(self.vases))
        while i < len(self.vases):
            goal_difference[i] = self.vases[i].goal - self.vases[i].value
            dist = math.hypot(self.r - self.vases[i].posX, self.c - self.vases[i].posY)
            goal_difference[i] = goal_difference[i] * dist
            i = i + 1
        return sum(goal_difference)


    def Aheuristic(self):
        i = 0
        goal_difference = [0] * (len(self.vases))
        while i < len(self.vases):
            if (self.vases[i].goal - self.vases[i]. value) > 0:
                goal_difference[i] = self.vases[i].goal - self.vases[i].value
                min = math.hypot(self.r - self.vases[i].posX, self.c - self.vases[i].posY)
                y = 0
                while y < len(self.vases):
                    if y != i:

                        dist = math.hypot(self.vases[y].posX - self.vases[i].posX, self.vases[y].posY - self.vases[i].posY)
                        if dist < min:
                            min = dist
                    y += 1
                goal_difference[i] = goal_difference[i] * min



            i = i + 1
        return sum(goal_difference)


    def __str__(self):
        """Serialize the state in a human-readable form"""
        s = ''
        empty = True
        for r in xrange(self.n):
            for c in xrange(self.n):
                if r == self.r and c == self.c:
                    s += '[P,P]'
                    empty = False
                for i in xrange(len(self.vases)):
                    if r == self.vases[i].posX and c == self.vases[i].posY:
                        s += '[%d' % self.vases[i].value
                        s += ',%d]' % self.vases[i].goal
                        empty = False

                if empty is True:
                    s += '|- -|'
                empty = True
            s += '\n'
        return s
    def __repr__(self):
        return self.__str__()


class WaterPump(Problem):
    def __init__(self, i, j, r, c, board):
        self.actions = ['empty', 'pump', 'takeFromI', 'transferFromI']
        self.i = i
        self.j = j
        self.make_initial_state(i, r, c, board)

    def make_initial_state(self, i, r, c, board):

        self.initial = WaterDistributionState(board, self.i, r, c)

        print('Problem:', self.__doc__, 'Initial state:')
        print(self.initial)
        print('==============')

    def goal_test(self, state):
        for i in range(len(state.vases)):
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
        list = range(len(state.vases))
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


class WaterPumpDistance(WaterPump):
    """In-admissible heuristic"""
    def h(self, node):
        return node.state.NAheuristic()


class WaterPumpAdmissible(WaterPump):
    """Admissible heuristic"""
    def h(self, node):
        return node.state.Aheuristic()


class WaterPumpInadmissible(WaterPump):
    """In-admissible heuristic that find a suboptimal path"""
    def h(self, node):
        return node.state.NAheuristic2()



def basicProblem():
    """A simple board with 3 vases"""
    vases = []
    vases.append(Vase(1, 3, 2, 4))
    vases.append(Vase(5, 5, 1, 1))
    vases.append(Vase(1, 1, 3, 4))
    return vases


def standardProblem():
    """A board with 4 vases"""
    vases = []
    vases.append(Vase(1, 2, 3, 5))
    vases.append(Vase(2, 2, 2, 3))
    vases.append(Vase(4, 0, 1, 1))
    vases.append(Vase(6, 1, 5, 6))
    return vases

def standardProblem2():

    vases = []
    vases.append(Vase(0, 0, 6, 7))
    vases.append(Vase(5, 4, 2, 4))
    vases.append(Vase(3, 3, 2, 2))
    vases.append(Vase(7, 4, 1, 6))
    vases.append(Vase(5, 5, 4, 7))
    return vases



def standardProblem3():
    """A board with 6 vases"""
    vases = []
    vases.append(Vase(1, 2, 3, 5))
    vases.append(Vase(2, 2, 2, 3))
    vases.append(Vase(4, 0, 1, 1))
    vases.append(Vase(6, 1, 5, 6))
    vases.append(Vase(7, 7, 4, 4))
    vases.append(Vase(5, 6, 0, 1))
    return vases