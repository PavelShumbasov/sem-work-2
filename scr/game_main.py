import pygame
from platform import Platform
from ball import Ball
from obstacles_generator import ObstaclesGenerator
from game_client import GameClient
from collections import deque
from server_message import ServerMessage
from _thread import start_new_thread
from obstacle import Obstacle
from button import Button

PATH = "C:/Users/79176/PycharmProjects/sem-work-2/scr/"


class Game:
    WIDTH = 800
    HEIGHT = 600
    FPS = 70
    GAME_NAME = "ARKANOID"
    PLATFORM_SIZE = 0.1 * WIDTH, 0.1 * WIDTH * 0.2
    OBSTACLE_SIZE = 0.1 * WIDTH, 0.1 * WIDTH * 0.4
    BALL_SIZE = PLATFORM_SIZE[1], PLATFORM_SIZE[1]
    OBSTACLE_COLORS_NUM = 4
    HOST = 'localhost'
    PORT = 5050
    EVENT_PLATFORM_POSITION = "PLATFORM"
    EVENT_OBSTACLE_CREATION = "OBSTACLE_CREATION"
    EVENT_BALL_POSITION = "BALL"
    BUTTON_SIZE = 0.4 * WIDTH, 0.2 * HEIGHT
    FONT_SIZE = 30
    WAIT_OPP = "Ожидание второго игрока..."

    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("Arial", self.FONT_SIZE)
        self.wait_opp_text = self.font.render(self.WAIT_OPP, True, (255, 255, 255))

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.GAME_NAME)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 36)
        self.load_pictures()

        self.button_start = Button(self.screen, self.button_sprites, self.WIDTH / 2 - self.BUTTON_SIZE[0] / 2,
                                   self.HEIGHT / 2 - self.BUTTON_SIZE[1] * 1.5, "START")
        self.button_exit = Button(self.screen, self.button_sprites, self.WIDTH / 2 - self.BUTTON_SIZE[0] / 2,
                                  self.HEIGHT / 2 - self.BUTTON_SIZE[1] * 0.3, "EXIT")
        self.start_menu()

        self.game_client = None
        self.player_number = None
        start_new_thread(self.get_player_number, ())
        print("Запуск сцены ожидания")
        self.waiting_room()
        self.messages = deque()

        if self.player_number == "1":
            self.platform = Platform(self.screen, self.platform1_sprite, self.WIDTH / 2,
                                     self.HEIGHT - self.platform1_sprite.get_height())
            self.platform_opp = Platform(self.screen, self.platform2_sprite, self.WIDTH / 2, 0, False)
            is_controlled = True
        else:
            self.platform = Platform(self.screen, self.platform2_sprite, self.WIDTH / 2, 0)
            self.platform_opp = Platform(self.screen, self.platform1_sprite, self.WIDTH / 2,
                                         self.HEIGHT - self.platform1_sprite.get_height(), False)
            is_controlled = False

        self.ball = Ball(self.screen, self.ball_sprite, self.WIDTH / 2, self.HEIGHT / 2, self.platform,
                         self.platform_opp, is_controlled)
        self.obstacles_que = deque()
        self.generator = ObstaclesGenerator(self.screen, self.obstacle_sprites, self.obstacle_hitted_sprites, self.ball,
                                            is_controlled, self.obstacles_que)
        self.game_objects = [self.platform, self.platform_opp, self.ball, self.generator]
        start_new_thread(self.get_data_from_server, ())

        self.previous_position = self.platform.position

    def load_pictures(self):
        self.platform1_sprite = pygame.transform.scale(pygame.image.load(PATH + "images/platform1.png"),
                                                       self.PLATFORM_SIZE)
        self.platform2_sprite = pygame.transform.scale(pygame.image.load(PATH + "images/platform2.png"),
                                                       self.PLATFORM_SIZE)
        self.ball_sprite = pygame.transform.scale(pygame.image.load(PATH + "images/ball.png"), self.BALL_SIZE)
        self.obstacle_sprites = [
            pygame.transform.scale(pygame.image.load(PATH + f"images/obstacle{i + 1}.png"), self.OBSTACLE_SIZE)
            for i in range(self.OBSTACLE_COLORS_NUM)]
        self.obstacle_hitted_sprites = [
            pygame.transform.scale(pygame.image.load(PATH + f"images/obstacle{i + 1}_hitted.png"), self.OBSTACLE_SIZE)
            for i in range(self.OBSTACLE_COLORS_NUM)]
        self.button_sprites = [
            pygame.transform.scale(pygame.image.load(PATH + "images/button_main.png"), self.BUTTON_SIZE),
            pygame.transform.scale(pygame.image.load(PATH + "images/button_hovered.png"), self.BUTTON_SIZE),
            pygame.transform.scale(pygame.image.load(PATH + "images/button_clicked.png"), self.BUTTON_SIZE)]

    def get_data_from_server(self):
        for message in self.game_client.get_data_from_server():
            self.messages.append(message)

    def get_player_number(self):
        self.game_client = GameClient(self.HOST, self.PORT)
        self.player_number = self.game_client.get_player_number()

    def waiting_room(self):
        while not self.player_number:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.wait_opp_text, ((self.WIDTH - self.wait_opp_text.get_width()) / 2,
                                                  (self.HEIGHT - self.wait_opp_text.get_height()) / 2))
            self.clock.tick(self.FPS)
            pygame.display.update()

    def start_menu(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            if self.button_exit.update():
                exit()
            if self.button_start.update():
                break
            self.clock.tick(self.FPS)
            pygame.display.update()

    def send_data_to_server(self):
        if self.platform.position != self.previous_position:
            self.game_client.send_data(
                ServerMessage.prepare_data(self.EVENT_PLATFORM_POSITION, f"{self.platform.x}&{self.platform.y}"))
        while len(self.obstacles_que) > 0:
            obstacle = self.obstacles_que.pop()
            self.game_client.send_data(
                ServerMessage.prepare_data(self.EVENT_OBSTACLE_CREATION,
                                           f"{obstacle.x}&{obstacle.y}&{obstacle.lives}"))
        if self.player_number == "1":
            self.game_client.send_data(
                ServerMessage.prepare_data(self.EVENT_BALL_POSITION, f"{self.ball.x}&{self.ball.y}"))

    def process_data_from_server(self):
        while len(self.messages) > 0:
            event = ServerMessage(self.messages.pop())
            if event.type == self.EVENT_PLATFORM_POSITION:
                if event.data.count("&") == 1:
                    self.platform_opp.position = tuple(map(float, event.data.split("&")))
            elif event.type == self.EVENT_OBSTACLE_CREATION:
                if event.data.count("&") == 2:
                    x, y, start_lives = event.data.split("&")
                    self.generator.obstacles.append(
                        Obstacle(self.screen, self.obstacle_sprites[int(start_lives) - 1], float(x), float(y),
                                 int(start_lives), self.obstacle_hitted_sprites[int(start_lives) - 1]))
            elif event.type == self.EVENT_BALL_POSITION:
                if event.data.count("&") == 1:
                    self.ball.position = tuple(map(float, event.data.split("&")))

    def main_game(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            self.screen.fill((0, 0, 0))

            self.process_data_from_server()

            for game_object in self.game_objects:
                game_object.update()

            self.send_data_to_server()

            self.previous_position = self.platform.x, self.platform.y
            self.clock.tick(self.FPS)
            pygame.display.update()


game = Game()
game.main_game()
