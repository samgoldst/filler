import random
import time
from collections import OrderedDict
from typing import List, Tuple
from copy import deepcopy


class Board:
    options = []

    @staticmethod
    def set_options(num):
        Board.options = [str(n) for n in range(num)]

    def __init__(self, size: Tuple[int, int], seed=random.randint(0, 1 << 32)):
        random.seed(seed)
        if len(Board.options) == 0:
            raise Exception("Set number of options before creating Board object by doing Board.set_options(int)")
        self.size = size
        m: List[List[str]] = [["X" for j in range(size[1] + 2)] for i in range(size[0] + 2)]
        for i in range(1, len(m) - 1):
            for j in range(1, len(m[1]) - 1):
                possible = OrderedDict()
                for o in Board.options:
                    possible[o] = None
                possible.pop(m[i - 1][j], None)
                possible.pop(m[i + 1][j], None)
                possible.pop(m[i][j - 1], None)
                possible.pop(m[i][j + 1], None)
                m[i][j] = random.sample(list(possible), 1)[0]
        self.map = m
        self.map[-2][1] = " "
        self.map[1][-2] = "█"

    def __str__(self, print_outline=False) -> str:
        if print_outline:
            output: str = ""
            for row in self.map:
                for s in row:
                    output += s
                output += '\n'
            return output[:-1]

        else:
            output: str = ""
            for row in self.map[1:-1]:
                for s in row[1:-1]:
                    output += s
                output += '\n'
            return output[:-1]

    def play_move(self, player: str, new_color: str):
        if new_color in " █X":
            return
        for i in range(1, self.size[0] + 1):
            for j in range(1, self.size[1] + 1):
                if (self.map[i][j] == new_color and
                        (self.map[i - 1][j] == player or
                         self.map[i + 1][j] == player or
                         self.map[i][j - 1] == player or
                         self.map[i][j + 1] == player)):
                    self.map[i][j] = player

    def evaluate(self) -> int:
        return sum([row.count(" ") for row in self.map]) - sum([row.count("█") for row in self.map])

    def is_done(self):
        for row in self.map:
            for cell in row:
                if cell in self.options:
                    return False
        return True

    @staticmethod
    def ordermoves(board: 'Board', player):
        counts = {}
        for choice in Board.options:
            total = Board.count(board, player, choice)
            if total != 0:
                counts[choice] = total
        return sorted(counts, key=lambda x: counts[x], reverse=True)

    @staticmethod
    def minimax(board: 'Board', maxing, depth, alpha, beta) -> Tuple[int, str]:
        if depth == 0 or board.is_done():
            return board.evaluate(), "NA"
        if maxing:
            choices = Board.ordermoves(board, " ")
            maximum = float("-inf")
            best_move = "0"
            for move in choices:
                new_board = deepcopy(board)
                new_board.play_move(" ", move)
                score, _ = Board.minimax(new_board, False, depth - 1, alpha, beta)
                if score > maximum:
                    maximum = score
                    best_move = move
                if score > beta:
                    break
                alpha = max(alpha, score)
            return maximum, best_move
        else:
            choices = Board.ordermoves(board, "█")
            minimum = float("inf")
            best_move = "0"
            for move in choices:
                new_board = deepcopy(board)
                new_board.play_move("█", move)
                score, _ = Board.minimax(new_board, True, depth - 1, alpha, beta)
                if score < minimum:
                    minimum = score
                    best_move = move
                if score < alpha:
                    break
                beta = min(beta, score)
            return minimum, best_move

    @staticmethod
    def count(board, player: str, new_color: str):
        c = 0
        for i in range(1, board.size[0] + 1):
            for j in range(1, board.size[1] + 1):
                if (board.map[i][j] == new_color and
                        (board.map[i - 1][j] == player or
                         board.map[i + 1][j] == player or
                         board.map[i][j - 1] == player or
                         board.map[i][j + 1] == player)):
                    c += 1
        return c
