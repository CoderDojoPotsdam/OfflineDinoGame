import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()

window_size = [500, 500]

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Diiiiiino")
clock = pygame.time.Clock()
fps = 60

# define constants
start_speed = 150
speed_increase_per_second = 1
jump_height = 600
gravity_up = 1800
gravity_down = 2400
gravity = gravity_up

# component initialization; todo: images
dino = pygame.Rect(50, 10, 30, 40)
ground = pygame.Rect(0, window_size[1] / 2, window_size[0], window_size[1] / 2)
cactus = []
score = 0
# additional task: birds

# for dino gravity+jumping
dino_fall_velocity = 0
is_jumping = True
speed = start_speed

def init_variables():
  global speed
  global is_jumping
  global dino_fall_velocity
  global cactus
  global score
  speed = start_speed
  dino.y = 10
  is_jumping = True
  dino_fall_velocity = 0
  cactus = []
  score = 0


def main_loop():
  init_variables()
  while True:
    # time since last loop in seconds
    delta = clock.tick(fps) / 1000

    handle_input()

    increase_speed_over_time(delta, speed_increase_per_second)
    increase_score(delta)

    remove_offscreen_cactus()
    add_cactus()

    # move cactus and check if they collide with dino
    move_cactus(delta)
    game_over = check_for_cactus_collision()
    # if cactus touches dino, break main loop
    if(game_over):
      break

    # gravity
    move_dino(delta)

    draw_components()

def handle_input():
  global is_jumping
  global dino_fall_velocity
  # check keyboard input and window close signal
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE and not is_jumping:
        is_jumping = True
        dino_fall_velocity = -jump_height

def increase_speed_over_time(delta, increase_per_second):
  global speed
  # increase speed by given amount
  speed += increase_per_second * delta

def increase_score(delta):
  global score
  score += delta * 10

def remove_offscreen_cactus():
  global cactus
  # remove cactus which are out of sight
  cactus = list(filter(lambda c: c.x > -c.width, cactus))

def add_cactus():
  global cactus
  # add cactus if necessary
  if(len(cactus) < 10):
    # get position of last cactus to place new cactus behind it
    last_cactus_pos = ground.width
    if(len(cactus) > 0):
      last_cactus_pos = cactus[-1].x
    # define attributes of new cactus
    cactus_width = 20
    cactus_height = 30
    cactus_x = last_cactus_pos + random.randrange(cactus_width + int(speed), cactus_width + int(5*speed))
    cactus_y = ground.y - cactus_height
    new_cactus = pygame.Rect(cactus_x, cactus_y, cactus_width, cactus_height)
    # add new cactus
    cactus.append(new_cactus)

def move_cactus(delta):
  global speed
  global cactus
  for c in cactus:
    c.x = c.x - speed * delta

def check_for_cactus_collision():
  global cactus
  global dino
  for c in cactus:
    if(dino.colliderect(c)):
      return True
  return False

def move_dino(delta):
  global dino_fall_velocity
  global dino
  global is_jumping
  if(dino_fall_velocity < 0):
    gravity = gravity_up
  else:
    gravity = gravity_down
  dino_fall_velocity += gravity * delta
  dino.y = dino.y + dino_fall_velocity * delta
  if(dino.y > ground.y - dino.height):
    is_jumping = False
    dino.y = ground.y - dino.height
    dino_fall_velocity = 0

def display_score():
  global score
  # use default font with given size
  font = pygame.font.SysFont(None, 24)
  text = font.render(str(int(score)), True, RED)
  #pygame.draw.rect(text, BLACK, text.get_rect(), 1)
  screen.blit(text, ((window_size[0] - text.get_rect().width), 5))

def draw_components():
  # update display and redraw all components
  screen.fill(BLACK)
  pygame.draw.rect(screen, YELLOW, dino)
  pygame.draw.rect(screen, WHITE, ground)
  for c in cactus:
    pygame.draw.rect(screen, GREEN, c)
  display_score()
  pygame.display.update()

def game_over():
  # use default font with given size
  font = pygame.font.SysFont(None, 48)
  text = font.render('Game Over!', True, RED)
  pygame.draw.rect(text, WHITE, text.get_rect(), 1)
  # keep display alive and listen for quit/continue
  while True:
    clock.tick(fps)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          return
    screen.blit(text, ((window_size[0] - text.get_rect().width)/2, 50))
    pygame.display.update()

def main():
  while True:
    main_loop()
    game_over()

if __name__ == "__main__":
  main()
