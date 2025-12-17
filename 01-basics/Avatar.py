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

# Fonts
try:
    pixel_font = pygame.font.SysFont("Trebuchet MS", 38, bold=True)
except:
    pixel_font = pygame.font.SysFont("Arial", 38, bold=True)
button_font = pygame.font.SysFont("Trebuchet MS", 20, bold=True)

# --- VARIABELEN ---
selected_frog_index = None
glow_timer = 0 

# --- DECORATIE & OMGEVING ---
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
    main_color = (210, 240, 210)
    shadow_color = (20, 50, 20)
    x_pos = (WIDTH // 2) - (pixel_font.size(text)[0] // 2)
    offsets = [(1, 1), (-1, -1), (1, -1), (-1, 1), (2, 2)]
    for ox, oy in offsets:
        shadow_surf = pixel_font.render(text, True, shadow_color)
        screen.blit(shadow_surf, (x_pos + ox, y_pos + oy))
    text_surf = pixel_font.render(text, True, main_color)
    screen.blit(text_surf, (x_pos, y_pos))

def draw_body_glow(surface, img, x, y):
    mask = pygame.mask.from_surface(img)
    glow_color = (255, 255, 255)
    for i in range(10, 0, -2):
        alpha = 40 - (i * 3)
        if alpha <= 0: continue
        s = mask.to_surface(setcolor=(*glow_color, alpha), unsetcolor=(0,0,0,0))
        scale = 1.0 + (i * 0.02)
        new_size = (int(s.get_width() * scale), int(s.get_height() * scale))
        glow_layer = pygame.transform.smoothscale(s, new_size)
        off_x = (glow_layer.get_width() - img.get_width()) // 2
        off_y = (glow_layer.get_height() - img.get_height()) // 2
        surface.blit(glow_layer, (x - off_x, y - off_y))

def draw_selection_arrow(surface, x, y, color):
    bounce = math.sin(glow_timer * 2) * 10
    arrow_y = y - 50 + bounce
    points = [
        (x + 42, arrow_y + 25), 
        (x + 22, arrow_y),      
        (x + 62, arrow_y)       
    ]
    pygame.draw.polygon(surface, (20, 50, 20), [(p[0]+2, p[1]+2) for p in points])
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, (255, 255, 255), points, 2)

def draw_button(x, y, label, mouse_pos):
    rect = pygame.Rect(x, y, 110, 45)
    is_hovered = rect.collidepoint(mouse_pos)
    color = (40, 100, 60) if not is_hovered else (60, 150, 80) 
    pygame.draw.rect(screen, (20, 50, 30), (x+3, y+3, 110, 45), border_radius=10) 
    pygame.draw.rect(screen, color, rect, border_radius=15)
    txt = button_font.render(label, True, (255, 255, 255))
    screen.blit(txt, txt.get_rect(center=rect.center))

# --- ASSETS ---
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

# Originele kikkerkleuren (teruggezet)
frog_colors = [(30,30,30), (180,20,20), (20,60,180), (180,180,20), (160,20,160)]

# Lichte pijlkleuren (jouw verzoek)
arrow_colors = [
    (144, 238, 144),  # Lichtgroen
    (255, 160, 60),   # Licht Oranje
    (173, 216, 230),  # Lichtblauw
    (255, 255, 150),  # Geel
    (255, 182, 193)   # Licht Roze
]

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
    glow_timer += 0.05 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(frogs)):
                x, y = positions[i]
                if pygame.Rect(x, y, 85, 85).collidepoint(event.pos):
                    selected_frog_index = i

    draw_river_environment()
    draw_balanced_title("Select your frog", 55)

    for i, frog in enumerate(frogs):
        x, y = positions[i]
        is_hovered = pygame.Rect(x, y, 85, 85).collidepoint(mouse_pos)
        is_selected = (selected_frog_index == i)

        # Trager springen (20 frames)
        if is_hovered and jump_frames[i] == 0: jump_frames[i] = 20
        if jump_frames[i] > 0:
            jump_offsets[i] = -40 * math.sin(math.pi * (20 - jump_frames[i]) / 20)
            jump_frames[i] -= 1
        else: jump_offsets[i] = 0

        screen.blit(lilypad_img, (x, y + 60))
        curr_x, curr_y = x, y + jump_offsets[i]
        
        if is_selected:
            # Pijl gebruikt de lichte kleur uit arrow_colors
            draw_selection_arrow(screen, x, curr_y, arrow_colors[i])
            
            size = (int(85 * 1.1), int(85 * 1.1))
            disp_frog = pygame.transform.smoothscale(frog, size)
            adj_x, adj_y = curr_x - 4, curr_y - 4
            draw_body_glow(screen, disp_frog, adj_x, adj_y)
            screen.blit(disp_frog, (adj_x, adj_y))
        else:
            screen.blit(frog, (curr_x, curr_y))

    draw_button(50, 560, "BACK", mouse_pos)
    draw_button(WIDTH - 160, 560, "NEXT", mouse_pos)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()