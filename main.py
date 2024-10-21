from pico2d import *

# 테스트를 위한 임시 변수
global Player_x
global Player_y
Player_x = 400
Player_y = 120


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

    def update(self):
        if self.state == 'standing':
            self.image = load_image('kamijo_sheet/kamijo_stand.png')
            self.framex = (self.framex + 1) % 6
        elif self.state == 'walk':
            self.image = load_image('kamijo_sheet/kamijo_walk.png')

            self.framex = (self.framex + 1) % 5
            self.framey = self.frame_step // 5
            self.frame_step += 1
            if self.frame_step == 10:
                self.frame_step = 0


    def draw(self):
        if self.direct == 1:
            self.image.clip_draw(self.framex * 140, self.framey * 140, 140, 140, self.x, self.y,150, 150)
        else:
            self.image.clip_composite_draw(self.framex * 140, self.framey * 140, 140, 140, 0, 'h', self.x, self.y, 150, 150)



class Grass:
    def __init__(self):
        self.image = load_image('UI/ground.png')
        self.x = 400
        self.y = 30

    def draw(self):
        global Player_x, Player_y
        offset_x = Player_x - 400
        offset_y = Player_y - 120
        self.image.draw(self.x - offset_x, self.y - offset_y)

    def update(self):
        pass

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

    def draw(self):
        global Player_x, Player_y
        offset_x = Player_x - 400
        offset_y = Player_y - 120
        self.image.draw(self.x - offset_x, self.y - offset_y)

    def update(self):
        pass

def reset_frame():
    global player

    player.frame_step = 0
    player.framex = 0
    player.framey = 0

def handle_events():
    global running, Player_x, Player_y
    global player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT: #왼쪽키
            reset_frame()
            Player_x = Player_x - 10
            player.state = 'walk'
            player.direct = -1
        if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT: #오른쪽키
            reset_frame()
            Player_x = Player_x + 10
            player.state = 'walk'
            player.direct = 1
        if event.type == SDL_KEYDOWN and event.key == SDLK_UP: #위키
            reset_frame()
            Player_y = Player_y + 10
        if event.type == SDL_KEYDOWN and event.key == SDLK_DOWN: #아래키
            reset_frame()
            Player_y = Player_y - 10

        #ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        if event.type == SDL_KEYUP and event.key == SDLK_LEFT:  # 왼쪽키
            reset_frame()
            player.state = 'standing'
        if event.type == SDL_KEYUP and event.key == SDLK_RIGHT:  # 오른쪽키
            reset_frame()
            player.state = 'standing'

def reset_world():
    global running
    global grass
    global sky_grass
    global player
    global world

    running = True
    world = []

    grass = Grass()
    world.append(grass)

    sky_grass = [Sky_Grass(i) for i in range(3)]
    world += sky_grass

    player = Kamijo()
    world.append(player)

def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()
