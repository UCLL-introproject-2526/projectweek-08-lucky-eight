import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lucky Frog Jump 🐸")
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
    pygame.image.load("assets/frog.png").convert_alpha(), (50, 50)
)
lilypad_img = pygame.transform.smoothscale(
    pygame.image.load("assets/lilypad.png").convert_alpha(), (60, 26)
)
bush_img_orig = pygame.image.load("assets/bushes.png").convert_alpha()

# 🍀 klavertje
try:
    clover_img = pygame.transform.smoothscale(
        pygame.image.load("assets/clover.png").convert_alpha(), (26, 26)
    )
except:
    # fallback klavertje (getekend)
    clover_img = pygame.Surface((26,26), pygame.SRCALPHA)
    pygame.draw.circle(clover_img, (0,200,0), (13,7), 6)
    pygame.draw.circle(clover_img, (0,200,0), (7,13), 6)
    pygame.draw.circle(clover_img, (0,200,0), (19,13), 6)
    pygame.draw.circle(clover_img, (0,200,0), (13,19), 6)

# =====================
# PLATFORM
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

        # wrap zoals Doodle Jump
        if self.x < RIVER_X - 30:
            self.x = RIVER_X + RIVER_W - 20
        if self.x > RIVER_X + RIVER_W - 20:
            self.x = RIVER_X - 30

    def update(self, platforms):
        global SCROLL_SPEED

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
# ACHTERGROND (ONGEWIJZIGD)
# =====================
def draw_background(bridge_y, ripple_offset, bushes):
    screen.fill((34,139,34))

    pygame.draw.rect(screen, (60,160,210), (RIVER_X, 0, RIVER_W, HEIGHT))

    for i in range(0, HEIGHT, 35):
        y = (i + ripple_offset) % HEIGHT
        pygame.draw.line(screen, (120,200,230),
                         (RIVER_X+20, y),
                         (RIVER_X+RIVER_W-20, y), 2)

    pygame.draw.rect(screen, (100,70,40), (RIVER_X-8, 0, 8, HEIGHT))
    pygame.draw.rect(screen, (100,70,40), (RIVER_X+RIVER_W, 0, 8, HEIGHT))

    if bridge_y < HEIGHT:
        pygame.draw.rect(screen, (120,80,40), (0, bridge_y, WIDTH, BRIDGE_HEIGHT))

    for bush in bushes:
        screen.blit(bush[0], (bush[1], bush[2]))

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
            pygame.quit(); sys.exit()
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

        # 🌊 in water gevallen
        if frog.y > HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                frog.reset()

    draw_background(bridge_y, ripple_offset, bushes)
    for p in platforms:
        p.draw()
    frog.draw()

    # 🍀 levens tekenen
    for i in range(lives):
        screen.blit(clover_img, (10 + i * 30, 10))

    if game_over:
        txt = font_big.render("GAME OVER", True, (255,255,255))
        sub = font_small.render("Press R to restart", True, (220,220,220))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 40))
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 10))

    pygame.display.flip()