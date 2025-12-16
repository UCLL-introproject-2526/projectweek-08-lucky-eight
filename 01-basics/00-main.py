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
selected_frog = None

# ================= FONTS =================
pixel_font = pygame.font.SysFont("Trebuchet MS", 38, bold=True)
button_font = pygame.font.SysFont("Trebuchet MS", 20, bold=True)

# ================= MENU BG =================
menu_bg = pygame.transform.scale(
    pygame.image.load("assets/lucky jump menu.png").convert(),
    (WIDTH, HEIGHT)
)

# ================= BUTTON =================
def draw_button(x, y, label, mouse_pos):
    rect = pygame.Rect(x, y, 110, 45)
    hover = rect.collidepoint(mouse_pos)
    color = (40,100,60) if not hover else (60,150,80)
    pygame.draw.rect(screen, (20,50,30), (x+3,y+3,110,45), border_radius=10)
    pygame.draw.rect(screen, color, rect, border_radius=15)
    txt = button_font.render(label, True, (255,255,255))
    screen.blit(txt, txt.get_rect(center=rect.center))
    return rect

# ================= MENU =================
def menu():
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(menu_bg, (0,0))

        start = pygame.Rect(WIDTH//2-55,380,110,45)
        select = pygame.Rect(WIDTH//2-55,440,110,45)
        quitb = pygame.Rect(WIDTH//2-55,500,110,45)

        draw_button(start.x,start.y,"START",mouse_pos)
        draw_button(select.x,select.y,"SELECT",mouse_pos)
        draw_button(quitb.x,quitb.y,"QUIT",mouse_pos)

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
# ================= AVATAR (JOUW CODE) ====================
# =========================================================

random.seed(42)

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

frog_colors = [(0,0,0),(120,0,0),(0,0,120),(120,120,0),(120,0,120)]
frogs=[]
for c in frog_colors:
    f=frog_orig.copy()
    tint=pygame.Surface(f.get_size(),pygame.SRCALPHA); tint.fill((*c,0))
    f.blit(tint,(0,0),special_flags=pygame.BLEND_RGBA_ADD)
    frogs.append(f)

total_w=len(frogs)*115
start_x=(WIDTH-total_w)//2+10
positions=[(start_x+i*115,260) for i in range(len(frogs))]
jump_offsets=[0]*5
jump_frames=[0]*5

# ================= AVATAR =================
def avatar():
    global selected_frog
    while True:
        mouse_pos = pygame.mouse.get_pos()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if pygame.Rect(50,560,110,45).collidepoint(e.pos):
                    return "menu"
                if pygame.Rect(WIDTH-160,560,110,45).collidepoint(e.pos):
                    return "game"

                for i,(x,y) in enumerate(positions):
                    if pygame.Rect(x,y,85,85).collidepoint(e.pos):
                        selected_frog = i

        draw_river_environment()
        draw_balanced_title("Select your frog", 55)

        for i,frog in enumerate(frogs):
            x,y=positions[i]
            rect=pygame.Rect(x,y,85,85)

            if rect.collidepoint(mouse_pos) and jump_frames[i]==0:
                jump_frames[i]=10
            if jump_frames[i]>0:
                jump_offsets[i]=-40*math.sin(math.pi*(10-jump_frames[i])/10)
                jump_frames[i]-=1
            else:
                jump_offsets[i]=0

            screen.blit(lilypad_img,(x,y+60))
            screen.blit(frog,(x,y+jump_offsets[i]))

        draw_button(50,560,"BACK",mouse_pos)
        draw_button(WIDTH-160,560,"NEXT",mouse_pos)

        pygame.display.flip()
        clock.tick(60)

# ================= GAME =================
def game():
    while True:
        screen.fill((0,0,0))
        frog_img=frogs[selected_frog] if selected_frog is not None else frogs[0]
        screen.blit(frog_img,(WIDTH//2-42,300))

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE:
                return "menu"

        pygame.display.flip()
        clock.tick(60)

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
