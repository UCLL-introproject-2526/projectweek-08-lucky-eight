import pygame
import random
import math

# Initialisatie
pygame.init()
WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lucky Frog River Selection 🍀")
clock = pygame.time.Clock()

# --- VASTE LAYOUT SEED ---
random.seed(42) 

# Fonts - We behouden de Trebuchet MS font uit jouw code
try:
    pixel_font = pygame.font.SysFont("Trebuchet MS", 38, bold=True)
except:
    pixel_font = pygame.font.SysFont("Arial", 38, bold=True)
button_font = pygame.font.SysFont("Trebuchet MS", 20, bold=True)

# --- DECORATIE DATA ---
grass_texture = []
for _ in range(60): 
    grass_texture.append((random.randint(0, WIDTH), random.randint(0, 150)))   
    grass_texture.append((random.randint(0, WIDTH), random.randint(500, HEIGHT))) 

bush_positions = []
flower_data = []

def generate_decorations():
    for _ in range(3):
        bush_positions.append((random.randint(50, WIDTH-120), random.randint(40, 80)))
    for _ in range(4):
        flower_data.append({'pos': (random.randint(20, WIDTH-40), random.randint(50, 110)), 'type': random.randint(0, 1)})
    for _ in range(3):
        bush_positions.append((random.randint(50, WIDTH-120), random.randint(550, 580)))
    for _ in range(5):
        flower_data.append({'pos': (random.randint(20, WIDTH-40), random.randint(540, 600)), 'type': random.randint(0, 1)})

ripples = [[random.randint(0, WIDTH), random.randint(180, 470), random.uniform(0.5, 1.5)] for _ in range(15)]

def draw_river_environment():
    screen.fill((34, 139, 34)) 
    for tx, ty in grass_texture:
        pygame.draw.line(screen, (25, 100, 25), (tx, ty), (tx, ty + 4), 1)
    
    pygame.draw.rect(screen, (60, 160, 210), (0, 160, WIDTH, 330))
    pygame.draw.rect(screen, (100, 70, 40), (0, 155, WIDTH, 8)) 
    pygame.draw.rect(screen, (100, 70, 40), (0, 485, WIDTH, 8)) 

    for r in ripples:
        r[0] -= r[2] 
        if r[0] < -50: r[0] = WIDTH + 50
        pygame.draw.line(screen, (100, 190, 230), (r[0], r[1]), (r[0]+30, r[1]), 2)

    for bx, by in bush_positions: screen.blit(bush_img, (bx, by))
    for flower in flower_data:
        img = yellow_flower_img if flower['type'] == 0 else orange_flower_img
        screen.blit(img, (flower['pos']))

def draw_balanced_title(text, y_pos):
    # Kleuren aangepast: Zachtgroen (niet fel) met een donkere (niet pikzwarte) uitlijning
    main_color = (210, 240, 210)    # Zacht lichtgroen
    shadow_color = (20, 50, 20)     # Donkergroene schaduw/uitlijning
    
    x_pos = (WIDTH // 2) - (pixel_font.size(text)[0] // 2)

    # De donkere uitlijning (we tekenen de schaduw licht verschoven rondom de tekst)
    # Dit geeft een diepte-effect dat "cute" maar leesbaar is
    offsets = [(1, 1), (-1, -1), (1, -1), (-1, 1), (2, 2)]
    for ox, oy in offsets:
        shadow_surf = pixel_font.render(text, True, shadow_color)
        screen.blit(shadow_surf, (x_pos + ox, y_pos + oy))

    # De hoofdtekst in zachtgroen erbovenop
    text_surf = pixel_font.render(text, True, main_color)
    screen.blit(text_surf, (x_pos, y_pos))

def draw_button(x, y, label, mouse_pos):
    rect = pygame.Rect(x, y, 110, 45)
    is_hovered = rect.collidepoint(mouse_pos)
    color = (40, 100, 60) if not is_hovered else (60, 150, 80) 
    pygame.draw.rect(screen, (20, 50, 30), (x+3, y+3, 110, 45), border_radius=10) 
    pygame.draw.rect(screen, color, rect, border_radius=15)
    txt = button_font.render(label, True, (255, 255, 255))
    screen.blit(txt, txt.get_rect(center=rect.center))

# --- ASSETS LADEN ---
try:
    frog_orig = pygame.image.load("assets/frog.png").convert_alpha()
    frog_orig = pygame.transform.smoothscale(frog_orig, (85, 85))
    lilypad_img = pygame.image.load("assets/lilypad.png").convert_alpha()
    lilypad_img = pygame.transform.smoothscale(lilypad_img, (85, 40))
    bush_img = pygame.image.load("assets/bushes.png").convert_alpha()
    bush_img = pygame.transform.smoothscale(bush_img, (75, 60))
    yellow_flower_img = pygame.image.load("assets/yellowflower.png").convert_alpha()
    yellow_flower_img = pygame.transform.smoothscale(yellow_flower_img, (22, 22))
    orange_flower_img = pygame.image.load("assets/orangeflower.png").convert_alpha()
    orange_flower_img = pygame.transform.smoothscale(orange_flower_img, (22, 22))
except:
    bush_img = pygame.Surface((75, 60), pygame.SRCALPHA); pygame.draw.ellipse(bush_img, (20, 80, 20), (0, 0, 75, 60))
    yellow_flower_img = pygame.Surface((22, 22), pygame.SRCALPHA); pygame.draw.circle(yellow_flower_img, (255, 255, 0), (11, 11), 9)
    orange_flower_img = pygame.Surface((22, 22), pygame.SRCALPHA); pygame.draw.circle(orange_flower_img, (255, 165, 0), (11, 11), 9)
    frog_orig = pygame.Surface((85, 85), pygame.SRCALPHA)

generate_decorations()

frog_colors = [(0,0,0), (120,0,0), (0,0,120), (120,120,0), (120,0,120)]
frogs = []
for c in frog_colors:
    f = frog_orig.copy()
    tint = pygame.Surface(f.get_size(), pygame.SRCALPHA); tint.fill((*c, 0))
    f.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
    frogs.append(f)

total_frogs_width = len(frogs) * 115
start_x = (WIDTH - total_frogs_width) // 2 + 10
positions = [(start_x + i*115, 260) for i in range(len(frogs))]
jump_offsets = [0] * 5
jump_frames = [0] * 5

# --- MAIN LOOP ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    draw_river_environment()
    draw_balanced_title("Select your frog", 55)

    for i, frog in enumerate(frogs):
        x, y = positions[i]
        frog_rect = pygame.Rect(x, y, 85, 85)
        if frog_rect.collidepoint(mouse_pos) and jump_frames[i] == 0: jump_frames[i] = 10
        if jump_frames[i] > 0:
            jump_offsets[i] = -40 * math.sin(math.pi * (10 - jump_frames[i]) / 10)
            jump_frames[i] -= 1
        else: jump_offsets[i] = 0

        screen.blit(lilypad_img, (x, y + 60))
        curr_y = y + jump_offsets[i]
        
        if frog_rect.collidepoint(mouse_pos):
            mask = pygame.mask.from_surface(frog)
            glow = mask.to_surface(setcolor=(255, 255, 255, 100), unsetcolor=(0,0,0,0))
            screen.blit(glow, (x-2, curr_y))
            screen.blit(glow, (x+2, curr_y))

        screen.blit(frog, (x, curr_y))

    draw_button(50, 560, "BACK", mouse_pos)
    draw_button(WIDTH - 160, 560, "NEXT", mouse_pos)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()