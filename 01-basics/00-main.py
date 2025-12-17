import pygame
import random
import math
import sys

# ================= INIT =================
pygame.init()
WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lucky Jump")
clock = pygame.time.Clock()

# ================= STATE =================
selected_frog_index = None

# ================= FONTS =================
try:
    pixel_font = pygame.font.SysFont("Trebuchet MS", 38, bold=True)
except:
    pixel_font = pygame.font.SysFont("Arial", 38, bold=True)
button_font = pygame.font.SysFont("Trebuchet MS", 20, bold=True)

# ================= MENU BG =================
menu_bg = pygame.transform.scale(
    pygame.image.load("assets/lucky jump menu.png").convert(),
    (WIDTH, HEIGHT)
)

# ================= BUTTON =================
def draw_button(x, y, label, mouse_pos):
    rect = pygame.Rect(x, y, 110, 45)
    is_hovered = rect.collidepoint(mouse_pos)
    color = (40, 100, 60) if not is_hovered else (60, 150, 80)
    pygame.draw.rect(screen, (20, 50, 30), (x+3, y+3, 110, 45), border_radius=10)
    pygame.draw.rect(screen, color, rect, border_radius=15)
    txt = button_font.render(label, True, (255, 255, 255))
    screen.blit(txt, txt.get_rect(center=rect.center))
    return rect

# ================= MENU =================
def menu():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(menu_bg, (0, 0))

        start = pygame.Rect(WIDTH//2-55, 380, 110, 45)
        select = pygame.Rect(WIDTH//2-55, 440, 110, 45)
        quitb = pygame.Rect(WIDTH//2-55, 500, 110, 45)

        draw_button(start.x, start.y, "START", mouse_pos)
        draw_button(select.x, select.y, "SELECT", mouse_pos)
        draw_button(quitb.x, quitb.y, "QUIT", mouse_pos)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if select.collidepoint(e.pos):
                    return "avatar"
                if start.collidepoint(e.pos):
                    return "game"
                if quitb.collidepoint(e.pos):
                    pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(60)

# =========================================================
# ================= AVATAR (ONGEWIJZIGD) ==================
# =========================================================

random.seed(42)
glow_timer = 0

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
    for bx, by in bush_positions:
        screen.blit(bush_img, (bx, by))
    for flower in flower_data:
        img = yellow_flower_img if flower['type'] == 0 else orange_flower_img
        screen.blit(img, flower['pos'])

def draw_balanced_title(text, y_pos):
    main_color = (210, 240, 210)
    shadow_color = (20, 50, 20)
    x_pos = (WIDTH // 2) - (pixel_font.size(text)[0] // 2)
    for ox, oy in [(1,1),(-1,-1),(1,-1),(-1,1),(2,2)]:
        screen.blit(pixel_font.render(text, True, shadow_color),(x_pos+ox,y_pos+oy))
    screen.blit(pixel_font.render(text, True, main_color),(x_pos,y_pos))

def draw_body_glow(surface, img, x, y):
    mask = pygame.mask.from_surface(img)
    for i in range(10, 0, -2):
        alpha = 40 - (i * 3)
        if alpha <= 0: continue
        s = mask.to_surface(setcolor=(255,255,255,alpha), unsetcolor=(0,0,0,0))
        scale = 1.0 + (i * 0.02)
        new_size = (int(s.get_width()*scale), int(s.get_height()*scale))
        glow_layer = pygame.transform.smoothscale(s, new_size)
        off_x = (glow_layer.get_width()-img.get_width())//2
        off_y = (glow_layer.get_height()-img.get_height())//2
        surface.blit(glow_layer, (x-off_x, y-off_y))

def draw_selection_arrow(surface, x, y, color):
    bounce = math.sin(glow_timer * 2) * 10
    arrow_y = y - 50 + bounce
    points = [(x+42,arrow_y+25),(x+22,arrow_y),(x+62,arrow_y)]
    pygame.draw.polygon(surface, (20,50,20), [(p[0]+2,p[1]+2) for p in points])
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, (255,255,255), points, 2)

# ================= ASSETS =================
frog_orig = pygame.transform.smoothscale(
    pygame.image.load("assets/frog.png").convert_alpha(), (85,85))
lilypad_img = pygame.transform.smoothscale(
    pygame.image.load("assets/lilypad.png").convert_alpha(), (85,40))
bush_img = pygame.transform.smoothscale(
    pygame.image.load("assets/bushes.png").convert_alpha(), (75,60))
yellow_flower_img = pygame.transform.smoothscale(
    pygame.image.load("assets/yellowflower.png").convert_alpha(), (22,22))
orange_flower_img = pygame.transform.smoothscale(
    pygame.image.load("assets/orangeflower.png").convert_alpha(), (22,22))

generate_decorations()

frog_colors = [(30,30,30),(180,20,20),(20,60,180),(180,180,20),(160,20,160)]
arrow_colors = [(144,238,144),(255,160,60),(173,216,230),(255,255,150),(255,182,193)]

frogs=[]
for c in frog_colors:
    f=frog_orig.copy()
    tint=pygame.Surface(f.get_size(),pygame.SRCALPHA); tint.fill((*c,0))
    f.blit(tint,(0,0),special_flags=pygame.BLEND_RGBA_ADD)
    frogs.append(f)

start_x=(WIDTH-len(frogs)*115)//2+10
positions=[(start_x+i*115,260) for i in range(len(frogs))]
jump_offsets=[0]*5
jump_frames=[0]*5

# ================= AVATAR =================
def avatar():
    global glow_timer, selected_frog_index
    while True:
        mouse_pos = pygame.mouse.get_pos()
        glow_timer += 0.05

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if pygame.Rect(50,560,110,45).collidepoint(e.pos):
                    return "menu"
                if pygame.Rect(WIDTH-160,560,110,45).collidepoint(e.pos):
                    if selected_frog_index is not None:
                        return "game"
                for i,(x,y) in enumerate(positions):
                    if pygame.Rect(x,y,85,85).collidepoint(e.pos):
                        selected_frog_index = i

        draw_river_environment()
        draw_balanced_title("Select your frog", 55)

        for i,frog in enumerate(frogs):
            x,y=positions[i]
            hovered = pygame.Rect(x,y,85,85).collidepoint(mouse_pos)
            selected = (selected_frog_index == i)

            if hovered and jump_frames[i]==0:
                jump_frames[i]=20
            if jump_frames[i]>0:
                jump_offsets[i]=-40*math.sin(math.pi*(20-jump_frames[i])/20)
                jump_frames[i]-=1
            else:
                jump_offsets[i]=0

            screen.blit(lilypad_img,(x,y+60))
            curr_y=y+jump_offsets[i]

            if selected:
                draw_selection_arrow(screen,x,curr_y,arrow_colors[i])
                size=(int(85*1.1),int(85*1.1))
                big=pygame.transform.smoothscale(frog,size)
                draw_body_glow(screen,big,x-4,curr_y-4)
                screen.blit(big,(x-4,curr_y-4))
            else:
                screen.blit(frog,(x,curr_y))

        draw_button(50,560,"BACK",mouse_pos)
        draw_button(WIDTH-160,560,"NEXT",mouse_pos)

        pygame.display.flip()
        clock.tick(60)

# ================= GAME =================
def game():
    import pygame
    import random
    import sys

    screen = pygame.display.get_surface()
    WIDTH, HEIGHT = screen.get_width(), screen.get_height()

    clock = pygame.time.Clock()
    FPS = 60

    # =====================
    # CONSTANTEN
    # =====================
    RIVER_W = 300
    RIVER_X = WIDTH // 2 - RIVER_W // 2
    BRIDGE_HEIGHT = 60

    GRAVITY = 0.6
    JUMP_POWER = -14
    MOVE_SPEED = 5

    SCROLL_THRESHOLD = HEIGHT // 3
    SCROLL_SPEED = 0

    MAX_LIVES = 5

    # =====================
    # ASSETS
    # =====================
    frog_img = pygame.transform.smoothscale(
    frogs[selected_frog_index] if selected_frog_index is not None else frogs[0],
    (50, 50)
)

    lilypad_img = pygame.transform.smoothscale(
        pygame.image.load("assets/lilypad.png").convert_alpha(), (60, 26)
    )
    bush_img_orig = pygame.image.load("assets/bushes.png").convert_alpha()

    # 🍀 GROEN KLAVERTJE
    try:
        clover_img = pygame.transform.smoothscale(
            pygame.image.load("assets/clover.png").convert_alpha(), (26, 26)
        )
        tint = pygame.Surface(clover_img.get_size(), pygame.SRCALPHA)
        tint.fill((0, 220, 0, 255))
        clover_img.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    except:
        clover_img = pygame.Surface((26, 26), pygame.SRCALPHA)
        GREEN = (0, 220, 0)
        pygame.draw.circle(clover_img, GREEN, (13, 7), 6)
        pygame.draw.circle(clover_img, GREEN, (7, 13), 6)
        pygame.draw.circle(clover_img, GREEN, (19, 13), 6)
        pygame.draw.circle(clover_img, GREEN, (13, 19), 6)

    # =====================
    # LILYPAD
    # =====================
    class Lilypad:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def rect(self):
            return pygame.Rect(self.x, self.y, 60, 26)

        def draw(self):
            screen.blit(lilypad_img, (self.x, self.y))

    # =====================
    # KIKKER
    # =====================
    class Frog:
        def __init__(self):
            self.reset()

        def reset(self):
            self.x = WIDTH // 2 - 25
            self.y = HEIGHT - 140
            self.vel_y = JUMP_POWER

        def move(self, keys):
            if keys[pygame.K_LEFT]:
                self.x -= MOVE_SPEED
            if keys[pygame.K_RIGHT]:
                self.x += MOVE_SPEED

            # wrap
            if self.x < RIVER_X - 30:
                self.x = RIVER_X + RIVER_W - 20
            if self.x > RIVER_X + RIVER_W - 20:
                self.x = RIVER_X - 30

        def update(self, platforms):
            nonlocal SCROLL_SPEED

            self.vel_y += GRAVITY
            self.y += self.vel_y

            frog_rect = pygame.Rect(self.x, self.y, 50, 50)

            if self.vel_y > 0:
                for p in platforms:
                    if frog_rect.colliderect(p.rect()):
                        if self.y + 50 <= p.y + 15:
                            self.y = p.y - 50
                            self.vel_y = JUMP_POWER
                            break

            if self.y < SCROLL_THRESHOLD:
                SCROLL_SPEED = SCROLL_THRESHOLD - self.y
                self.y = SCROLL_THRESHOLD
            else:
                SCROLL_SPEED = 0

        def draw(self):
            screen.blit(frog_img, (self.x, self.y))


    # =====================
    # ACHTERGROND (GEFIKST)
    # =====================
    def draw_background(ripple_offset, bushes):
        # 1. Teken het gras (overal)
        screen.fill((34, 139, 34))
        
        # 2. Teken de gras-sprietjes (textuur) uit de globale lijst
        for tx, ty in grass_texture:
            screen.blit(pixel_font.render("", False, (0,0,0)), (0,0)) # Dummy voor font check
            pygame.draw.line(screen, (25, 100, 25), (tx, ty), (tx, ty + 4), 1)

        # 3. Teken de rivier in het midden
        pygame.draw.rect(screen, (60, 160, 210), (RIVER_X, 0, RIVER_W, HEIGHT))

        # 4. Teken de rimpels (bewegend) binnen de rivier
        for r in ripples:
            # We laten de rimpels binnen de RIVER_X en RIVER_X + RIVER_W blijven
            ry = (r[1] + ripple_offset) % HEIGHT # Laat ze naar beneden stromen
            rx = RIVER_X + (r[0] % (RIVER_W - 30))
            pygame.draw.line(screen, (100, 190, 230), (rx, ry), (rx + 30, ry), 2)

        # 5. Modderranden van de rivier
        pygame.draw.rect(screen, (100, 70, 40), (RIVER_X - 8, 0, 8, HEIGHT))
        pygame.draw.rect(screen, (100, 70, 40), (RIVER_X + RIVER_W, 0, 8, HEIGHT))

        # 6. Teken de struiken
        for bush in bushes:
            screen.blit(bush[0], (bush[1], bush[2]))

    # =====================
    # 👉 NIEUWE BRUG (ENKEL VISUEEL)
    # =====================
    def draw_bottom_bridge():
        y = HEIGHT - BRIDGE_HEIGHT
        pygame.draw.rect(screen, (120, 80, 40), (0, y, WIDTH, BRIDGE_HEIGHT))
        for x in range(0, WIDTH, 40):
            pygame.draw.rect(screen, (100, 65, 35),
                             (x + 5, y + 10, 30, BRIDGE_HEIGHT - 20))
        pygame.draw.rect(screen, (80, 50, 25), (0, y, WIDTH, 6))

    # =====================
    # SETUP
    # =====================
    frog = Frog()
    platforms = []
    lives = MAX_LIVES
    game_over = False

    for i in range(8):
        x = RIVER_X + random.randint(20, RIVER_W - 80)
        y = HEIGHT - i * 80
        platforms.append(Lilypad(x, y))

    bushes = []
    for _ in range(12):
        scale = random.randint(40, 60)
        img = pygame.transform.smoothscale(bush_img_orig, (scale, scale))
        bushes.append((img, RIVER_X-60, random.randint(0, HEIGHT)))
        bushes.append((img, RIVER_X+RIVER_W+10, random.randint(0, HEIGHT)))

    bridge_y = HEIGHT - BRIDGE_HEIGHT
    ripple_offset = 0

    font_big = pygame.font.SysFont("Trebuchet MS", 36, bold=True)
    font_small = pygame.font.SysFont("Trebuchet MS", 18)

    # =====================
    # GAME LOOP
    # =====================
    while True:
        clock.tick(FPS)
        ripple_offset += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                lives = MAX_LIVES
                frog.reset()
                game_over = False

        keys = pygame.key.get_pressed()

        if not game_over:
            frog.move(keys)
            frog.update(platforms)

            for p in platforms:
                p.y += SCROLL_SPEED

            platforms = [p for p in platforms if p.y < HEIGHT + 50]
            while len(platforms) < 8:
                x = RIVER_X + random.randint(20, RIVER_W - 80)
                y = min(p.y for p in platforms) - random.randint(70, 100)
                platforms.append(Lilypad(x, y))

            if frog.y > HEIGHT:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    frog.reset()

        draw_background(ripple_offset, bushes)

        for p in platforms:
            p.draw()
        frog.draw()

        for i in range(lives):
            screen.blit(clover_img, (10 + i * 30, 10))

        draw_bottom_bridge()

        if game_over:
            txt = font_big.render("GAME OVER", True, (255,255,255))
            sub = font_small.render("Press R to restart", True, (220,220,220))
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 40))
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 10))

        pygame.display.flip()


# ================= MAIN =================
def main():
    state="menu"
    while True:
        if state=="menu":
            state=menu()
        elif state=="avatar":
            state=avatar()
        elif state=="game":
            state=game()

main()
