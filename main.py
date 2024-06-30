import pygame
from damas.constants import *
from damas.tablero import Tablero
from damas.game import Game
from minimax.algoritmo import minimax
from damas.button import Button
import random
pygame.init()
# Constants
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Damas')
FPS = 60
font = pygame.font.SysFont('arialblack', 100, False, False)
font2 = pygame.font.SysFont('arialblack', 50, False, False)
# Buttons
pvp_btn = Button(WIDTH//2 - 150, 400, PVP, 1.5)
pvc_btn = Button(WIDTH//2 - 150, 600, PVC, 1.5)
restart_btn = Button(WIDTH//2 - 150, 400, RESTART, 1.5)
menu_btn = Button(WIDTH//2 - 150, 600, MENU, 1.5)
# Menu state
menu_state = "menu"
game_mode = None
# Obtiene la posición del mouse
def obtener_posicion_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
# Dibuja el texto
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    WIN.blit(img, (x, y))
# Main function
def main():
    global menu_state, game_mode
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS) # Fija el número de fotogramas por segundo
        WIN.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if menu_state == "menu":
                    if pvp_btn.draw(WIN):
                        menu_state = "game"
                        game_mode = "pvp"
                        game = Game(WIN)
                    if pvc_btn.draw(WIN):
                        menu_state = "game"
                        game_mode = "pvc"
                        game = Game(WIN)
                        game.turn = random.choice([WHITE, GRAY])
                elif menu_state == "game":
                    row, col = obtener_posicion_mouse(pos)
                    game.select(row, col)
                elif menu_state == "end":
                    if restart_btn.draw(WIN):
                        game.reset()
                        menu_state = "game"
                    if menu_btn.draw(WIN):
                        game = None
                        menu_state = "menu"

        if menu_state == "menu":
            WIN.blit(BG, (0, 0))
            WIN.blit(TITULO, (WIDTH//2 - TITULO.get_width()//2, 50))
            draw_text("Elige un modo", font2, BLACK, WIDTH//2 - 180, 300)
            pvp_btn.draw(WIN)
            pvc_btn.draw(WIN)
        elif menu_state == "game" and game is not None:
            if game_mode == "pvc" and game.turn == GRAY:
                value, new_board = minimax(game.get_board(), 4, GRAY, game)
                game.ai_move(new_board)
            if game.winner() is not None:
                winner = game.winner()
                menu_state = "end"
            game.update()
        elif menu_state == "end":
            WIN.fill(WHITE)
            draw_text(f"{winner} gana!", font, BLACK, WIDTH//2 - 300, HEIGHT//2 - 200)
            restart_btn.draw(WIN)
            menu_btn.draw(WIN)
            pygame.display.update()

        pygame.display.update()
    pygame.quit()

main()