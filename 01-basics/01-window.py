import pygame

def create_window(width=800, height=600, title="Lucky Jump"):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)
    return screen
