import sys
import pygame
from settings import *
from level import Level

def run_game():
    if not pygame.get_init():
        pygame.init()
    screen = pygame.display.get_surface() or pygame.display.set_mode((WIDTH_LEVEL, HEIGHT_LEVEL))
    clock = pygame.time.Clock()
    level = Level()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                
        keys = pygame.key.get_pressed()
        level.update(keys)
        level.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)