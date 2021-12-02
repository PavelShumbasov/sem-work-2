import pygame
from platform import Platform


class GameClient:
    WIDTH = 800
    HEIGHT = 600
    FPS = 30
    GAME_NAME = "ARCANOID"

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.GAME_NAME)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 36)
        self.load_pictures()
        self.platform = Platform(self.screen, self.platform1_sprite, self.WIDTH / 2,
                                 self.HEIGHT - self.platform1_sprite.get_height())

    def load_pictures(self):
        self.platform1_sprite = pygame.image.load("images/platform1.png")
        self.platform2_sprite = pygame.image.load("images/platform2.png")
        self.ball_sprite = pygame.image.load("images/ball.png")

    def main_game(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.platform.move_left()
            elif keys[pygame.K_d]:
                self.platform.move_right()

            self.screen.fill((0, 0, 0))

            self.platform.update()

            self.clock.tick(self.FPS)
            pygame.display.update()


game = GameClient()
game.main_game()