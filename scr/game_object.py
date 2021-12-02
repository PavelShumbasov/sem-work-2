import pygame


class GameObject:
    def __init__(self, screen, sprite, x, y):
        self.screen = screen
        self.sprite = sprite
        self.x = x
        self.y = y

        self.width = sprite.get_width()
        self.height = sprite.get_height()

    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y))

    def check_collision(self, other_object):
        return self.x <= other_object.x + other_object.width / 2 <= self.x + self.width and \
               self.y <= other_object.y + other_object.height / 2 <= self.y + self.height


