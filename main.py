import pygame
import random

### these tasks are necessary for a functional dino game:
# 1. move_cactus
# 2. add_cactus
# 3. remove_offscreen_cactus
# 4. collide_cactus

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()

# define constants
START_GAME_SPEED = 150
GAME_SPEED_INCREASE_PER_SECOND = 1
GAME_SCORE_PER_SECOND = 10
JUMP_VELOCITY = 600
GRAVITY_UP = 1800
GRAVITY_DOWN = 2400
CACTUS_SIZE = (20, 30)
DINO_START_POSITION = (50, 10)
DINO_SIZE = (30, 40)

# size of window
window_size = [500, 500]
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Diiiiiino")
clock = pygame.time.Clock()
fps = 60

# component initialization
dino = pygame.Rect(DINO_START_POSITION, DINO_SIZE)
dino_img = pygame.image.load("dino-20.png")  # image is 20*20px
dino_img = pygame.transform.scale(dino_img, DINO_SIZE)
ground = pygame.Rect(0, window_size[1] / 2, window_size[0], window_size[1] / 2)
# (optional) task: create ground image and uncomment the two following lines; changes in draw_components function necessary as well (read comments there)
# ground_img = pygame.image.load("ground.png")
# ground_img = pygame.transform.scale(ground_img, (ground.width, ground.height))
cactus = []
# (optional) task: create cactus image and uncomment the two following lines; changes in draw_components function necessary as well (read comments there)
# cactus_img = pygame.image.load("cactus.png")
# cactus_img = pygame.transform.scale(cactus_img, CACTUS_SIZE)

# (optional, more complex) task: create another array for birds which will spawn in air when at high score

# (optional) task: allow user to enter custom parameters via pythons input() function


def main_loop():
    speed = START_GAME_SPEED
    dino.y = DINO_START_POSITION[1]
    is_jumping = True
    dino_fall_velocity = 0
    score = 0

    while True:
        # time since last loop in seconds
        delta = clock.tick(fps) / 1000

        jump_requested = handle_input()
        if jump_requested and not is_jumping:
            is_jumping = True
            dino_fall_velocity = -JUMP_VELOCITY

        # increase speed over time
        speed += GAME_SPEED_INCREASE_PER_SECOND * delta
        # increase speed over time
        score += GAME_SCORE_PER_SECOND * delta

        remove_offscreen_cactus()
        add_cactus(speed)

        # move cactus and check if they collide with dino
        move_cactus(delta, speed)
        is_game_over = check_for_cactus_collision()
        # if cactus touches dino, break main loop
        if is_game_over:
            break

        # jumping + gravity for dino
        dino_fall_velocity, is_jumping = move_dino(
            delta, dino_fall_velocity, is_jumping
        )

        # draw all changes to screen
        draw_components(score)


def remove_offscreen_cactus():
    # remove cactus which are out of sight
    # task: remove all cactus in the array "cactus" which are out of sight (left the screen on the left side)
    pass


def add_cactus(speed):
    # add cactus if necessary
    if len(cactus) < 10:
        # get position of last cactus to place new cactus behind it
        # hint: you might want to calc position of last cactus
        # last_cactus_pos = ?
        # define attributes of new cactus; hint: use speed and last_cactus_pos as parameters to prevent too narrow placement at high speed
        # task: calculate a random x coordinate (width) for a new cactus; you can use the given last_cactus_pos if it helps and random.randrange(a, b) to get a random integer between a and b
        cactus_x = ground.width / 2
        # task: calculate the right y coordinate (height) for a new cactus (hint: it's for all the same)
        cactus_y = 0
        new_cactus = pygame.Rect((cactus_x, cactus_y), CACTUS_SIZE)
        # add new cactus
        cactus.append(new_cactus)


def move_cactus(delta, speed):
    # task: move cactus from right to left with given speed
    pass


def check_for_cactus_collision():
    # task: return True if the dino collides with a cactus; hint: check for each cactus individually and use .x, .y, .height and .width
    return False


### NO MORE TASKS DOWN HERE ###


def handle_input():
    # check keyboard input and window close signal
    jump_requested = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump_requested = True
    return jump_requested


def move_dino(delta, fall_velocity, is_jumping):
    if fall_velocity < 0:
        gravity = GRAVITY_UP
    else:
        gravity = GRAVITY_DOWN
    fall_velocity += gravity * delta
    dino.y = dino.y + fall_velocity * delta
    if dino.y > ground.y - dino.height:
        is_jumping = False
        dino.y = ground.y - dino.height
        fall_velocity = 0
    return (fall_velocity, is_jumping)


def display_score(score):
    # use default font with given size
    font = pygame.font.SysFont(None, 24)
    text = font.render(str(int(score)), True, RED)
    screen.blit(text, ((window_size[0] - text.get_rect().width), 5))


def draw_components(score):
    # update display and redraw all components
    screen.fill(BLUE)
    # pygame.draw.rect(screen, YELLOW, dino) # uncomment (and comment line below) to get a rectangle instead of dino image
    screen.blit(dino_img, (dino.x, dino.y))
    pygame.draw.rect(screen, WHITE, ground)
    # screen.blit(ground_img, (ground.x, ground.y)) # uncomment (and comment line above) to use image of ground instead of the reactangle
    for c in cactus:
        pygame.draw.rect(screen, GREEN, c)
        # screen.blit(cactus_img, (c.x, c.y)) # uncomment (and comment line above) to use cactus image
    display_score(score)
    pygame.display.update()


def game_over():
    # use default font with given size
    font = pygame.font.SysFont(None, 48)
    text = font.render("Game Over!", True, RED)
    pygame.draw.rect(text, WHITE, text.get_rect(), 2)
    # keep display alive and listen for quit/continue
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        screen.blit(text, ((window_size[0] - text.get_rect().width) / 2, 50))
        pygame.display.update()


def main():
    while True:
        main_loop()
        game_over()


if __name__ == "__main__":
    main()
