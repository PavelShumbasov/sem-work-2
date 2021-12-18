from game_object import GameObject
import pygame


class Button(GameObject):
    MAIN_STATE = 0
    HOVERED_STATE = 1
    CLICKED_STATE = 2

    def __init__(self, screen, sprite, x, y):
        super().__init__(screen, sprite, x, y)

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

        return is_hovered and is_clicked
