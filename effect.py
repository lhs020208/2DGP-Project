from pico2d import load_image, load_music, load_wav
import os

class EFFECT:
    normal_heat = None
    special_heat = None

    def __init__(self):
        if EFFECT.normal_heat is None:
            sound_path = os.path.join(os.path.dirname(__file__), 'UI', 'normal_heat.wav')
            EFFECT.normal_heat = load_wav(sound_path)
            EFFECT.normal_heat.set_volume(32)
        if EFFECT.special_heat is None:
            sound_path = os.path.join(os.path.dirname(__file__), 'UI', 'special_heat.wav')
            EFFECT.special_heat = load_wav(sound_path)
            EFFECT.special_heat.set_volume(32)

    def draw(self):
        pass

    def update(self):
        pass

    def play_nh_sound(self):
        if EFFECT.normal_heat is not None:
            EFFECT.normal_heat.play()
        else:
            print("Sound not loaded!")

    def play_sh_sound(self):
        if EFFECT.special_heat is not None:
            EFFECT.special_heat.play()
        else:
            print("Sound not loaded!")