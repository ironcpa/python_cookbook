def doctest_1_3():
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
    """


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
