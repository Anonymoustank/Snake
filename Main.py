import pyglet
from pyglet.window import key, mouse
HEIGHT, WIDTH = 1280, 720
window = pyglet.window.Window(HEIGHT, WIDTH, "Game", resizable = False)
window.set_mouse_visible(False)

label = pyglet.text.Label('Press an arrow key to begin', font_name='Times New Roman', font_size=36, x=2 * (window.width//3), y=window.height//2, anchor_x='center', anchor_y='center')
started = False
has_won = False
moving = False

batch = pyglet.graphics.Batch()
all_snakes = [pyglet.shapes.Rectangle(HEIGHT//2, WIDTH//2, 50, 50, color=(55, 55, 255), batch=batch)]

all_locations = [all_snakes[0].position]

@window.event
def on_draw():
    window.clear()
    if started == False:
        label.draw()
    else:
        batch.draw()

def refresh(time):
    global all_locations, all_snakes
    distance = 5
    new_x, new_y = all_locations[0]
    if moving == "Up":
        new_y += distance
    elif moving == "Down":
        new_y -= distance
    elif moving == "Right":
        new_x += distance
    elif moving == "Left":
        new_x -= distance
    del(all_locations[len(all_locations) - 1])
    all_locations = [(new_x, new_y)] + all_locations
    for i in range(len(all_locations)):
        all_snakes[i].position = all_locations[i]

@window.event
def on_key_press(symbol, modifiers):
    global started, moving
    started = True
    if has_won == False:
        if symbol == key.A or symbol == key.LEFT:
            moving = "Left"
        elif symbol == key.D or symbol == key.RIGHT:
            moving = "Right"
        elif symbol == key.S or symbol == key.DOWN:
            moving = "Down"
        elif symbol == key.W or symbol == key.UP:
            moving = "Up"

if __name__ == "__main__":
    pyglet.clock.schedule_interval(refresh, 1.0/120.0)
    pyglet.app.run()
