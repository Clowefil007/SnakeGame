import pygame
import sys
from settings import WIDTH, HEIGHT, FPS, COLORS, BLOCK_SIZE, SPAWN1, SPAWN2, BAR
from snake import Snake
from apple import Apple
from button import Button


class Game:
    # BUILT-IN FUNCTION
    def __init__(self):
        # general
        self.width = WIDTH
        self.height = HEIGHT
        self.block_size = BLOCK_SIZE
        self.fps = FPS
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.bar = BAR
        self.running = True
        # snake
        self.snake1 = Snake(SPAWN1, COLORS["dark_green"], COLORS["green"], COLORS["violet"])
        self.snake2 = Snake(SPAWN2, COLORS["shadow"], COLORS["pink"], COLORS["violet"])
        # apple
        self.apple = Apple(pygame.image.load('apple.png').convert_alpha())
        # buttons
        self.restart_button = Button(self.width/2-50, self.height/50,
                                     pygame.image.load('restart_button.png').convert_alpha())

        self.mouse_pos = pygame.mouse.get_pos()

        self.background = pygame.image.load('background.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.start = False
        self.spawn1 = False
        self.spawn2 = False

    # DRAW
    def draw(self):
        # SCREEN FILL
        self.screen.blit(self.background, (0, 0))
        pygame.draw.rect(self.screen, COLORS['black'], (0, 0, self.width, self.bar))
        if self.start:
            pygame.draw.line(self.screen, COLORS['red'], (self.width/2, 0), (self.width/2, self.height))
        # SCORE
        self.screen.blit(self.snake1.text, (self.width - 180, self.height/50))
        self.screen.blit(self.snake2.text, (140, self.height/50))
        # BUTTON
        self.restart_button.draw(self.screen)
        # APPLE DRAW
        self.apple.draw(self.screen)
        # SNAKE 1 DRAW
        self.snake1.draw(self.screen)
        # SNAKE 2 DRAW
        self.snake2.draw(self.screen)
        # APPLE DRAW
        self.apple.draw(self.screen)
        # SCREEN UPDATE
        pygame.display.flip()

    # EVENTS
    def events(self):
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            # keys and movement
            if event.type == pygame.KEYDOWN:

                if self.start is False:
                    # SNAKE 1 KEYS
                    if event.key == pygame.K_LEFT:
                        self.snake1.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.snake1.move_right()
                    if event.key == pygame.K_DOWN:
                        self.snake1.move_down()
                    if event.key == pygame.K_UP:
                        self.snake1.move_up()
                    if event.key == pygame.K_RCTRL:
                        self.snake1.wall_drop()

                    # SNAKE 2 KEYS
                    if event.key == pygame.K_a:
                        self.snake2.move_left()
                    if event.key == pygame.K_d:
                        self.snake2.move_right()
                    if event.key == pygame.K_s:
                        self.snake2.move_down()
                    if event.key == pygame.K_w:
                        self.snake2.move_up()
                    if event.key == pygame.K_LCTRL:
                        self.snake2.wall_drop()

    # COLLISIONS
    def collisions(self):
        # border
        if self.snake1.border_collision:
            self.snake1.border_collision_check()
        else:
            self.snake1.none_border()
        if self.snake2.border_collision:
            self.snake2.border_collision_check()
        else:
            self.snake2.none_border()
        # snakes
        self.snake1.head_collision_check(self.snake2)
        self.snake2.head_collision_check(self.snake1)
        self.snake1.body_collision_check(self.snake2)
        self.snake2.body_collision_check(self.snake1)
        self.snake1.wall_collision_check(self.snake2)
        self.snake2.wall_collision_check(self.snake1)

        if self.snake1.death:
            self.snake2.death_signal()
        if self.snake2.death:
            self.snake1.death_signal()

    # MOVEMENT
    def movements(self):
        self.snake1.move()
        self.snake2.move()

    # MOUSE
    def mouse(self):
        self.mouse_pos = pygame.mouse.get_pos()

    def start_game(self):
        if self.spawn1:
            if self.mouse_pos[0] > self.width/2 and self.height - self.block_size > self.mouse_pos[1] > self.bar:
                self.snake1.head.topleft = self.mouse_pos
                if pygame.mouse.get_pressed()[0]:
                    self.snake1.head.topleft = self.mouse_pos
                    self.spawn1 = False

        if self.spawn2:
            if self.mouse_pos[0] < self.width/2 and self.height - self.block_size > self.mouse_pos[1] > self.bar:
                self.snake2.head.topleft = self.mouse_pos
                if pygame.mouse.get_pressed()[0]:
                    self.snake2.head.topleft = self.mouse_pos
                    self.spawn2 = False

        if self.spawn1 is False and self.spawn2 is False:
            self.start = False

    # UPDATES
    def updates(self):
        # body update
        self.snake2.body_update()
        self.snake1.body_update()
        # bonus activation
        self.snake1.bonus()
        self.snake2.bonus()

    # SCORE
    def score(self):
        if self.apple.collision_check(self.snake1):
            self.snake1.update_score(1)
        if self.apple.collision_check(self.snake2):
            self.snake2.update_score(1)

    # RESTART/PLAY AGAIN BUTTON
    def play_again(self):
        # button has been clicked
        if self.restart_button.click(self.mouse_pos):
            self.start = True
            self.spawn1 = True
            self.spawn2 = True
            self.snake1.reset()
            self.snake2.reset()

    # GAME LOOP
    def game_loop(self):
        while self.running:
            self.clock.tick(self.fps)

            self.mouse()
            if self.start:
                self.start_game()

            self.events()

            if self.start is False:
                self.movements()
                self.collisions()
                self.score()

            self.updates()

            self.play_again()

            self.draw()
