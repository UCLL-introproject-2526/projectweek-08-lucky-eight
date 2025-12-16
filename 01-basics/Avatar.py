import pygame
import random
import math

# Initialisatie
pygame.init()
WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lucky Frog River Selection 🍀")
clock = pygame.time.Clock()

# Fonts
pixel_font = pygame.font.SysFont("Courier New", 42, bold=True)
button_font = pygame.font.SysFont("Courier New", 20, bold=True)

# --- TEXTUUR DATA ---
# Genereer vaste posities voor de gras-textuur (bovenaan en onderaan)
grass_texture = []
for _ in range(40):
    grass_texture.append((random.randint(0, WIDTH), random.randint(0, 110)))   # Bovenkant
    grass_texture.append((random.randint(0, WIDTH), random.randint(370, 480))) # Onderkant

# Water animatie details
ripples = [[random.randint(0, WIDTH), random.randint(140, 340), random.uniform(0.5, 1.5)] for _ in range(10)]

def draw_river_environment():
    # 1. Basis Gras (Land)
    screen.fill((34, 139, 34)) 
    
    # 2. Gras Textuur (kleine donkere sprietjes)
    for tx, ty in grass_texture:
        pygame.draw.line(screen, (25, 100, 25), (tx, ty), (tx, ty + 4), 1)
        pygame.draw.line(screen, (25, 100, 25), (tx + 2, ty + 1), (tx + 2, ty + 5), 1)
    
    # 3. De Rivier
    water_color = (60, 160, 210)
    pygame.draw.rect(screen, water_color, (0, 120, WIDTH, 240))
    
    # 4. Rivier randjes (modder/oever)
    pygame.draw.rect(screen, (100, 70, 40), (0, 115, WIDTH, 8)) 
    pygame.draw.rect(screen, (100, 70, 40), (0, 357, WIDTH, 8)) 

    # 5. Water rimpelingen & Textuur
    for r in ripples:
        r[0] -= r[2] 
        if r[0] < -50: r[0] = WIDTH + 50
        # Lichtblauwe schittering
        pygame.draw.line(screen, (100, 190, 230), (r[0], r[1]), (r[0]+30, r[1]), 2)
        # Donkere diepte-lijn voor meer water-textuur
        pygame.draw.line(screen, (50, 140, 190), (r[0]-10, r[1]+3), (r[0]+20, r[1]+3), 1)

def draw_lilypad(x, y):
    w, h = 100, 35
    pad_rect = pygame.Rect(x-5, y+60, w, h)
    water_color = (60, 160, 210)
    
    pygame.draw.ellipse(screen, (20, 70, 30), pad_rect) 
    pygame.draw.ellipse(screen, (45, 180, 90), (pad_rect.x+2, pad_rect.y+2, w-4, h-4)) 
    
    center = pad_rect.center
    pts = [center, (pad_rect.right + 10, pad_rect.top - 5), (pad_rect.right + 10, pad_rect.bottom + 5)]
    pygame.draw.polygon(screen, water_color, pts)

def draw_glow_title(text, pos):
    for off in range(5, 0, -1):
        glow_surf = pixel_font.render(text, True, (0, 255, 100))
        glow_surf.set_alpha(100 // off)
        screen.blit(glow_surf, (pos[0] + off, pos[1] + off))
    main = pixel_font.render(text, True, (255, 255, 255))
    screen.blit(main, pos)

def draw_button(x, y, label, mouse_pos):
    rect = pygame.Rect(x, y, 110, 45)
    is_hovered = rect.collidepoint(mouse_pos)
    color = (40, 100, 60) if not is_hovered else (60, 150, 80) 
    
    pygame.draw.rect(screen, (20, 50, 30), (x+3, y+3, 110, 45), border_radius=10) 
    pygame.draw.rect(screen, color, rect, border_radius=10)
    
    txt = button_font.render(label, True, (255, 255, 255))
    screen.blit(txt, txt.get_rect(center=rect.center))

# Kikkers laden
try:
    frog_orig = pygame.image.load("assets/frog.png").convert_alpha()
    frog_orig = pygame.transform.smoothscale(frog_orig, (85, 85))
except:
    frog_orig = pygame.Surface((85, 85), pygame.SRCALPHA)
    pygame.draw.ellipse(frog_orig, (34, 139, 34), (5, 20, 75, 60))

frog_colors = [(0,0,0), (120,0,0), (0,0,120), (120,120,0), (120,0,120)]
frogs = []
for c in frog_colors:
    f = frog_orig.copy()
    tint = pygame.Surface(f.get_size(), pygame.SRCALPHA)
    tint.fill((*c, 0))
    f.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
    frogs.append(f)

positions = [(40 + i*105, 190) for i in range(len(frogs))]
jump_offsets = [0] * 5
jump_frames = [0] * 5

# --- MAIN LOOP ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    draw_river_environment()
    draw_glow_title("Select your frog", (110, 40))

    for i, frog in enumerate(frogs):
        x, y = positions[i]
        frog_rect = pygame.Rect(x, y, 85, 85)
        
        if frog_rect.collidepoint(mouse_pos):
            if jump_frames[i] == 0: jump_frames[i] = 10
        
        if jump_frames[i] > 0:
            jump_offsets[i] = -35 * math.sin(math.pi * (10 - jump_frames[i]) / 10)
            jump_frames[i] -= 1
        else:
            jump_offsets[i] = 0

        draw_lilypad(x, y)
        curr_y = y + jump_offsets[i]
        
        if frog_rect.collidepoint(mouse_pos):
            mask = pygame.mask.from_surface(frog)
            glow = mask.to_surface(setcolor=(255, 255, 255, 120), unsetcolor=(0,0,0,0))
            for o in range(3, 0, -1):
                screen.blit(glow, (x-o, curr_y))
                screen.blit(glow, (x+o, curr_y))

        screen.blit(frog, (x, curr_y))

    draw_button(25, 400, "BACK", mouse_pos)
    draw_button(465, 400, "NEXT", mouse_pos)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
