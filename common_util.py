import inspect


def call_funcs(vars, predicate):
    # test_funcs = [v for k, v in vars().items() if k.startswith('test_')]
    test_funcs = [v for k, v in vars.items() if predicate(k)]
    print(test_funcs)
    for func in test_funcs:
        print('call {} {}'.format(func, '='*30))
        func()


def test_sample():
    print("i'm {}".format(inspect.stack()[0][3]))


if __name__ == '__main__':
    call_funcs(vars(), lambda s: s.startswith('test_'))
