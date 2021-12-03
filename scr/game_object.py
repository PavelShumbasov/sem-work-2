import pygame

DEBUG = True


class GameObject:
    def __init__(self, screen, sprite, x, y):
        self.screen = screen
        self.sprite = sprite
        self.x = x
        self.y = y

        self.width = sprite.get_width()
        self.height = sprite.get_height()

    @property
    def right_border(self):
        return self.x + self.width

    @property
    def left_border(self):
        return self.x

    @property
    def bottom_border(self):
        return self.y + self.height

    @property
    def top_border(self):
        return self.y

    @property
    def center_x(self):
        return self.x + self.width / 2

    @property
    def center_y(self):
        return self.y + self.height / 2

    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y))

    def check_collision(self, other_object):
        return self.left_border <= other_object.center_x <= self.right_border and \
               self.top_border <= other_object.center_y <= self.bottom_border

    def update(self):  # Сигнал для определения абстрактного метода, должен быть определен в классах-наследниках
        if DEBUG:
            print(f"Обновление объекта {self}")
