from pico2d import load_image


class State_bar:
    def __init__(self):
        self.enemy0_sb = load_image('ui/kfm_hp3.png')
        self.enemy1_sb = load_image('ui/kfm_hp3.png')
        self.player_sb = load_image('ui/kamijo_hp3.png')
        self.dmg = load_image('ui/dmg.png')

    def draw(self, php, ehp0, ehp1):
        self.player_sb.draw(100, 52)
        self.enemy0_sb.draw(500, 52)
        self.enemy1_sb.draw(700, 52)

        y, x = self.extract_digits(php)
        self.dmg.clip_draw(10 + 98 * x, 10 + 60 * y, 100, 60, 120, 40, 100, 60)
        y, x = self.extract_digits(ehp0)
        self.dmg.clip_draw(10 + 98 * x, 10 + 60 * y, 100, 60, 490, 40, 100, 60)
        y, x = self.extract_digits(ehp1)
        self.dmg.clip_draw(10 + 98 * x, 10 + 60 * y, 100, 60, 690, 40, 100, 60)

    def update(self):
        pass

    def minus_hp(self, object, hp):
        hp -= 1
        if object == 'E0':
            self.enemy0_sb = load_image(f'ui/kfm_hp{hp}.png')

        elif object == 'E1':
            self.enemy1_sb = load_image(f'ui/kfm_hp{hp}.png')

        elif object == 'P':
            self.player_sb = load_image(f'ui/kamijo_hp{hp}.png')
        return hp

    def extract_digits(self, number):

        # 100의 자리 숫자 추출
        hundreds_digit = (number // 100) % 10

        # 10의 자리 숫자 추출
        tens_digit = (number // 10) % 10

        return hundreds_digit, tens_digit