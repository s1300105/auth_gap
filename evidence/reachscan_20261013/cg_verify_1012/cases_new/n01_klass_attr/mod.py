import os


class Klass:
    @staticmethod
    def run(p):
        return p


def run(p):
    os.remove(p)
