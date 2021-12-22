import pygame


class LifeHolder:
    FONT_SIZE = 25
    COLOR = (255, 255, 255)

    def __init__(self, screen, x, y, start_life):
        self.lives = start_life
        self.x = x
        self.y = y
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", self.FONT_SIZE)
        self.rendered_text = self.font.render(str(self.lives), True, self.COLOR)

    def decrease(self):
        self.lives -= 1
        self.rendered_text = self.font.render(str(self.lives), True, self.COLOR)
        return self.lives == 0

    def draw(self):
        self.screen.blit(self.rendered_text, (self.x, self.y))

    def update(self):
        self.draw()
