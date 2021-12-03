import pygame
from game_object import GameObject


class Ball(GameObject):
    SPEED = 6

    def __init__(self, screen, sprite, x, y, platform):
        super().__init__(screen, sprite, x, y)
        self.dx = self.SPEED
        self.dy = self.SPEED
        self.platform = platform

    def update(self):
        if self.platform.check_collision(self):
            self.dy = -self.dy
            print("СТОЛКНОВЕНИЕ!!!")

        if self.bottom_border >= self.screen.get_height() or self.top_border <= 0:
            self.dy = -self.dy
            print("Проигрыш")

        if self.left_border <= 0 or self.right_border >= self.screen.get_width():
            self.dx = -self.dx


        self.x += self.dx
        self.y += self.dy
        self.draw()
