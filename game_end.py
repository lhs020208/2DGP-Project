from pico2d import load_image


class GAME_END:
    def __init__(self):
        self.image = None

    def draw(self):
        if self.image is not None:
            self.image.draw(400, 300)

    def update(self):
        pass

    def change_image(self, num):
        if num == 1:
            self.image =load_image('UI/DIE.png')
        elif num == 2:
            self.image = load_image('UI/WIN.png')
