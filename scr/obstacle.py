import pygame
from game_object import GameObject


class Obstacle(GameObject):
    def __init__(self, screen, sprite, x, y, start_lives, sprite_bumped):
        super().__init__(screen, sprite, x, y)
        self.lives = start_lives
        self.sprite_bumped = sprite_bumped

    def update(self):
        self.draw()

    def decrease(self):
        self.lives -= 1
        if self.lives == 1:
            self.sprite = self.sprite_bumped

    @property
    def is_alive(self):
        return self.lives > 0