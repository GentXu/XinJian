import test2


test1 = {"name": 10}


def set_test1(val):
    test1["name"] = val


def get_test1():
    return test1["name"]


if __name__ == '__main__':
    set_test1(20)
    print(get_test1())
    #test = test2.Test()
    print(test2.get_test())
    print(get_test1())
