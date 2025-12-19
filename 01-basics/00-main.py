import pygame
import random
import math
import sys
import audio

# ===== WATER & RIPPLE KLEUREN PER LEVEL =====
LEVEL_WATER = {
    0: (120, 200, 215),  # level 1 – natuur
    1: (170, 220, 240),  # level 2 – winter
    2: (255, 215, 225),  # level 3 – candy
    3: (180, 245, 235),  # level 4 – zomer
    4: (170, 120, 210),  # level 5 – halloween
}


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
        pygame.image.load("assets/images/select level background.png").convert(),
        (WIDTH, HEIGHT)
    )
except:
    level_select_bg = pygame.Surface((WIDTH, HEIGHT))
    level_select_bg.fill((30, 60, 30))

# Alle 5 level achtergronden laden
level_backgrounds = []
for i in range(1, 6):
    try:
        img = pygame.transform.scale(pygame.image.load(f"assets/images/level {i} background.png").convert(), (WIDTH, HEIGHT))
        level_backgrounds.append(img)
    except:
        # Fallback kleur als het plaatje mist
        surf = pygame.Surface((WIDTH, HEIGHT))
        surf.fill((34, 40 + (i*20), 34)) 
        level_backgrounds.append(surf)
# Menu achtergrond
menu_bg = pygame.transform.scale(
    pygame.image.load("assets/images/lucky jump menu.png").convert(),
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

# DE NIEUWE GAME ACHTERGROND
# ================= GAME OVER IMAGES =================
game_over_images = []

try:
    game_over_images = [
        pygame.image.load("assets/images/game over.png").convert_alpha(),          # level 1 (groen)
        pygame.image.load("assets/images/game over (winter).png").convert_alpha(), # level 2 (blauw)
        pygame.image.load("assets/images/game over (candy).png").convert_alpha(),  # level 3 (roze)
        pygame.image.load("assets/images/game over (zomer).png").convert_alpha(), # level 4 (geel)
        pygame.image.load("assets/images/game over (halloween).png").convert_alpha(),  # level 5 (paars)
    ]

    game_over_images = [
        pygame.transform.smoothscale(img, (420, 420))
        for img in game_over_images
    ]
except:
    game_over_images = []

try:
    game_bg_img = pygame.transform.scale(
        pygame.image.load("assets/images/gameriver.png").convert(),
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

# --- menu water animation ---
menu_waves = []
menu_wave_timer = 0

def menu():
    global menu_wave_timer, menu_waves

    # --- init water sparkles ---
    if not hasattr(menu, "water_sparkles"):
        menu.water_sparkles = []
        for _ in range(25):
            menu.water_sparkles.append([
                random.randint(0, WIDTH),
                random.randint(200, HEIGHT),
                random.uniform(0.3, 1.0)
            ])

    while True:
        dt = clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(menu_bg, (0, 0))

        # --- water ripple animation ---
        menu_wave_timer += dt

        if menu_wave_timer > 1.2:
            menu_wave_timer = 0
            menu_waves.append({
                "x": random.randint(200, WIDTH - 200),
                "y": random.randint(250, HEIGHT - 200),
                "r": 0,
                "alpha": 120
            })

        for wave in menu_waves[:]:
            wave["r"] += 15
            wave["alpha"] -= 2

            if wave["alpha"] <= 0:
                menu_waves.remove(wave)
                continue

            surf = pygame.Surface((wave["r"]*2, wave["r"]*2), pygame.SRCALPHA)
            pygame.draw.circle(
                surf,
                (220, 255, 255, wave["alpha"]),
                (wave["r"], wave["r"]),
                wave["r"],
                2
            )
            screen.blit(surf, (wave["x"] - wave["r"], wave["y"] - wave["r"]))

        # --- draw water sparkles ---
        for s in menu.water_sparkles:
            s[1] -= s[2]
            if s[1] < 200:
                s[1] = HEIGHT
                s[0] = random.randint(0, WIDTH)

            pygame.draw.circle(
                screen,
                (220, 255, 255),
                (int(s[0]), int(s[1])),
                2
            )

            pygame.draw.circle(
                screen,
                (220, 255, 255),
                (int(s[0]), int(s[1])),
                2
            )
        
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
        dt = clock.get_time() / 1000
        
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

# ================= AVATAR =================
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
frog_orig = pygame.transform.smoothscale(pygame.image.load("assets/images/frog.png").convert_alpha(), (85,85))
lilypad_img = pygame.transform.smoothscale(pygame.image.load("assets/images/lilypad.png").convert_alpha(), (85,40))
bush_img = pygame.transform.smoothscale(pygame.image.load("assets/images/bushes.png").convert_alpha(), (75,60))
yellow_flower_img = pygame.transform.smoothscale(pygame.image.load("assets/images/yellowflower.png").convert_alpha(), (22,22))
orange_flower_img = pygame.transform.smoothscale(pygame.image.load("assets/images/orangeflower.png").convert_alpha(), (22,22))

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

    paused = False
    pause_buttons = {}



    # ASSETS
    frog_img = pygame.transform.smoothscale(
        frogs[selected_frog_index] if selected_frog_index is not None else frogs[0],
        (50, 50)
    )
    # NIEUW: Obstakel afbeeldingen inladen
    enemy_imgs = []
    enemy_names = ["", "winter obstakel", "candy obstakel", "zomer obstakel", "halloween obstakel"]
    
    for name in enemy_names:
        if name == "": 
            enemy_imgs.append(None) # Level 1 heeft geen vijand
            continue
        try:
            img = pygame.image.load(f"assets/images/{name}.png").convert_alpha()
            # Schaal ze naar een mooi formaat, bijv. 45x45 pixels
            enemy_imgs.append(pygame.transform.smoothscale(img, (45, 45)))
        except:
            # Fallback: als het plaatje mist, maken we een gekleurd vlakje
            surf = pygame.Surface((45, 45), pygame.SRCALPHA)
            pygame.draw.rect(surf, (255, 0, 0), (0, 0, 45, 45))
            enemy_imgs.append(surf)
    lilypad_img_game = pygame.transform.smoothscale(
        pygame.image.load("assets/images/lilypad.png").convert_alpha(), (60, 26)
    )

    try:
        clover_img = pygame.transform.smoothscale(
            pygame.image.load("assets/images/clover.png").convert_alpha(), (26, 26)
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
    # NIEUW: Enemy klasse
    class Enemy:
        def __init__(self, x, y, level_idx):
            self.x, self.y = x, y
            self.level_idx = level_idx
            # Snelheid: level 2 is traag, level 5 is heel snel
            self.speed = 1.2 + (level_idx * 1.0) 
            self.dir = 1
            self.image = enemy_imgs[level_idx]

        def update(self, scroll):
            self.y += scroll
            self.x += self.speed * self.dir
            # Blijf binnen de rivierbreedte
            if self.x < RIVER_X or self.x > RIVER_X + RIVER_W - 45:
                self.dir *= -1

        def rect(self):
            return pygame.Rect(self.x, self.y, 40, 40) # Iets kleiner voor eerlijke collision

        def draw(self):
            if self.image:
                screen.blit(self.image, (self.x, self.y))
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
            # We zetten hem in het midden van de rivier
            self.x = WIDTH // 2 - 25
            # We zetten hem onderaan, maar we geven hem een flinke sprong omhoog
            self.y = HEIGHT - 100 
            self.vel_y = -16  # Dit geeft hem een automatische 'super jump' bij de start
            self.on_platform = False
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

    # ===== FALLING LEAF CLASS =====
    class FallingLeaf:
        def __init__(self):
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(-200, -50)
            self.speed_y = random.uniform(2, 4)
            self.speed_x = random.uniform(-1, 1)
            self.rotation = random.randint(0, 360)
            self.rot_speed = random.uniform(-2, 2)

        def update(self):
            self.y += self.speed_y
            self.x += math.sin(pygame.time.get_ticks() * 0.005) + self.speed_x
            self.rotation += self.rot_speed

        def draw(self):
            leaf_surf = pygame.Surface((15, 8), pygame.SRCALPHA)
            pygame.draw.ellipse(leaf_surf, (34, 100, 34), (0, 0, 15, 8))
            rotated_leaf = pygame.transform.rotate(leaf_surf, self.rotation)
            screen.blit(rotated_leaf, (self.x, self.y))

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

    # ===== BLADEREN SETUP =====
    falling_leaves = []
    leaf_timer_start = pygame.time.get_ticks()
    show_leaves = (selected_level_index == 0)  # alleen natuur level

    pause_rect = pygame.Rect(WIDTH - 140, 40, 120, 35)
    scored_platforms = set ()

    font_big = pygame.font.SysFont("Trebuchet MS", 36, bold=True)
    font_small = pygame.font.SysFont("Trebuchet MS", 18)

    pause_rect = pygame.Rect(WIDTH - 60, 10, 40, 40)


    # RIPPLE EFFECT
    ripples = [[
        random.randint(RIVER_X + 10, RIVER_X + RIVER_W - 40),
        random.randint(0, HEIGHT),
        random.uniform(0.5, 2)
    ] for _ in range(45)]
# Voeg dit toe bij de andere variabelen (onder collect_clovers = [])
    enemies = []
    invincibility_timer = 0  # Om te voorkomen dat je alle levens in 1 klap verliest
    while True:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
    # pauze openen
                if pause_rect.collidepoint(event.pos) and not paused:
                 paused = True

    # pause-menu knoppen
                if paused and pause_buttons:
                   if pause_buttons["continue"].collidepoint(event.pos):
                      paused = False

                   elif pause_buttons["restart"].collidepoint(event.pos):
                     lives, score = MAX_LIVES, 0
                     game_over = False
                     gameover_played = False
                     frog.reset()
                     collect_clovers.clear()
                     paused = False
     
                   elif pause_buttons["quit"].collidepoint(event.pos):
                       return "menu"


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

                # Kans op klavertje
                if random.random() < 0.35:
                    collect_clovers.append(CollectibleClover(p.x + 17, p.y - 22))

                # NIEUW: Kans op enemy vanaf Level 2 (index 1)
                # De kans wordt groter per level
                enemy_chance = 0.1 + (selected_level_index * 0.05)
                if selected_level_index >= 1 and random.random() < enemy_chance:
                    enemies.append(Enemy(RIVER_X + random.randint(0, 200), p.y - 50, selected_level_index))
                
            # Update invincibility timer
            if invincibility_timer > 0:
                invincibility_timer -= 1

            for p in platforms: p.y += SCROLL_SPEED
            for c in collect_clovers: c.y += SCROLL_SPEED
            
            # NIEUW: Update vijanden
            for en in enemies:
                en.update(SCROLL_SPEED)

            # Verwijder vijanden die uit beeld zijn
            enemies = [en for en in enemies if en.y < HEIGHT + 50]
            # (Bestaande code voor platforms en clovers behouden...)

            # NIEUW: Check collision met vijanden
            frog_rect = pygame.Rect(frog.x, frog.y, 50, 50)
            for en in enemies[:]:
                if frog_rect.colliderect(en.rect()) and invincibility_timer == 0:
                    lives -= 1
                    invincibility_timer = 60 # 1 seconde onkwetsbaar (bij 60 FPS)
                    sfx.play("gameover") # Of een ander geluidje
                    if lives <= 0:
                        game_over = True    

            frog_rect = pygame.Rect(frog.x, frog.y, 50, 50)
            for c in collect_clovers[:]:
                if frog_rect.colliderect(c.rect()):
                    collect_clovers.remove(c)
                    score += 5  # NIEUW

            if frog.y > HEIGHT + 50: # Iets meer ruimte geven voor hij dood gaat
                lives -= 1
                if lives > 0:
                    frog.reset() # Hij springt nu van onderen weer het scherm in
                else:
                    game_over = True
                    if not gameover_played:
                        sfx.play("gameover")
                        gameover_played = True
        # ===== BLADEREN LOGICA =====
        current_time = pygame.time.get_ticks()

        # Stop na 1 seconde
        if show_leaves and current_time - leaf_timer_start > 1000:
          show_leaves = False

        # Nieuwe blaadjes maken
        if show_leaves and len(falling_leaves) < 15:
           falling_leaves.append(FallingLeaf())

        # Update bladeren
        for leaf in falling_leaves[:]:
            leaf.update()
            if leaf.y > HEIGHT:
                falling_leaves.remove(leaf)

        # ACHTERGROND (Gebruik gekozen level, anders de standaard rivier)
        if selected_level_img:
            screen.blit(selected_level_img, (0, 0))
        else:
            screen.blit(game_bg_img, (0, 0))

        # RIPPLE (kleur per level)
        ripple_color = LEVEL_WATER.get(selected_level_index, (100, 190, 230))

        for r in ripples:
            r[1] += r[2] + SCROLL_SPEED * 0.3

            if r[1] > HEIGHT + 10:
               r[1] = -10
               r[0] = random.randint(RIVER_X + 10, RIVER_X + RIVER_W - 40)
  
            offset = math.sin(
                pygame.time.get_ticks() * 0.004 + r[1] * 0.15
            ) * 4

            pygame.draw.line(
                screen,
                ripple_color,
                (r[0] + offset, r[1]),
                (r[0] + 30 + offset, r[1]),
                 2
            )


        for p in platforms: p.draw()
        for c in collect_clovers: c.draw()  # NIEUW
        for p in platforms: p.draw()
        for c in collect_clovers: c.draw()
        for en in enemies: en.draw() # NIEUW: Teken de vijanden
        
        # Geef de kikker een knipper effect als hij geraakt is
        if invincibility_timer % 10 < 5:
            frog.draw()
        frog.draw()

        # ===== TEKEN BLADEREN BOVENOP =====
        for leaf in falling_leaves:
            leaf.draw()


        # LIVES linksboven (ongewijzigd)
        for i in range(lives):
            screen.blit(clover_img, (10 + i * 30, 10))

        # SCORE rechtsboven (NIEUW)
        # --- SCORE on green leaf (top-right) ---
        leaf_r = 22
        gap_ui = 10 

        leaf_x = pause_rect.left - gap_ui - leaf_r
        leaf_y = pause_rect.centery

        # shadow
        pygame.draw.circle(screen, (10, 40, 20), (leaf_x + 2, leaf_y + 2), leaf_r)

        # leaf body
        pygame.draw.circle(screen, (70, 170, 90), (leaf_x, leaf_y), leaf_r)
        pygame.draw.circle(screen, (60, 150, 80), (leaf_x - 6, leaf_y - 4), leaf_r - 6)

        # border
        pygame.draw.circle(screen, (255, 255, 255), (leaf_x, leaf_y), leaf_r, 2)

        # score text centered
        score_txt = font_small.render(str(score), True, (255, 255, 255))
        screen.blit(
            score_txt,
            (leaf_x - score_txt.get_width() // 2, leaf_y - score_txt.get_height() // 2)
        )
    
        # PAUSE button 
        pause_w, pause_h = 28, 28
        pause_margin_right = 10
        pause_margin_top = 10

        pause_rect = pygame.Rect(
            WIDTH - pause_w - pause_margin_right,
            pause_margin_top, 
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

# ===== PAUSE MENU =====
        if paused:
            pause_buttons.clear()

            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            box_w, box_h = 300, 230
            box = pygame.Rect(
                WIDTH // 2 - box_w // 2,
                HEIGHT // 2 - box_h // 2,
                box_w,
                box_h
            )

            pygame.draw.rect(screen, (30, 30, 30), box, border_radius=20)
            pygame.draw.rect(screen, (255, 255, 255), box, 3, border_radius=20)

            title = font_big.render("Paused", True, (255, 255, 255))
            screen.blit(
                title,
                (box.centerx - title.get_width() // 2, box.y + 20)
            )

            mouse_pos = pygame.mouse.get_pos()

            button_x = box.centerx - 55  # 110 / 2

            pause_buttons["continue"] = draw_button(
            button_x, box.y + 70, "CONTINUE", mouse_pos
            )
            pause_buttons["restart"] = draw_button(
            button_x, box.y + 125, "RESTART", mouse_pos
            )  
            pause_buttons["quit"] = draw_button(
            button_x, box.y + 180, "QUIT", mouse_pos
            )


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
                f"Highscore: {score}",
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