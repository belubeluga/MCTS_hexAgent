import pygame


class ClickAgent:
    def action(self, board, env):
        """
        Toma la acción basada en la posición del clic del ratón.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos

                        col = (
                            x - env.unwrapped.margin + (env.unwrapped.cell_size // 2)
                        ) // env.unwrapped.cell_size
                        row = (
                            y - env.unwrapped.margin + (env.unwrapped.cell_size // 2)
                        ) // env.unwrapped.cell_size
                        if (
                            0 <= col < env.unwrapped.num_cols
                            and 0 <= row < env.unwrapped.num_rows
                        ):
                            action = row * env.unwrapped.num_cols + col
                            if board[row][col] == 0:
                                return action

    def name(self):
        return {"nombre": "Click", "apellido": "Agent", "legajo": 10}

    def __str__(self):
        return "🖱️ClickAgent"

    def reset(self):
        pass
