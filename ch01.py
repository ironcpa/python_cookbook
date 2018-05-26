import common_util


# 1.1 unpacking a sequence into separate variables
def doctest_0101():
    """
    # simple unpacking from tuple
    >>> data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
    >>> name, shares, price, date = data
    >>> name
    'ACME'
    >>> date
    (2012, 12, 21)

    # simple unpacking from tuple 2
    >>> name, shares, price, (year, mon, day) = data
    >>> name
    'ACME'
    >>> year
    2012
    >>> mon
    12
    >>> day
    21

    # exception on mismatching element's count
    >>> p = (4, 5)
    >>> x, y, z = p
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ValueError: not enough values to unpack (expected 3, got 2)

    # unpacking from string
    >>> s = 'Hello'
    >>> a, b, c, d, e = s
    >>> a
    'H'
    >>> b
    'e'
    >>> c
    'l'

    # using _ for place holder
    >>> data = ['ACME', 50, 91.1, (2012, 12, 21)]
    >>> _, shares, price, _ = data
    >>> shares
    50
    >>> price
    91.1
    >>>
    """
    pass


# unpacking elements from iterables of arbitrary length
# use '*' expression
# works only on python3, syntax error on python2
def doctest_0102():
    """
    # use star(*) to unpack n elements into varaiable
    >>> record = ('aaa', 'bbb', 'ccc', '111-222-333', '444-555-666')
    >>> a, b, *phones = record
    >>> a
    'aaa'
    >>> b
    'bbb'
    >>> phones
    ['ccc', '111-222-333', '444-555-666']

    # showing some patterns
    >>> record = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    >>> *a, b = record
    >>> a
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> b
    10
    >>> a, *b = record
    >>> a
    1
    >>> b
    [2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> a, *b, c = record
    >>> a
    1
    >>> b
    [2, 3, 4, 5, 6, 7, 8, 9]
    >>> c
    10
    """

    # sample usage
    # iterating sequence of tuples of varying length
    records = [
            ('foo', 1, 2),
            ('bar', 'hello'),
            ('foo', 3, 4),
    ]

    def do_foo(x, y):
        print('foo', x, y)

    def do_bar(s):
        print('bar', s)

    for tag, *args in records:
        if tag == 'foo':  # use 1st el as key
            do_foo(*args)
        elif tag == 'bar':
            do_bar(*args)

    """
    # sample usage
    # splitting commands
    >>> line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'
    >>> uname, *fields, homedir, sh = line.split(':')
    >>> uname
    'nobody'
    >>> homedir
    '/var/empty'
    >>> sh
    '/usr/bin/false'
    >>> fields
    ['*', '-2', '-2', 'Unprivileged User']

    # sample usage
    # extract some fields from complex data of fiels
    >>> record = ('augie', 50, 123.45, (12, 18, 2018))
    >>> name, *_, (*_, year) = record  # use *_ here to ignore n elements
    >>> name
    'augie'
    >>> year
    2018
    """
    pass


# how to keep latest n items : use deque
def doctest_0103():
    """
    # simple usage of deque
    >>> from collections import deque
    >>> q = deque(maxlen=3)
    >>> q.append(1)
    >>> q.append(2)
    >>> q.append(3)
    >>> q
    deque([1, 2, 3], maxlen=3)
    >>> q.append(4)
    >>> q
    deque([2, 3, 4], maxlen=3)
    >>> q.append(5)
    >>> q
    deque([3, 4, 5], maxlen=3)

    # unbounded deque example
    >>> q = deque()  # no parameter
    >>> q.append(1)
    >>> q.append(2)
    >>> q.append(3)
    >>> q
    deque([1, 2, 3])
    >>> q.appendleft(4)  # deque's interface
    >>> q
    deque([4, 1, 2, 3])
    >>> q.pop()
    3
    >>> q
    deque([4, 1, 2])
    >>> q.popleft()  # deque's interface
    4
    """
    pass


# find largest or smallest n items
def doctest_0104():
    """
    # use heapq.nlargest, nsmallest
    >>> nums = [1, 0, 2, 23, 7, -4, 18, 23, 42, 37, 2]
    >>> import heapq
    >>> heapq.nlargest(3, nums)
    [42, 37, 23]
    >>> heapq.nsmallest(3, nums)
    [-4, 0, 1]

    # can be used w/ key
    >>> complex_data = [
    ...     {'name': 'aaa', 'value': 91.1},
    ...     {'name': 'bbb', 'value': 543.22},
    ...     {'name': 'ccc', 'value': 23.9},
    ...     {'name': 'ddd', 'value': 31.7},
    ...     {'name': 'eee', 'value': 16.35},
    ... ]
    >>> heapq.nlargest(2, complex_data, key=lambda s: s['value'])
    [{'name': 'bbb', 'value': 543.22}, {'name': 'aaa', 'value': 91.1}]
    >>> heapq.nsmallest(2, complex_data, key=lambda s: s['value'])
    [{'name': 'eee', 'value': 16.35}, {'name': 'ccc', 'value': 23.9}]

    # heapify : get smallest first
    >>> nums = [1, 0, 2, 23, 7, -4, 18, 23, 42, 37, 2]
    >>> heap = list(nums)  # for heapify source
    >>> heap
    [1, 0, 2, 23, 7, -4, 18, 23, 42, 37, 2]
    >>> heapq.heapify(heap)
    >>> heap
    [-4, 0, 1, 23, 2, 2, 18, 23, 42, 37, 7]
    >>> heapq.heappop(heap)  # gets next smallest
    -4
    >>> heapq.heappop(heap)
    0
    >>> heapq.heappop(heap)
    1
    >>> heapq.heappop(heap)
    2
    >>> heap  # check remains
    [2, 7, 18, 23, 23, 37, 42]
    """


# priority queue : using heap
def doctest_0105():
    import heapq

    class PriorityQueue:
        def __init__(self):
            self._queue = []
            self._index = 0

        def push(self, item, priority):
            heapq.heappush(self._queue, (-priority, self._index, item))
            self._index += 1

        def pop(self):
            return heapq.heappop(self._queue)[-1]
    pass


# keep dictionries in order
# use OrderedDict
def doctest_0107():
    """
    # dict preserves insert order
    >>> from collections import OrderedDict
    >>> d = OrderedDict()
    >>> d['foo'] = 1
    >>> d['bar'] = 2
    >>> d['spam'] = 3
    >>> d['grok'] = 4
    >>> d
    OrderedDict([('foo', 1), ('bar', 2), ('spam', 3), ('grok', 4)])

    # useful cuz preserves insert order after json dumps
    #   (or other format like csv)
    >>> import json
    >>> json.dumps(d)
    '{"foo": 1, "bar": 2, "spam": 3, "grok": 4}'
    """


# calc on dict
#  - min, max
def doctest_0108():
    """
    >>> data = {
    ...     'aaa': 45.23,
    ...     'bbb': 612.78,
    ...     'ccc': 205.55,
    ...     'ddd': 37.28,
    ...     'eee': 10.75,
    ... }

    # direct application : sorted by key
    #  - not what we intended
    >>> min(data)
    'aaa'
    >>> max(data)
    'eee'

    # to supply sort key w/ values
    # create zip to apply min() or max() or sorted()
    >>> min_val = min(zip(data.values(), data.keys()))
    >>> min_val
    (10.75, 'eee')
    >>> max_val = max(zip(data.values(), data.keys()))
    >>> max_val
    (612.78, 'bbb')
    >>> sorted_data = sorted(zip(data.values(), data.keys()))
    >>> sorted_data
    [(10.75, 'eee'), (37.28, 'ddd'), (45.23, 'aaa'), (205.55, 'ccc'), (612.78, 'bbb')]

    # be aware that zip object consumed when max or min applied
    >>> zipped = zip(data.values(), data.keys())
    >>> max(zipped)
    (612.78, 'bbb')
    >>> next(zipped)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    StopIteration
    """


# find commonalities in 2 dicts
def doctest_0109():
    """
    >>> a = {
    ...     'x': 1,
    ...     'y': 2,
    ...     'z': 3
    ... }
    >>> b = {
    ...     'w': 10,
    ...     'x': 11,
    ...     'y': 2
    ... }
    >>> c = {
    ...     'y': 2
    ... }

    # we can use set operators for dicts
    >>> a.keys() & b.keys()
    {'y', 'x'}
    >>> a.keys() - b.keys()
    {'z'}
    >>> a.items() & b.items()
    {('y', 2)}
    >>> a.items() & b.items() & c.items()  #  - can be applied on 3 dicts
    {('y', 2)}

    # way to filter dict w/ set operation
    >>> filterd = {key:a[key] for key in a.keys() - {'z', 'w'}}
    >>> filterd
    {'y': 2, 'x': 1}
    """


# remove duplicates from seqeuence
def doctest_0110():
    """
    # simple dup elimination
    #  - use set
    #  - but this way lose insert ordering
    >>> a = [1, 5, 2, 1, 9, 1, 5, 10]
    >>> set(a)  # doesn't preserve ordering
    {1, 2, 5, 9, 10}

    # for hashable type
    >>> def dedupe(items):
    ...     seen = set()
    ...     for item in items:
    ...         if item not in seen:
    ...             yield item
    ...             seen.add(item)
    ...
    >>> a = [1, 5, 2, 1, 9, 1, 5, 10]
    >>> list(dedupe(a))
    [1, 5, 2, 9, 10]

    # for unhashable type : dict
    >>> def dedupe(items, key=None):
    ...     seen = set()
    ...     for item in items:
    ...         val = item if key is None else key(item)
    ...         if val not in seen:
    ...             yield item
    ...             seen.add(val)
    ...
    >>> a = [
    ...     {'x': 1, 'y': 2},
    ...     {'x': 1, 'y': 3},
    ...     {'x': 1, 'y': 2},
    ...     {'x': 2, 'y': 4},
    ... ]
    >>> list(dedupe(a, key=lambda d: (d['x'], d['y'])))
    [{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]
    >>> list(dudupe(a, key=lambda d: d['x']))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    NameError: name 'dudupe' is not defined
    >>> list(dedupe(a, key=lambda d: d['x']))
    [{'x': 1, 'y': 2}, {'x': 2, 'y': 4}]
    """


def remove_dup(items):
    """for hashable type"""
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)
    '''
    # sample usage on file
    with open(somefile, 'r') as f:
        for line in remove_dup(f):
            ...
    '''


def remove_dict_dup(items, key=None):
    """for unhashable type like dict"""
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


# naming a slice
def doctest_0111():
    """
    # define slice make code readable
    >>> items = [0, 1, 2, 3, 4, 5, 6]
    >>> a = slice(2, 4)
    >>> items[2:4]
    [2, 3]
    >>> items[a]
    [2, 3]
    >>> a
    slice(2, 4, None)

    # jumping slice
    >>> a = slice(10, 50, 2)
    >>> a
    slice(10, 50, 2)
    """


# get top n frequent items
def doctest_0112():
    """
    >>> words = [
    ...     'aaa', 'bbb', 'ccc', 'ddd', 'aaa',
    ...     'aaa', 'eee', 'bbb', 'ccc', 'ccc'
    ... ]

    # use Counter
    >>> from collections import Counter
    >>> word_counts = Counter(words)
    >>> top_two = word_counts.most_common(2)
    >>> top_two
    [('aaa', 3), ('ccc', 3)]

    # get count for item
    >>> word_counts['aaa']

    # Counter is manipulatable
    >>> word_counts['aaa'] += 1
    >>> word_counts['aaa']
    4

    # add other list's counts
    >>> add = ['aaa', 'ddd', 'eee']
    >>> word_counts.update(add)
    >>> word_counts
    Counter({'aaa': 5, 'ccc': 3, 'bbb': 2, 'ddd': 2, 'eee': 2})

    # Counter can be calculated
    >>> word_counts2 = word_counts
    >>> combine = word_counts + word_counts2
    >>> combine
    Counter({'aaa': 10, 'ccc': 6, 'bbb': 4, 'ddd': 4, 'eee': 4})
    """


# sort list of dict by key
def test_0113():
    rows = [
        {'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
        {'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
        {'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
        {'fname': 'Big', 'lname': 'Jones', 'uid': 1004},
    ]

    from operator import itemgetter
    from pprint import pprint

    # get key w/ itemgetter()
    rows_by_fname = sorted(rows, key=itemgetter('fname'))
    rows_by_uid = sorted(rows, key=itemgetter('uid'))

    pprint(rows_by_fname)
    pprint(rows_by_uid)

    # get multiple keys w/ itemgetter()
    rows_by_lfname = sorted(rows, key=itemgetter('lname', 'fname'))

    pprint(rows_by_lfname)

    # we can just use lambda
    #  - but itemgetter() is bit faster
    rows_by_fname = sorted(rows, key=lambda r: r['fname'])
    rows_by_lfname = sorted(rows, key=lambda r: (r['lname'], r['fname']))

    # can be applied on the other functions like min(), max() ...
    min(rows, key=itemgetter('uid'))
    max(rows, key=itemgetter('uid'))


# sort custom object
def test_0114():
    class User:
        def __init__(self, id):
            self.id = id

        def __repr__(self):
            return 'user({})'.format(self.id)

    users = [User(23), User(3), User(99)]
    # sort custom object
    #  - use key with sort field
    s = sorted(users, key=lambda u: u.id)
    print(s)
    from operator import attrgetter
    #  - or use attrgetter instead
    #    - this can be bit faster like 0113's itemgetter
    s = sorted(users, key=attrgetter('id'))
    print(s)


# group by
def test_0115():
    rows = [
        {'address': '5412 N CLARK', 'date': '07/01/2012'},
        {'address': '5148 N CLARK', 'date': '07/04/2012'},
        {'address': '5800 N 58TH', 'date': '07/02/2012'},
        {'address': '2122 N CLARK', 'date': '07/03/2012'},
        {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
        {'address': '1060 N ADDISON', 'date': '07/02/2012'},
        {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
        {'address': '1039 N GRANVILLE', 'date': '07/04/2012'},
    ]

    from operator import itemgetter
    from itertools import groupby
    from pprint import pprint

    # sort before apply group by
    rows.sort(key=itemgetter('date'))
    pprint(rows)

    # iterate in groups
    for date, items, in groupby(rows, key=itemgetter('date')):
        print(date)
        for i in items:
            print('    ', i)

    # check groupby object
    print(groupby(rows, key=itemgetter('date')))

    # use defaultdict to make random access dict
    #  - this doesn't need sorting first
    from collections import defaultdict
    rows_by_date = defaultdict(list)
    pprint(rows_by_date)
    for row in rows:
        rows_by_date[row['date']].append(row)
    pprint(rows_by_date)
    print(rows_by_date['07/01/2012'])


# filtering sequences
def test_0116():
    # using list comprehension
    sample = [1, 4, -5, 10, -7, 2, 3, -1]
    filtered = [n for n in sample if n > 0]
    print(filtered)

    # use generator exp for large data
    pos = (n for n in sample if n > 0)
    for x in pos:
        print(x)

    # use filter() when filtering criteria is complex
    sample = ['1', '2', '-3', '-', '4', 'N/A', '5']

    def is_int(val):
        try:
            int(val)
            return True
        except ValueError:
            return False

    ivals = list(filter(is_int, sample))
    print(ivals)

    # use compress to filter data w/ boolen sequence
    addresses = [
        '5412 N CLARK',
        '5148 N CLARK',
        '5800 N 58TH',
        '2122 N CLARK',
        '5645 N RAVENSWOOD',
        '1060 N ADDISON',
        '4801 N BROADWAY',
        '1039 N GRANVILLE',
    ]
    counts = [1, 3, 10, 4, 1, 7, 6, 1]

    from itertools import compress
    more5 = [n > 5 for n in counts]
    print(more5)
    #  - filter only matching True items
    filtered = list(compress(addresses, more5))
    print(filtered)


# get subset of dic
def test_0117():
    prices = {
        'ACME': 45.23,
        'AAPL': 612.78,
        'IBM': 205.55,
        'HPQ': 37.20,
        'FB': 10.75
    }

    # use dict comprehension
    sub = {key: value for key, value in prices.items() if value > 200}
    print(sub)

    # use dict creator
    #  - this is slower than dict comprehension
    sub2 = dict((key, value) for key, value in prices.items() if value > 200)
    print(sub2)


# mapping names to sequence elements
#  - using namedtuple
def test_0118():
    from collections import namedtuple
    Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
    sub = Subscriber('aaa@bbb.com', '2012-10-19')
    print(sub.addr, sub.joined)


# 원본 데이터를 변환하면서 reduce 함수 적용하기
def test_0119():
    # use generator exp
    nums = [1, 2, 3, 4, 5]
    s = sum(x * x for x in nums)
    print('sum:', s)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    common_util.call_funcs(vars(), lambda s: s.startswith('test_'))
    '''
    test_funcs = [v for k, v in vars().items() if k.startswith('test_')]
    for func in test_funcs:
        print('call {} ================='.format(func))
        func()
    '''
