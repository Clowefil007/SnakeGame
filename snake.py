import pygame

from settings import BLOCK_SIZE, VELOCITY, MAX_LEN_TAIL, WIDTH, HEIGHT,\
    BORDER_COLLISION, COLORS, TIME_BONUS, WHEN, BONUS, HARD, GROW, MINIMUM_VELOCITY, VELOCITY_DECREASE, BAR, TIME_DEATH
Rect = pygame.Rect
pygame.font.init()


class Snake:
    # BUILT-IN FUNCTION
    def __init__(self, starting_position, color_body, color_head, color_score):
        # general
        self.width = WIDTH
        self.height = HEIGHT
        self.size = BLOCK_SIZE
        self.bar = BAR
        """self.head = starting_position.copy()"""
        self.body = []  # list of [x, y]
        self.max_len_tail = MAX_LEN_TAIL
        self.x_velocity = 0  # lateral movement
        self.y_velocity = 0  # horizontal movement
        self.color_body = color_body
        self.color_head = color_head
        self.color_score = color_score
        self.border_collision = BORDER_COLLISION
        self.body_collision = True
        self.head_collision = True

        # velocity
        self.velocity = VELOCITY
        self.og_velocity = VELOCITY
        self.grow = GROW
        self.minimum_velocity = MINIMUM_VELOCITY
        self.velocity_decrease = VELOCITY_DECREASE

        # creating rect and mask
        self.head = Rect(starting_position, (self.size, self.size))
        self.snake_surface = pygame.Surface((self.size, self.size))
        self.snake_mask = pygame.mask.from_surface(self.snake_surface)

        # score
        self.score = 0
        self.font = pygame.font.Font(None, 100)
        self.text = self.font.render(f'{self.score}', True, self.color_score)

        # bonus
        self.wanna_bonus = BONUS
        self.time_bonus = TIME_BONUS
        self.when = WHEN
        self.add_when = WHEN
        self.killing_bonus = False
        self.hard = HARD

        # reset
        self.og_head = color_head
        self.og_body = color_body
        self.og_position = starting_position
        self.time_death = TIME_DEATH
        self.death = False

        # wall
        self.wall = []

    # UPDATING SCORE
    def update_score(self, n):
        self.score += n
        self.text = self.font.render(f'{self.score}', True, self.color_score)

    # MOVEMENTS (changing velocity/direction)
    def move_up(self):
        if self.y_velocity < + self.velocity:
            self.x_velocity = 0
            self.y_velocity = - self.velocity

    def move_down(self):
        if self.y_velocity > - self.velocity:
            self.x_velocity = 0
            self.y_velocity = self.velocity

    def move_left(self):
        if self.x_velocity < + self.velocity:
            self.x_velocity = - self.velocity
            self.y_velocity = 0

    def move_right(self):
        if self.x_velocity > - self.velocity:
            self.x_velocity = + self.velocity
            self.y_velocity = 0

    # UPDATING COORDINATES
    def move(self):
        head_x = self.head[0] + self.x_velocity
        head_y = self.head[1] + self.y_velocity
        self.head.topleft = (head_x, head_y)

    # UPDATING BODY
    def body_update(self):
        self.body.insert(0, self.head.copy())
        if len(self.body) > self.max_len_tail:
            self.body.pop()

    # GAME-MODE WITH BORDERS
    def border_collision_check(self):
        if self.head[0] <= 0:
            self.zero()
        if self.head[1] <= self.bar:
            self.zero()
        if self.head[0] >= self.width - self.size:
            self.zero()
        if self.head[1] >= self.height - self.size:
            self.zero()

    # GAME-MODE WITHOUT BORDERS
    def none_border(self):
        if self.head[0] < 0:
            self.head[0] = self.width - self.size
        if self.head[1] < self.bar:
            self.head[1] = self.height - self.size
        if self.head[0] > self.width - self.size:
            self.head[0] = 0
        if self.head[1] > self.height - self.size:
            self.head[1] = self.bar

    # CHECKING COLLISION BETWEEN HEADS OF SNAKES
    def head_collision_check(self, snake_in_collision):
        # bonus deactivated
        if self.head_collision:
            if self.head.colliderect(snake_in_collision.head):
                if snake_in_collision.score == self.score:
                    self.zero()
                    snake_in_collision.zero()
                elif snake_in_collision.score > self.score:
                    self.zero()
                else:
                    snake_in_collision.zero()

        # each has his bonus activated
        if self.head_collision is False and snake_in_collision.head_collision is False:
            if self.head.colliderect(snake_in_collision.head):
                self.zero()
                snake_in_collision.zero()

        # bonus activated
        elif self.head_collision is False:
            if self.head.colliderect(snake_in_collision.head):
                snake_in_collision.zero()

    # CHECKING BODY COLLISION
    def body_collision_check(self, snake_in_collision):

        # bonus deactivated
        if self.body_collision:
            if self.head.collidelist(snake_in_collision.body) != -1:
                self.zero()

        # hard game mode activated
        if self.body_collision is False:
            if self.hard:
                if self.head.collidelist(snake_in_collision.body) != -1:
                    snake_in_collision.zero()

    # CHECKING WALL COLLISION
    def wall_collision_check(self, snake_in_collision):
        if self.body_collision:
            if self.head.collidelist(snake_in_collision.wall) != -1:
                self.zero()

    # BONUS
    def bonus(self):
        # bonus game mode activated
        if self.wanna_bonus:
            # bonus activation
            if self.score % self.when == 0 and self.score != 0:
                self.killing_bonus = True
                self.wanna_bonus = False
        if self.score % self.when == 0 and self.score != 0:
            self.when += self.add_when

        # bonus activated
        if self.killing_bonus:
            self.bonus_on()
            # time duration
            self.time_bonus -= 1
            if self.time_bonus <= 0:
                self.bonus_off()

    def wall_drop(self):
        for body_part in self.body:
            self.wall.append(body_part)
            self.body = []
            self.max_len_tail = 0
            self.velocity = self.og_velocity

    # DRAW
    def draw(self, screen):
        for wall_part in self.wall:
            pygame.draw.rect(screen, self.og_body, wall_part)
        for tail_part in self.body:
            pygame.draw.rect(screen, self.color_body, tail_part)
        pygame.draw.rect(screen, self.color_head, self.head)

    # AFTER DYING SETTINGS
    def zero(self):
        self.x_velocity = 0
        self.y_velocity = 0
        self.velocity = 0
        self.body = []
        self.max_len_tail = 0
        self.color_head = COLORS["dark_red"]
        self.killing_bonus = False
        self.death = True

    # RESET SETTINGS
    def reset(self):
        self.color_head = self.og_head
        self.color_body = self.og_body

        self.head.topleft = self.og_position
        self.x_velocity = 0
        self.y_velocity = 0
        self.velocity = VELOCITY

        self.max_len_tail = MAX_LEN_TAIL
        self.body = []

        # self.update_score(-self.score)

        self.killing_bonus = False
        self.body_collision = True
        self.head_collision = True
        self.when = WHEN
        self.wanna_bonus = True

        self.death = False
        self.time_death = TIME_DEATH

    # BONUS ACTIVATED SETTINGS
    def bonus_on(self):
        self.body_collision = False
        self.head_collision = False
        self.color_head = COLORS["orange"]
        self.color_body = COLORS["yellow"]

    # BONUS DEACTIVATED SETTINGS
    def bonus_off(self):
        self.killing_bonus = False
        self.wanna_bonus = True
        self.color_body = self.og_body
        self.color_head = self.og_head
        self.body_collision = True
        self.head_collision = True
        self.time_bonus = TIME_BONUS

    def death_signal(self):
        self.time_death -= 1
        if self.time_death <= 0:
            self.zero()
