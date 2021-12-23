class ServerMessage:
    SEPARATOR = "#"

    def __init__(self, data):
        if data.count(self.SEPARATOR) == 1:
            self.type, self.data = data.split(self.SEPARATOR)
        else:
            self.type = None

    @staticmethod
    def prepare_data(type_, data):
        return type_ + ServerMessage.SEPARATOR + data + " "
