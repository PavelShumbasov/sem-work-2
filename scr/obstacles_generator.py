import pygame
from obstacle import Obstacle
from random import randint


class ObstaclesGenerator:

    SPEED = 90

    def __init__(self, screen, obstacle_sprites, obstacle_hitted_sprites, ball):
        self.screen = screen
        self.obstacle_sprites = obstacle_sprites
        self.obstacle_hitted_sprites = obstacle_hitted_sprites
        self.ball = ball
        self.timer = 0
        self.obstacles = []

    def generate_position(self):
        x = randint(0, self.screen.get_width() // self.obstacle_sprites[0].get_width()) * self.obstacle_sprites[0].get_width()
        y = randint(3, self.screen.get_height() // self.obstacle_sprites[0].get_height() - 3) * self.obstacle_sprites[0].get_height()
        return x, y

    def __generate(self):
        x, y = self.generate_position()
        while len(list(filter(lambda obs: obs.position == (x, y), self.obstacles))) > 0:
            x, y = self.generate_position()
        color_num = randint(0, len(self.obstacle_sprites) - 1)
        self.obstacles.append(Obstacle(self.screen, self.obstacle_sprites[color_num], x, y, color_num + 1,
                                       self.obstacle_hitted_sprites[color_num]))

    def generate(self):
        self.timer += 1
        if self.timer == self.SPEED:
            self.__generate()
            self.timer = 0

    def check_obstacles(self):
        for obstacle in self.obstacles:
            if obstacle.is_alive:
                if (abs(self.ball.top_border - obstacle.bottom_border) <= self.ball.height / 4
                    or abs(self.ball.bottom_border - obstacle.top_border) <= self.ball.height / 4) \
                        and obstacle.left_border <= self.ball.center_x <= obstacle.right_border:
                    self.ball.reverse_vertical_direction()
                    print('Ударился вертикально')
                    obstacle.decrease()

                if (abs(self.ball.left_border - obstacle.right_border) <= self.ball.width / 3
                    or abs(self.ball.right_border - obstacle.left_border) <= self.ball.width / 3) \
                        and obstacle.top_border <= self.ball.center_y <= obstacle.bottom_border:
                    self.ball.reverse_horizontal_direction()
                    print('Ударился горизонтально')
                    obstacle.decrease()

                obstacle.update()

    def update(self):
        self.check_obstacles()
        self.generate()