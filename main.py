import matplotlib.pyplot as plt
import numpy as np
from Automaton import Automaton
from dfs_bfs import dfs, bfs
from astar import astar


def save_image(
        output_name : str,
        board : Automaton) -> None:
    fig = plt.figure(figsize=(3, 3))
    ax = plt.axes()
    ax.set_axis_off()
    ax.imshow(np.array(board.board), interpolation='none', cmap='RdPu')
    plt.savefig('{output_name}.png'.format(output_name=output_name), dpi=300)


if __name__ == '__main__':
    board = Automaton(50, 50, 254)
    output_name = "test"
    board.transform_to_rgb()
    #save_image(output_name, board)
    has_path, path = dfs(board)
    board.mark_visited(path)
    save_image(output_name+"dfs", board)