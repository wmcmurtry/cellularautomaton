import random
from typing import List


class Automaton:

    def __init__(self, rows, cols, rule):
        """
        :param rows:
            size of automaton
        :param cols:
            number of iterations to run automaton
        :param rule:
            what rule to determine next cell
        """
        self.rows = rows
        self.cols = cols
        self.mapping = self.create_rule_key(rule)
        self.board = self.apply_rule()

    @staticmethod
    def create_rule_key(rule : str) -> dict[str, str]:
        """
        :param rule:
            if rule = 30 (b00011110):
                if neighbor cells are 111 --> 0
                if neighbor cells are 110 --> 0
                if neighbor cells are 101 --> 0
                if neighbor cells are 100 --> 1
                if neighbor cells are 011 --> 1
                ....
                etc
        :return:
            a dictionary mapping neighbor cells to next iteration depending on rule
        """
        assert 0 <= rule < 256, "Rule number must be between 0 and 255 inclusive"
        rule_in_binary = format(rule, "b")

        # rules must have length 8
        while len(rule_in_binary) < 8:
            rule_in_binary = "0" + rule_in_binary

        # each key (representing neighbors) gets mapped to a digit in rule
        keys = ["111", "110", "101", "100", "011", "010", "001", "000"]
        return {key: value for key, value in list(zip(keys, rule_in_binary))}

    def apply_rule(self) -> List[List[float]]:
        # Create array of size state with one initial index randomly set to 1
        new_state = [0.0] * self.cols
        new_state[self.cols // 2] = 1.0

        # set result to initial
        result = [[float(item) for item in new_state]]
        for _ in range(self.rows-1):
            # new row for each  iteration
            new_state = []
            for i in range(self.cols):

                # if i ==0, use rightmost cell as neighbor
                if i == 0:
                    l, m, r = result[-1][-1], result[-1][0], result[-1][1]

                # if i == rightmost column, use leftmost cell as neighbor
                elif i == self.cols - 1:
                    l, m, r = result[-1][-2], result[-1][-1], result[-1][0]

                # normal case: cells neighbors are it's left and right
                else:
                    l, m, r = result[-1][i - 1], result[-1][i], result[-1][i + 1]

                # represent cell and neighbors as string, eg "101"
                key = str(int(l)) + str(int(m)) + str(int(r))

                # use mapping to determine cell's value on next iteration
                new_state.extend(self.mapping[key])
            result.append([float(item) for item in new_state])

        return result

    def transform_to_rgb(self) -> None:

        # iterate through each cell in board
        for row in range(self.rows):
            for col in range(self.cols):

                # if cell is 1, assign a random rgb value, otherwise use white
                if self.board[row][col] == 1.0:
                    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                    self.board[row][col] = (r, g, b)
                else:
                    # (255, 255, 255) is white
                    self.board[row][col] = (255, 255, 255)

    def mark_visited(self, visited : set) -> None:
        # if there is a path, mark all cells on path as black
        # if there is no path, mark all cells reached by search algorithm as black
        for pair in visited:
            self.board[pair[0]][pair[1]] = (0, 0, 0)

