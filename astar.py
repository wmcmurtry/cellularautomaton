import heapq
import random
from typing import List, Tuple

from Automaton import Automaton
from utils import manhattan_distance, Grid_point, getchildren


def astar(board : Automaton) -> Tuple[bool, List[Tuple[int]]]:
    """
    :param board:
        Instantiation of automaton class
    :return:
        a path of nodes from start to finish if path is possible. otherwise, a list of nodes visited.
        follows pseudocode from https://www.geeksforgeeks.org/a-search-algorithm/
    """
    # Initialize variables
    open_list = []
    closed_list = set()
    start = Grid_point(random.randint(0, board.rows), random.randint(0, board.cols), 0, 0, 0)
    finish = Grid_point(random.randint(0, board.rows), random.randint(0, board.cols), 0, 0, 0)
    parent_map = dict()

    # add starting node to open heap
    open_list.append(start)
    heapq.heapify(open_list)

    while len(open_list) > 0:
        # pop item from heap with smallest f and get its children
        curr = heapq.heappop(open_list)
        children = getchildren(curr, board,finish)

        for child in children:
            # add child coordinates to parent map
            if (child.x, child.y) not in parent_map:
                parent_map[(child.x, child.y)] = (curr.x, curr.y)

            # if child is finish coordinate, get path using parent map and return
            if child.x == finish.x and child.y == finish.y:
                path = []
                curr = finish
                x = 1
                while curr != (start.x, start.y):
                    # on first iteration, curr is a grid_point, and not a pair of coordinates
                    if x == 1:
                        path.append((curr.x, curr.y))
                        x += 1
                        curr = parent_map[(curr.x, curr.y)]
                    else:
                        path.append((curr[0], curr[1]))
                        curr = parent_map[(curr[0], curr[1])]
                path = path + [(start.x, start.y)]
                path.reverse()
                return True, path

            # if child is on closed list, skip it
            if (child.x, child.y) in closed_list:
                continue

            # no path cost
            child.g = curr.g
            # heuristic
            child.h = manhattan_distance(child, finish)
            child.f = child.g+child.h

            # since no node will be on closed with a lower f, add to open list
            if child not in open_list:
                heapq.heappush(open_list, child)

        closed_list.add((curr.x, curr.y))
    return False, list(closed_list)
