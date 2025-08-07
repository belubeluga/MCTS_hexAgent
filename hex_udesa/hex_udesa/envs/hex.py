import gymnasium as gym
import numpy as np
import pygame
from gymnasium import spaces

bg_color = (40, 40, 40)
red_color = (215, 90, 80)
muted_red_color = (115, 90, 80)
blue_color = (70, 90, 215)
muted_blue_color = (70, 90, 115)
empty_color = (150, 150, 150)

class IllegalMoveError(Exception):
    """Excepción lanzada cuando se intenta realizar un movimiento ilegal."""
    pass

class HexEnv(gym.Env):
    metadata = {"render_modes": ["human", "console"], "render_fps": float("inf")}
    cell_radius = 20
    margin = 50


    def __init__(self, render_mode=None, board_size=11):
        super().__init__()
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size), dtype=int)
        self.current_player = 1
        self.action_space = spaces.Discrete(board_size * board_size)
        self.observation_space = spaces.Box(
            low=-1, high=1, shape=(board_size, board_size), dtype=int
        )
        self.render_mode = render_mode
        self.names = {"agent1": "Blue", "agent2": "Red"}

        if self.render_mode == "human":
            pygame.init()
            self.cell_size = self.cell_radius * 2
            self.window_width = (
                self.cell_size * (self.board_size + 2) * (2**0.5) + self.margin * 2
            )
            self.window_height = (
                self.cell_size * (self.board_size + 2) * 0.9 + self.margin * 2
            )
            self.screen = pygame.display.set_mode((
                self.window_width,
                self.window_height,
            ))
            pygame.display.set_caption("Hex Game")
        self.last_move = None

    def reset(self, seed=None, options=None):
        self.names = options if options is not None else {"agent1": "Blue", "agent2": "Red"}
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_player = 1
        return self.board.copy(), {}

    def step(self, action):
        row, col = divmod(action, self.board_size)
        self.last_move = (row, col)
        if self.board[row][col] != 0:
            raise IllegalMoveError("Movimiento ilegal: la posición ya está ocupada.")

        self.board[row][col] = self.current_player

        if self.check_win():
            return self.board.copy(), 1, True, True, {"winner": self.current_player}

        self.current_player *= -1
        return self.board.copy(), 0, False, False, {}

    def render(self, mode=None):
        if self.render_mode == "human":
            self._render_human()
        elif self.render_mode == "console":
            self._render_console()

    def _render_human(self):
        self.screen.fill(bg_color)

        for row in range(self.board_size + 2):
            for col in range(self.board_size + 2):
                x = self.margin + col * self.cell_size * 1.05 + row * self.cell_radius
                y = self.margin * 2 + row * self.cell_size * 0.9
                color = empty_color  # Empty cell

                if col == 0 and row == 0:
                    color = bg_color
                elif col == self.board_size + 1 and row == self.board_size + 1:
                    color = bg_color
                elif col == 0 and row == self.board_size + 1:
                    color = bg_color
                elif col == self.board_size + 1 and row == 0:
                    color = bg_color

                elif row == 0 or row == self.board_size + 1 :
                    color = muted_red_color
                elif col == 0 or col == self.board_size + 1:
                    color = muted_blue_color

                elif self.board[row - 1][col - 1] == 1:
                    color = blue_color  # Player 1
                elif self.board[row - 1][col - 1] == -1:
                    color = red_color  # Player -1

                if 0 < row < self.board_size + 1 and 0 < col < self.board_size + 1:
                    # Draw outline
                    hexagon = [
                        (
                            x + self.cell_radius * (2**0.28) * np.sin(np.pi * i / 3),
                            y + self.cell_radius * (2**0.28) * np.cos(np.pi * i / 3),
                        )
                        for i in range(6)
                    ]
                    pygame.draw.polygon(self.screen, bg_color, hexagon)

                # Draw nice hexagons of radius self.cell_radius
                hexagon = [
                    (
                        x + self.cell_radius * (2**0.14) * np.sin(np.pi * i / 3),
                        y + self.cell_radius * (2**0.14) * np.cos(np.pi * i / 3),
                    )
                    for i in range(6)
                ]
                pygame.draw.polygon(self.screen, color, hexagon)

                # dot on last move
                if (row - 1, col - 1) == self.last_move:
                    pygame.draw.circle(
                        self.screen, bg_color, (int(x), int(y)), self.cell_radius // 3
                    )

        # Draw agent names
        font = pygame.font.Font(None, self.cell_size)
        name1 = font.render(self.names["agent1"], True, blue_color)
        name2 = font.render(self.names["agent2"], True, red_color)
        name1_pos = (
            self.margin,
            self.margin - self.cell_size * .5
        )
        name2_pos = (
            self.window_width - self.margin - name2.get_width(),
            self.margin - self.cell_size * .5
        )
        if self.current_player == 1:
            rect = name1.get_rect(topleft=name1_pos)
            pygame.draw.rect(self.screen, muted_blue_color, rect.inflate(10, 5), border_radius=10)
        else:
            rect = name2.get_rect(topleft=name2_pos)
            pygame.draw.rect(self.screen, muted_red_color, rect.inflate(10, 5), border_radius=10)
        self.screen.blit(name1, name1_pos)
        self.screen.blit(name2, name2_pos)
            
        pygame.display.flip()

    def _render_console(self):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[: self.board_size]

        print("  " + "  ".join(letters))  # Column headers
        for i, row in enumerate(self.board):
            for _ in range(i):
                print(" ", end="")

            row_str = " ".join(
                "🔵" if cell == 1 else "🔴" if cell == -1 else "⚬ " for cell in row
            )
            print(f"{i + 1:<2}{row_str}", end="")

            print()

        # Print agent names
        if self.current_player == 1:
            name1, name2 = f"[{self.names['agent1']}]", self.names["agent2"]
        else:
            name1, name2 = self.names["agent1"], f"[{self.names['agent2']}]"
        print(f"{name1} (🔵): Connect left to right")
        print(f"{name2} (🔴): Connect top to bottom")

    def check_win(self):
        visited = set()

        def dfs(row, col, target):
            if not (0 <= row < self.board_size and 0 <= col < self.board_size):
                return False
            if (row, col) in visited or self.board[row][col] != target:
                return False
            if (target == 1 and col == self.board_size - 1) or (
                target == -1 and row == self.board_size - 1
            ):
                return True

            visited.add((row, col))
            neighbors = [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
                (row - 1, col + 1),
                (row + 1, col - 1),
            ]
            return any(dfs(nr, nc, target) for nr, nc in neighbors)

        if self.current_player == 1:
            return any(dfs(row, 0, 1) for row in range(self.board_size))
        else:
            return any(dfs(0, col, -1) for col in range(self.board_size))

    def close(self):
        if self.render_mode == "human":
            pygame.quit()
