import socket
from _thread import start_new_thread

PORT = 7070
HOST = "localhost"


class Server:
    CLIENTS_IN_QUEUE = 5
    MAX_PLAYERS = 300
    DATA_SIZE = 1024
    ENCODING = "utf-8"

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(self.CLIENTS_IN_QUEUE)
        self.players = []

    def start_game_session(self, connection, player_number):
        while len(self.players) != player_number:
            pass
        if player_number % 2 == 1:
            partner_numb = player_number + 1
            welcome_message = "1"
        else:
            partner_numb = player_number - 1
            welcome_message = "2"

        connection.send(str.encode(welcome_message))

        while True:
            data = connection.recv(self.DATA_SIZE).decode(self.ENCODING)
            print(data)
            if not data:
                break

            if partner_numb < len(self.players):
                self.players[partner_numb].send(data.encode(self.ENCODING))
            else:
                connection.send("No opponents".encode(self.ENCODING))

        connection.close()

    def create_game_rooms(self):
        while True:
            connection, address = self.server_socket.accept()
            if not connection or len(self.players) >= self.MAX_PLAYERS:
                raise Exception("Не удалось подключиться :(")

            self.players.append(connection)

            start_new_thread(self.start_game_session, (connection, len(self.players),))


game_server = Server(HOST, PORT)
game_server.create_game_rooms()
