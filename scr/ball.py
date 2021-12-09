import pygame
from game_object import GameObject


class Ball(GameObject):
    SPEED = 6

    def __init__(self, screen, sprite, x, y, platform):
        super().__init__(screen, sprite, x, y)
        self.dx = self.SPEED
        self.dy = self.SPEED
        self.platform = platform

    def check_borders(self):
        if self.platform.check_collision(self):
            self.reverse_vertical_direction()
            print("СТОЛКНОВЕНИЕ!!!")

        if self.bottom_border >= self.screen.get_height() or self.top_border <= 0:
            self.reverse_vertical_direction()
            print("Проигрыш")

        if self.left_border <= 0 or self.right_border >= self.screen.get_width():
            self.reverse_horizontal_direction()

        self.x += self.dx
        self.y += self.dy

    def reverse_vertical_direction(self):
        self.dy = -self.dy

    def reverse_horizontal_direction(self):
        self.dx = -self.dx

    def update(self):
        self.check_borders()
        self.draw()
