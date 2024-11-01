from pico2d import load_image


class KFM:
    image = None
    state = 'standing'
    def __init__(self):
        self.x = 450
        self.y = 125
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
            self.image = load_image('kfm_sheet/kfm_stand.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 6, 1, 6)
            self.frame_step += 1
            if self.frame_step == 6:
                self.frame_step = 0
        elif self.state == 'walk':
            self.image = load_image('kfm_sheet/kfm_walk.png')
            self.framex,self.framey = self.find_frame_position(self.frame_step,4,2,8 )
            self.frame_step += 1
            if self.frame_step == 8:
                self.frame_step = 0
        elif self.state == 'run':
            self.image = load_image('kfm_sheet/kfm_run.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 6, 1, 6)
            self.frame_step += 1
            if self.frame_step == 6:
                self.frame_step = 0
        elif self.state == 'jump':
            self.image = load_image('kfm_sheet/kfm_jump.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 5, 1, 5)
            self.frame_step += 1
            if self.frame_step == 5:
                self.frame_step = 4
        elif self.state == 'double jump':
            self.image = load_image('kfm_sheet/kfm_jump.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 5, 1, 5)
            self.frame_step += 1
            if self.frame_step == 5:
                self.frame_step = 4
        elif self.state == 'normal_attack':
            self.image = load_image('kfm_sheet/kfm_normal_attack.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 6, 1, 6)
            self.frame_step += 1
            if self.frame_step == 6:
                self.frame_step = 0
                self.framex = 0
                self.framey = 0
                self.state = 'standing'
        elif self.state == 'special_attack':
            self.image = load_image('kfm_sheet/kfm_special_attack.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 6, 1, 6)
            self.frame_step += 1
            if self.frame_step == 6:
                self.frame_step = 0
                self.framex = 0
                self.framey = 0
                self.state = 'standing'
        elif self.state == 'hit':
            self.image = load_image('kfm_sheet/kfm_hit.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 5, 1, 5)
            self.frame_step += 1
            if self.frame_step == 5:
                self.frame_step = 0
                self.framex = 0
                self.framey = 0
                self.state = 'standing'
        elif self.state == 'thrown':
            self.image = load_image('kfm_sheet/kfm_thrown.png')
            self.framex, self.framey = self.find_frame_position(self.frame_step, 5, 1, 5)
            self.frame_step += 1
            if self.frame_step == 5:
                self.frame_step = 3


    def draw(self, player_x, player_y):
        offset_x = player_x - 400
        offset_y = player_y - 120
        if self.direct == 1:
            self.image.clip_draw(self.framex * 140, self.framey * 140, 140, 140, self.x- offset_x, self.y- offset_y,150, 150)
        else:
            self.image.clip_composite_draw(self.framex * 140, self.framey * 140, 140, 140, 0, 'h', self.x- offset_x, self.y- offset_y, 150, 150)

    def get_normal_attack_hitbox(self, player_x, player_y):
        offset_x = player_x - 400
        offset_y = player_y - 120
        pos_x = self.x - offset_x
        pos_y = self.y - offset_y
        if self.state == 'normal_attack' and self.frame_step in [3]:

            kfm_box = 140
            kfm_w = 95
            kfm_left = pos_x - kfm_w / 2
            kfm_right = pos_x + kfm_w / 2
            kfm_bottom = pos_y - kfm_box / 2

            if self.direct == 1:
                ENA_left = kfm_left
                ENA_right = kfm_left + 94
                ENA_top = kfm_bottom + 61
                ENA_bottom = kfm_bottom + 88
            else:
                ENA_left = kfm_right
                ENA_right = kfm_right - 94
                ENA_top = kfm_bottom + 61
                ENA_bottom = kfm_bottom + 88

            return 1, ENA_left, ENA_right, ENA_top, ENA_bottom # 공격 여부, L, R, T, B
        else:
            return 0,0,0,0,0

    def get_special_attack_hitbox(self, player_x, player_y):
        offset_x = player_x - 400
        offset_y = player_y - 120
        pos_x = self.x - offset_x
        pos_y = self.y - offset_y
        if self.state == 'special_attack' and self.frame_step in [2, 3]:

            kfm_box = 140
            kfm_w = 81
            kfm_left = pos_x - kfm_w / 2
            kfm_right = pos_x + kfm_w / 2
            kfm_bottom = pos_y - kfm_box / 2

            if self.direct == 1:
                ENA_left = kfm_left + 50
                ENA_right = kfm_left + 109
                ENA_top = kfm_bottom + 45
                ENA_bottom = kfm_bottom + 64
            else:
                ENA_left = kfm_right - 50
                ENA_right = kfm_right - 109
                ENA_top = kfm_bottom + 45
                ENA_bottom = kfm_bottom + 64

            return 1, ENA_left, ENA_right, ENA_top, ENA_bottom # 공격 여부, L, R, T, B
        else:
            return 0,0,0,0,0