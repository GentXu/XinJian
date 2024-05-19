import importlib

import module1


class Test:
    def __init__(self):
        self.test3 = 10


def get_test():
    module1.set_test1(30)
    return module1.get_test1()


if __name__ == '__main__':
    test = Test()
    print(test.get_test())
