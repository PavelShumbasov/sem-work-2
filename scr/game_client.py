import pygame
from platform import Platform


class GameClient:
    WIDTH = 800
    HEIGHT = 600
    FPS = 30
    GAME_NAME = "ARCANOID"
    PLATFORM_SIZE = 0.1 * WIDTH, 0.1 * WIDTH * 0.2

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
        self.platform1_sprite = pygame.transform.scale(pygame.image.load("images/platform1.png"), self.PLATFORM_SIZE)
        self.platform2_sprite = pygame.transform.scale(pygame.image.load("images/platform2.png"), self.PLATFORM_SIZE)
        self.ball_sprite = pygame.image.load("images/ball.png")

    def main_game(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            self.screen.fill((0, 0, 0))

            self.platform.update()

            self.clock.tick(self.FPS)
            pygame.display.update()


game = GameClient()
game.main_game()