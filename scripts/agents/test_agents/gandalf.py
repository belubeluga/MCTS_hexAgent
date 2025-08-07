import numpy as np


class GandalfAgent:
    def __init__(self):
        self.legajo = 9
        self.reset()

    def action(self, board):
        # this agent previously tried to see if it was first or second player by
        # counting num_pieces % 2. Now we always assume our opponent is -1,
        # so we just find the center of mass of board == -1.

        board_size = board.shape[0]
        num_pieces = np.sum(board != 0)
        target_row = np.floor(board_size * self.desired_place)

        # We no longer deduce "cardinality" from parity; we just fix the opponent as -1.
        cardinality = -1

        # If there are no opponent pieces yet, place in a random cell near target_row
        if num_pieces == 0:
            center_of_mass = np.array([np.random.randint(board_size), target_row])
        else:
            oponents_pieces = np.where(board == cardinality)
            center_of_mass = np.mean(oponents_pieces, axis=1)  # average x,y coords

        # The old code used an if/else for horizontal vs vertical. Now it always
        # takes the 'else' branch (because cardinality = -1).
        if cardinality == 1:
            target = np.array([center_of_mass[0], target_row])
        else:
            target = np.array([target_row, center_of_mass[1]])

        # Check every unoccupied cell, pick the one closest to our target
        distances = {}
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    distances[i * len(board) + j] = np.linalg.norm(
                        np.array([i, j]) - target
                    )
        return min(distances, key=distances.get)

    def name(self):
        return {"nombre": "Gandalf", "apellido": "the grey", "legajo": self.legajo}

    def __str__(self):
        return f"🧙💍🧒⛰️u shall not pass🧝🏰🌋"

    def reset(self):
        # float from 0 to 1
        self.desired_place = np.random.rand()
