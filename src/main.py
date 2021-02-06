import fire
from bnc import Bnc


class Main(object):
    def __init__(self):
        self.bnc = Bnc()


if __name__ == '__main__':
    fire.Fire(Main)
