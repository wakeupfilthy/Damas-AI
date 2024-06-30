from copy import deepcopy
import pygame
from damas.constants import WHITE, GRAY

# Algoritmo Minimax
def minimax(position, depth, max_player, game):
    # Caso base
    if depth == 0 or position.gana() != None:
        return position.evaluate(), position # Evaluar la posición
    # Si se esta maximizando
    if max_player:
        maxEval = float('-inf') # Inicializar el valor máximo
        best_move = None # Mejor movimiento
        for move in get_all_moves(position, GRAY, game): # Obtener todos los movimientos
            evaluation = minimax(move, depth-1, False, game)[0] # Evaluar el movimiento
            maxEval = max(maxEval, evaluation) # Obtener el máximo
            if maxEval == evaluation: # Si el máximo es igual a la evaluación, obtener el mejor movimiento
                best_move = move 
        return maxEval, best_move # Retornar el máximo y el mejor movimiento
    else: # Si se esta minimizando
        minEval = float('inf')
        best_move = None # Mejor movimiento
        for move in get_all_moves(position, WHITE, game): # Obtener todos los movimientos
            evaluation = minimax(move, depth-1, True, game)[0] # Evaluar el movimiento
            minEval = min(minEval, evaluation)
            if minEval == evaluation: # Si el mínimo es igual a la evaluación, obtener el mejor movimiento
                best_move = move
        return minEval, best_move
# Simular un movimiento
def simulate_move(piece, move, board, skip):
    board.mover(piece, move[0], move[1])
    if skip:
        board.remover(skip)
    return board
# Obtener todos los movimientos
def get_all_moves(board, color, game):
    moves = [] # Lista de movimientos
    for piece in board.get_all_pieces(color): # Obtener todas las piezas
        valid_moves = board.get_valid_moves(piece) # Obtener los movimientos válidos de cada pieza
        for move, skip in valid_moves.items(): # Obtener los movimientos y las piezas saltadas
            draw_board = deepcopy(board) # Copiar el tablero
            temp_piece = draw_board.get_piece(piece.row, piece.col) # Obtener la pieza
            new_board = simulate_move(temp_piece, move, draw_board, skip) # Simular el movimiento
            moves.append(new_board) # Agregar el tablero a la lista de movimientos
    return moves
