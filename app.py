import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Frog Test 🐸")

frog = pygame.image.load("assets/frog1.png").convert_alpha()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((120, 200, 120))  # achtergrond
    screen.blit(frog, (250, 180)) # teken kikker
    pygame.display.flip()

pygame.quit()