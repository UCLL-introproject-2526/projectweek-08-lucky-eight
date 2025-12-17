import pygame
import os

# ================= MUSIC =================
BASE_DIR = os.path.dirname(__file__) 
ASSETS_DIR = os.path.join(BASE_DIR, "assets") 

def init_music():
    music_path = os.path.join(ASSETS_DIR, "music", "bg.mp3")
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)

def toggle_music():
    if pygame.mixer.music.get_busy():
       pygame.mixer.music.pause()
    else:
       pygame.mixer.music.unpause()

def volume_up():
    vol = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(min(vol + 0.1, 1.0))

def volume_down():
    vol = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(max(vol - 0.1, 0.0))


# ================= SFX =================
def load_sfx():
    sfx_path = os.path.join(ASSETS_DIR, "sfx")
    
    sounds = {
    "jump": pygame.mixer.Sound(os.path.join(sfx_path, "jump.wav")),
    "land": pygame.mixer.Sound(os.path.join(sfx_path, "land.wav")),
    "gameover": pygame.mixer.Sound(os.path.join(sfx_path, "gameover.wav")),
    }

    sounds["jump"].set_volume(0.5)
    sounds["land"].set_volume(0.5)
    sounds["gameover"].set_volume(0.6)

    return sounds