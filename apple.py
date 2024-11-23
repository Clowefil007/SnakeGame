import pygame
import random
from settings import APPLE_SIZE, HEIGHT, WIDTH, BAR, APPLE_N
Rect = pygame.Rect


class Apple:
    # BUILT-IN FUNCTION
    def __init__(self, img):
        # general
        self.size = APPLE_SIZE
        self.height = HEIGHT
        self.width = WIDTH
        self.bar = BAR
        self.apple_n = APPLE_N
        # creating rect from image
        self.image = img
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.apple_list = []
        self.apple_rect = self.image.get_rect()
        for x in range(0, APPLE_N):
            apple = (random.randrange(0, self.width - self.size), random.randrange(self.bar, self.height - self.size))
            apple_rect = self.image.get_rect()
            apple_rect.topleft = apple
            self.apple_list.append(apple_rect)

        # creating mask
        self.apple_mask = pygame.mask.from_surface(self.image)

    # GENERATING NEW COORDINATES
    def new_spawn_apple(self, new_apple):
        self.apple_list.remove(new_apple)
        apple_x = random.randrange(0, self.width - self.size)
        apple_y = random.randrange(self.bar, self.height - self.size)
        new_apple.topleft = (apple_x, apple_y)
        self.apple_list.append(new_apple)

    # CHECKING FOR COLLISIONS BETWEEN APPLE AND SNAKE
    def collision_check(self, snake):
        for apple in self.apple_list:
            if self.apple_mask.overlap(snake.snake_mask, (snake.head[0] - apple.topleft[0],
                                                          snake.head[1] - apple.topleft[1])):
                self.new_spawn_apple(apple)
                snake.max_len_tail += snake.grow
                if snake.velocity >= snake.minimum_velocity:
                    snake.velocity -= snake.velocity_decrease
                return True
        return False

    # DRAW
    def draw(self, screen):
        for apple in self.apple_list:
            screen.blit(self.image, apple.topleft)
