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
grass_texture = []
for _ in range(40):
    grass_texture.append((random.randint(0, WIDTH), random.randint(0, 150)))   
    grass_texture.append((random.randint(0, WIDTH), random.randint(500, HEIGHT))) 

ripples = [[random.randint(0, WIDTH), random.randint(180, 470), random.uniform(0.5, 1.5)] for _ in range(12)]

def draw_river_environment():
    # 1. Basis Gras
    screen.fill((34, 139, 34)) 
    
    # 2. Gras Textuur
    for tx, ty in grass_texture:
        pygame.draw.line(screen, (25, 100, 25), (tx, ty), (tx, ty + 4), 1)
    
    # 3. De Rivier (Gecentreerd)
    water_color = (60, 160, 210)
    pygame.draw.rect(screen, water_color, (0, 160, WIDTH, 330))
    
    # 4. Modder oevers
    pygame.draw.rect(screen, (100, 70, 40), (0, 155, WIDTH, 8)) 
    pygame.draw.rect(screen, (100, 70, 40), (0, 485, WIDTH, 8)) 

    # 5. Water rimpelingen
    for r in ripples:
        r[0] -= r[2] 
        if r[0] < -50: r[0] = WIDTH + 50
        pygame.draw.line(screen, (100, 190, 230), (r[0], r[1]), (r[0]+30, r[1]), 2)

def draw_lilypad_img(x, y):
    # Lilypad blitten (solide, geen transparantie)
    screen.blit(lilypad_img, (x - 10, y + 55))

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

# --- ASSETS LADEN ---
try:
    frog_orig = pygame.image.load("assets/frog.png").convert_alpha()
    frog_orig = pygame.transform.smoothscale(frog_orig, (85, 85))
except:
    frog_orig = pygame.Surface((85, 85), pygame.SRCALPHA)
    pygame.draw.ellipse(frog_orig, (34, 139, 34), (5, 20, 75, 60))

try:
    # Laad de Lilypad
    lilypad_img = pygame.image.load("assets/lilypad.png").convert_alpha()
    lilypad_img = pygame.transform.smoothscale(lilypad_img, (110, 50))
    
    # LICHTGROENE TINT toevoegen
    # We maken een overlay die de afbeelding lichter en groener maakt
    light_tint = pygame.Surface(lilypad_img.get_size(), pygame.SRCALPHA)
    light_tint.fill((100, 255, 100, 40)) # Lichtgroen met lage opacity
    lilypad_img.blit(light_tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
except:
    lilypad_img = pygame.Surface((110, 50), pygame.SRCALPHA)
    pygame.draw.ellipse(lilypad_img, (144, 238, 144), (0, 0, 110, 50)) # Lichtgroen fallback

frog_colors = [(0,0,0), (120,0,0), (0,0,120), (120,120,0), (120,0,120)]
frogs = []
for c in frog_colors:
    f = frog_orig.copy()
    tint = pygame.Surface(f.get_size(), pygame.SRCALPHA)
    tint.fill((*c, 0))
    f.blit(tint, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
    frogs.append(f)

positions = [(40 + i*105, 260) for i in range(len(frogs))]
jump_offsets = [0] * 5
jump_frames = [0] * 5

# --- MAIN LOOP ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    draw_river_environment()
    draw_glow_title("Select your frog", (110, 70))

    for i, frog in enumerate(frogs):
        x, y = positions[i]
        frog_rect = pygame.Rect(x, y, 85, 85)
        
        if frog_rect.collidepoint(mouse_pos):
            if jump_frames[i] == 0: jump_frames[i] = 10
        
        if jump_frames[i] > 0:
            jump_offsets[i] = -40 * math.sin(math.pi * (10 - jump_frames[i]) / 10)
            jump_frames[i] -= 1
        else:
            jump_offsets[i] = 0

        # Teken de lichtgroene Lilypad
        draw_lilypad_img(x, y)
        
        curr_y = y + jump_offsets[i]
        
        if frog_rect.collidepoint(mouse_pos):
            mask = pygame.mask.from_surface(frog)
            glow = mask.to_surface(setcolor=(255, 255, 255, 120), unsetcolor=(0,0,0,0))
            for o in range(3, 0, -1):
                screen.blit(glow, (x-o, curr_y))
                screen.blit(glow, (x+o, curr_y))

        screen.blit(frog, (x, curr_y))

    draw_button(40, 550, "BACK", mouse_pos)
    draw_button(450, 550, "NEXT", mouse_pos)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()