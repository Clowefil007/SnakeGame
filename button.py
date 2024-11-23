import pygame


class Button:
    # BUILT-IN FUNCTION
    def __init__(self, x, y, img):
        # creating rect from image
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # button has been clicked
        self.action = False

    # DRAW
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    # CHECKING IF BUTTON CLICK
    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.action = True
                return self.action
        else:
            self.action = False
