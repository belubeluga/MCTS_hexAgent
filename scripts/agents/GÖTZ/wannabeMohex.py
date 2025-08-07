import random
import time
import numpy as np

""" Gotz Agent : wannabeMohex """

# ════════════════════════════════════════════════════════════════════════
# MCTS con:
#   - UnionFind
#   - Amaf
#   - Virtual bridges en union find
#  ════════════════════════════════════════════════════════════════════════


# ════════════════════════════════════════════════════════════════════════
#✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　
#︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹
#
#                             WANNABE MOHEX
#                            
#︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹
#✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　
# ════════════════════════════════════════════════════════════════════════

class wannabeMohex:

    def __init__(self, size = 13, time_limit = 30.0 - 0.02):
        self.first_move = True
        self.size = size
        self.time_limit = time_limit

    def name(self):
        return {"nombre": "wannabeMohex", "apellido": "Gotz", "legajo": 35725}
    
    def __str__(self):
        return "wannabeMohex"
    
    def reset(self):
        pass

    def action(self, board):
        #primero turno == elijo random (legal)
        if self.first_move:
            self.first_move = False
            return np.random.choice(np.flatnonzero(board == 0))

        return self.mcts(board)
    
    #  ════════════════════════════════════════════════════════════════════════
    #   FUNCIONES PROPIAS DE MCTS
    #  ════════════════════════════════════════════════════════════════════════

    def mcts(self, board):
        start_time = time.time()
        legal_moves = np.flatnonzero(board == 0)

        wins = {move: 0 for move in legal_moves}
        plays = {move: 0 for move in legal_moves}

        amaf_wins = {move: 0 for move in legal_moves}
        amaf_plays = {move: 0 for move in legal_moves}

        k = 10000 #parámetro arbitrario

        while time.time() - start_time < self.time_limit:

            # SELECCIÓN (random)
            initial_move = self.explore(legal_moves)

            # Rollout
            board_copy = board.copy()
            simulation_result, played_moves = self.simulate(board_copy, initial_move)
            
            # Premiación 
            plays[initial_move] += 1
            if simulation_result == 1:
                wins[initial_move] += 1

            for move in played_moves:
                if move in amaf_plays:
                    amaf_plays[move] += 1
                    if simulation_result == 1:
                        amaf_wins[move] += 1    

        #ELECCIÓN DEL BEST MOVE (best child)
        best_score = -1
        best_move = None
        for move in legal_moves:
            if plays[move] > 0:
                # si hay estadísticas AMAF para el movimiento, se combinan ambas
                if amaf_plays[move] > 0:
                    beta = np.sqrt(k / (3 * plays[move] + k))
                    classic_winrate = wins[move] / plays[move]
                    amaf_winrate = amaf_wins[move] / amaf_plays[move]
                    combined_winrate = (1 - beta) * classic_winrate + beta * amaf_winrate
                else:
                    combined_winrate = wins[move] / plays[move]
                if combined_winrate > best_score:
                    best_score = combined_winrate
                    best_move = move
        
        return best_move if best_move is not None else random.choice(legal_moves)
           
    def explore(self, legal_moves):
        #exploro de forma random (evito sesgos)
        return random.choice(legal_moves)

    def simulate(self, board, move):
        played_moves = [move]
        board[np.unravel_index(move, (self.size, self.size))] = 1
        next_turn = -1

        while True: #simulo hasta no poder más
            new_legal_moves = np.flatnonzero(board == 0)
            if len(new_legal_moves) == 0: #si no se puede jugar
                break

            move = self.explore(new_legal_moves)
            board[np.unravel_index(move, (self.size, self.size))] = next_turn
            
            if next_turn == 1:
                played_moves.append(move) #me guardo las jugadas propias
            next_turn = -next_turn 
        
        winner = self.get_winner(board, self.size)
        return winner, played_moves
    
    #  ════════════════════════════════════════════════════════════════════════
    #   FUNCIONES PARA EVALUACIÓN
    #  ════════════════════════════════════════════════════════════════════════

    def get_connections(self, i, j):
        neighbors = []
        valid_connections = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]

        for valid_i, valid_j in valid_connections:
            new_i, new_j = i + valid_i, j + valid_j
            if 0 <= new_i < self.size and 0 <= new_j < self.size:
                neighbors.append((new_i, new_j))
        return neighbors

    def get_winner(self, board, size):
        def is_valid(i, j):
            return 0 <= i < size and 0 <= j < size

        # JUGADOR 1 (izq - derecha)
        uf1 = UnionFind(size * size + 2)
        left_virtual = size * size
        right_virtual = size * size + 1

        for i in range(size):
            for j in range(size):
                if board[i][j] == 1:
                    index = i * size + j
                    if j == 0:
                        uf1.union(index, left_virtual)
                    if j == size - 1:
                        uf1.union(index, right_virtual)
                    for di, dj in [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]:
                        ni, nj = i + di, j + dj
                        if is_valid(ni, nj) and board[ni][nj] == 1:
                            uf1.union(index, ni * size + nj)

                    # VIRTUAL BRIDGES (conexiones aseguradas) --> ya las uno
                    bridge_dirs = [
                        ((0, 2), [(0, 1), (1, 1)]),
                        ((-1, 2), [(-1, 1), (0, 1)]),
                        ((1, 0), [(0, 0), (1, -1)]),
                    ]
                    for (ddi, ddj), intermediates in bridge_dirs:
                        ni, nj = i + ddi, j + ddj
                        if is_valid(ni, nj) and board[ni][nj] == 1:
                            valid_bridge = True 
                            for (idi, idj) in intermediates:
                                ci, cj = i + idi, j + idj
                                if not is_valid(ci, cj) or board[ci][cj] != 0:
                                    valid_bridge = False
                                    break
                            if valid_bridge: #si el puente vacío lo uno
                                uf1.union(index, ni * size + nj)

        if uf1.connected(left_virtual, right_virtual):
            return 1

        # JUGADOR -1 (arriba - abajo) --> misma lógica q arriba
        uf2 = UnionFind(size * size + 2)
        top_virtual = size * size
        bottom_virtual = size * size + 1

        for i in range(size):
            for j in range(size):
                if board[i][j] == -1:
                    index = i * size + j
                    if i == 0:
                        uf2.union(index, top_virtual)
                    if i == size - 1:
                        uf2.union(index, bottom_virtual)
                    for di, dj in [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]:
                        ni, nj = i + di, j + dj
                        if is_valid(ni, nj) and board[ni][nj] == -1:
                            uf2.union(index, ni * size + nj)
                    bridge_dirs = [
                        ((2, 0), [(1, 0), (1, -1)]),
                        ((1, -2), [(0, -1), (1, -1)]),
                    ]
                    for (ddi, ddj), intermediates in bridge_dirs:
                        ni, nj = i + ddi, j + ddj
                        if is_valid(ni, nj) and board[ni][nj] == -1:
                            valid_bridge = True
                            for (idi, idj) in intermediates:
                                ci, cj = i + idi, j + idj
                                if not is_valid(ci, cj) or board[ci][cj] != 0:
                                    valid_bridge = False
                                    break
                            if valid_bridge:
                                uf2.union(index, ni * size + nj)

        if uf2.connected(top_virtual, bottom_virtual):
            return -1

        return 0



# ════════════════════════════════════════════════════════════════════════
#✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　
#︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹
#                             UNION FIND
#︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹︶︶୨୧︶︶⊹︶︶⊹
#✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　 . ✦ . 　⁺ 　
# ════════════════════════════════════════════════════════════════════════

class UnionFind:
    # optimizada con path halving y union by rank

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)    
    
