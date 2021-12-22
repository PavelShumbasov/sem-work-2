import pygame
from game_object import GameObject


class Ball(GameObject):
    SPEED = 6

    def __init__(self, screen, sprite, x, y, platform, platform_opp, is_controlled):
        super().__init__(screen, sprite, x, y)
        self.dx = self.SPEED
        self.dy = self.SPEED
        self.platform = platform
        self.platform_opp = platform_opp
        self.timer = 0
        self.is_controlled = is_controlled

    def check_borders(self):
        if self.platform.check_collision(self) and self.dy > 0 \
                or self.platform_opp.check_collision(self) and self.dy < 0:
            self.reverse_vertical_direction()
            print("СТОЛКНОВЕНИЕ!!!")

        if self.bottom_border >= self.screen.get_height() and self.dy > 0 or self.top_border <= 0 and self.dy < 0:
            self.reverse_vertical_direction()
            print("Проигрыш")

        if self.left_border <= 0 and self.dx < 0 or self.right_border >= self.screen.get_width() and self.dx > 0:
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
        if self.is_controlled:
            self.check_borders()
        self.draw()
