import pygame
from game_object import GameObject


class Ball(GameObject):
    SPEED = 6

    def __init__(self, screen, sprite, x, y, platform, obstacles):
        super().__init__(screen, sprite, x, y)
        self.dx = self.SPEED
        self.dy = self.SPEED
        self.platform = platform
        self.obstacles = obstacles

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

    def check_obstacles(self):
        for obstacle in self.obstacles:
            if obstacle.is_alive:
                if (abs(self.top_border - obstacle.bottom_border) <= self.height / 2
                        or abs(self.bottom_border - obstacle.top_border) <= self.height / 2) \
                        and obstacle.left_border <= self.center_x <= obstacle.right_border:
                    self.reverse_vertical_direction()
                    obstacle.decrease()

                if (abs(self.left_border - obstacle.right_border) <= self.width / 2
                        or abs(self.right_border - obstacle.left_border) <= self.width / 2) \
                        and obstacle.top_border <= self.center_y <= obstacle.bottom_border:
                    self.reverse_horizontal_direction()
                    obstacle.decrease()

    def update(self):
        self.check_borders()
        self.check_obstacles()
        self.draw()
