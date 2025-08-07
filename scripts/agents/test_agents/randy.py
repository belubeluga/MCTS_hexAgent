import numpy as np


class RandomAgent:
    def __init__(self):
        self.legajo = 0
        self.reset()

    def action(self, board):
        return np.random.choice(np.flatnonzero(board == 0))

    def name(self):
        return {"nombre": "Random", "apellido": "Agent", "legajo": self.legajo}

    def __str__(self):
        return f"🎲Randall_M {self.legajo}"

    def reset(self):
        self.legajo = 42 * np.random.randint(100)
