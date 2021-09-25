import random


class Board:

    def __init__(self, rows, cols, rule):
        self.rows = rows
        self.cols = cols
        self.mapping = self.create_rule_key(rule)
        self.board = self.apply_rule()

    @staticmethod
    def create_rule_key(rule):
        assert 0 <= rule < 256, "Rule number must be between 0 and 255 inclusive"
        rule_in_binary = format(rule, "b")
        while len(rule_in_binary) < 8:
            rule_in_binary = "0" + rule_in_binary
        keys = ["111", "110", "101", "100", "011", "010", "001", "000"]
        return {key: value for key, value in list(zip(keys, rule_in_binary))}

    def apply_rule(self):
        # Create array of size state with one initial index randomly set to 1
        new_state = [0.0] * self.cols
        new_state[self.cols // 2] = 1.0

        # set result to initial
        result = [[float(item) for item in new_state]]
        for _ in range(self.rows-1):
            new_state = []
            for i in range(self.cols):
                if i == 0:
                    l, m, r = result[-1][-1], result[-1][0], result[-1][1]
                elif i == self.cols - 1:
                    l, m, r = result[-1][-2], result[-1][-1], result[-1][0]
                else:
                    l, m, r = result[-1][i - 1], result[-1][i], result[-1][i + 1]
                key = str(int(l)) + str(int(m)) + str(int(r))
                new_state.extend(self.mapping[key])
            result.append([float(item) for item in new_state])

        return result

    def transform_to_rgb(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 1.0:
                    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                    self.board[row][col] = (r, g, b)
                else:
                    self.board[row][col] = (255, 255, 255)

    def mark_visited(self, visited):
        for pair in visited:
            self.board[pair[0]][pair[1]] = (0, 0, 0)

