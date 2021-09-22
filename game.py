import pathlib
import random
import pyglet

TILE_SIZE = 64

window = pyglet.window.Window()

class State:
    def __init__(self):
        self.snake = [(1, 2), (2, 2)]
        self.food = [(2, 0), (5, 1), (1, 4)]
        self.direction = (1, 0)
        self.width = 10
        self.height = 10
        self.alive = True



    def move(self):
        if not self.alive:
            return


        old_x, old_y = self.snake[-1]
        direction_x, direction_y = self.direction
        new_x = old_x + direction_x
        new_y = old_y + direction_y

        new_x = new_x % self.width
        new_y = new_y % self.height

        new_head = new_x, new_y

        if new_head in self.snake:
            self.alive = False

        self.snake.append(new_head)

        if new_head in self.food:
            self.food.remove(new_head)
            self.add_food()
        else:
            del self.snake[0]

    def add_food(self):
        for i in range(100):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            position = x, y
            if not (position in self.snake or position in self.food):
                self.food.append(position)
                return

state = State()
state.width = window.width // TILE_SIZE
state.height = window.height // TILE_SIZE

green_image = pyglet.image.load("green.png")
apple_image = pyglet.image.load("apple.png")

snake_tiles = {}
snake_tiles_path = pathlib.Path("snake-tiles")
for path in snake_tiles_path.glob("*.png"):
    snake_tiles[path.stem] = pyglet.image.load(path)

def direction(a, b, default):
    if a == 'nic':
        return default
    if b == 'nic':
        return default
    a_x, a_y = a
    b_x, b_y = b
    if a_x == b_x + 1:
        return 'right'
    elif a_x == b_x - 1:
        return 'left'
    elif a_y == b_y + 1:
        return 'top'
    elif a_y == b_y - 1:
        return 'bottom'
    else:
        return default

@window.event
def on_draw():
    window.clear()

    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    for a, b, c in zip(['nic'] + state.snake[:-1],
                       state.snake,
                       state.snake[1:] + ['nic']):
        x, y = b
        begin = direction(a, b, "tail")
        end = direction(c, b, "head")
        if not state.alive and end == "head":
            end = "dead"
        snake_tiles[begin + "-" + end].blit(x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)

    for x, y in state.food:
        apple_image.blit(x * TILE_SIZE, y * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)

@window.event
def on_key_press(symbol, mod):
    if symbol == pyglet.window.key.UP:
        state.direction = (0, 1)
    if symbol == pyglet.window.key.DOWN:
        state.direction = (0, -1)
    if symbol == pyglet.window.key.RIGHT:
        state.direction = (1, 0)
    if symbol == pyglet.window.key.LEFT:
        state.direction = (-1, 0)

def tick(dt):
    state.move()

pyglet.clock.schedule_interval(tick, 1/6)

pyglet.app.run()
