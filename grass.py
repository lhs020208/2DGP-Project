from pico2d import load_image


class Grass:
    def __init__(self):
        self.image = load_image('UI/ground.png')
        self.x = 400
        self.y = 30

    def draw(self, player_x, player_y):
        offset_x = player_x - 400
        offset_y = player_y - 120
        self.image.draw(self.x - offset_x, self.y - offset_y)

    def update(self):
        pass
