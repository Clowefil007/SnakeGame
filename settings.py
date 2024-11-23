
# GAME
# screen
WIDTH = 1300
HEIGHT = 750
BAR = HEIGHT//9
FPS = 60

COLORS = {'red': (255, 0, 0),
          'dark_red': (51, 0, 0),
          'green': (0, 255, 0),
          'white': (255, 255, 255),
          'black': (0, 0, 0),
          'violet': (57, 115, 172),
          'shadow': (102, 102, 153),
          'dark_green': (0, 102, 0),
          'light_blue': (230, 230, 255),
          'orange': (255, 153, 0),
          'yellow': (255, 255, 102),
          'pink': (255, 0, 255)}

# SNAKE
VELOCITY = 4
BLOCK_SIZE = 20
SPAWN2 = [4*BLOCK_SIZE, HEIGHT - 4*BLOCK_SIZE]
SPAWN1 = [WIDTH - 4*BLOCK_SIZE, HEIGHT - 4*BLOCK_SIZE]
MAX_LEN_TAIL = 10
GROW = 20
MINIMUM_VELOCITY = 4
VELOCITY_DECREASE = 0.2

# APPLE
APPLE_N = 4
APPLE_SIZE = 50

BORDER_COLLISION = False
TIME_DEATH = FPS * 10

# BONUS
BONUS = True
# seconds
TIME_BONUS = FPS * 7
# when get score in apples
WHEN = 5
# harder version
HARD = False
