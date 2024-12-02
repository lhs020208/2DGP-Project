from pico2d import load_image, load_music, load_wav
import os

class EFFECT:
    normal_heat_sound = None
    special_heat_sound = None
    dead_sound = None

    def __init__(self):
        if EFFECT.normal_heat_sound is None:
            sound_path = os.path.join(os.path.dirname(__file__), 'UI', 'normal_heat.wav')
            EFFECT.normal_heat_sound = load_wav(sound_path)
            EFFECT.normal_heat_sound.set_volume(32)
        if EFFECT.special_heat_sound is None:
            sound_path = os.path.join(os.path.dirname(__file__), 'UI', 'special_heat.wav')
            EFFECT.special_heat_sound = load_wav(sound_path)
            EFFECT.special_heat_sound.set_volume(32)
        if EFFECT.dead_sound is None:
            sound_path = os.path.join(os.path.dirname(__file__), 'UI', 'dead.wav')
            EFFECT.dead_sound = load_wav(sound_path)
            EFFECT.dead_sound.set_volume(32)

    def draw(self):
        pass

    def update(self):
        pass

    def play_nh_sound(self):
        if EFFECT.normal_heat_sound is not None:
            EFFECT.normal_heat_sound.play()
        else:
            print("Sound not loaded!")

    def play_sh_sound(self):
        if EFFECT.special_heat_sound is not None:
            EFFECT.special_heat_sound.play()
        else:
            print("Sound not loaded!")

    def play_dead_sound(self):
        if EFFECT.dead_sound is not None:
            EFFECT.dead_sound.play()
        else:
            print("Sound not loaded!")