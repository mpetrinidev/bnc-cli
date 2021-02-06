import fire
from bnb import Bnb


class Main(object):
    def __init__(self):
        self.bnb = Bnb()


if __name__ == '__main__':
    fire.Fire(Main)
