import random
from collections import deque
import heapq


class grid_point():
    def __init__(self,x,y,f=0,g=0,h=0):
        self.x =x
        self.y = y
        self.f =f
        self.g = 0
        self.h = 0

    def __lt__(self, other):
        return self.f<other.f


def can_pass(board, i, j):
    return all([75 < x <= 255 for x in board.board[i][j]])


def dfs(board):
    start = (random.randint(0, board.rows), random.randint(0, board.cols))
    finish = (random.randint(0, board.rows), random.randint(0, board.cols))
    stack = []
    visited = set()
    stack.append(start)
    parent_map = dict()
    has_path = False
    path = []
    if start == finish:
        return stack
    while stack:
        parent = stack.pop()
        if parent in visited:
            continue
        if parent == finish:
            has_path = True
            break
        visited.add(parent)
        if not can_pass(board, parent[0], parent[1]):
            continue
        children = (parent[0] + 1, parent[1]), (parent[0] - 1, parent[1]), (parent[0], parent[1] + 1), (
            parent[0], parent[1] - 1)
        for c in children:
            if 0 <= c[0] < board.rows and 0 <= c[1] < board.cols:
                stack.append(c)
                if c not in parent_map:
                    parent_map[c] = parent
    if has_path:
        curr = finish
        while curr != start:
            path.append(curr)
            curr = parent_map[curr]
        return has_path, path
    else:
        return has_path, list(visited)


def bfs(board):
    start = (random.randint(0, board.rows), random.randint(0, board.cols))
    finish = (random.randint(0, board.rows), random.randint(0, board.cols))
    q = deque()
    visited = set()
    q.append(start)
    parent_map = dict()
    has_path = False
    path = []
    if start == finish:
        return True, []
    while q:
        parent = q.popleft()
        if parent in visited or not (0<=parent[0]<board.rows) or not (0<=parent[1]<board.cols):
            continue
        if parent == finish:
            has_path = True
            break
        visited.add(parent)
        if not can_pass(board, parent[0], parent[1]):
            continue
        children = (parent[0] + 1, parent[1]), (parent[0] - 1, parent[1]), (parent[0], parent[1] + 1), (
            parent[0], parent[1] - 1)
        for c in children:
            if 0 <= c[0] < board.rows and 0 <= c[1] < board.cols:
                q.append(c)
                if c not in parent_map:
                    parent_map[c] = parent
    if has_path:
        curr = finish
        while curr != start:
            path.append(curr)
            curr = parent_map[curr]
        return has_path, path
    else:
        return has_path, list(visited)


def manhattan_distance(a,b):
    return abs(a.x - b.x) + abs(a.y-b.y)


def getchildren(point,board):
    result = []
    for p in (point.x + 1, point.y), (point.x - 1, point.y), (point.x, point.y + 1), (
            point.x, point.y - 1):
        if (0<=p[0]<board.rows) and (0<=p[1]<board.cols) and can_pass(board,p[0],p[1]):
            result.append(grid_point(p[0],p[1],0,0,0))
    return result


def astar(board):
    open_list = []
    closed_list = set()
    path = []
    start = grid_point(0, 0,0,0,0)
    finish = grid_point(15,15,0,0,0)
    parent_map = dict()
    open_list.append(start)
    heapq.heapify(open_list)
    outer_iterations = 0
    cnt = 0
    while len(open_list) > 0:
        cnt +=1
        if cnt %100 ==0:
            print(len(closed_list),len(open_list))
        curr = heapq.heappop(open_list)
        children = getchildren(curr, board)
        for child in children:
            if (child.x, child.y) not in parent_map:
                parent_map[(child.x, child.y)] = (curr.x, curr.y)
            if child.x == finish.x and child.y == finish.y:
                curr = finish
                x = 1
                while curr != (start.x, start.y):
                    if x == 1:
                        path.append((curr.x, curr.y))
                        x += 1
                        curr = parent_map[(curr.x, curr.y)]
                    else:
                        path.append((curr[0], curr[1]))
                        curr = parent_map[(curr[0], curr[1])]
                return path + [(start.x, start.y)]
            if child in open_list or (child.x,child.y) in closed_list:
                continue
            child.g = curr.g +1
            child.h = manhattan_distance(child,finish)
            child.f = child.g+child.h
            if child not in open_list:
                heapq.heappush(open_list, child)
        closed_list.add((curr.x,curr.y))
    return []


'''            if curr.x == finish.x and curr.y == finish.y:
                curr = finish
                x = 1
                while curr != (start.x,start.y):
                    print(path)
                    if x == 1:
                        path.append((curr.x,curr.y))
                        x+=1
                        curr = parent_map[(curr.x,curr.y)]
                    else:
                        path.append((curr[0], curr[1]))
                        curr = parent_map[(curr[0],curr[1])]
                return path + [(start.x,start.y)]
            children = getchildren(curr,board)
    
            for child in children:
                if (child.x,child.y) not in parent_map:
                    parent_map[(child.x,child.y)] = (curr.x,curr.y)
                if len([item for item in visited if item.x == child.x and item.y == child.y])>0:
                    continue
                child.g = curr.g
                child.h = manhattan_distance(child,finish)
                child.f = child.g + child.h
    
                if len([item for item in not_visited if item.x == child.x and item.y == child.y and item.g < child.g])>0:
                    continue
                not_visited.append(child)
        return False
'''