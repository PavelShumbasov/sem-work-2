import pygame
from game_object import GameObject


class Ball(GameObject):
    SPEED = 6
    DELAY = 3

    def __init__(self, screen, sprite, x, y, platform):
        super().__init__(screen, sprite, x, y)
        self.dx = self.SPEED
        self.dy = self.SPEED
        self.platform = platform
        self.timer = 0

    def check_borders(self):
        if self.platform.check_collision(self) and self.timer > self.DELAY:
            self.reverse_vertical_direction()
            print("СТОЛКНОВЕНИЕ!!!")

        if (self.bottom_border >= self.screen.get_height() or self.top_border <= 0) and self.timer > self.DELAY:
            self.reverse_vertical_direction()
            print("Проигрыш")

        if (self.left_border <= 0 or self.right_border >= self.screen.get_width()) and self.timer > self.DELAY:
            self.reverse_horizontal_direction()

        self.x += self.dx
        self.y += self.dy

    def reverse_vertical_direction(self):
        self.timer = 0
        self.dy = -self.dy

    def reverse_horizontal_direction(self):
        self.timer = 0
        self.dx = -self.dx

    def update(self):
        self.timer += 1
        self.check_borders()
        self.draw()
