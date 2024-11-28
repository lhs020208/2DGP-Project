from pico2d import load_image


class State_bar:
    def __init__(self):
        self.enemy0_sb = load_image('ui/kfm_hp3.png')
        self.enemy1_sb = load_image('ui/kfm_hp3.png')
        self.player_sb = load_image('ui/kamijo_hp3.png')

    def draw(self):
        self.player_sb.draw(100, 52)
        self.enemy0_sb.draw(500, 52)
        self.enemy1_sb.draw(700, 52)

    def update(self):
        pass
