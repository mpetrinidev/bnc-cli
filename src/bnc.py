from spot import Spot
from credentials import Credentials


class Bnc:
    def __init__(self):
        self.credentials = Credentials()
        self.spot = Spot()
