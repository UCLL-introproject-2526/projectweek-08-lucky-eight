import pygame
import sys
import os

pygame.init()

# ---------------- INSTELLINGEN ----------------
WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lucky Jump")
clock = pygame.time.Clock()

# ---------------- ACHTERGROND ----------------
BG_PATH = os.path.join("assets", "lucky jump menu.png")

if not os.path.exists(BG_PATH):
    print("❌ Afbeelding niet gevonden:", BG_PATH)
    pygame.quit()
    sys.exit()

background = pygame.image.load(BG_PATH).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# ---------------- KLEUREN ----------------
BUTTON_GREEN = (70, 180, 120)
BUTTON_DARK = (40, 140, 90)
WHITE = (255, 255, 255)

# ---------------- FONT ----------------
button_font = pygame.font.Font(None, 42)

# ---------------- KNOP ----------------
def draw_button(text, x, y, w, h, mouse_pos):
    rect = pygame.Rect(x, y, w, h)
    color = BUTTON_DARK if rect.collidepoint(mouse_pos) else BUTTON_GREEN
    pygame.draw.rect(screen, color, rect, border_radius=20)

    label = button_font.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=rect.center))
    return rect

# ---------------- MENU ----------------
def menu():
    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Achtergrond
        screen.blit(background, (0, 0))

        # Donkere overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 70))
        screen.blit(overlay, (0, 0))

        # Knoppen
        start_btn = draw_button("START", 300, 340, 200, 55, mouse_pos)
        avatar_btn = draw_button("SELECT FROG", 300, 410, 200, 55, mouse_pos)
        quit_btn = draw_button("QUIT", 300, 480, 200, 55, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    return "game"
                if avatar_btn.collidepoint(event.pos):
                    return "avatar"
                if quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

# ---------------- AVATAR (PLACEHOLDER) ----------------
def avatar():
    while True:
        screen.fill((0, 0, 0))
        text = button_font.render("Avatar select (ESC = terug)", True, WHITE)
        screen.blit(text, (220, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        pygame.display.flip()
        clock.tick(60)

# ---------------- GAME (PLACEHOLDER) ----------------
def game():
    while True:
        screen.fill((0, 0, 0))
        text = button_font.render("Game start hier (ESC = menu)", True, WHITE)
        screen.blit(text, (230, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        pygame.display.flip()
        clock.tick(60)

# ---------------- MAIN LOOP ----------------
def main():
    state = "menu"
    while True:
        if state == "menu":
            state = menu()
        elif state == "avatar":
            state = avatar()
        elif state == "game":
            state = game()

main()
