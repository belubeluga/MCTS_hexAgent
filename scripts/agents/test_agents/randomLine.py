import numpy as np


class RandomLine:

    def __init__(self):

        self.lineNumber = None

    def action(self, board):

        # Selects a random line and tries to complete it
        boardSize = len(board)

        if not self.lineNumber:
            self.lineNumber = np.random.randint(boardSize)

        freeColumns = []
        for column in range(boardSize):

            if board[self.lineNumber][column] == 0:

                freeColumns.append(column)

        if len(freeColumns) == 0:

            return np.random.choice(np.flatnonzero(board == 0))

        else: 
            
            selectedColumn = np.random.choice(freeColumns)
            return (self.lineNumber*boardSize) + selectedColumn

    def name(self):
        return {"nombre": "Random Line", "apellido": "Agent", "legajo": 123}

    def __str__(self):
        return "🃏 Random Line"

    def reset(self):
        pass