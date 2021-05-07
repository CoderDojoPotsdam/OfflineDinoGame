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
speed = 80
speed_increase_per_second = 1
jump_height = 600
gravity = 2000

# component initialization
dino = pygame.Rect(50, 10, 40, 60)
ground = pygame.Rect(0, window_size[1] / 2, window_size[0], window_size[1] / 2)
cactus = []

# for dino gravity+jumping
dino_velocity_y = 0
is_jumping = True
while True:
  # time since last loop in seconds
  delta = clock.tick(fps) / 1000

  # check keyboard input and window close signal
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE and not is_jumping:
        is_jumping = True
        dino_velocity_y = -jump_height

  # increase speed by set amount
  speed += speed_increase_per_second * delta

  # remove cactus which are out of sight
  cactus = list(filter(lambda c: c.x > -c.width, cactus))

  # add cactus if necessary
  if(len(cactus) < 10):
    # get position of last cactus to place new cactus behind it
    last_cactus_pos = ground.width
    if(len(cactus) > 0):
      last_cactus_pos = cactus[-1].x
    # define attributes of new cactus
    cactus_width = 20
    cactus_height = 40
    cactus_x = ground.width + random.randrange(1, int(speed)) * cactus_width
    cactus_y = ground.y - cactus_height
    new_cactus = pygame.Rect(cactus_x, cactus_y, cactus_width, cactus_height)
    # add new cactus
    cactus.append(new_cactus)

  # move cactus and check if they collide with dino
  game_over = False
  for c in cactus:
    c.x = c.x - speed * delta
    if(dino.colliderect(c)):
      game_over = True
  # if cactus touches dino, break main loop
  if(game_over):
    break

  # gravity
  dino_velocity_y += gravity * delta
  dino.y = dino.y + dino_velocity_y * delta
  if(dino.y > ground.y - dino.height):
    is_jumping = False
    dino.y = ground.y - dino.height
    dino_velocity_y = 0

  # update display and redraw all components
  screen.fill(BLACK)
  pygame.draw.rect(screen, YELLOW, dino)
  pygame.draw.rect(screen, WHITE, ground)
  for c in cactus:
    pygame.draw.rect(screen, GREEN, c)
  pygame.display.update()

# use default font with given size
font = pygame.font.SysFont(None, 48)
text = font.render('Game Over!', True, RED)
pygame.draw.rect(text, WHITE, text.get_rect(), 1)
# keep display alive
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
  screen.blit(text, ((window_size[0] - text.get_rect().width)/2, 50))
  pygame.display.update()
