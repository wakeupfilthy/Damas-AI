import pygame
from damas.constants import *
from damas.tablero import Tablero
from damas.piece import Piece
# Clase Juego
class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    # Inicializar el juego
    def _init(self):
        self.selected = None
        self.board = Tablero()
        self.turn = WHITE
        self.valid_moves = {}
    # Actualizar el juego
    def update(self):
        self.board.dibujar(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
# Reiniciar el juego
    def reset(self):
        self._init()
# Obtener el ganador
    def winner(self):
        return self.board.gana()
# Seleccionar una pieza
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False
    # Mover una pieza
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.mover(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remover(skipped)
            self.change_turn()
        else:
            return False
        return True
    # Cambiar de turno
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = GRAY
        else:
            self.turn = WHITE
# Dibujar los movimientos válidos
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)
# Obtener el tablero
    def get_board(self):
        return self.board
# Realizar un movimiento de la IA
    def ai_move(self, board):
        self.board = board
        self.change_turn()