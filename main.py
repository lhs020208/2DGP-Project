from pico2d import *

# 테스트를 위한 임시 변수
global a
global b
a = 400
b = 100

class Grass:
    def __init__(self):
        self.image = load_image('UI/ground.png')
        self.x = 400
        self.y = 30

    def draw(self):
        global a, b
        offset_x = a - 400
        offset_y = b - 100
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
        global a, b
        offset_x = a - 400
        offset_y = b - 100
        self.image.draw(self.x - offset_x, self.y - offset_y)

    def update(self):
        pass

def handle_events():
    global running, a, b
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            a = a - 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            a = a + 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            b = b + 10
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            b = b - 10

def reset_world():
    global running
    global grass
    global sky_grass
    global world

    running = True
    world = []

    grass = Grass()
    world.append(grass)

    sky_grass = [Sky_Grass(i) for i in range(3)]
    world += sky_grass

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
