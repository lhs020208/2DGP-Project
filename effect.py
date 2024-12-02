from pico2d import load_image, load_music, load_wav
import os

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class EFFECT:
    normal_heat_sound = None
    special_heat_sound = None
    dead_sound = None
    image = None
    state = None

    def __init__(self):
        if self.normal_heat_sound is None:
            sound_path = os.path.join(os.path.dirname(__file__), 'UI', 'normal_heat.wav')
            self.normal_heat_sound = load_wav(sound_path)
            self.normal_heat_sound.set_volume(32)
        if self.special_heat_sound is None:
            sound_path = os.path.join(os.path.dirname(__file__), 'UI', 'special_heat.wav')
            self.special_heat_sound = load_wav(sound_path)
            self.special_heat_sound.set_volume(32)
        if self.dead_sound is None:
            sound_path = os.path.join(os.path.dirname(__file__), 'UI', 'dead.wav')
            self.dead_sound = load_wav(sound_path)
            self.dead_sound.set_volume(32)
        self.frame_step = 0
        self.framex = 0
        self.framey = 0
        self.x, self.y = 0,0

    def draw(self, player_x, player_y):
        offset_x = player_x - 400
        offset_y = player_y - 200

        if self.image is None:
            pass
        elif self.state == 'nh':
            self.image.clip_draw(self.framex * 110, self.framey * 110, 110, 110, self.x, self.y)
        elif self.state == 'sh':
            self.image.clip_draw(self.framex * 144, self.framey * 144, 144, 144, self.x, self.y)
        elif self.state == 'die':
            self.image.clip_draw(self.framex * 118, self.framey * 118, 118, 118, self.x - offset_x, 50 - offset_y, 300, 600)

    def update(self, frame_time):
        if self.image is None:
            pass
        elif self.state == 'nh':
            self.framex, self.framey = self.find_frame_position(int(self.frame_step), 4, 2, 8)
            self.frame_step = (self.frame_step + FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time)
            if int(self.frame_step) == 8:
                self.frame_step = 0
                self.framex = 0
                self.framey = 0
                self.image = None
        elif self.state == 'sh':
            self.framex, self.framey = self.find_frame_position(int(self.frame_step), 6, 2, 12)
            self.frame_step = (self.frame_step + FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time)
            if int(self.frame_step) == 12:
                self.frame_step = 0
                self.framex = 0
                self.framey = 0
                self.image = None
        elif self.state == 'die':
            self.framex, self.framey = self.find_frame_position(int(self.frame_step), 6, 3, 17)
            self.frame_step = (self.frame_step + FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time)
            if int(self.frame_step) == 17:
                self.frame_step = 0
                self.framex = 0
                self.framey = 0
                self.image = None

    def play_nh_sound(self):
        if self.normal_heat_sound is not None:
            self.normal_heat_sound.play()
        else:
            print("Sound not loaded!")

    def play_sh_sound(self):
        if self.special_heat_sound is not None:
            self.special_heat_sound.play()
        else:
            print("Sound not loaded!")

    def play_dead_sound(self):
        if self.dead_sound is not None:
            self.dead_sound.play()
        else:
            print("Sound not loaded!")

    def set_image(self, state, L,T,R,B):
        if state == 'nh':
            self.image = load_image('UI/effect_sheet/normal_attack.png')
            self.state = 'nh'
        elif state == 'sh':
            self.image = load_image('UI/effect_sheet/special_attack.png')
            self.state = 'sh'
        elif state == 'die':
            self.image = load_image('UI/effect_sheet/die.png')
            self.state = 'die'
        self.x = (L + R) / 2
        self.y = (T + B) / 2
        self.frame_step = 0

    def find_frame_position(self, frame_step, w, h, max_frame):
        frame_index = frame_step

        self.framex = frame_index % w
        self.framey = frame_index // w

        total_rows = (max_frame + w - 1) // w  # Total rows in the sheet
        self.framey = total_rows - 1 - self.framey

        return self.framex, self.framey