import pygame
import random
import math
import sys
import audio

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
selected_frog_index = None

# ================= FONTS =================
try:
    pixel_font = pygame.font.SysFont("Trebuchet MS", 38, bold=True)
except:
    pixel_font = pygame.font.SysFont("Arial", 38, bold=True)
button_font = pygame.font.SysFont("Trebuchet MS", 20, bold=True)

# ================= ASSETS =================
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
                    return "game"
                if quitb.collidepoint(e.pos):
                    pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(60)

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
                    if selected_frog_index is not None: return "game"
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
        def rect(self):
            return pygame.Rect(self.x, self.y, 60, 26)
        def draw(self):
            screen.blit(lilypad_img_game, (self.x, self.y))

    # NIEUW: collectible klavertje (gebruikt zelfde groene sprite)
    class CollectibleClover:
        def __init__(self, x, y):
            self.x, self.y = x, y
        def rect(self):
            return pygame.Rect(self.x, self.y, 26, 26)
        def draw(self):
            screen.blit(clover_img, (self.x, self.y))

    class Frog:
        def __init__(self):
            self.reset()
        def reset(self):
            self.x = WIDTH // 2 - 25
            self.y = HEIGHT - 140
            self.vel_y = JUMP_POWER
        def move(self, keys):
            if keys[pygame.K_LEFT]: self.x -= MOVE_SPEED
            if keys[pygame.K_RIGHT]: self.x += MOVE_SPEED
            if self.x < RIVER_X - 30: self.x = RIVER_X + RIVER_W - 20
            if self.x > RIVER_X + RIVER_W - 20: self.x = RIVER_X - 30
        def update(self, platforms):
            nonlocal SCROLL_SPEED
            self.vel_y += GRAVITY
            self.y += self.vel_y
            frog_rect = pygame.Rect(self.x, self.y, 50, 50)
            if self.vel_y > 0:
                for p in platforms:
                    if frog_rect.colliderect(p.rect()) and self.y + 50 <= p.y + 15:
                        self.y = p.y - 50
                        self.vel_y = JUMP_POWER
                        sfx["land"].play()
                        sfx["jump"].play()
                        break
            if self.y < SCROLL_THRESHOLD:
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                lives, game_over, score = MAX_LIVES, False, 0
                gameover_played = False
                frog.reset()
                collect_clovers.clear()

        if not game_over:
            frog.move(pygame.key.get_pressed())
            frog.update(platforms)

            for p in platforms: p.y += SCROLL_SPEED
            for c in collect_clovers: c.y += SCROLL_SPEED  # NIEUW

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
                    score += 1  # NIEUW

            if frog.y > HEIGHT:
                lives -= 1
                if lives <= 0:
                    game_over = True
                if not gameover_played:
                    sfx["gameover"].play()
                    gameover_played = True
                else:
                    frog.reset()

        # ACHTERGROND
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

        draw_bottom_bridge()

        if game_over:
            txt = font_big.render("GAME OVER", True, (255, 255, 255))
            sub = font_small.render("Press R to restart", True, (220, 220, 220))
            screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.flip()


# ================= MAIN =================
def main():
    state="menu"
    play_music()
    while True:
        if state=="menu": state=menu()
        elif state=="avatar": state=avatar()
        elif state=="game": state=game()

main()