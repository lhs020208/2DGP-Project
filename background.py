from pico2d import load_image, load_music


class BGP:
    def __init__(self):
        self.image = load_image('UI/background.png')
        self.x = 400
        self.y = 400
        self.bgm = load_music('UI/BGM.mp3')
        self.bgm.set_volume(16)
        self.bgm.repeat_play()

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass

