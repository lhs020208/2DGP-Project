from pico2d import load_image


class KFM:
    image = None
    state = 'standing'
    def __init__(self):
        self.x = 450
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
        elif self.state == 'heat':
            self.image = load_image('kfm_sheet/kfm_heat.png')
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
