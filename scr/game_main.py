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
from life_holder import LifeHolder

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
    PORT = 5050
    EVENT_PLATFORM_POSITION = "PLATFORM"
    EVENT_OBSTACLE_CREATION = "OBSTACLE_CREATION"
    EVENT_BALL_POSITION = "BALL"
    EVENT_TOP_PLATFORM_DECREASE = "DECREASE_TOP"
    EVENT_BOTTOM_PLATFORM_DECREASE = "DECREASE_BOTTOM"
    BUTTON_SIZE = 0.4 * WIDTH, 0.2 * HEIGHT
    FONT_SIZE = 30
    WAIT_OPP = "Ожидание второго игрока..."
    TIME_TO_RESTART = 10
    AMOUNT_OF_LIFE = 7

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
        self.waiting_room()
        start_new_thread(self.get_data_from_server, ())
        while True:
            self.messages = deque()
            self.winner = None

            self.is_playing = True
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

            self.life_holder_bottom = LifeHolder(self.screen, self.WIDTH - 40, self.HEIGHT - 40, self.AMOUNT_OF_LIFE)
            self.life_holder_top = LifeHolder(self.screen, self.WIDTH - 40, 0, self.AMOUNT_OF_LIFE)

            self.ball = Ball(self.screen, self.ball_sprite, self.WIDTH / 2, self.HEIGHT / 2, self.platform,
                             self.platform_opp, is_controlled)
            self.obstacles_que = deque()
            self.generator = ObstaclesGenerator(self.screen, self.obstacle_sprites, self.obstacle_hitted_sprites, self.ball,
                                                is_controlled, self.obstacles_que)
            self.game_objects = [self.platform, self.platform_opp, self.ball, self.generator, self.life_holder_bottom,
                                 self.life_holder_top]

            self.previous_position = self.platform.position

            self.main_game()
            self.winner_scene()

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
            if message.count(" ") != 1:
                messages = message.split()
                for mess in messages:
                    self.messages.append(mess)
            else:
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

    def check_collision(self):
        if self.player_number == "1":
            check_end = False
            if self.ball.bottom_border >= self.screen.get_height() and self.ball.dy > 0:
                check_end = self.life_holder_bottom.decrease()
                self.game_client.send_data(ServerMessage.prepare_data(self.EVENT_BOTTOM_PLATFORM_DECREASE, " "))
            elif self.ball.top_border <= 0 and self.ball.dy < 0:
                check_end = self.life_holder_top.decrease()
                self.game_client.send_data(ServerMessage.prepare_data(self.EVENT_TOP_PLATFORM_DECREASE, " "))
            if check_end:
                self.stop_game()

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
            print("Отправка платформы")
            self.game_client.send_data(
                ServerMessage.prepare_data(self.EVENT_OBSTACLE_CREATION, obstacle))
        if self.player_number == "1":
            self.game_client.send_data(
                ServerMessage.prepare_data(self.EVENT_BALL_POSITION, f"{self.ball.x}&{self.ball.y}"))

    def stop_game(self):
        self.winner = "Красный" if self.life_holder_top.lives == 0 else "Синий"
        self.is_playing = False

    def process_data_from_server(self):
        check_end = False
        while len(self.messages) > 0:
            event = ServerMessage(self.messages.pop())
            if event.type == self.EVENT_PLATFORM_POSITION:
                if event.data.count("&") == 1:
                    self.platform_opp.position = tuple(map(float, event.data.split("&")))
            elif event.type == self.EVENT_OBSTACLE_CREATION:
                print("Создание платформы")
                if event.data.count("&") == 2:
                    x, y, start_lives = event.data.split("&")
                    self.generator.obstacles.append(
                        Obstacle(self.screen, self.obstacle_sprites[int(start_lives) - 1], float(x), float(y),
                                 int(start_lives), self.obstacle_hitted_sprites[int(start_lives) - 1]))
            elif event.type == self.EVENT_BALL_POSITION:
                if event.data.count("&") == 1:
                    self.ball.position = tuple(map(float, event.data.split("&")))
            elif event.type == self.EVENT_TOP_PLATFORM_DECREASE:
                check_end = self.life_holder_top.decrease()
            elif event.type == self.EVENT_BOTTOM_PLATFORM_DECREASE:
                check_end = self.life_holder_bottom.decrease()
            if check_end:
                self.stop_game()

    def winner_scene(self):
        for i in range(self.FPS * self.TIME_TO_RESTART):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            self.screen.fill((0, 0, 0))
            winner_text = self.font.render("Победил " + self.winner, True, (255, 255, 255))
            self.screen.blit(winner_text, ((self.WIDTH - winner_text.get_width()) / 2,
                                           (self.HEIGHT - winner_text.get_height()) / 2))

            time_to_restart = self.font.render(f"До перезапуска: {self.TIME_TO_RESTART - (i // self.FPS)}",
                                               True, (255, 255, 255))
            self.screen.blit(time_to_restart, ((self.WIDTH - time_to_restart.get_width()) / 2,
                                           (self.HEIGHT + time_to_restart.get_height()) / 2))
            self.clock.tick(self.FPS)
            pygame.display.update()

    def main_game(self):
        while self.is_playing:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            self.screen.fill((0, 0, 0))

            self.process_data_from_server()

            self.check_collision()

            for game_object in self.game_objects:
                game_object.update()

            self.send_data_to_server()

            self.previous_position = self.platform.x, self.platform.y
            self.clock.tick(self.FPS)
            pygame.display.update()


game = Game()
