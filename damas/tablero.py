import pygame
from .piece import Piece
from .constants import *
# Clase Tablero
class Tablero:
    def __init__(self):
        self.tablero = []
        self.white_pieces = self.gray_pieces = 12
        self.white_kings = self.gray_kings = 0
        self.crear_tablero()
# Dibujar el tablero
    def dibujar_tablero(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, WOOD, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
# Crear el tablero con las piezas iniciales en forma de matriz
    def crear_tablero(self):
        for row in range(ROWS):
            self.tablero.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.tablero[row].append(Piece(row, col, GRAY))
                    elif row > 4:
                        self.tablero[row].append(Piece(row, col, WHITE))
                    else:
                        self.tablero[row].append(0)
                else:
                    self.tablero[row].append(0)
# Dibujar el tablero y las piezas
    def dibujar(self, win):
        self.dibujar_tablero(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.tablero[row][col]
                if piece != 0:
                    piece.draw(win)
# Mover una pieza a una fila y columna
    def mover(self, piece, row, col):
        # Intercambiar la posición de la pieza
        self.tablero[piece.row][piece.col], self.tablero[row][col] = self.tablero[row][col], self.tablero[piece.row][piece.col]
        piece.move(row, col)
        # Si la pieza llega al final del tablero, hacerla rey
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE and not piece.king: # Si la pieza es blanca y no es rey, aumentar el contador de reyes blancos
                self.white_kings += 1
            elif piece.color == GRAY and not piece.king:
                self.gray_kings += 1
    # Obtener una pieza en una fila y columna
    def get_piece(self, row, col):
        return self.tablero[row][col]
    # Remover una pieza
    def remover(self, pieces):
        for piece in pieces:
            self.tablero[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.white_pieces -= 1 # Si la pieza es blanca, disminuir el contador de piezas blancas
                else:
                    self.gray_pieces -= 1
    # Verificar si hay un ganador
    def gana(self):
        # Si no hay piezas blancas o grises, retornar el color del ganador
        if self.white_pieces <= 0:
            return "GRAY"
        elif self.gray_pieces <= 0:
            return "WHITE"

        return None
    # Obtener los movimientos válidos de una pieza
    def get_valid_moves(self, piece):
        moves = {} # Diccionario de movimientos
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        # Si la pieza es blanca o rey, obtener los movimientos hacia arriba
        if piece.color == WHITE or piece.king:
            moves.update(self._saltar_izquierda(row - 1, max(row-3, -1), -1, left, piece.color, []))
            moves.update(self._saltar_derecha(row - 1, max(row-3, -1), -1, right, piece.color, []))
        # Si la pieza es gris o rey, obtener los movimientos hacia abajo
        if piece.color == GRAY or piece.king:
            moves.update(self._saltar_izquierda(row + 1, min(row+3, ROWS), 1, left, piece.color, []))
            moves.update(self._saltar_derecha(row + 1, min(row+3, ROWS), 1, right, piece.color, []))
        
        return moves
    # Obtener los movimientos de salto hacia la izquierda
    def _saltar_izquierda(self, start, stop, step, left, color, skipped):
        moves = {} # Diccionario de movimientos
        last = [] # Lista de piezas saltadas
        for r in range(start, stop, step):
            if left < 0: # Si la posición a la izquierda es menor a 0, salir del ciclo
                break
            current = self.tablero[r][left] # Obtener la pieza actual
            if current == 0: # Si la posición actual está vacía
                if skipped and not last: # Si se saltó una pieza y no hay piezas saltadas, salir del ciclo
                    break
                elif skipped: # Si se saltó una pieza, agregar las piezas saltadas al diccionario de movimientos
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last # Si no se saltó ninguna pieza, agregar las piezas saltadas al diccionario de movimientos
                if last:
                    if step == -1: # Si el paso es hacia arriba, obtener los movimientos hacia la izquierda
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS) # Si el paso es hacia abajo, obtener los movimientos hacia la izquierda
                    # Obtener los movimientos hacia la izquierda y derecha
                    moves.update(self._saltar_izquierda(r + step, row, step, left - 1, color, skipped=last))
                    moves.update(self._saltar_derecha(r + step, row, step, left + 1, color, skipped=last))
                break
            elif current.color == color: # Si la pieza actual es del mismo color, salir del ciclo
                break
            else:
                last = [current] # Si no, agregar la pieza actual a la lista de piezas saltadas
            left -= 1
        return moves
    # Obtener los movimientos de salto hacia la derecha
    def _saltar_derecha(self, start, stop, step, right, color, skipped):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS: # Si la posición a la derecha es mayor o igual a la cantidad de columnas, salir del ciclo
                break
            current = self.tablero[r][right] # Obtener la pieza actual
            if current == 0:
                if skipped and not last: # Si se saltó una pieza y no hay piezas saltadas, salir del ciclo
                    break
                elif skipped: # Si se saltó una pieza, agregar las piezas saltadas al diccionario de movimientos
                    moves[(r, right)] = last + skipped
                else: # Si no se saltó ninguna pieza, agregar las piezas saltadas al diccionario de movimientos
                    moves[(r, right)] = last
                if last: # Si hay piezas saltadas
                    if step == -1: # Si el paso es hacia arriba, obtener los movimientos hacia la derecha
                        row = max(r-3, 0) 
                    else: # Si el paso es hacia abajo, obtener los movimientos hacia la derecha
                        row = min(r+3, ROWS)
                    # Obtener los movimientos hacia la izquierda y derecha
                    moves.update(self._saltar_izquierda(r + step, row, step, right - 1, color, skipped=last))
                    moves.update(self._saltar_derecha(r + step, row, step, right + 1, color, skipped=last))
                break
            elif current.color == color: # Si la pieza actual es del mismo color, salir del ciclo
                break
            else:
                last = [current] # Si no, agregar la pieza actual a la lista de piezas saltadas
            right += 1
        return moves
# Funcion de evaluacion para el algoritmo minimax
    def evaluate(self):
        # Calcular la diferencia de piezas y reyes entre las piezas blancas y grises
        return self.gray_pieces - self.white_pieces + (self.gray_kings - self.white_kings) * 0.5
    # Obtener todas las piezas de un color
    def get_all_pieces(self, color):
        pieces = []
        for row in self.tablero:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
