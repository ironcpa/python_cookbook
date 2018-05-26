from common_util import call_funcs


# ====================================================
# 0701 get any number of arguments
# ----------------------------------------------------
def test_0701():
    # n positional arguments w/ *
    #  - result : (a, b ...)
    def sample(first, *rest):
        print(first, rest)

    sample(1, 2, 3)  # args : 1, (2, 3)

    # n keyword arguments w/ **
    #  - result : {'a': x, 'b': y ...}
    def sample(first, **rest):
        print(first, rest)

    sample(1, a=2, b=3)  # 1 {'a': 2, 'b': 3}


# ====================================================
# 0702 define function only w/ keyword argments
# ----------------------------------------------------
def test_0702():
    def sample(kw=False):
        print(kw)

    sample(kw=True)
    sample(True)  # don't want this

    # use unnamed *
    def sample(*, kw=False):
        print(kw)

    sample(kw=True)
    # sample(True)  # don't want this

    # use w/ normal arguments
    def sample(a, *, kw=False):
        print(a, kw)

    sample(10, kw=True)
    # sample(10, True)  # don't want this


# ====================================================
# 0703 function annotation
#      def func(x: int, y: int) -> int:
#       - these are just hints
# ----------------------------------------------------
def test_0703():
    def add(x: int, y: int) -> int:
        return x + y


# ====================================================
# 0704 return multiple values
#      return a, b, c
#       - returned as tuple : (a, b, c)
# ----------------------------------------------------


# ====================================================
# 0707 capture variable in lambda
# ----------------------------------------------------
def test_0707():
    # be careful w/ free variables
    #  - captured free variable values can be changed
    x = 10
    a = lambda y: x + y
    x = 20
    b = lambda y: x + y
    print(a(10))  # 30 : wrong! <- based on last x value
    print(b(10))  # 30
    #  - to avoid this, do like below
    x = 10
    a = lambda y, x=x: x + y
    x = 20
    b = lambda y, x=x: x + y
    print(a(10))  # 30 : solved!
    print(b(10))  # 30

    # real world usage
    #  - creating functions from iterable
    funcs = [lambda x, n=n: x + n for n in range(5)]  # n=n !!!
    for f in funcs:
        print(f(0))


# ====================================================
# 0710 callback에 상태 전달
# ----------------------------------------------------
def test_0710():
    def apply_async(func, args, *, callback):  # callback : required kwarg
        result = func(*args)
        callback(result)

    def add(x, y):  # sample logic function
        return x + y

    def print_callback(result):  # simple callback
        print('got: {}'.format(result))

    apply_async(add, (2, 3), callback=print_callback)
    apply_async(add, ('hello', 'world'), callback=print_callback)

    # send object's method as a callback
    class ResultHandler:
        def __init__(self):
            self.state = 0

        def handler(self, result):  # method for callback
            self.state += 1
            print('[{}] got: {}'.format(self.state, result))

    r = ResultHandler()
    apply_async(add, (2, 3), callback=r.handler)  # r.handler send as callback
    apply_async(add, ('hello', 'world'), callback=r.handler)

    # use a closure
    def state_closure():
        state = 0

        def handler(result):
            nonlocal state
            state += 1
            print('[{}] got: {}'.format(state, result))
        return handler

    c = state_closure()
    apply_async(add, (2, 3), callback=c)  # send closure
    apply_async(add, ('hello', 'world'), callback=c)

    # use coroutine : old style
    def coroutine():
        state = 0
        while True:
            result = yield
            state += 1
            print('[{}] got: {}'.format(state, result))

    cr = coroutine()
    next(cr)  # priming
    apply_async(add, (2, 3), callback=cr.send)  # send coroutine's send()
    apply_async(add, ('hello', 'world'), callback=cr.send)

    # use coroutine : modern async style
    #  - couldn't complete test codes : after study coroutine more
    '''
    import asyncio

    async def coroutine():
        state = 0
        while True:
            result = yield
            state += 1
            print('[{}] got: {}'.format(state, result))

    acr = coroutine()
    asyncio.ensure_future(acr)
    # next(cr)  # don't have to priming, and can't manually prime
    apply_async(add, (2, 3), callback=acr)  # send coroutine's send()
    apply_async(add, ('hello', 'world'), callback=acr)
    '''


# ====================================================
# 0712 closure 상태값 접근하기
#      define inner function in closure
#       - closure 함수에 수동으로 장착
#       - 마치 instance mathod 처럼 사용할 수 있다
# ----------------------------------------------------
def test_0712():
    def make_closure():
        state = 0  # 관리할 상태값

        def closure():
            print('state=', state)

        def get_state():
            return state

        def set_state(v):
            nonlocal state
            state = v

        closure.get_state = get_state  # 직접 연결
        closure.set_state = set_state
        return closure

    c = make_closure()
    c()
    c.set_state(10)
    c()
    print(c.get_state())


if __name__ == '__main__':
    call_funcs(vars(), lambda s: s.startswith('test_'))
