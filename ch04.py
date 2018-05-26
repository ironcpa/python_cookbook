from common_util import call_funcs


# iterators n generators


# ====================================================
# 0401 manual consuming iterator
# ----------------------------------------------------
def test_0401():
    # use next(iterable)
    items = [1, 2, 3]

    #  - basic iterating pattern
    with open('/etc/passwd') as f:
        try:
            while True:
                line = next(f)  # manual call next()
                print(line, end='')
        except StopIteration:
            pass
    #  - stop on terminating value
    with open('/etc/passwd') as f:
        while True:
            line = next(f, None)  # get None on exception
            if line is None:
                break
            print(line, end='')

    #  - iter() : get iterator from iterable
    #    - list is not a iterator
    it = iter(items)
    next(it)
    next(it)
    next(it)  # until StopIteration


# ====================================================
# 0402 iterator 구현 방법 : __iter__
# ----------------------------------------------------
def test_0402():
    # just define __iter__() n delegate to children iterable
    class Node:
        def __init__(self):
            self._items = []

        def __iter__(self):  # this makes Node iterable
            return iter(self._items)

        def add_child(self, item):
            self._items.append(item)


# ====================================================
# 0403 generator
# ----------------------------------------------------
def test_0403():
    # basic generator function example
    def frange(start, stop, inc):
        x = start
        while x < stop:
            yield x
            x += inc

    #  - loop generator
    for n in frange(0, 4, 0.5):
        print(n)

    #  - send iterable argument
    ls = list(frange(0, 1, 0.125))
    print(ls)


# ====================================================
# 0404 iterator protocol 구현
# ----------------------------------------------------
def test_0404():
    # depth 1st tree example
    class Node:
        def __init__(self, value):
            self._value = value
            self._children = []

        def __repr__(self):
            return 'Node({!r})'.format(self._value)

        def add_child(self, node):
            self._children.append(node)

        def __iter__(self):
            return iter(self._children)

        # - simple recursive way of defining iterator
        #   - using generator and yield from
        #   - using only iterator code can be too complex
        #     (refer python_cookbook 0404's DepthFirstIterator)
        def depth_first(self):
            yield self
            for c in self:  # way of __iter__
                yield from c.depth_first()  # way to yield from other generator

    #  - usage
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child1.add_child(Node(5))
    for c in root.depth_first():
        print(c)


# ====================================================
# 0405 iterating in reverse
# ----------------------------------------------------
def test_0405():
    # use reversed()
    #  - iterable이 너무 크면 메모리 크게 소요됨
    a = [1, 2, 3, 4]
    print(reversed(a))  # get reversed object w/ reversed()
    for x in reversed(a):
        print(x)

    # define __revered__ in class to custom reversal
    class CountDown:
        def __init__(self, start):
            self.start = start

        def __iter__(self):
            n = self.start
            while n > 0:
                yield n
                n -= 1

        def __reversed__(self):
            n = 1
            while n <= self.start:
                yield n
                n += 1


# ====================================================
# 0406 내부 상태를 가진 generator 정의
# ----------------------------------------------------
def test_0406():
    from collections import deque

    # generator 함수로 __iter__() 정의한 class 정의
    #  - ex : 최근 3건 fetch history 저장하는 list
    class line_history:
        def __init__(self, lines, histlen=3):
            self.lines = lines
            self.history = deque(maxlen=histlen)

        def __iter__(self):  # generator로 정의한 __iter__()
            for line_no, line in enumerate(self.lines, 1):
                self.history.append((line_no, line))  # 내부 상태 저장
                yield line

        def clear(self):
            self.history.clear()

    with open('ch04_data/sample_0406.txt') as f:
        lines = line_history(f)  # 마치 generator 함수처럼 사용
        print(lines)
        for line in lines:  # __iter__() 구현했으므로 for 적용 가능
            print(line)
            if 'python' in line:  # 'phthon' 있으면 history 출력
                for line_no, hline in lines.history:
                    print('\t{}:{}'.format(line_no, hline), end='')

    with open('ch04_data/sample_0406.txt') as f:
        it = iter(line_history(f))  # for 아닌 next() 접근시 iter() 사용 필요
        print(next(it))
        print(next(it))


# ====================================================
# 0407 iterator | generator 에 대한 slice
# ----------------------------------------------------
def test_0407():
    def count(n):  # simple generator
        while True:
            yield n
            n += 1

    c = count(0)
    print(next(c))
    print(next(c))
    print(next(c))
    print(next(c))
    print(next(c))

    # c[10:20]  # dosen't work
    # itertools.islice()
    import itertools
    for x in itertools.islice(c, 10, 20):
        print(x)
    print('after islice', next(c))  # c has been consumed by islice counts


# ====================================================
# 0408 skipping the first part of an iterable
# ----------------------------------------------------
def test_0408():
    # to discard first parts, use itertools.dropwhile()
    from itertools import dropwhile
    with open('/etc/passwd') as f:
        for line in dropwhile(lambda line: line.startswith('#'), f):
            print(line, end='')

    # to filter all cases, use condition on genexp
    with open('/etc/passwd') as f:
        for line in (l for l in f if not l.startswith('#')):
            print(line, end='')
            print(line, end='')


# ====================================================
# 0409 iterating over all possible combinations or permutations
# ----------------------------------------------------
def test_0409():
    items = ['a', 'b', 'c']

    # itertools.permutations()
    from itertools import permutations
    for p in permutations(items):
        print(p)
    #  - can get smaller length result
    for p in permutations(items, 2):
        print(p)

    # itertools.combinations()
    #  - no duplications
    from itertools import combinations
    for c in combinations(items, 3):  # combi of 3
        print(c)
    for c in combinations(items, 2):  # combi of 2
        print(c)
    # itertools.combinations_with_replacement()
    from itertools import combinations_with_replacement
    for c in combinations_with_replacement(items, 3):
        print(c)


# ====================================================
# 0410 index-value 형태로 순회하기
# ----------------------------------------------------
def test_0410():
    ls = ['a', 'b', 'c']

    # use enumerate()
    #  - 시작번호 설정 가능
    ls = ['a', 'b', 'c']
    for i, v in enumerate(ls, 1):  # start i = 1
        print(i, v)


# ====================================================
# 0411 n개 sequence 동시 순회
# ----------------------------------------------------
def test_0411():
    # zip()
    #  - zip(a, b) produces tuples (a[n], b[n])
    #  - zip can get n : zip(a, b, c)
    xs = [1, 5, 4, 2, 10, 7]
    ys = [101, 70, 37, 15, 62, 99]
    for x, y in zip(xs, ys):
        print(x, y)
    #  - for different len of seqences
    #    - zip_longest : default zip is for shortest
    #      - fillvalue parameter for shortages
    from itertools import zip_longest
    xs = [1, 5, 4, 2, 10, 7]
    ys = [101, 70]
    for e in zip_longest(xs, ys, fillvalue='invalid'):
        print(e)

    # create dict w/ zip
    keys = ['name', 'shares', 'price']
    vals = ['ACME', 100, 450.1]
    s = dict(zip(keys, vals))  # creating dict from 2 lists
    print(s)


# ====================================================
# 0412 n개 sequence 연결 순회
# ----------------------------------------------------
def test_0412():
    # itertools.chain()
    from itertools import chain
    xs = [1, 2, 3, 4]
    ys = ['x', 'y', 'z']
    for e in chain(xs, ys):
        print(e)


# ====================================================
# 0412_01 n개 sequence nested 순회 : 중첩 for 문 펼치기
# ----------------------------------------------------
def test_0412_my():
    # itertools.product()
    from itertools import product
    xs = [1, 2, 3, 4]
    ys = ['a', 'b', 'c']
    for x, y in product(xs, ys):
        print(x, y)


# ====================================================
# 0413 creating data processing pipelines
# ----------------------------------------------------
'''
def test_0413():
    import os
    import fnmatch
    import gzip
    import bz2
    import re

    def gen_find(filepat, top):
        for path, dirlist, filelist in os.walk(top):
            yield os.path.join(path, name)

    def gen_opener(filename):
        for filename in filenames:
            if filename.endswith('.gz')
'''


# ====================================================
# 0414 flattening a nested sequence
# ----------------------------------------------------
def test_0414():
    from collections import Iterable

    # define recursive generator like this
    #  - ignore str, bytes types : to avoid side-effects on those type lists
    def flatten(items, ignore_types=(str, bytes)):
        for x in items:
            if isinstance(x, Iterable) and not isinstance(x, ignore_types):
                yield from flatten(x)  # use yield from instead of for loops
            else:
                yield x

    items = [1, 2, [3, 4, [5, 6], 7], 8]
    for x in flatten(items):
        print(x)


# ====================================================
# 0415 n개 시퀀스를 정렬하여 merge
# ----------------------------------------------------
def test_0415():
    # use heapq.merge()
    import heapq
    a = [1, 4, 7, 10]
    b = [2, 5, 6, 11]
    for c in heapq.merge(a, b):
        print(c)

    # usage : 여러 파일 데이터 -> 정렬된 파일로 만들기
    with open('ch04_data/0415_data1.txt', 'rt') as file1, \
         open('ch04_data/0415_data2.txt', 'rt') as file2, \
         open('ch04_data/0415_merged.txt', 'wt') as outf:
        for line in heapq.merge(file1, file2):
            outf.write(line)


# ====================================================
# 0416 replacing infinite while loops w/ an iterator
# ----------------------------------------------------
def test_0416():
    import sys

    # iter(lambda)
    #  - iter()는 인자없는 callable과 종료값(centinal)을 받을 수 있음
    #    - 특정 데이터에 대한 조건을 주어 순회할 수 있음
    f = open('/etc/passwd')
    for chunk in iter(lambda: f.read(10), ''):
        sys.stdout.write(chunk)


if __name__ == '__main__':
    call_funcs(vars(), lambda s: s.startswith('test_'))
    # test_0404()
