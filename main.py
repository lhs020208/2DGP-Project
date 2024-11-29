from pico2d import *
import time

import game_engine

open_canvas()
game_engine.reset_world()

current_time = time.time()

while game_engine.running:
    game_engine.handle_events()
    if game_engine.start:
        game_engine.update_world()
        game_engine.render_world()
    else:
        clear_canvas()
        game_engine.loading.draw(400,300)
        update_canvas()
    delay(0.03)
    game_engine.frame_time = time.time() - current_time
    game_engine.frame_rate = 1.0 / game_engine.frame_time
    current_time += game_engine.frame_time

close_canvas()