import time


class ApiTime:
    def __init__(self):
        pass

    @staticmethod
    def get_timestamp():
        return int(time.time() * 1000)
