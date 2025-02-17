from config import config


class Service:
    app_name = None

    def __init__(self, app_name):
        self.app_name = app_name

    def check_status(self):
        return "I"

