from pico2d import load_image


class Sky_Grass:
    def __init__(self, i):
        self.image = load_image('UI/sky_ground.png')
        if i == 0:
            self.x = -100
            self.y = 330
        elif i == 1:
            self.x = 900
            self.y = 330
        else:
            self.x = 400
            self.y = 530

    def draw(self, player_x, player_y):
        offset_x = player_x - 400
        offset_y = player_y - 120
        self.image.draw(self.x - offset_x, self.y - offset_y)

    def update(self):
        pass

    def get_hitbox(self, player_x, player_y):
        w = 500
        h = 37
        offset_x = player_x - 400
        offset_y = player_y - 120

        floor_L = self.x - offset_x - w / 2
        floor_R = self.x - offset_x + w / 2
        floor_T = self.y - offset_y + h / 2 - 15

        return floor_L, floor_R, floor_T
