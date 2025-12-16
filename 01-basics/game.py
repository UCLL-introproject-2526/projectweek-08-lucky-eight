import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lucky Jump")
clock = pygame.time.Clock()
FPS = 60

# =====================
# CONSTANTEN
# =====================
RIVER_W = 300                 # bredere rivier
RIVER_X = WIDTH//2 - RIVER_W//2
LOG_SPACING = 110
BRIDGE_HEIGHT = 60
CURRENT_SPEED = 0.8            # stroming

# =====================
# ASSETS
# =====================
try:
    frog_img = pygame.image.load("assets/frog.png").convert_alpha()
    frog_img = pygame.transform.smoothscale(frog_img, (50, 50))
except:
    frog_img = pygame.Surface((50,50), pygame.SRCALPHA)
    pygame.draw.ellipse(frog_img, (50,205,50), (0,0,50,50))

try:
    lilypad_img = pygame.image.load("assets/lilypad.png").convert_alpha()
    lilypad_img = pygame.transform.smoothscale(lilypad_img, (60, 26))
except:
    lilypad_img = pygame.Surface((60,26), pygame.SRCALPHA)
    pygame.draw.ellipse(lilypad_img, (144,238,144), (0,0,60,26))

try:
    bush_img_orig = pygame.image.load("assets/bushes.png").convert_alpha()
except:
    bush_img_orig = pygame.Surface((50,50), pygame.SRCALPHA)
    pygame.draw.circle(bush_img_orig, (0,100,0), (25,25), 25)

# =====================
# LILYPADS
# =====================
class Log:
    def __init__(self, y):
        self.x = RIVER_X + random.randint(10, RIVER_W - 70)
        self.y = y
        self.speed = random.choice([2, 3])

    def update(self, logs):
        self.y += self.speed + CURRENT_SPEED
        if self.y > HEIGHT + 50:
            highest = min(l.y for l in logs)
            self.y = highest - LOG_SPACING
            self.x = RIVER_X + random.randint(10, RIVER_W - 70)

    def draw(self):
        screen.blit(lilypad_img, (self.x, self.y))

    def rect(self):
        return pygame.Rect(self.x, self.y, 60, 26)

# =====================
# KIKKER
# =====================
class Frog:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WIDTH//2 - 25
        self.y = HEIGHT - BRIDGE_HEIGHT - 50
        self.vel_y = 0
        self.on_log = None
        self.started = False

    def jump(self):
        if not self.started:
            self.started = True
        self.vel_y = -14
        self.on_log = None

    def update(self, logs):
        self.vel_y += 0.6
        self.y += self.vel_y

        self.on_log = None
        for log in logs:
            if pygame.Rect(self.x, self.y, 50, 50).colliderect(log.rect()):
                self.on_log = log
                self.y = log.y - 38
                self.vel_y = 0

        # meegaan met stroming
        if self.started and self.on_log:
            self.y += self.on_log.speed + CURRENT_SPEED

        # dood in water
        if self.started:
            if RIVER_X < self.x < RIVER_X + RIVER_W:
                if self.on_log is None:
                    self.reset()

        # blijf op brug voor start
        if not self.started:
            self.y = HEIGHT - BRIDGE_HEIGHT - 50
            self.vel_y = 0

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= 5
        if keys[pygame.K_RIGHT]:
            self.x += 5
        self.x = max(0, min(WIDTH-50, self.x))

    def draw(self):
        screen.blit(frog_img, (self.x, self.y))

# =====================
# ACHTERGROND + DETAILS
# =====================
def draw_background(bridge_y, ripple_offset, bushes):
    screen.fill((34,139,34))

    # rivier
    pygame.draw.rect(screen, (60,160,210), (RIVER_X, 0, RIVER_W, HEIGHT))

    # water stroming (rimpels)
    for i in range(0, HEIGHT, 35):
        y = (i + ripple_offset) % HEIGHT
        pygame.draw.line(screen, (120,200,230),
                         (RIVER_X+20, y),
                         (RIVER_X+RIVER_W-20, y), 2)

    # oevers
    pygame.draw.rect(screen, (100,70,40), (RIVER_X-8, 0, 8, HEIGHT))
    pygame.draw.rect(screen, (100,70,40), (RIVER_X+RIVER_W, 0, 8, HEIGHT))

    # brug (met details)
    if bridge_y < HEIGHT:
        pygame.draw.rect(screen, (120,80,40), (0, bridge_y, WIDTH, BRIDGE_HEIGHT))
        for x in range(0, WIDTH, 40):
            pygame.draw.rect(screen, (100,65,35), (x, bridge_y+5, 35, BRIDGE_HEIGHT-10))
        for x in range(0, WIDTH, 80):
            pygame.draw.rect(screen, (70,45,25), (x+10, bridge_y+BRIDGE_HEIGHT-8, 12, 12))

    # struiken langs rivier
    for bush in bushes:
        screen.blit(bush[0], (bush[1], bush[2]))

# =====================
# SETUP
# =====================
frog = Frog()
logs = []
bridge_y = HEIGHT - BRIDGE_HEIGHT
ripple_offset = 0

start_y = bridge_y + 40
for i in range(6):
    logs.append(Log(start_y - i * LOG_SPACING))

# struiken genereren (meer, gestructureerd langs oevers, niet in water)
bushes = []
for i in range(15):
    scale = random.randint(40,60)
    bush_img = pygame.transform.smoothscale(bush_img_orig, (scale, scale))
    # linker oever
    x = RIVER_X - 60 + random.randint(-10,10)
    y = random.randint(0, HEIGHT-50)
    bushes.append((bush_img, x, y))
    # rechter oever
    x = RIVER_X + RIVER_W + 10 + random.randint(-10,10)
    y = random.randint(0, HEIGHT-50)
    bushes.append((bush_img, x, y))

# =====================
# GAME LOOP
# =====================
running = True
while running:
    clock.tick(FPS)
    ripple_offset += CURRENT_SPEED * 3

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                frog.jump()

    keys = pygame.key.get_pressed()
    frog.move(keys)

    for log in logs:
        log.update(logs)

    frog.update(logs)

    # brug drijft weg
    if frog.started:
        bridge_y += CURRENT_SPEED + 1

    draw_background(bridge_y, ripple_offset, bushes)

    for log in logs:
        log.draw()
    frog.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
