class ServerMessage:
    SEPARATOR = "#"

    def __init__(self, data):
        self.type, self.data = data.split(self.SEPARATOR)

    @staticmethod
    def prepare_data(type_, data):
        return type_ + ServerMessage.SEPARATOR + data
