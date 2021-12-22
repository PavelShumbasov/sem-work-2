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
        self.collider = pygame.Rect(self.x, self.y, self.width, self.height)

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

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, position):
        self.x, self.y = position

    def draw(self):
        self.collider.x = self.x
        self.collider.y = self.y
        self.screen.blit(self.sprite, (self.x, self.y))

    def check_collision(self, other_object):
        return self.collider.colliderect(other_object.collider)

    def update(self):  # Сигнал для определения абстрактного метода, должен быть определен в классах-наследниках
        if DEBUG:
            print(f"Обновление объекта {self}")
