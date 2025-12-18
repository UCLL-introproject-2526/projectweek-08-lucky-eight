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

    return SoundLibrary (sounds)

class SoundLibrary:
    def __init__(self, sounds_dict: dict[str, pygame.mixer.Sound]):
        self.sounds = sounds_dict
        
    def play(self, sound_id: str):
        snd = self.sounds.get(sound_id)
        if snd is None:
           print(f"[Audio] Missing sound id: {sound_id}")
           return
        snd.play()

    def derive_id(root_dir: str, file_path: str) -> str:
        rel = os.path.relpath(file_path, root_dir) 
        no_ext = os.path.splitext(rel)[0] 
        return no_ext.replace("\\", "/") 
    
    


    def load_sfx():
        sfx_dir = os.path.join(ASSETS_DIR, "sfx")
        
        sounds = {
        "jump": pygame.mixer.Sound(os.path.join(sfx_dir, "jump.wav")),
        "land": pygame.mixer.Sound(os.path.join(sfx_dir, "land.wav")),
        "gameover": pygame.mixer.Sound(os.path.join(sfx_dir, "gameover.wav")),
}

        sounds["jump"].set_volume(0.6)
        sounds["land"].set_volume(0.5)
        sounds["gameover"].set_volume(0.6)

        return sounds
    
    def toggle_music_mute():
        global MUSIC_MUTED
        MUSIC_MUTED = not MUSIC_MUTED
        pygame.mixer.music.set_volume(0 if MUSIC_MUTED else 1)

    def toggle_sfx_mute(sfx_dict):
        global SFX_MUTED
        SFX_MUTED = not SFX_MUTED
        vol = 0 if SFX_MUTED else 1
        for snd in sfx_dict.values():
            snd.set_volume(vol)