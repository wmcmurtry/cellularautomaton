from typing import Tuple, Dict, List
from Automaton import Automaton


class Grid_point:
    """
    Represents a point on Automaton with f, g, and h costs from A* Search.
    """
    def __init__(self,
                 x : int,
                 y : int,
                 f : int = 0,
                 g : int = 0,
                 h : int = 0):

        self.x = x
        self.y = y
        self.f = f
        self.g = g
        self.h = h

    """
    Implements a comparator. Needed to add points to a min-heap.
    """
    def __lt__(self, other):
        return self.f < other.f


def get_path(
        start : Tuple[int],
        finish : Tuple[int],
        parent_map : Dict[Tuple[int],Tuple[int]]
        ) -> List[Tuple[int]]:
    """
    :param start:
        Starting coordinates of maze search
    :param finish:
        Goal state of maze
    :param parent_map:
        Maps each node to its parent
    :return:
        The path taken by search algorithm to reach finish from start
    """
    curr = finish
    path = []
    while curr != start:
        path.append(curr)
        curr = parent_map[curr]
    path.reverse()
    return path


def can_pass(
        board : Automaton,
        i : int,
        j : int) -> bool:
    """
    :param board:
        Instantiation of Automaton class
    :param i:
        x coordinate of point on board
    :param j:
        y coordinate of point on board
    :return:
        True if point can be traversed. False otherwise.
    """
    # range 75-255 is arbitrary, but  produces good mazes
    return all([75 < x <= 255 for x in board.board[i][j]])


def manhattan_distance(
        a : Grid_point,
        b : Grid_point) -> int:
    """
    :param a:
        first point
    :param b:
        second point
    :return:
        manhattan distance that is used as heuristic in A* search
    """

    return abs(a.x - b.x) + abs(a.y - b.y)


def getchildren(
        point : Grid_point,
        board : Automaton,
        finish : Tuple[int]) -> List[Grid_point]:
    """
    :param point:
        parent node
    :param board:
        Instantiation of Automaton class
    :param finish:
        Goal state
    :return:
        eligible descendants of parent node
    """
    result = []
    # right, left, up, down
    for p in (point.x + 1, point.y), (point.x - 1, point.y), (point.x, point.y + 1), (
            point.x, point.y - 1):
        # Check  bounds. check if valid cell or if finish cell
        if (0 <= p[0] < board.rows) and (0 <= p[1] < board.cols) and\
                (can_pass(board, p[0], p[1]) or (p[0] == finish.x and p[1] == finish.y)):
            result.append(Grid_point(p[0], p[1], 0 , 0, 0))
    return result
