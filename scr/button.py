from game_object import GameObject
import pygame


class Button(GameObject):
    MAIN_STATE = 0
    HOVERED_STATE = 1
    CLICKED_STATE = 2

    def __init__(self, screen, sprite, x, y, text):
        super().__init__(screen, sprite[0], x, y)
        self.sprite = sprite
        self.text = text
        font = pygame.font.SysFont("Arial", int(sprite[0].get_height() * 0.8))
        self.rendered_text = font.render(text, True, (15, 15, 15))

    def update(self):
        m_x, m_y = pygame.mouse.get_pos()
        is_clicked = pygame.mouse.get_pressed()[0]
        is_hovered = self.left_border <= m_x <= self.right_border and self.top_border <= m_y <= self.bottom_border
        if is_hovered and is_clicked:
            self.screen.blit(self.sprite[self.CLICKED_STATE], (self.x, self.y))
        elif is_hovered:
            self.screen.blit(self.sprite[self.HOVERED_STATE], (self.x, self.y))
        else:
            self.screen.blit(self.sprite[self.MAIN_STATE], (self.x, self.y))
        self.screen.blit(self.rendered_text, (
            self.center_x - self.rendered_text.get_width() / 2, self.center_y - self.rendered_text.get_height() / 2))
        return is_hovered and is_clicked
