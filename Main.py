import pygame as pg
import random
GREEN = (20, 255, 140)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
HEIGHT, WIDTH = 640, 720
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Snake")

myfont = pg.font.SysFont('verdana', 25)

textsurface = myfont.render("Press any arrow key to start", True, (WHITE))
started = False
has_won = False
moving = False

class Block(pg.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        
        self.image = pg.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        # Draw the player (a rectangle)
        pg.draw.rect(self.image, color, [0, 0, width, height])
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.center = (int(width/2), int(height/2))

batch = pg.sprite.Group()
all_snakes = [Block(GREEN, 50, 50)]
all_locations = [(HEIGHT//2, WIDTH//2)]
batch.add(all_snakes[0])
apple = Block(RED, 15, 15)
apple.rect.x = random.randint(100, WIDTH - 100)
apple.rect.y = random.randint(100, HEIGHT - 100)

apple_group = pg.sprite.Group()
apple_group.add(apple)
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill(BLACK)
    if started == False:
        screen.blit(textsurface,(0,0))
    else:
        batch.update()
        apple_group.update()
        batch.draw(screen)
        apple_group.draw(screen)
    pg.display.update()

    keys = pg.key.get_pressed()
    if has_won == False:
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            moving = "Left"
        elif keys[pg.K_d] or keys[pg.K_RIGHT]:
            moving = "Right"
        elif keys[pg.K_s] or keys[pg.K_DOWN]:
            moving = "Down"
        elif keys[pg.K_w] or keys[pg.K_UP]:
            moving = "Up"
    if moving != False:
        started = True

    distance = 5
    new_x, new_y = all_locations[0]
    if moving == "Up":
        new_y -= distance
    elif moving == "Down":
        new_y += distance
    elif moving == "Right":
        new_x += distance
    elif moving == "Left":
        new_x -= distance
    del(all_locations[len(all_locations) - 1])
    all_locations = [(new_x, new_y)] + all_locations
    for i in range(len(all_locations)):
        all_snakes[i].rect.x = all_locations[i][0]
        all_snakes[i].rect.y = all_locations[i][1]
pg.quit()


