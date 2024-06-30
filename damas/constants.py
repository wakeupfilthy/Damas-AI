import pygame
# Constantes del juego
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
## RGB colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WOOD = (248, 196, 113)
GRAY = (164, 164, 164)
GREEN = (130, 224, 170)
# Imagen de la corona
CORONA=pygame.transform.scale(pygame.image.load('assets/corona.png'), (80, 60))
# Imagenes de botones
PVP = pygame.image.load('assets/1.png')
PVC = pygame.image.load('assets/2.png')
BG = pygame.image.load('assets/checkers.jpg')
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
TITULO = pygame.image.load('assets/DAMAS.png')
RESTART = pygame.image.load('assets/restart.png')
MENU = pygame.image.load('assets/menu.png')
