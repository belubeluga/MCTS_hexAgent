import numpy as np

class SmartAgent1:
    def action(self, board):
        """
        Main entry point. Decide which move to make, given a board.
        'board' is from the agent's perspective: our stones = +1, opponent's = -1,
        and we are always connecting left–to–right (the new environment already orients us).
        """

        # 1) [Removed orientation detection step - we always see ourselves as +1, left->right]

        # 2) Check for a winning move for us (+1).
        for move in self.available_moves(board):
            if self.simulate_win(board, move, +1):
                return move

        # 3) Block opponent’s winning move (opponent = -1).
        for move in self.available_moves(board):
            if self.simulate_win(board, move, -1):
                return move

        # 3.5) 50-50 chance to make a random move
        if np.random.rand() < 0.5:
            return np.random.choice(self.available_moves(board))
        
        # 4) Block opponent’s chain of 3+.
        move_to_block_chain = self.continue_long_chain(board, -1)
        if move_to_block_chain is not None:
            return move_to_block_chain

        # 5) Extend our own chain of 3+.
        move_to_extend_chain = self.continue_long_chain(board, +1)
        if move_to_extend_chain is not None:
            return move_to_extend_chain

        # 6) Otherwise, play near the center.
        move_center = self.play_towards_center(board)
        return move_center

    # ------------------------------------------------------------------------
    #                 1) Helpers for moves (no orientation needed)
    # ------------------------------------------------------------------------

    def available_moves(self, board):
        """Return a list of all empty-cell indices."""
        return [i for i, cell in enumerate(board.flatten()) if cell == 0]

    def simulate_win(self, board, move, piece):
        """
        Return True if placing 'piece' (+1 or -1) at 'move' would
        give that piece a winning path left-to-right in 'board'.
        """
        n = len(board)
        temp = board.copy()
        row, col = divmod(move, n)
        temp[row][col] = piece
        return self.check_win(temp, piece)

    def check_win(self, board, piece):
        """
        If piece == +1, check for a left->right path.
        If piece == -1, check for a top->bottom path.
        """
        n = len(board)
        visited = set()

        # Decide which direction to check, based on the piece:
        if piece == +1:
            # Left -> Right
            start_positions = [(r, 0) for r in range(n) if board[r][0] == piece]
            def target_check(r, c):
                return (c == n - 1)
        else:
            # piece == -1 => Top -> Bottom
            start_positions = [(0, c) for c in range(n) if board[0][c] == piece]
            def target_check(r, c):
                return (r == n - 1)

        def dfs(r, c):
            if (r, c) in visited or not (0 <= r < n and 0 <= c < n):
                return False
            if board[r][c] != piece:
                return False
            if target_check(r, c):
                return True
            visited.add((r, c))

            neighbors = [
                (r - 1, c), (r + 1, c),
                (r, c - 1), (r, c + 1),
                (r - 1, c + 1), (r + 1, c - 1)
            ]
            return any(dfs(nr, nc) for (nr, nc) in neighbors)

        return any(dfs(sr, sc) for (sr, sc) in start_positions)


    # ------------------------------------------------------------------------
    #            2) Logic for chain of 3 or more (no orientation needed)
    # ------------------------------------------------------------------------

    def continue_long_chain(self, board, piece):
        """
        Finds possible moves that would create or extend a chain of 3+
        for 'piece'. Return the first such move, or None if none found.
        (We don't need orientation here; just adjacency.)
        """
        n = len(board)
        neighbors = [
            (-1, 0), (1, 0),
            (0, -1), (0, 1),
            (-1, 1), (1, -1)
        ]

        def dfs_chain_length(r, c, visited, temp):
            if (r, c) in visited or not (0 <= r < n and 0 <= c < n):
                return 0
            if temp[r][c] != piece:
                return 0
            visited.add((r, c))
            total = 1
            for (dr, dc) in neighbors:
                nr, nc = r + dr, c + dc
                total += dfs_chain_length(nr, nc, visited, temp)
            return total

        for move in self.available_moves(board):
            row, col = divmod(move, n)
            temp = board.copy()
            temp[row][col] = piece
            visited = set()
            length = dfs_chain_length(row, col, visited, temp)
            if length >= 3:
                return move

        return None

    # ------------------------------------------------------------------------
    #            3) Fallback: play near the center
    # ------------------------------------------------------------------------

    def play_towards_center(self, board):
        """Pick a move whose (row,col) is closest to the true center of the board."""
        n = len(board)
        center = (n // 2, n // 2)
        moves = self.available_moves(board)
        best_move = None
        best_dist = float("inf")

        for m in moves:
            r, c = divmod(m, n)
            dist = abs(r - center[0]) + abs(c - center[1])
            if dist < best_dist:
                best_dist = dist
                best_move = m
        return best_move

    # ------------------------------------------------------------------------
    #                 4) Metadata
    # ------------------------------------------------------------------------

    def name(self):
        return {"nombre": "Smart", "apellido": "Agent1", "legajo": 101}

    def __str__(self):
        return "🤖SmartAgent1"
