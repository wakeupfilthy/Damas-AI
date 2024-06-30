import pygame
from .constants import WHITE, GRAY, SQUARE_SIZE, CORONA
# Clase Pieza
class Piece:
    # Constantes para dibujar la pieza
    PADDING = 15
    OUTLINE = 2
    # Constructor
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.king = False
        if self.color == WHITE:
            self.direction = -1
        else:
            self.direction = 1
        self.calc_pos()
    # Calcular la posición de la pieza
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
    # Hacer rey a la pieza
    def make_king(self):
        self.king = True
    # Dibujar la pieza
    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GRAY, (self.x, self.y), radius, self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king: # Si la pieza es rey, dibujar la corona
            win.blit(CORONA, (self.x - CORONA.get_width()//2, self.y - CORONA.get_height()//2))
    # Mover la pieza a una fila y columna
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
    # Representación de la pieza
    def __repr__(self):
        return str(self.color)
        
