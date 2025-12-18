import pygame
import random
import math
import sys
import audio

# ===== GLOBAL SETTINGS =====
music_muted = False
sound_muted = False

# ================= INIT =================
pygame.init()
pygame.mixer.init()

audio.init_music()
sfx = audio.load_sfx()

WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lucky Jump")
clock = pygame.time.Clock()

# ================= STATE =================
selected_level_index = 0
selected_frog_index = None
selected_level_img = None  # Slaat de gekozen achtergrond op

# ================= FONTS =================
try:
    pixel_font = pygame.font.SysFont("Trebuchet MS", 38, bold=True)
except:
    pixel_font = pygame.font.SysFont("Arial", 38, bold=True)
button_font = pygame.font.SysFont("Trebuchet MS", 20, bold=True)

# ================= ASSETS =================
# Level Select achtergrond inladen
try:
    level_select_bg = pygame.transform.scale(
        pygame.image.load("assets/select level background.png").convert(),
        (WIDTH, HEIGHT)
    )
except:
    level_select_bg = pygame.Surface((WIDTH, HEIGHT))
    level_select_bg.fill((30, 60, 30))

# Alle 5 level achtergronden laden
level_backgrounds = []
for i in range(1, 6):
    try:
        img = pygame.transform.scale(pygame.image.load(f"assets/level {i} background.png").convert(), (WIDTH, HEIGHT))
        level_backgrounds.append(img)
    except:
        # Fallback kleur als het plaatje mist
        surf = pygame.Surface((WIDTH, HEIGHT))
        surf.fill((34, 40 + (i*20), 34)) 
        level_backgrounds.append(surf)
# Menu achtergrond
menu_bg = pygame.transform.scale(
    pygame.image.load("assets/lucky jump menu.png").convert(),
    (WIDTH, HEIGHT)
)

# muziek achtergrond
import os

def play_music():
    pygame.mixer.music.load(os.path.join("assets", "music", "bg.mp3"))
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)

# ================= SFX =================

jump_sfx = pygame.mixer.Sound("assets/sfx/jump.wav")
land_sfx = pygame.mixer.Sound("assets/sfx/land.wav")
gameover_sfx = pygame.mixer.Sound("assets/sfx/gameover.wav")

jump_sfx.set_volume(0.5)
land_sfx.set_volume(0.5)
gameover_sfx.set_volume(0.6)

# 👉 DE NIEUWE GAME ACHTERGROND
# ================= GAME OVER IMAGES =================
game_over_images = []

try:
    game_over_images = [
        pygame.image.load("assets/game over.png").convert_alpha(),          # level 1 (groen)
        pygame.image.load("assets/game over (winter).png").convert_alpha(), # level 2 (blauw)
        pygame.image.load("assets/game over (candy).png").convert_alpha(),  # level 3 (roze)
        pygame.image.load("assets/game over (zomer).png").convert_alpha(), # level 4 (geel)
        pygame.image.load("assets/game over (halloween).png").convert_alpha(),  # level 5 (paars)
    ]

    game_over_images = [
        pygame.transform.smoothscale(img, (420, 420))
        for img in game_over_images
    ]
except:
    game_over_images = []

try:
    game_bg_img = pygame.transform.scale(
        pygame.image.load("assets/gameriver.png").convert(),
        (WIDTH, HEIGHT)
    )
except:
    # Fallback als het bestand niet gevonden wordt
    game_bg_img = pygame.Surface((WIDTH, HEIGHT))
    game_bg_img.fill((34, 139, 34))

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
def level_select():
    global selected_level_img
    global selected_level_index

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(level_select_bg, (0, 0))
        
        draw_balanced_title("Choose Your World", 40)

        level_buttons = []
        for i in range(5):
            bx, by = WIDTH // 2 - 20, 130 + (i * 85)
            # Preview plaatje
            p_rect = pygame.Rect(WIDTH // 2 - 140, by, 100, 55)
            pygame.draw.rect(screen, (255, 255, 255), p_rect.inflate(6,6), border_radius=5)
            preview = pygame.transform.scale(level_backgrounds[i], (100, 55))
            screen.blit(preview, (p_rect.x, p_rect.y))

            btn = draw_button(bx, by + 5, f"LEVEL {i+1}", mouse_pos)
            level_buttons.append((btn, i))

        back_btn = draw_button(50, HEIGHT - 70, "BACK", mouse_pos)

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if back_btn.collidepoint(e.pos): return "menu"
                for btn, idx in level_buttons:
                    if btn.collidepoint(e.pos):
                        selected_level_img = level_backgrounds[idx]
                        selected_level_index = idx
                        return "game"


        pygame.display.flip()
        clock.tick(60)
def menu():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(menu_bg, (0, 0))
        
        btn_w, btn_h = 180, 55
        gap = 18
        
        x = WIDTH // 2 - btn_w // 2
        y_start = 380

        start = pygame.Rect(WIDTH//2-55, 380, 110, 45)
        select = pygame.Rect(WIDTH//2-55, 440, 110, 45)
        settings_rect = pygame.Rect(WIDTH//2-55, 500, 110, 45)
        quitb = pygame.Rect(WIDTH//2-55, 560, 110, 45)

        draw_button(start.x, start.y, "START", mouse_pos)
        draw_button(select.x, select.y, "SELECT", mouse_pos)
        draw_button(settings_rect.x, settings_rect.y, "SETTINGS", mouse_pos)
        draw_button(quitb.x, quitb.y, "QUIT", mouse_pos)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            # 🎵 Audio controls
            if e.type == pygame.KEYDOWN and e.key == pygame.K_m:
                audio.toggle_music()
                
            if e.type == pygame.KEYDOWN and (e.key == pygame.K_PLUS or e.key == pygame.K_EQUALS):
                audio.volume_up()
                
            if e.type == pygame.KEYDOWN and e.key == pygame.K_MINUS:
                audio.volume_down()

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if select.collidepoint(e.pos):
                    return "avatar"
                if start.collidepoint(e.pos):
                    return "level_select"
                if settings_rect.collidepoint(e.pos):
                    return "settings" 
                if quitb.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

def draw_toggle_icon(screen, rect, is_muted, kind):
    pygame.draw.rect(screen, (40, 180, 60), rect, border_radius=14)
    pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=14)

    cx, cy = rect.center

    if kind == "sound":
        body = pygame.Rect(0, 0, rect.w // 5, rect.h // 3)
        body.center = (cx - rect.w // 10, cy)
        pygame.draw.rect(screen, (255, 255, 255), body, border_radius=4)

        tri = [
            (body.right, body.top),
            (body.right + rect.w // 10, cy),
            (body.right, body.bottom),
        ]
        pygame.draw.polygon(screen, (255, 255, 255), tri)
        pygame.draw.arc(
            screen, (255, 255, 255),
            pygame.Rect(cx - rect.w//20, cy - rect.h//6, rect.w//6, rect.h//3),
            -0.8, 0.8, 3
        )

    elif kind == "music":
        stem_x = cx - rect.w // 20
        stem_top = cy - rect.h // 6
        stem_bot = cy + rect.h // 8
        pygame.draw.line(screen, (255, 255, 255), (stem_x, stem_top), (stem_x, stem_bot), 5)
        pygame.draw.circle(screen, (255, 255, 255), (stem_x - rect.w//15, stem_bot), rect.w//12)
        pygame.draw.line(screen, (255, 255, 255), (stem_x, stem_top), (stem_x + rect.w//8, stem_top + rect.h//12), 5)

    if is_muted:
        pygame.draw.line(
            screen, (220, 40, 40),
            (rect.left + 10, rect.bottom - 10),
            (rect.right - 10, rect.top + 10),
            6
        )

def settings_menu():
    global sound_muted, music_muted
    screen = pygame.display.get_surface()
    WIDTH, HEIGHT = screen.get_width(), screen.get_height()
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("Trebuchet MS", 40, bold=True)
    font_small = pygame.font.SysFont("Trebuchet MS", 22, bold=True)

    global music_muted, sound_muted

    box_w, box_h = 110, 90
    gap = 50
    y = HEIGHT // 2 - 20

    music_rect = pygame.Rect(WIDTH//2 - gap//2 - box_w, y, box_w, box_h)
    sound_rect = pygame.Rect(WIDTH//2 + gap//2, y, box_w, box_h)

    back_rect = pygame.Rect(40, 40, 120, 45)

    while True:
        clock.tick(60)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "menu"

            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "menu"

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if back_rect.collidepoint(e.pos):
                    return "menu"

                if music_rect.collidepoint(e.pos):
                    music_muted = not music_muted
                    if music_muted:
                        pygame.mixer.music.set_volume(0.0)
                    else:
                        pygame.mixer.music.set_volume(1.0)

                if sound_rect.collidepoint(e.pos):
                    sound_muted = not sound_muted

        screen.fill((20, 80, 160))

        title = font_big.render("Settings", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 110))

        panel = pygame.Rect(WIDTH//2 - 260, HEIGHT//2 - 90, 520, 220)
        pygame.draw.rect(screen, (10, 40, 90), panel, border_radius=24)


        lab_sound = font_small.render("Sound", True, (255, 255, 255))
        lab_music = font_small.render("Music", True, (255, 255, 255))
        screen.blit(lab_music, (music_rect.centerx - lab_music.get_width()//2, music_rect.top - 30))
        screen.blit(lab_sound, (sound_rect.centerx - lab_sound.get_width()//2, sound_rect.top - 30))


        draw_toggle_icon(screen, music_rect, music_muted, "music")
        draw_toggle_icon(screen, sound_rect, sound_muted, "sound")

        pygame.draw.rect(screen, (40, 40, 40), back_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), back_rect, 2, border_radius=10)
        back_txt = font_small.render("Back", True, (255, 255, 255))
        screen.blit(back_txt, (back_rect.centerx - back_txt.get_width()//2, back_rect.centery - back_txt.get_height()//2))

        pygame.display.flip()

# ================= AVATAR (ONGEWIJZIGD) =================
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

# ================= ASSETS (AVATAR) =================
frog_orig = pygame.transform.smoothscale(pygame.image.load("assets/frog.png").convert_alpha(), (85,85))
lilypad_img = pygame.transform.smoothscale(pygame.image.load("assets/lilypad.png").convert_alpha(), (85,40))
bush_img = pygame.transform.smoothscale(pygame.image.load("assets/bushes.png").convert_alpha(), (75,60))
yellow_flower_img = pygame.transform.smoothscale(pygame.image.load("assets/yellowflower.png").convert_alpha(), (22,22))
orange_flower_img = pygame.transform.smoothscale(pygame.image.load("assets/orangeflower.png").convert_alpha(), (22,22))

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

def avatar():
    global glow_timer, selected_frog_index
    while True:
        mouse_pos = pygame.mouse.get_pos()
        glow_timer += 0.05
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if pygame.Rect(50,560,110,45).collidepoint(e.pos): return "menu"
                if pygame.Rect(WIDTH-160,560,110,45).collidepoint(e.pos):
                 if selected_frog_index is not None: 
                  return "level_select"  
                for i,(x,y) in enumerate(positions):
                    if pygame.Rect(x,y,85,85).collidepoint(e.pos): selected_frog_index = i
        draw_river_environment()
        draw_balanced_title("Select your frog", 55)
        for i,frog in enumerate(frogs):
            x,y=positions[i]
            hovered = pygame.Rect(x,y,85,85).collidepoint(mouse_pos)
            selected = (selected_frog_index == i)
            if hovered and jump_frames[i]==0: jump_frames[i]=20
            if jump_frames[i]>0:
                jump_offsets[i]=-40*math.sin(math.pi*(20-jump_frames[i])/20)
                jump_frames[i]-=1
            else: jump_offsets[i]=0
            screen.blit(lilypad_img,(x,y+60))
            curr_y=y+jump_offsets[i]
            if selected:
                draw_selection_arrow(screen,x,curr_y,arrow_colors[i])
                size=(int(85*1.1),int(85*1.1))
                big=pygame.transform.smoothscale(frog,size)
                draw_body_glow(screen,big,x-4,curr_y-4)
                screen.blit(big,(x-4,curr_y-4))
            else: screen.blit(frog,(x,curr_y))
        draw_button(50,560,"BACK",mouse_pos)
        draw_button(WIDTH-160,560,"NEXT",mouse_pos)
        pygame.display.flip()
        clock.tick(60)

# ================= GAME =================
def game():
    screen = pygame.display.get_surface()
    WIDTH, HEIGHT = screen.get_width(), screen.get_height()
    clock = pygame.time.Clock()

    # CONSTANTEN
    RIVER_W, RIVER_X = 300, WIDTH // 2 - 150
    BRIDGE_HEIGHT = 60
    GRAVITY, JUMP_POWER, MOVE_SPEED = 0.6, -14, 5
    SCROLL_THRESHOLD = HEIGHT // 3
    SCROLL_SPEED = 0
    MAX_LIVES = 5

    # ASSETS
    frog_img = pygame.transform.smoothscale(
        frogs[selected_frog_index] if selected_frog_index is not None else frogs[0],
        (50, 50)
    )
    lilypad_img_game = pygame.transform.smoothscale(
        pygame.image.load("assets/lilypad.png").convert_alpha(), (60, 26)
    )

    try:
        clover_img = pygame.transform.smoothscale(
            pygame.image.load("assets/clover.png").convert_alpha(), (26, 26)
        )
        tint = pygame.Surface(clover_img.get_size(), pygame.SRCALPHA)
        tint.fill((0, 220, 0, 255))
        clover_img.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    except:
        clover_img = pygame.Surface((26, 26), pygame.SRCALPHA)
        pygame.draw.circle(clover_img, (0, 220, 0), (13, 13), 10)

    class Lilypad:
        def __init__(self, x, y):
            self.x, self.y = x, y
            self.scored = False
        def rect(self):
            return pygame.Rect(self.x, self.y, 60, 26)
        def draw(self):
            screen.blit(lilypad_img_game, (self.x, self.y))

    # NIEUW: collectible klavertje 
    class CollectibleClover:
        def __init__(self, x, y):
            self.x, self.y = x, y
        def rect(self):
            return pygame.Rect(self.x, self.y, 26, 26)
        def draw(self):
            screen.blit(clover_img, (self.x, self.y))

    class Frog:
        def __init__(self):
            self.reset ()
        def reset(self):
            self.x = WIDTH // 2 - 25
            self.y = HEIGHT - 80
            self.vel_y = 0
            self.on_platform = False
            self.last_platform = None
            self.just_landed = False
        def move(self, keys):
            if keys[pygame.K_LEFT]: self.x -= MOVE_SPEED
            if keys[pygame.K_RIGHT]: self.x += MOVE_SPEED
            if self.x < RIVER_X:
               self.x = RIVER_X
            if self.x > RIVER_X + RIVER_W - 50:
                self.x = RIVER_X + RIVER_W - 50
        def update(self, platforms):
            nonlocal score
            nonlocal SCROLL_SPEED
            self.vel_y += GRAVITY
            self.y += self.vel_y
            frog_rect = pygame.Rect(self.x, self.y, 50, 50)
            if self.vel_y > 0:
                for p in platforms:
                    if frog_rect.colliderect(p.rect()) and self.y + 50 <= p.y + 15:
                        self.y = p.y - 50
                        self.vel_y = JUMP_POWER
                        sfx.play("jump")
                        sfx.play("land")

                        if not p.scored:
                         p.scored = True
                         score += 1

                        break
            if self.vel_y < 0 and self.y < SCROLL_THRESHOLD:
                SCROLL_SPEED = SCROLL_THRESHOLD - self.y
                self.y = SCROLL_THRESHOLD
            else:
                SCROLL_SPEED = 0

        def draw(self):
            screen.blit(frog_img, (self.x, self.y))

    def draw_bottom_bridge():
        y = HEIGHT - BRIDGE_HEIGHT
        pygame.draw.rect(screen, (120, 80, 40), (0, y, WIDTH, BRIDGE_HEIGHT))
        for x in range(0, WIDTH, 40):
            pygame.draw.rect(screen, (100, 65, 35), (x + 5, y + 10, 30, BRIDGE_HEIGHT - 20))
        pygame.draw.rect(screen, (80, 50, 25), (0, y, WIDTH, 6))

    # SETUP GAME
    frog = Frog()
    platforms = [Lilypad(RIVER_X + random.randint(20, 220), HEIGHT - i * 80) for i in range(8)]
    lives, game_over = MAX_LIVES, False
    gameover_played = False

    # NIEUW
    collect_clovers = []
    score = 0
    paused = False
    pause_rect = pygame.Rect(WIDTH - 140, 40, 120, 35)
    scored_platforms = set ()

    font_big = pygame.font.SysFont("Trebuchet MS", 36, bold=True)
    font_small = pygame.font.SysFont("Trebuchet MS", 18)

    # RIPPLE EFFECT
    ripples = [[
        random.randint(RIVER_X + 10, RIVER_X + RIVER_W - 40),
        random.randint(0, HEIGHT),
        random.uniform(0.5, 2)
    ] for _ in range(45)]

    while True:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
             if pause_rect.collidepoint(event.pos):
                 paused = not paused

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                lives, game_over, score = MAX_LIVES, False, 0
                gameover_played = False
                frog.reset()
                collect_clovers.clear()
                paused = False

        if (not game_over) and (not paused):
            frog.move(pygame.key.get_pressed())
            frog.update(platforms)

            for p in platforms: p.y += SCROLL_SPEED
            for c in collect_clovers: c.y += SCROLL_SPEED

            platforms = [p for p in platforms if p.y < HEIGHT + 50]
            collect_clovers = [c for c in collect_clovers if c.y < HEIGHT + 50]

            while len(platforms) < 8:
                p = Lilypad(
                    RIVER_X + random.randint(20, 220),
                    min(pl.y for pl in platforms) - random.randint(70, 100)
                )
                platforms.append(p)

                # NIEUW: kans op klavertje
                if random.random() < 0.35:
                    collect_clovers.append(
                        CollectibleClover(p.x + 17, p.y - 22)
                    )

            frog_rect = pygame.Rect(frog.x, frog.y, 50, 50)
            for c in collect_clovers[:]:
                if frog_rect.colliderect(c.rect()):
                    collect_clovers.remove(c)
                    score += 5  # NIEUW

            if frog.y > HEIGHT:
                lives -= 1
                if lives <= 0:
                    game_over = True
                if not gameover_played:
                    sfx.play("gameover")
                    gameover_played = True
                else:
                    frog.reset()

        # ACHTERGROND (Gebruik gekozen level, anders de standaard rivier)
        if selected_level_img:
            screen.blit(selected_level_img, (0, 0))
        else:
            screen.blit(game_bg_img, (0, 0))

        # RIPPLE
        for r in ripples:
            r[1] += r[2] + SCROLL_SPEED * 0.3
            if r[1] > HEIGHT + 10:
                r[1] = -10
                r[0] = random.randint(RIVER_X + 10, RIVER_X + RIVER_W - 40)
            offset = math.sin(pygame.time.get_ticks() * 0.005 + r[1]) * 3
            pygame.draw.line(
                screen, (100, 190, 230),
                (r[0] + offset, r[1]),
                (r[0] + 30 + offset, r[1]), 2
            )

        for p in platforms: p.draw()
        for c in collect_clovers: c.draw()  # NIEUW
        frog.draw()

        # LIVES linksboven (ongewijzigd)
        for i in range(lives):
            screen.blit(clover_img, (10 + i * 30, 10))

        # SCORE rechtsboven (NIEUW)
        score_txt = font_small.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_txt, (WIDTH - score_txt.get_width() - 10, 10))
        # PAUSE button 
        pause_w, pause_h = 28, 28
        pause_rect = pygame.Rect(
            WIDTH - score_txt.get_width() - 10 - pause_w - 10,
            8,
            pause_w,
            pause_h
        )

        pygame.draw.rect(screen, (255, 255, 255), pause_rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), pause_rect, 2, border_radius=6)

        if not paused:
            pygame.draw.rect(screen, (0, 0, 0), (pause_rect.x + 8, pause_rect.y + 6, 4, 16))
            pygame.draw.rect(screen, (0, 0, 0), (pause_rect.x + 16, pause_rect.y + 6, 4, 16))
        else:
            pygame.draw.polygon(screen, (0, 0, 0), [
                (pause_rect.x + 9, pause_rect.y + 6),
                (pause_rect.x + 9, pause_rect.y + 22),
                (pause_rect.x + 21, pause_rect.y + 14),
            ])

        # PAUSE button (right side, under/near score)
        pause_label = "Resume" if paused else "Pause"
        pause_txt = font_small.render(pause_label, True, (255, 255, 255))

        pygame.draw.rect(screen, (40, 40, 40), pause_rect, border_radius=6)
        pygame.draw.rect(screen, (255, 255, 255), pause_rect, 2, border_radius=6)

        if not paused:
            # ⏸ pause icon
            pygame.draw.rect(screen, (0, 0, 0),
                             (pause_rect.x + 8, pause_rect.y + 6, 4, 16))
            pygame.draw.rect(screen, (0, 0, 0),
                             (pause_rect.x + 16, pause_rect.y + 6, 4, 16))
        else:
            # ▶ play icon
            pygame.draw.polygon(screen, (0, 0, 0), [
                (pause_rect.x + 9, pause_rect.y + 6),
                (pause_rect.x + 9, pause_rect.y + 22),
                (pause_rect.x + 21, pause_rect.y + 14),
            ])  
        draw_bottom_bridge()

        if game_over:
            # donkere overlay
             overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
             overlay.fill((0, 0, 0, 150))
             screen.blit(overlay, (0, 0))

            # bounce effect
             t = pygame.time.get_ticks()
             bounce = 1.0 + math.sin(t * 0.004) * 0.05
             size = int(420 * bounce)

             if game_over_images:
                img = pygame.transform.smoothscale(
                    game_over_images[selected_level_index],
                    (size, size)
                )
                rect = img.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2 - 30)
                )
                screen.blit(img, rect)

             sub = font_small.render(
                "Press R to restart",
                True,
                (240, 240, 240)
            )
             score_txt = font_small.render(
                f"Final Score: {score}",
                True,
                (255, 255, 255)
            )

             screen.blit(
                sub,
                (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 190)
            )
             screen.blit(
                score_txt,
                (WIDTH // 2 - score_txt.get_width() // 2, HEIGHT // 2 + 220)
            )



       
        pygame.display.flip()


# ================= MAIN =================
def main():
    state = "menu"
    play_music()
    while True:
        if state == "menu": state = menu()
        elif state == "avatar": state = avatar()
        elif state == "level_select": state = level_select() # VOEG DEZE TOE
        elif state == "game": state = game()
        elif state == "settings": state = settings_menu()
main()