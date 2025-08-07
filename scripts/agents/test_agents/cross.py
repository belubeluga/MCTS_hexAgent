import numpy as np


class CrossAgent:
    def __init__(self):
        self.legajo = 1337
        self.reset()

    def action(self, board):
        # make a cross on the center of the board
        # only use unused cells
        board_size = board.shape[0]
        center = board_size // 2

        # check if the center is empty
        if board[center, center] == 0:
            return center * board_size + center
        # go in the four directions radially
        for i in range(1, center + 1):
            if center + i < board_size and board[center + i, center] == 0:
                return (center + i) * board_size + center
            if center - i >= 0 and board[center - i, center] == 0:
                return (center - i) * board_size + center
            if center + i < board_size and board[center, center + i] == 0:
                return center * board_size + center + i
            if center - i >= 0 and board[center, center - i] == 0:
                return center * board_size + center - i
        # if all else fails, return a random action
        return np.random.choice(
            np.where(board == 0)[0]
        ) * board_size + np.random.choice(np.where(board == 0)[1])

    def name(self):
        return {"nombre": "Cross", "apellido": "Agent", "legajo": self.legajo}

    def __str__(self):
        return f"❌"

    def reset(self):
        pass
