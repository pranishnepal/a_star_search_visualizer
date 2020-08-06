import pygame
import algorithm

SCREEN_WIDTH = 750
NR_OF_GRID_ROWS = 50
SURFACE = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_WIDTH))
pygame.display.set_caption("A star path visualizer")

algorithm.path_finder(SURFACE, SCREEN_WIDTH, NR_OF_GRID_ROWS)
