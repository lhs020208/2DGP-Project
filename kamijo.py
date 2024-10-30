from pico2d import load_image

class Kamijo:
    image = None
    state = 'standing'
    def __init__(self):
        self.x = 400
        self.y = 120
        self.frame_step = 0
        self.framex = 0
        self.framey = 0
        self.direct = 1

    def find_frame_position(self, frame_step, w, h, max_frame):
        frame_index = frame_step

        self.framex = frame_index % w
        self.framey = frame_index // w

        total_rows = (max_frame + w - 1) // w  # Total rows in the sheet
        self.framey = total_rows - 1 - self.framey

        return self.framex, self.framey

    def update(self):
        if self.state == 'standing':
            self.image = load_image('kamijo_sheet/kamijo_stand.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 6, 1, 6)
            self.frame_step += 1
            if self.frame_step == 6:
                self.frame_step = 0
        elif self.state == 'walk':
            self.image = load_image('kamijo_sheet/kamijo_walk.png')
            self.framex,self.framey = self.find_frame_position(self.frame_step,5,2,10 )
            self.frame_step += 1
            if self.frame_step == 10:
                self.frame_step = 0
        elif self.state == 'block':
            self.image = load_image('kamijo_sheet/kamijo_block.png')
            self.framex = 0
            self.framey = 0
        elif self.state == 'run':
            self.image = load_image('kamijo_sheet/kamijo_run.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 5, 3, 13)
            self.frame_step += 1
            if self.frame_step == 13:
                self.frame_step = 0
        elif self.state == 'jump':
            self.image = load_image('kamijo_sheet/kamijo_jump.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 5, 2, 10)
            self.frame_step += 1
            if self.frame_step == 10:
                self.frame_step = 7
        elif self.state == 'double jump':
            self.image = load_image('kamijo_sheet/kamijo_jump.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 5, 2, 10)
            self.frame_step += 1
            if self.frame_step == 10:
                self.frame_step = 7
        elif self.state == 'normal_attack':
            self.image = load_image('kamijo_sheet/kamijo_normal_attack.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 5, 1, 5)
            self.frame_step += 1
            if self.frame_step == 5:
                self.reset_frame()
                self.state = 'standing'

        elif self.state == 'special_attack':
            self.image = load_image('kamijo_sheet/kamijo_special_attack.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 5, 2, 10)
            self.frame_step += 1
            if self.frame_step == 10:
                self.reset_frame()
                self.state = 'standing'
        elif self.state == 'hit':
            self.image = load_image('kamijo_sheet/kamijo_hit.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 3, 1, 3)
            self.frame_step += 1
            if self.frame_step == 3:
                self.reset_frame()
                self.state = 'standing'
        elif self.state == 'thrown':
            self.image = load_image('kamijo_sheet/kamijo_thrown.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 2, 1, 2)
            self.frame_step += 1
            if self.frame_step == 2:
                self.frame_step = 0


    def draw(self):
        if self.direct == 1:
            self.image.clip_draw(self.framex * 140, self.framey * 140, 140, 140, self.x, self.y,150, 150)
        else:
            self.image.clip_composite_draw(self.framex * 140, self.framey * 140, 140, 140, 0, 'h', self.x, self.y, 150, 150)

    def reset_frame(self):
        """플레이어의 프레임 초기화"""
        self.frame_step = 0
        self.framex = 0
        self.framey = 0

    def get_normal_attack_hitbox(self):
        if self.state == 'normal_attack' and self.frame_step in [1, 2, 3]:
            kamijo_box = 140
            kamijo_w = 81
            player_left = self.x - kamijo_w / 2
            player_right = self.x + kamijo_w / 2
            player_bottom = self.y - kamijo_box / 2

            if self.direct == 1:
                PNA_left = player_left + 40
                PNA_right = player_left + 80
                PNA_top = player_bottom + 93
                PNA_bottom = player_bottom + 77
            else:
                PNA_left = player_right - 40
                PNA_right = player_right - 80
                PNA_top = player_bottom + 93
                PNA_bottom = player_bottom + 77

            return 1, PNA_left, PNA_right, PNA_top, PNA_bottom # 공격 여부, L, R, T, B
        else:
            return 0,0,0,0,0

    def get_special_attack_hitbox(self):
        if self.state == 'special_attack' and self.frame_step in [1, 2, 3, 4]:
            kamijo_box = 140
            kamijo_w = 109
            player_left = self.x - kamijo_w / 2
            player_right = self.x + kamijo_w / 2
            player_bottom = self.y - kamijo_box / 2

            if self.direct == 1:
                PSA_left = player_left + 50
                PSA_right = player_left + 109
                PSA_top = player_bottom + 45
                PSA_bottom = player_bottom + 64
            else:
                PSA_left = player_right - 50
                PSA_right = player_right - 109
                PSA_top = player_bottom + 45
                PSA_bottom = player_bottom + 64

            return 1, PSA_left, PSA_right, PSA_top, PSA_bottom # 공격 여부, L, R, T, B
        else:
            return 0,0,0,0,0