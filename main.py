import matplotlib.pyplot as plt
import numpy as np
import random


# This is a sample Python script.
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def create_rule_key(rule_number):
    assert 0 <= rule_number < 256, "Rule number must be between 0 and 255 inclusive"
    rule_in_binary = format(rule_number, "b")
    while len(rule_in_binary) < 8:
        rule_in_binary = "0" + rule_in_binary
    keys = ["111", "110", "101", "100", "011", "010", "001", "000"]
    return {key: value for key, value in list(zip(keys, rule_in_binary))}


def apply_rule(size, iterations, mapping):
    # Create array of size state with one initial index randomly set to 1
    new_state = [0.0] * (size)
    new_state[size // 2] = 1.0

    # set result to initial
    result = [[float(item) for item in new_state]]
    for _ in range(iterations):
        new_state = []
        for i in range(size):
            if i == 0:
                l, m, r = result[-1][-1], result[-1][0], result[-1][1]
            elif i == size - 1:
                l, m, r = result[-1][-2], result[-1][-1], result[-1][0]
            else:
                l, m, r = result[-1][i - 1], result[-1][i], result[-1][i + 1]
            key = str(int(l)) + str(int(m)) + str(int(r))
            new_state.extend(mapping[key])
        result.append([float(item) for item in new_state])

    return result


def save_image(output_name, result_array):
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes()
    ax.set_axis_off()
    ax.imshow(np.array(result_array), interpolation='none', cmap='RdPu')
    plt.savefig('{output_name}.png'.format(output_name=output_name), dpi=300)


def transform_to_rgb(result_map):
    for row in range(len(result_map)):
        for col in range(len(result_map[0])):
            if result_map[row][col] == 1.0:
                r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                result_map[row][col] = (r, g, b)
            else:
                result_map[row][col] = (255, 255, 255)
    return result_map


def dfs(board):
    start = (0,0)
    finish = (15,26)
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
        children = (parent[0]+1,parent[1]), (parent[0]-1,parent[1]),(parent[0],parent[1]+1),(parent[0],parent[1]-1)
        for c in children:
            if 0 <=c[0]<len(board) and 0<=c[1]<len(board[0]):
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


def can_pass(board, i, j):
    return all([75 < x <= 255 for x in board[i][j]])


def mark_visited(board, visited):
    for pair in visited:
        board[pair[0]][pair[1]] = (0, 0, 0)
    return board


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mapping = create_rule_key(30)
    automaton = apply_rule(size=30, iterations=30, mapping=mapping)
    automaton = transform_to_rgb(automaton)
    has_path, path = dfs(automaton)
    print(has_path)
    if has_path:
        automaton = mark_visited(automaton, path)
    else:
        automaton = mark_visited(automaton, path)
    save_image("test", automaton)
