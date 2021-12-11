import socket


class GameClient:
    ENCODING = "UTF-8"
    DATA_SIZE = 1024

    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def get_data_from_server(self):
        while True:
            server_response = self.client_socket.recv(self.DATA_SIZE)
            yield server_response

    def send_data(self, data):
        self.client_socket.send(data.encode(self.ENCODING))