import matplotlib.pyplot as plt
import numpy as np
from Board import Board
from SearchAlgorithm import dfs, bfs,astar
import random


def save_image(output_name, board):
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes()
    ax.set_axis_off()
    ax.imshow(np.array(board.board), interpolation='none', cmap='RdPu')
    plt.savefig('{output_name}.png'.format(output_name=output_name), dpi=300)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    board = Board(30, 30, 30)
    board.transform_to_rgb()
    has_path = astar(board)
    has_path.reverse()
    print(has_path)
    board.mark_visited(has_path)
    save_image("test", board)