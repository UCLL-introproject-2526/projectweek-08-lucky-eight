import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Frog Test 🐸")

# originele kikker laden
frog_orig = pygame.image.load("assets/frog.png").convert_alpha()

# kleuren voor variaties (RGB add)
colors = [(0,0,0), (100,0,0), (0,100,0), (0,0,100), (100,100,0)]
frogs = []

for color in colors:
    frog = frog_orig.copy()
    # maak een surface met dezelfde grootte, met alpha
    tint = pygame.Surface(frog.get_size(), pygame.SRCALPHA)
    tint.fill((*color, 0))  # 0 alpha om transparantie te behouden
    # blend kleuren bij elkaar
    frog.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
    frogs.append(frog)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((120, 200, 120))  # achtergrond

    # teken de 5 kikkers op rij
    for i, frog in enumerate(frogs):
        screen.blit(frog, (50 + i*100, 180))

    pygame.display.flip()

pygame.quit()
