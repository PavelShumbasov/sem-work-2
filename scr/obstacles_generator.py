import pygame
from obstacle import Obstacle
from random import randint


class ObstaclesGenerator:
    SPEED = 90

    def __init__(self, screen, obstacle_sprites, obstacle_hitted_sprites, ball, is_controlled, obstacles_que):
        self.screen = screen
        self.obstacle_sprites = obstacle_sprites
        self.obstacle_hitted_sprites = obstacle_hitted_sprites
        self.ball = ball
        self.timer = 0
        self.obstacles = []
        self.is_controlled = is_controlled
        self.obstacles_que = obstacles_que

    def generate_position(self):
        x = randint(0, self.screen.get_width() // self.obstacle_sprites[0].get_width()) * self.obstacle_sprites[
            0].get_width()
        y = randint(3, self.screen.get_height() // self.obstacle_sprites[0].get_height() - 3) * self.obstacle_sprites[
            0].get_height()
        return x, y

    def __generate(self):
        x, y = self.generate_position()
        while len(list(filter(lambda obs: obs.position == (x, y), self.obstacles))) > 0 \
                and not x <= self.ball.x <= x + self.obstacle_sprites[0].get_width() \
                and not y <= self.ball.y <= y + self.obstacle_sprites[0].get_height():
            x, y = self.generate_position()
        color_num = randint(0, len(self.obstacle_sprites) - 1)
        self.obstacles.append(Obstacle(self.screen, self.obstacle_sprites[color_num], x, y, color_num + 1,
                                       self.obstacle_hitted_sprites[color_num]))
        self.obstacles_que.append(self.obstacles[-1])

    def generate(self):
        self.timer += 1
        if self.timer == self.SPEED:
            self.__generate()
            self.timer = 0

    def check_obstacles(self):
        for obstacle in self.obstacles[::-1]:
            if obstacle.is_alive:
                if (abs(self.ball.top_border - obstacle.bottom_border) <= self.ball.height / 1.5
                    or abs(self.ball.bottom_border - obstacle.top_border) <= self.ball.height / 1.5) \
                        and obstacle.left_border <= self.ball.center_x <= obstacle.right_border:
                    self.ball.reverse_vertical_direction()
                    print('Ударился вертикально')
                    obstacle.decrease()

                elif (abs(self.ball.left_border - obstacle.right_border) <= self.ball.width / 3
                      or abs(self.ball.right_border - obstacle.left_border) <= self.ball.width / 3) \
                        and obstacle.top_border <= self.ball.center_y <= obstacle.bottom_border:
                    self.ball.reverse_horizontal_direction()
                    print('Ударился горизонтально')
                    obstacle.decrease()

                obstacle.update()
            else:
                self.obstacles.remove(obstacle)

    def update(self):
        self.check_obstacles()
        if self.is_controlled:
            self.generate()
