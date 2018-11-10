'''
Created on Nov 7, 2018

@author: mark
'''
import heapq
import math
import random

def solve(start, finish, heuristic):
    
    """Find the shortest path from START to FINISH."""
    heap = []

    link = {} # parent node link
    h = {} # heuristic function cache
    g = {} # shortest path to a node

    g[start] = 0
    h[start] = 0
    link[start] = None


    heapq.heappush(heap, (0, 0, start))
    
    # keep a count of the  number of steps, and avoid an infinite loop.
    for kk in xrange(1000000):
        f, junk, current = heapq.heappop(heap)
        if current == finish:
            print "distance:", g[current], "steps:", kk
            return g[current], kk, build_path(start, finish, link)

        moves = current.get_moves()
        distance = g[current]
        for mv in moves:
            if mv not in g or g[mv] > distance + 1:
                g[mv] = distance + 1
                if mv not in h:
                    h[mv] = heuristic(mv)
                link[mv] = current
                heapq.heappush(heap, (g[mv] + h[mv], -kk, mv))
    else:
        raise Exception("did not find a solution")
    
def build_path(start, finish, parent):
    """
    Reconstruct the path from start to finish given
    a dict of parent links.

    """
    x = finish
    xs = [x]
    while x != start:
        x = parent[x]
        xs.append(x)
    xs.reverse()
    return xs

def no_heuristic(*args):
    """Dummy heuristic that doesn't do anything"""
    return 0

def manhattan_h(goal):
    def f(pos):
        dx, dy = pos.x - goal.x, pos.y - goal.y
        return abs(dx) + abs(dy)
    return f

class GridPosition(object):
    """Represent a position on a grid."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return "GridPosition(%d,%d)" % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_moves(self):
        # There are times when returning this in a shuffled order
        # would help avoid degenerate cases.  For learning, though,
        # life is easier if the algorithm behaves predictably.
        yield GridPosition(self.x + 1, self.y)
        yield GridPosition(self.x, self.y + 1)
        yield GridPosition(self.x - 1, self.y)
        yield GridPosition(self.x, self.y - 1)



grid_start = GridPosition(0,0)
grid_end = GridPosition(10,10)


solve(grid_start, grid_end, manhattan_h(grid_end))

