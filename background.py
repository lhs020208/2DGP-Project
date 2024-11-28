from pico2d import load_image


class BGP:
    def __init__(self):
        self.image = load_image('UI/background.png')
        self.x = 400
        self.y = 400

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass