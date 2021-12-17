import socket


class GameClient:
    ENCODING = "UTF-8"
    DATA_SIZE = 1024

    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.player_number = self.client_socket.recv(self.DATA_SIZE).decode(self.ENCODING)
        print(self.player_number + "game client")

    def get_data_from_server(self):
        while True:
            server_response = self.client_socket.recv(self.DATA_SIZE).decode(self.ENCODING)
            print("from GameClient ", server_response)
            if "#" in server_response:
                yield server_response

    def send_data(self, data):
        self.client_socket.send(data.encode(self.ENCODING))

    def get_player_number(self):
        return self.player_number
