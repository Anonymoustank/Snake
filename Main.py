import pygame as pg
import random
import time
GREEN = (20, 255, 140)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
HEIGHT, WIDTH = 640, 720
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Snake")
clock = pg.time.Clock()
myfont = pg.font.SysFont('verdana', 25)

loop_delay = 0

textsurface = myfont.render("Press any arrow key to start", True, (WHITE))
started = False
has_won = False
moving = False
dead = False

size = 40

current_time = time.perf_counter()

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
all_snakes = [Block(GREEN, size, size)]
all_snakes[0].rect.x = 50
all_snakes[0].rect.y = 50
all_locations = [(HEIGHT//2, WIDTH//2)]
batch.add(all_snakes[0])
apple = Block(RED, size, size)
apple.rect.x = random.randint(100, WIDTH - 100)
apple.rect.y = random.randint(100, HEIGHT - 100)

apple_group = pg.sprite.Group()
apple_group.add(apple)
running = True

while running:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill(BLACK)
    if started == False:
        text_rect = textsurface.get_rect(center = (WIDTH // 2, HEIGHT // 2))
        screen.blit(textsurface, text_rect)
    elif has_won == False and dead == False:
        batch.update()
        apple_group.update()
        batch.draw(screen)
        apple_group.draw(screen)
    elif dead == True:
        death_screen = myfont.render("You died", True, (WHITE))
        text_rect = death_screen.get_rect(center = (WIDTH // 2, HEIGHT // 2))
        screen.blit(death_screen, text_rect)

    pg.display.update()

    if all_snakes[0].rect.x >= WIDTH or all_snakes[0].rect.x < 0:
        dead = True
    elif all_snakes[0].rect.y >= HEIGHT or all_snakes[0].rect.y < 0:
        dead = True

    for i in range(1, len(all_snakes)):
        if all_snakes[0].rect.colliderect(all_snakes[i]):
            dead = True
            break
            
    for i in all_snakes:
        if i.rect.colliderect(apple):
            apple.rect.x = random.randint(1, (WIDTH // size) - 1) * size
            apple.rect.y = random.randint(1, (HEIGHT // size) - 1) * size
            all_snakes.append(Block(GREEN, size, size))
            batch.add(all_snakes[len(all_snakes) - 1])
            all_snakes[len(all_snakes) - 1].rect.x = -150
            all_snakes[len(all_snakes) - 1].rect.y = 100

    keys = pg.key.get_pressed()
    if has_won == False:
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            if moving != "Right":
                moving = "Left"
        elif keys[pg.K_d] or keys[pg.K_RIGHT]:
            if moving != "Left":
                moving = "Right"
        elif keys[pg.K_s] or keys[pg.K_DOWN]:
            if moving != "Up":
                moving = "Down"
        elif keys[pg.K_w] or keys[pg.K_UP]:
            if moving != "Down":
                moving = "Up"
    if moving != False:
        started = True

    distance = size
    if abs(current_time - time.perf_counter()) >= (1/4) and has_won == False and dead == False:
        new_x, new_y = all_locations[0]
        current_time = time.perf_counter()
        if moving == "Up":
            new_y -= distance
        elif moving == "Down":
            new_y += distance
        elif moving == "Right":
            new_x += distance
        elif moving == "Left":
            new_x -= distance
        if len(all_snakes) == len(all_locations) and loop_delay == 0:
            del(all_locations[len(all_locations) - 1])
        if loop_delay == 0:
            all_locations = [(new_x, new_y)] + all_locations
        else:
            all_locations[0] = (new_x, new_y)
        if loop_delay > 0:
            loop_delay -= 1
            for i in range(len(all_snakes) - 1):
                all_snakes[i].rect.x = int(all_locations[i][0])
                all_snakes[i].rect.y = int(all_locations[i][1])
        else:
            for i in range(len(all_snakes)):
                all_snakes[i].rect.x = int(all_locations[i][0])
                all_snakes[i].rect.y = int(all_locations[i][1])
pg.quit()


