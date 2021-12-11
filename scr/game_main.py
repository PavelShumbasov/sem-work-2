import pygame
from platform import Platform
from ball import Ball
from obstacle import Obstacle
from obstacles_generator import ObstaclesGenerator


class Game:
    WIDTH = 800
    HEIGHT = 600
    FPS = 30
    GAME_NAME = "ARKANOID"
    PLATFORM_SIZE = 0.1 * WIDTH, 0.1 * WIDTH * 0.2
    OBSTACLE_SIZE = 0.1 * WIDTH, 0.1 * WIDTH * 0.4
    BALL_SIZE = PLATFORM_SIZE[1], PLATFORM_SIZE[1]
    OBSTACLE_COLORS_NUM = 4

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.GAME_NAME)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 36)
        self.load_pictures()
        self.platform = Platform(self.screen, self.platform1_sprite, self.WIDTH / 2,
                                 self.HEIGHT - self.platform1_sprite.get_height())

        self.ball = Ball(self.screen, self.ball_sprite, self.WIDTH / 2, self.HEIGHT / 2, self.platform)
        self.generator = ObstaclesGenerator(self.screen, self.obstacle_sprites, self.obstacle_hitted_sprites, self.ball)
        self.game_objects = [self.platform, self.ball, self.generator]

    def load_pictures(self):
        self.platform1_sprite = pygame.transform.scale(pygame.image.load("images/platform1.png"), self.PLATFORM_SIZE)
        self.platform2_sprite = pygame.transform.scale(pygame.image.load("images/platform2.png"), self.PLATFORM_SIZE)
        self.ball_sprite = pygame.transform.scale(pygame.image.load("images/ball.png"), self.BALL_SIZE)
        self.obstacle_sprites = [
            pygame.transform.scale(pygame.image.load(f"images/obstacle{i + 1}.png"), self.OBSTACLE_SIZE)
            for i in range(self.OBSTACLE_COLORS_NUM)]
        self.obstacle_hitted_sprites = [
            pygame.transform.scale(pygame.image.load(f"images/obstacle{i + 1}_hitted.png"), self.OBSTACLE_SIZE)
            for i in range(self.OBSTACLE_COLORS_NUM)]

    def main_game(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            self.screen.fill((0, 0, 0))

            for game_object in self.game_objects:
                game_object.update()

            self.clock.tick(self.FPS)
            pygame.display.update()


game = Game()
game.main_game()
