import pygame
from platform import Platform
from ball import Ball
from obstacles_generator import ObstaclesGenerator
from game_client import GameClient
from collections import deque
from server_message import ServerMessage

PATH = "C:/Users/79176/PycharmProjects/sem-work-2/scr/"


class Game:
    WIDTH = 800
    HEIGHT = 600
    FPS = 30
    GAME_NAME = "ARKANOID"
    PLATFORM_SIZE = 0.1 * WIDTH, 0.1 * WIDTH * 0.2
    OBSTACLE_SIZE = 0.1 * WIDTH, 0.1 * WIDTH * 0.4
    BALL_SIZE = PLATFORM_SIZE[1], PLATFORM_SIZE[1]
    OBSTACLE_COLORS_NUM = 4
    HOST = 'localhost'
    PORT = 7070
    EVENT_PLATFORM_POSITION = "PLATFORM"

    def __init__(self):
        self.game_client = GameClient(self.HOST, self.PORT)
        self.player_number = self.game_client.get_player_number()
        print(self.player_number)
        self.messages = deque()

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.GAME_NAME)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 36)
        self.load_pictures()
        if self.player_number == "1":
            self.platform = Platform(self.screen, self.platform1_sprite, self.WIDTH / 2,
                                     self.HEIGHT - self.platform1_sprite.get_height())
            self.platform_opp = Platform(self.screen, self.platform2_sprite, self.WIDTH / 2, 0, False)
        else:
            self.platform = Platform(self.screen, self.platform2_sprite, self.WIDTH / 2, 0)
            self.platform_opp = Platform(self.screen, self.platform1_sprite, self.WIDTH / 2,
                                         self.HEIGHT - self.platform1_sprite.get_height(), False)

        self.ball = Ball(self.screen, self.ball_sprite, self.WIDTH / 2, self.HEIGHT / 2, self.platform)
        self.generator = ObstaclesGenerator(self.screen, self.obstacle_sprites, self.obstacle_hitted_sprites, self.ball)
        self.game_objects = [self.platform, self.platform_opp, self.ball, self.generator]

    def load_pictures(self):
        self.platform1_sprite = pygame.transform.scale(pygame.image.load(PATH + "images/platform1.png"), self.PLATFORM_SIZE)
        self.platform2_sprite = pygame.transform.scale(pygame.image.load(PATH + "images/platform2.png"), self.PLATFORM_SIZE)
        self.ball_sprite = pygame.transform.scale(pygame.image.load(PATH + "images/ball.png"), self.BALL_SIZE)
        self.obstacle_sprites = [
            pygame.transform.scale(pygame.image.load(PATH + f"images/obstacle{i + 1}.png"), self.OBSTACLE_SIZE)
            for i in range(self.OBSTACLE_COLORS_NUM)]
        self.obstacle_hitted_sprites = [
            pygame.transform.scale(pygame.image.load(PATH + f"images/obstacle{i + 1}_hitted.png"), self.OBSTACLE_SIZE)
            for i in range(self.OBSTACLE_COLORS_NUM)]

    def get_data_from_server(self):
        for message in self.game_client.get_data_from_server():
            self.messages.append(message)

    def main_game(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            self.screen.fill((0, 0, 0))
            while len(self.messages) > 0:
                event = ServerMessage(self.messages.pop())
                if event.type == self.EVENT_PLATFORM_POSITION:
                    self.platform_opp.position = tuple(map(float, event.data.split()))
            self.game_client.send_data(
                ServerMessage.prepare_data(self.EVENT_PLATFORM_POSITION, f"{self.platform.x} {self.platform.y}"))
            for game_object in self.game_objects:
                game_object.update()

            self.clock.tick(self.FPS)
            pygame.display.update()


game = Game()
game.main_game()
