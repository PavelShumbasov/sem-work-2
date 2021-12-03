import pygame
from game_object import GameObject


class Platform(GameObject):
    SPEED = 15

    def __init__(self, screen, sprite, x, y):
        super().__init__(screen, sprite, x, y)

    def move_left(self):
        if self.x > self.SPEED:
            self.x -= self.SPEED

    def move_right(self):
        if self.x + self.width < self.screen.get_width() - self.SPEED:
            self.x += self.SPEED

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.move_left()
        elif keys[pygame.K_d]:
            self.move_right()

    def update(self):
        self.move()
        self.draw()

