import random
from collections import deque
from utils import can_pass, get_path
from Automaton import Automaton
from typing import List, Tuple


def dfs(board : Automaton) -> Tuple[bool, List[Tuple[int]]]:
    """
    :param board:
        Instantiation of board class
    :return:
        First value is True/False if maze is/is not solvable.
        Second value is parent map that maps nodes to their parents. Used to find path.
        If maze is not solvable return empty list
    Implements iterative DFS using a stack
    """

    # Random start and end points
    start = (random.randint(0, board.rows), random.randint(0, board.cols))
    finish = (random.randint(0, board.rows), random.randint(0, board.cols))

    # Declare variables
    stack = []
    visited = set()
    stack.append(start)
    parent_map = dict()
    has_path = False

    if start == finish:
        return stack

    while stack:
        parent = stack.pop()
        if parent in visited:
            continue
        if parent == finish:
            has_path = True
            break

        # Since we haven't visited this node, now add it to visited
        visited.add(parent)

        # Some nodes are not passable
        if not can_pass(board, parent[0], parent[1]):
            continue

        # right, left, up, and down
        children = (parent[0] + 1, parent[1]), (parent[0] - 1, parent[1]), (parent[0], parent[1] + 1), (
            parent[0], parent[1] - 1)

        # Add children to stack and record their parents
        for c in children:
            if 0 <= c[0] < board.rows and 0 <= c[1] < board.cols:
                stack.append(c)
                if c not in parent_map:
                    parent_map[c] = parent

    if has_path:
        path = get_path(start, finish, parent_map)
        return True, path
    return False, list(visited)


def bfs(board : Automaton) -> Tuple[bool, List[Tuple[int]]]:
    """
    :param board:
        Instantiation of board class
    :return:
        First value is True/False if maze is/is not solvable.
        Second value is parent map that maps nodes to their parents. Used to find path.
        If maze is not solvable return empty list
    Implements iterative BFS using a queue
    """
    # Random start and end points
    start = (random.randint(0, board.rows), random.randint(0, board.cols))
    finish = (random.randint(0, board.rows), random.randint(0, board.cols))

    # Declare variables
    q = deque()
    visited = set()
    q.append(start)
    parent_map = dict()
    has_path = False

    if start == finish:
        return True, []
    while q:
        parent = q.popleft()
        if parent in visited or not (0<=parent[0]<board.rows) or not (0<=parent[1]<board.cols):
            continue
        if parent == finish:
            has_path = True
            break

        # Since we haven't visited this node, now add it to visited
        visited.add(parent)
        if not can_pass(board, parent[0], parent[1]):
            continue

        # right, left, up, down
        children = (parent[0] + 1, parent[1]), (parent[0] - 1, parent[1]), (parent[0], parent[1] + 1), (
            parent[0], parent[1] - 1)

        # add children to queue and record their parents
        for c in children:
            if 0 <= c[0] < board.rows and 0 <= c[1] < board.cols:
                q.append(c)
                if c not in parent_map:
                    parent_map[c] = parent

    if has_path:
        path = get_path(start, finish, parent_map)
        return has_path, path
    else:
        return has_path, list(visited)
