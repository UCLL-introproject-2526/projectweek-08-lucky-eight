import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lucky Frog River 🐸")
clock = pygame.time.Clock()
FPS = 60

# =====================
# CONSTANTEN
# =====================
RIVER_W = 300
RIVER_X = WIDTH // 2 - RIVER_W // 2
LOG_SPACING = 110
BRIDGE_HEIGHT = 60
CURRENT_SPEED = 0.8
GRAVITY = 0.6
JUMP_POWER = -14
MOVE_SPEED = 5

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

try:
    flower_img_orig = pygame.image.load("assets/yellowflower.png").convert_alpha()
except:
    flower_img_orig = pygame.Surface((20,20), pygame.SRCALPHA)
    pygame.draw.circle(flower_img_orig, (255,255,0), (10,10), 10)

# =====================
# LILIEBLAD
# =====================
class Lilypad:
    def __init__(self, y):
        self.x = RIVER_X + random.randint(10, RIVER_W - 70)
        self.y = y
        self.speed = random.choice([1.5, 2.0])

    def update(self):
        self.y += self.speed + CURRENT_SPEED
        if self.y > HEIGHT + 40:
            self.y = -LOG_SPACING
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
        self.x = WIDTH // 2 - 25
        self.y = HEIGHT - BRIDGE_HEIGHT - 50
        self.vel_y = 0
        self.vel_x = 0
        self.on_pad = False
        self.started = False

    def jump(self, direction=0):
        if self.on_pad or not self.started:
            self.vel_y = JUMP_POWER
            self.vel_x = MOVE_SPEED * direction
            self.on_pad = False
            self.started = True

    def update(self, pads):
        # zwaartekracht
        self.vel_y += GRAVITY
        self.y += self.vel_y
        self.x += self.vel_x
        self.on_pad = False

        frog_rect = pygame.Rect(self.x, self.y, 50, 50)

        # collision liliebladen
        for pad in pads:
            pad_rect = pad.rect()
            if frog_rect.colliderect(pad_rect) and self.vel_y > 0:
                if self.y + 50 - self.vel_y <= pad.y + 5:
                    self.y = pad.y - 50
                    self.vel_y = 0
                    self.vel_x = 0
                    self.on_pad = True

        # meegaan met stroming
        if self.on_pad:
            self.y += CURRENT_SPEED

        # dood in water
        if self.started and RIVER_X < self.x < RIVER_X + RIVER_W:
            if not self.on_pad and self.vel_y > 0:
                self.reset()

        # grenzen
        self.x = max(0, min(WIDTH - 50, self.x))
        if not self.started:
            self.y = HEIGHT - BRIDGE_HEIGHT - 50
            self.vel_y = 0
            self.vel_x = 0

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            self.x += MOVE_SPEED
        self.x = max(0, min(WIDTH - 50, self.x))

    def draw(self):
        screen.blit(frog_img, (self.x, self.y))

# =====================
# ACHTERGROND
# =====================
def draw_background(bridge_y, ripple_offset, bushes, flowers):
    screen.fill((34,139,34))

    # rivier
    pygame.draw.rect(screen, (60,160,210), (RIVER_X, 0, RIVER_W, HEIGHT))
    for i in range(0, HEIGHT, 35):
        y = (i + ripple_offset) % HEIGHT
        pygame.draw.line(screen, (120,200,230),
                         (RIVER_X+20, y),
                         (RIVER_X+RIVER_W-20, y), 2)

    # oevers
    pygame.draw.rect(screen, (100,70,40), (RIVER_X-8, 0, 8, HEIGHT))
    pygame.draw.rect(screen, (100,70,40), (RIVER_X+RIVER_W, 0, 8, HEIGHT))

    # brug
    if bridge_y < HEIGHT:
        pygame.draw.rect(screen, (120,80,40), (0, bridge_y, WIDTH, BRIDGE_HEIGHT))
        for x in range(0, WIDTH, 40):
            pygame.draw.rect(screen, (100,65,35), (x, bridge_y+5, 35, BRIDGE_HEIGHT-10))
        for x in range(0, WIDTH, 80):
            pygame.draw.rect(screen, (70,45,25), (x+10, bridge_y+BRIDGE_HEIGHT-8, 12, 12))

    # struiken
    for bush in bushes:
        screen.blit(bush[0], (bush[1], bush[2]))

    # bloemen
    for flower in flowers:
        screen.blit(flower[0], (flower[1], flower[2]))

# =====================
# SETUP
# =====================
frog = Frog()
pads = []
bridge_y = HEIGHT - BRIDGE_HEIGHT
ripple_offset = 0

# liliebladen
start_y = bridge_y + 40
for i in range(6):
    pads.append(Lilypad(start_y - i*LOG_SPACING))

# struiken langs oevers
bushes = []
for i in range(20):
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

# bloemen langs oevers
flowers = []
for i in range(25):
    scale = random.randint(15,25)
    flower_img = pygame.transform.smoothscale(flower_img_orig, (scale, scale))
    x = RIVER_X - 50 + random.randint(-5,5) if i%2==0 else RIVER_X + RIVER_W + 5 + random.randint(-5,5)
    y = random.randint(0, HEIGHT-25)
    flowers.append((flower_img, x, y))

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
                keys = pygame.key.get_pressed()
                direction = 0
                if keys[pygame.K_LEFT]:
                    direction = -1
                elif keys[pygame.K_RIGHT]:
                    direction = 1
                frog.jump(direction)

    keys = pygame.key.get_pressed()
    frog.move(keys)

    for pad in pads:
        pad.update()

    frog.update(pads)

    if frog.started:
        bridge_y += CURRENT_SPEED + 1

    draw_background(bridge_y, ripple_offset, bushes, flowers)

    for pad in pads:
        pad.draw()
    frog.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()
