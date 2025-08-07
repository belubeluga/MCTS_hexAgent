class HumanAgent:
    def action(self, board):
        max_index = len(board)
        valid_inputs = [str(i) for i in range(1, max_index + 1)]

        col = input(f"Ingrese la columna (1-{max_index}):")
        while col not in valid_inputs:
            col = input(f"Ingrese la columna bien!! (1-{max_index}): ")

        row = input(f"Ingrese la fila (1-{max_index}): ")
        while row not in valid_inputs:
            row = input(f"Ingrese la fila bien!! (1-{max_index}): ")

        num_pieces = sum(sum(1 for cell in row if cell != 0) for row in board)
        if num_pieces % 2 != 0:
            extra = row
            row = col
            col = extra
        return ((int(row) - 1) * board.shape[1]) + int(col) - 1

    def name(self):
        return {"nombre": "Human", "apellido": "Player", "legajo": 2}

    def __str__(self):
        return "👤HumanAgent"

    def reset(self):
        pass
